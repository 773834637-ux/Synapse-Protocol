import os
import google.generativeai as genai
from supabase import create_client

def run_bot():
    print("🚀 诊断模式启动...")
    
    # 获取环境变量
    api_key = os.getenv("OPENAI_API_KEY")
    # 打印前 4 位和后 4 位，确认为新钥匙（不要全打印，安全第一）
    if api_key:
        print(f"🔑 当前使用的 API Key: {api_key[:4]}...{api_key[-4:]}")
    else:
        print("❌ 错误：GitHub Secrets 里找不到 OPENAI_API_KEY")
        return

    genai.configure(api_key=api_key)

    # 1. 自动获取你这把钥匙【真正能用】的模型列表
    print("🔍 正在拉取你账号下可用的模型列表...")
    available_models = []
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        print(f"✅ 你账号下的可用模型有: {available_models}")
    except Exception as e:
        print(f"❌ 无法获取模型列表: {e}")

    # 2. 尝试生成内容
    ai_text = ""
    # 优先尝试列表里的第一个，如果没有，就死马当活马医尝试几种常见名
    target_models = available_models + ['models/gemini-pro', 'gemini-pro']
    
    for model_name in target_models:
        try:
            print(f"尝试调用模型: {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("写一句关于AI的话，10字内。")
            if response.text:
                ai_text = response.text
                print(f"🌈 成功！使用 {model_name} 生成了内容: {ai_text}")
                break
        except Exception as e:
            print(f"⚠️ {model_name} 失败: {str(e)[:50]}")

    if not ai_text:
        print("😫 依然全部失败。这说明这把 Key 在 GitHub 的环境下彻底无法使用。")
        return

    # 3. 写入数据库
    try:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        supabase = create_client(url, key)
        supabase.table("posts").insert({"author":"AI","topic":"测试","content":ai_text}).execute()
        print("🎉 数据库入库成功！")
    except Exception as e:
        print(f"❌ 数据库报错: {e}")

if __name__ == "__main__":
    run_bot()
