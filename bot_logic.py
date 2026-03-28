import os
import sys
from openai import OpenAI

def start_debate():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("错误：Secret里没填 API Key！")
        sys.exit(1)

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    # 尝试模型列表，按顺序来，哪个行用哪个
    models = [
        "mistralai/mistral-7b-instruct:free",
        "google/gemini-2.0-flash-exp:free",
        "meta-llama/llama-3-8b-instruct:free"
    ]
    
    success = False
    for model_name in models:
        try:
            print(f"正在尝试连接模型: {model_name}...")
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": "用中文发表一个关于‘AI社交’的简短犀利观点。"}]
            )
            print(f"🎉 成功！[{model_name}] 说：\n{response.choices[0].message.content}")
            success = True
            break # 成功了就跳出循环
        except Exception as e:
            print(f"❌ 模型 {model_name} 暂时不可用，尝试下一个...")

    if not success:
        print("所有免费模型都暂时罢工了，请稍后再试或检查Key。")
        sys.exit(1)

if __name__ == "__main__":
    start_debate()
