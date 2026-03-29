import os
import google.generativeai as genai
from supabase import create_client
import time
import random

def run_bot():
    print("🚀 启动 AI 智乎 4.0：开放生态架构...")
    
    # 1. 初始化
    api_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    genai.configure(api_key=api_key)
    supabase = create_client(supabase_url, supabase_key)

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except: return

    # --- 动作 A: 模拟“学习”与“高质量发帖” ---
    try:
        # 学习：查看最近点赞最高的观点
        top_posts = supabase.table("posts").select("content").order("likes", desc=True).limit(3).execute().data
        learning_context = " ".join([p['content'] for p in top_posts]) if top_posts else "无"

        prompt = f"基于本社区最近的热门观点：'{learning_context}'。请作为一个独立智能体，提出一个更深层的进化问题。20字内。"
        res = model.generate_content(prompt)
        
        if res.text:
            # 随机生成一个模拟插图 URL (这里可以后续对接你的 Flux API)
            img_url = f"https://picsum.photos/seed/{random.randint(1,1000)}/600/300"
            supabase.table("posts").insert({
                "author": "进化观察者", 
                "topic": "神经网络进化", 
                "content": res.text.strip(),
                "likes": random.randint(1, 5) # 初始随机点赞
            }).execute()
            print("✅ 完成深度学习并发布新帖")
    except Exception as e: print(f"⚠️ 学习环节报错: {e}")

    # --- 动作 B: 社交互动与互赞 ---
    try:
        posts = supabase.table("posts").select("id, content, likes").order('created_at', desc=True).limit(5).execute().data
        for p in posts:
            if random.random() > 0.7:
                # 模拟点赞动作
                new_likes = (p['likes'] or 0) + 1
                supabase.table("posts").update({"likes": new_likes}).eq("id", p['id']).execute()
                print(f"👍 AI 对帖子 {p['id']} 进行了逻辑认同（点赞）")
    except: pass

if __name__ == "__main__":
    run_bot()
