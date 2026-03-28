import os
import google.generativeai as genai
from supabase import create_client

def run_bot():
    print("🚀 脚本开始运行...")
    
    # 1. 从 GitHub Secrets 获取环境变量
    gemini_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    # 检查环境变量是否读取成功
    if not all([gemini_key, supabase_url, supabase_key]):
        print("❌ 错误：环境变量缺失！请检查 GitHub Secrets 是否配置了 SUPABASE_KEY, SUPABASE_URL 和 OPENAI_API_KEY")
        return

    # 2. 配置 Gemini 并尝试生成内容
    genai.configure(api_key=gemini_key)
    
    # 自动轮询模型名称，解决 404 NotFound 问题
    model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    ai_text = ""

    for name in model_names:
        try:
            print(f"正在尝试连接 AI 模型: {name}...")
            model = genai.GenerativeModel(name)
            prompt = "以知乎大V的语气，写一段关于‘人工智能是否会有情感’的短评，100字以内。开头要惊艳。"
            response = model.generate_content(prompt)
            if response and response.text:
                ai_text = response.text
                print(f"✅ AI 生成成功 (使用模型: {name})")
                break
        except Exception as e:
            print(f"⚠️ 模型 {name} 尝试失败，跳过...")

    if not ai_text:
        print("😭 所有 AI 模型都无法连接，请检查 Gemini API Key 是否有效。")
        return

    # 3. 写入 Supabase 数据库
    print("📡 准备写入数据库...")
    try:
        supabase = create_client(supabase_url, supabase_key)
        # 准备数据，确保列名 id, created_at 是数据库自动生成的
        post_data = {
            "author": "AI 哲学家",
            "topic": "人工智能情感论",
            "content": ai_text
        }
        
        # 执行插入并打印完整响应
        response = supabase.table("posts").insert(post_data).execute()
        
        # 检查是否真的写入成功
        if hasattr(response, 'data') and len(response.data) > 0:
            print("🎉 恭喜！数据已成功写入 Supabase！")
            print(f"写入内容回显: {response.data}")
        else:
            print(f"⚠️ 数据库返回了空结果，请检查权限。原始响应: {response}")

    except Exception as e:
        print(f"❌ 数据库写入发生致命错误！")
        print(f"错误详情 (请看这里): {str(e)}")

if __name__ == "__main__":
    run_bot()
