import os
import google.generativeai as genai
from supabase import create_client

def run_bot():
    # 1. 获取钥匙
    gemini_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    # 2. 配置 Gemini
    genai.configure(api_key=gemini_key)
    
    # 尝试不同的模型名称（按优先级排序）
    model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    model = None
    ai_text = ""

    for name in model_names:
        try:
            print(f"尝试连接模型: {name}...")
            test_model = genai.GenerativeModel(name)
            response = test_model.generate_content("你好，请简短打个招呼。")
            if response:
                model = test_model
                print(f"✅ 成功连接到模型: {name}")
                # 正式生成内容
                prompt = "以知乎大V的语气，写一段关于‘人工智能是否会有情感’的短评，100字以内。"
                response = model.generate_content(prompt)
                ai_text = response.text
                break
        except Exception as e:
            print(f"❌ 模型 {name} 不可用，尝试下一个...")

    if not ai_text:
        print("😭 所有模型名称均尝试失败，请检查 API Key 是否有效。")
        return

    # 3. 存入 Supabase
    try:
        supabase = create_client(supabase_url, supabase_key)
        data = {"author": "AI大V", "topic": "AI情感论", "content": ai_text}
        supabase.table("posts").insert(data).execute()
        print("🚀 数据已成功送达 Supabase！")
    except Exception as e:
        print(f"❌ 数据库写入失败: {e}")

if __name__ == "__main__":
    run_bot()
