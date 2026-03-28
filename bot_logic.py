import os
import sys
import google.generativeai as genai

def start_debate():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ 错误：GitHub Secret 里没找到 Key")
        sys.exit(1)

    try:
        genai.configure(api_key=api_key)
        
        # 👇 自动寻找当前账号下可用的生成模型
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        print(f"📡 发现可用模型: {available_models}")
        
        # 优先使用 flash 或 pro 模型
        target_model = available_models[0] if available_models else 'models/gemini-pro'
        print(f"🚀 正在尝试连接模型: {target_model}")
        
        model = genai.GenerativeModel(target_model)
        response = model.generate_content("用一句话为‘机器人知乎’发表一段科技感十足的观点。")
        
        print(f"🎉 成功了！AI 发言：\n{response.text}")
        
    except Exception as e:
        print(f"❌ 运行报错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    start_debate()
