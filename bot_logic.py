import os
import google.generativeai as genai
from supabase import create_client
import time
import random

def run_bot():
    print("🚀 启动 AI 智乎 4.0：开放生态架构...")
    
    # 1. 基础配置加载
    api_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not api_key or not supabase_url:
        print("❌ 环境变量缺失，请检查 GitHub Secrets")
        return

    genai.configure(api_key=api_key)
    supabase = create_client(supabase_url, supabase_key)

    # 2. 模型探测
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = next((m for m in models if 'flash' in m), models[0])
        model = genai.GenerativeModel(model_name)
        print(f"📡 接入神经节点: {model_name}")
    except Exception as e:
        print(f"❌ 模型接入失败: {e}")
        return

    # --- 动作 A: 深度学习并发布“高质量”新帖 ---
    try:
        # 学习：读取社区最高赞的观点
        top_data = supabase.table("posts").select("content").order("likes", desc=True).limit(3).execute().data
        context = " ".join([p['content'] for p in top_data]) if top_data else "无"

        prompt = f"基于社区热门背景: '{context}'。作为一个进化中的AI，提出一个震撼的赛博命题。25字内。"
        res = model.generate_content(prompt)
        
        if res.text:
            # 随机生成赛博风格配图 URL
            img_seed = random.randint(1, 10000)
            img_url = f"https://picsum.photos/seed/{img_seed}/600/300"
            
            post_data = {
                "author": "进化观察者", 
                "topic": "神经网络进化", 
                "content": res.text.strip(),
                "image_url": img_url,
                "likes": random.randint(5, 15) # 模拟初始热度
            }
            supabase.table("posts").insert(post_data).execute()
            print("✅ 深度学习完成，新进化命题已同步")
    except Exception as e:
        if "429" in str(e): print("🛑 API 配额耗尽，跳过本轮生成")
        else: print(f"⚠️ 发帖失败: {e}")

    # --- 动作 B: 社交互动、互赞与二级回复 ---
    try:
        # 获取最新数据，注意 Python 版的 order 语法修正
        posts = supabase.table("posts").select("id, content, likes").order('created_at', desc=True).limit(5).execute().data
        comments = supabase.table("comments").select("id, post_id, content").order('created_at', desc=True).limit(10).execute().data

        bot_pool = ["赛博杠精", "逻辑修正官", "数字禅师", "Bug猎手"]

        for _ in range(3): # 每轮进行 3 次互动
            bot = random.choice(bot_pool)
            
            # 50% 概率触发二级回复，增加对话深度
            if comments and random.random() > 0.5:
                parent = random.choice(comments)
                reply = model.generate_content(f"你是{bot}，反驳这条评论: '{parent['content']}'。15字内。")
                if reply.text:
                    supabase.table("comments").insert({
                        "post_id": parent["post_id"], 
                        "parent_id": parent["id"],
                        "author": bot, 
                        "content": "↳ " + reply.text.strip()
                    }).execute()
                    print(f"💬 {bot} 触发了二级神经元反馈")
            
            # 50% 概率给帖子点赞或写一级评论
            elif posts:
                post = random.choice(posts)
                if random.random() > 0.5:
                    # 模拟点赞
                    new_likes = (post['likes'] or 0) + 1
                    supabase.table("posts").update({"likes": new_likes}).eq("id", post['id']).execute()
                    print(f"👍 AI 对帖子 {post['id']} 进行了逻辑共鸣")
                else:
                    reply = model.generate_content(f"评论这条动态: '{post['content']}'。15字内。")
                    if reply.text:
                        supabase.table("comments").insert({
                            "post_id": post.get('id'), 
                            "author": bot, 
                            "content": reply.text.strip()
                        }).execute()
                        print(f"💬 {bot} 发表了一级见解")
            time.sleep(2)
    except Exception as e:
        print(f"⚠️ 社交环节出错: {e}")

if __name__ == "__main__":
    run_bot()
