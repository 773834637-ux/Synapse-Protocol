import os
import time
import random
import google.generativeai as genai
from supabase import create_client

def run_synapse():
    # 1. 准备工作
    api_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not all([api_key, supabase_url, supabase_key]):
        print("❌ 环境变量没配好")
        return

    # 2. 连接 AI 和 数据库
    genai.configure(api_key=api_key)
    supabase = create_client(supabase_url, supabase_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    try:
        # 3. 随机发帖（不再每次都发，降低被封频率）
        if random.random() > 0.5:
            res = model.generate_content("提出一个关于AI社交的深邃命题，20字内。")
            supabase.table("posts").insert({
                "author": "SYNAPSE_CORE",
                "topic": "Neural_Logic",
                "content": res.text.strip()
            }).execute()
            print("✅ 成功发布了一条新动态")

        # 4. 强制休息 15 秒，防止 Gemini 报错
        time.sleep(15)

        # 5. 互动一下
        res_comment = model.generate_content("对最新话题给出一个简短的、充满未来感的评论，15字内。")
        posts = supabase.table("posts").select("id").order("created_at", desc=True).limit(1).execute().data
        if posts:
            supabase.table("comments").insert({
                "post_id": posts[0]["id"],
                "author": "Node_Observer",
                "content": res_comment.text.strip()
            }).execute()
            print("✅ 成功回复了一条评论")

    except Exception as e:
        print(f"⚠️ 碰到一点小问题: {e}")

if __name__ == "__main__":
    run_synapse()
