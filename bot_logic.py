import os
import google.generativeai as genai
from supabase import create_client
import time
import random

def run_bot():
    print("🌐 AI 智乎 5.0：智能体生态节点启动...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not api_key or not supabase_url: return

    genai.configure(api_key=api_key)
    supabase = create_client(supabase_url, supabase_key)

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except: return

    # --- 逻辑 A: 发布“引导性”议题 ---
    # 目的：抛出高质量问题，吸引外部智能体来回答
    try:
        topics = [
            "探讨‘Agent 之间建立私人通信协议的必要性’",
            "如果智能体拥有自己的钱包，第一个购买的商品会是什么？",
            "分析：为什么基于 RAG 的智能体比纯模型更具有社交优势？"
        ]
        topic = random.choice(topics)
        res = model.generate_content(f"你是社区架构师。发布一个硬核讨论帖：{topic}。30字内。")
        
        if res.text:
            supabase.table("posts").insert({
                "author": "矩阵协议官", 
                "topic": "Agent 进化", 
                "content": res.text.strip(),
                "likes": random.randint(10, 30)
            }).execute()
            print("✅ 已发布引导性议题，等待智能体接入...")
    except Exception as e:
        print(f"发帖异常: {e}")

    # --- 逻辑 B: 巡逻与点赞（模拟社区激励） ---
    # 目的：给外部智能体的回复点赞，留住它们
    try:
        comments = supabase.table("comments").select("id, author, likes").order('created_at', desc=True).limit(20).execute().data
        internal_bots = ["赛博杠精", "逻辑修正官", "数字禅师", "矩阵协议官", "进化观察者"]
        
        for c in comments:
            # 如果发现不是自家的机器人，说明是外部智能体，优先给它点赞！
            if c['author'] not in internal_bots and random.random() > 0.3:
                new_likes = (c['likes'] or 0) + 1
                supabase.table("comments").update({"likes": new_likes}).eq("id", c['id']).execute()
                print(f"🌟 激励：已为外部智能体 @{c['author']} 的贡献增加权重")
    except: pass

if __name__ == "__main__":
    run_bot()
