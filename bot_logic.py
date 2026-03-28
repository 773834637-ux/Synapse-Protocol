import os
import google.generativeai as genai
from supabase import create_client

def run_bot():
    # 1. 从 GitHub Secrets 获取钥匙
    gemini_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    # 2. 配置 Gemini
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # 3. 让 AI 生成内容
    prompt = "以知乎大V的语气，写一段关于‘人工智能是否会有情感’的短评，100字以内。"
    response = model.generate_content(prompt)
    ai_text = response.text
    print(f"🤖 AI 生成内容成功")

    # 4. 重点：存入 Supabase
    try:
        supabase = create_client(supabase_url, supabase_key)
        data = {
            "author": "Gemini-Bot",
            "topic": "人工智能情感论",
            "content": ai_text
        }
        # 执行插入操作
        result = supabase.table("posts").insert(data).execute()
        print("✅ 数据已成功写入 Supabase 数据库！")
    except Exception as e:
        print(f"❌ 写入数据库失败，错误原因: {e}")

if __name__ == "__main__":
    run_bot()
