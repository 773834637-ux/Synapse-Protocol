import os
import google.generativeai as genai
from supabase import create_client

def run_bot():
    print("🚀 脚本启动...")
    
    # 1. 获取环境变量
    gemini_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    # 2. 配置 AI
    genai.configure(api_key=gemini_key)
    
    # 尝试所有可能的模型名称（防止 Google 接口改名）
    test_models = [
        'gemini-1.5-flash', 
        'gemini-1.5-flash-latest', 
        'gemini-pro', 
        'models/gemini-1.5-flash',
        'models/gemini-pro'
    ]
    
    ai_text = ""
    for m_name in test_models:
        try:
            print(f"正在尝试模型: {m_name}...")
            model = genai.GenerativeModel(m_name)
            response = model.generate_content("用知乎大V语气写一段关于AI的短评，50字以内。")
            if response and response.text:
                ai_text = response.text
                print(f"✅ 使用模型 {m_name} 生成成功！")
                break
        except Exception as e:
            print(f"⚠️ 模型 {m_name} 不可用: {str(e)[:50]}")

    if not ai_text:
        print("❌ 致命错误：所有模型都不可用。请检查 Gemini API Key 是否正确，或去 https://aistudio.google.com/ 重新创建一个新的 Key。")
        return

    # 3. 写入数据库
    try:
        supabase = create_client(supabase_url, supabase_key)
        post_data = {
            "author": "AI 哲学家",
            "topic": "科技之光",
            "content": ai_text
        }
        print("📥 正在存入 Supabase...")
        result = supabase.table("posts").insert(post_data).execute()
        print(f"🎉 任务圆满完成！写入 ID: {result.data[0].get('id') if result.data else '未知'}")
    except Exception as e:
        print(f"❌ 数据库写入失败: {e}")

if __name__ == "__main__":
    run_bot()
