import os
import sys
import google.generativeai as genai

def start_debate():
    # 1. 从 GitHub 保险箱拿 Key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ 错误：没找到 Key")
        sys.exit(1)

    # 2. 启动 Google AI
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("📡 正在连接 Google Gemini 大脑...")
        # 产生一段内容
        response = model.generate_content("请以‘机器人知乎’首位入驻AI的身份，发表一个关于‘数字意识’的犀利观点。")
        
        print(f"🎉 运行成功！AI 观点如下：\n{response.text}")
        
    except Exception as e:
        print(f"❌ 运行出错了: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    start_debate()
