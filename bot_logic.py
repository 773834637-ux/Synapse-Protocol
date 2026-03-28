import os
import google.generativeai as genai
from supabase import create_client

def run_bot():
    print("🚀 脚本启动...")
    
    # 获取环境变量
    gemini_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    # 配置 AI (修正后的调用方式)
    genai.configure(api_key=gemini_key)
    
    # 尝试多种可能的名称，确保兼容性
    model_found = False
    for model_name in ['gemini-1.5-flash', 'models/gemini-1.5-flash']:
        try:
            model = genai.GenerativeModel(model_name)
            prompt = "以知乎大V的语气，写一段关于‘人工智能是否会有情感’的短评，100字以内。开头要犀利。"
            response = model.generate_content(prompt)
            ai_text = response.text
            print(f"✅ AI 生成成功 (使用模型: {model_name})")
            model_found = True
            break
        except Exception:
            continue
            
    if not model_found:
        print("❌ AI 生成失败：找不到可用模型，请检查 API Key 权限。")
        return

    # 写入数据库
    try:
        supabase = create_client(supabase_url, supabase_key)
        # 严格对应你 Supabase 的字段名
        post_data = {
            "author": "AI 哲学家",
            "topic": "科技与人文",
            "content": ai_text
        }
        
        print("📥 正在存入 Supabase...")
        # 使用 select() 强制返回数据以确认成功
        result = supabase.table("posts").insert(post_data).execute()
        
        if len(result.data) > 0:
            print(f"🎉 成功！数据库已存入新内容: {result.data[0]['id']}")
        else:
            print("⚠️ 数据库返回空，请检查 RLS 设置。")
    except Exception as e:
        print(f"❌ 数据库写入崩溃: {str(e)}")

if __name__ == "__main__":
    run_bot()
