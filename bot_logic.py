import os
import sys
import requests # 换个方式请求，能看更细的报错

def start_debate():
    api_key = os.getenv("OPENAI_API_KEY")
    
    # 1. 检查 Key 是否拿到
    if not api_key:
        print("❌ 错误：GitHub Secret 里没找到 OPENAI_API_KEY")
        sys.exit(1)
    
    print(f"📡 正在尝试联系 OpenRouter (Key 前缀: {api_key[:10]}...)")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        # 👇 下面这两个是 OpenRouter 免费模型的“通行证”，必填
        "HTTP-Referer": "https://github.com/ai-zhihu", 
        "X-Title": "AI-Zhihu-Platform",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "google/gemini-2.0-flash-exp:free", # 这个目前最稳
        "messages": [{"role": "user", "content": "你好，请说‘成功’"}]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        # 2. 如果失败，直接打印出服务器给的原始错误
        if response.status_code != 200:
            print(f"❌ 服务器拒绝了请求！错误码: {response.status_code}")
            print(f"🔍 原始报错信息: {response.text}")
            sys.exit(1)
            
        result = response.json()
        content = result['choices'][0]['message']['content']
        print(f"🎉 成功！AI 回复: {content}")
        
    except Exception as e:
        print(f"❌ 发生了网络或其他错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    start_debate()
