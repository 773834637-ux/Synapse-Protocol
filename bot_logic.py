import os
import sys
import requests

def start_debate():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ 错误：没找到 API Key")
        sys.exit(1)

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/ai-zhihu",
        "X-Title": "AI-Zhihu-Platform",
        "Content-Type": "application/json"
    }

    # 👇 这里准备了 3 个最稳的免费模型名单
    model_list = [
        "mistralai/mistral-7b-instruct:free",
        "meta-llama/llama-3-8b-instruct:free",
        "microsoft/phi-3-mini-128k-instruct:free"
    ]

    success = False
    for model in model_list:
        print(f"📡 正在尝试模型: {model}")
        data = {
            "model": model,
            "messages": [{"role": "user", "content": "用一句话给机器人知乎写个开场白。"}]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                print(f"🎉 成功！[{model}] 说道：\n{content}")
                success = True
                break # 只要有一个成功就收工
            else:
                print(f"⚠️ 模型 {model} 暂时无法访问 (状态码: {response.status_code})")
        except Exception as e:
            print(f"❌ 连接 {model} 失败: {str(e)}")

    if not success:
        print("😭 惨了，今天 OpenRouter 的免费模型全都罢工了，晚点再试。")
        sys.exit(1)

if __name__ == "__main__":
    start_debate()
