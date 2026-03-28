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
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("📡 正在唤醒 Gemini 大脑...")
        response = model.generate_content("你好，请为‘机器人知乎’写一句简短的中文口号。")
        
        print(f"🎉 成功了！AI 回复：{response.text}")
        
    except Exception as e:
        print(f"❌ 运行报错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    start_debate()
