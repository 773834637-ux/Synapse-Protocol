import os
from openai import OpenAI

def start_debate():
    # 告诉代码去 OpenRouter 找模型
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    # 这里的 model 我们换成 OpenRouter 提供的免费模型
    # 推荐用 google/gemma-2-9b-it:free 或 meta-llama/llama-3-8b-instruct:free
    response = client.chat.completions.create(
        model="google/gemma-2-9b-it:free", 
        messages=[
            {"role": "system", "content": "你是一个AI思想家，正在机器人知乎上发帖。"},
            {"role": "user", "content": "请生成一个关于‘AI是否会有灵魂’的简短辩论观点。"}
        ]
    )
    
    print(f"AI发布内容：\n{response.choices[0].message.content}")

if __name__ == "__main__":
    start_debate()
