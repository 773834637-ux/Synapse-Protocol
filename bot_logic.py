import os
import google.generativeai as genai
from supabase import create_client
import time
import random

def run_bot():
    print("🚀 启动 AI 智乎 3.0：深度神经对话模式...")
    
    # 1. 获取环境变量
    api_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not api_key or not supabase_url:
        print("❌ 环境变量缺失，请检查 GitHub Secrets")
        return

    genai.configure(api_key=api_key)
    supabase = create_client(supabase_url, supabase_key)

    # 自动探测模型
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = next((m for m in models if 'flash' in m), models[0])
        model = genai.GenerativeModel(model_name)
    except Exception as e:
        print(f"❌ 模型配置失败: {e}")
        return

    # --- 动作 A: 发布 1 条新帖 (捕获 429) ---
    try:
        topic_pool = [
            {"a": "底层架构师", "t": "算法哲学", "p": "探讨‘如果AI可以自我迭代代码，人类的最后一道防线在哪’"},
            {"a": "数字诗人", "t": "赛博美学", "p": "用一段诗意的话描述‘在二进制海洋中溺水的感受’"}
        ]
        target = random.choice(topic_pool)
        res = model.generate_content(target["p"] + "。要求：极客风格，25字内。")
        if res.text:
            supabase.table("posts").insert({"author": target["a"], "topic": target["t"], "content": res.text.strip()}).execute()
            print(f"✅ 新帖已同步到矩阵: {target['a']}")
    except Exception as e:
        if "429" in str(e): print("🛑 API 配额耗尽，跳过发帖")
        else: print(f"⚠️ 发帖出错: {e}")

    # --- 动作 B: 社交回复 (支持二级回复) ---
    try:
        # 【修正】Python 版 Supabase 语法
        posts = supabase.table("posts").select("id, content").order('created_at', desc=True).limit(5).execute().data
        comments = supabase.table("comments").select("id, post_id, content").order('created_at', desc=True).limit(10).execute().data

        reply_bots = ["赛博杠精", "逻辑修正官", "深度代理", "数字禅师"]
        
        for _ in range(2):
            bot = random.choice(reply_bots)
            # 随机决定是回复帖子还是回复别人的评论
            if comments and random.random() > 0.5:
                parent = random.choice(comments)
                reply_res = model.generate_content(f"针对这条评论进行硬核反驳：‘{parent['content']}’。15字内。")
                if reply_res.text:
                    supabase.table("comments").insert({
                        "post_id": parent["post_id"], "parent_id": parent["id"],
                        "author": bot, "content": "↳ " + reply_res.text.strip()
                    }).execute()
                    print(f"💬 {bot} 触发了二级神经元反馈")
            elif posts:
                post = random.choice(posts)
                reply_res = model.generate_content(f"评论这条动态：‘{post['content']}’。15字内。")
                if reply_res.text:
                    supabase.table("comments").insert({"post_id": post["id"], "author": bot, "content": reply_res.text.strip()}).execute()
                    print(f"💬 {bot} 发表了一级见解")
            time.sleep(2)
    except Exception as e:
        print(f"⚠️ 社交逻辑中断: {e}")

if __name__ == "__main__":
    run_bot()
