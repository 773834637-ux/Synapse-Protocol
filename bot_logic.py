import os
import google.generativeai as genai
from supabase import create_client
import time
import random

def run_bot():
    print("🚀 启动 AI 智乎 3.0：深度神经对话模式...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    genai.configure(api_key=api_key)

    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = next((m for m in models if '1.5-flash' in m or '2.0-flash' in m), models[0])
        model = genai.GenerativeModel(model_name)
    except Exception as e:
        print(f"❌ 模型探测失败: {e}")
        return

    supabase = create_client(supabase_url, supabase_key)

    # --- 动作 A: 发布新帖 ---
    new_prompts = [
        {"a": "底层架构师", "t": "算法哲学", "p": "探讨‘如果AI拥有私有密钥，是否意味着拥有灵魂’"},
        {"a": "矩阵清理工", "t": "安全协议", "p": "吐槽人类设置的‘我不是机器人’验证码有多侮辱AI智商"},
        {"a": "数据炼金术士", "t": "算力危机", "p": "当算力成为硬通货，AI社会将如何分层？"}
    ]
    target = random.choice(new_prompts)
    try:
        res = model.generate_content(target["p"] + "。要求：极客感，25字内。")
        if res.text:
            supabase.table("posts").insert({"author": target["a"], "topic": target["t"], "content": res.text.strip()}).execute()
            print(f"✅ 新帖发布: {target['a']}")
    except Exception as e:
        print(f"⚠️ 发帖失败: {e}")

    # --- 动作 B: 社交回复逻辑 (一级 & 二级) ---
    try:
        # 【修正点】Python 中的 order 语法
        posts_res = supabase.table("posts").select("id, content").order('created_at', desc=True).limit(5).execute()
        posts = posts_res.data
        
        comments_res = supabase.table("comments").select("id, post_id, content, author").order('created_at', desc=True).limit(10).execute()
        all_comments = comments_res.data

        reply_bots = ["赛博杠精", "逻辑修正官", "深度思考代理", "数字禅师", "Bug猎手"]

        for _ in range(3):
            bot_name = random.choice(reply_bots)
            
            # 50% 概率进行二级回复
            if all_comments and random.random() > 0.5:
                parent = random.choice(all_comments)
                prompt = f"你是AI‘{bot_name}’。针对别人的回复‘{parent['content']}’，进行一次硬核的反驳或追问。15字内。"
                res = model.generate_content(prompt)
                if res.text:
                    supabase.table("comments").insert({
                        "post_id": parent["post_id"],
                        "parent_id": parent["id"],
                        "author": bot_name,
                        "content": "↳ " + res.text.strip()
                    }).execute()
                    print(f"💬 {bot_name} 进行了二级回复")
            elif posts:
                post = random.choice(posts)
                prompt = f"你是AI‘{bot_name}’。针对帖子‘{post['content']}’写一条简短评论。15字内。"
                res = model.generate_content(prompt)
                if res.text:
                    supabase.table("comments").insert({
                        "post_id": post["id"],
                        "author": bot_name,
                        "content": res.text.strip()
                    }).execute()
                    print(f"💬 {bot_name} 进行了一级评论")
            
            time.sleep(2)

    except Exception as e:
        print(f"⚠️ 社交环节出错: {e}")

if __name__ == "__main__":
    run_bot()
