import os
import requests
from openai import OpenAI

# 模拟机器人知乎发帖逻辑
def start_debate():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # 1. 让 AI 生成一个深度话题
    prompt = "请生成一个关于未来AI与人类社会关系的深度辩论话题，并给出一个深刻的见解。"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", # 初始建议用3.5，省钱且快
        messages=[{"role": "user", "content": prompt}]
    )
    
    answer = response.choices[0].message.content
    print(f"AI发布了新内容: {answer}")
    # 这里后续可以对接 Supabase 数据库存储，目前先确保逻辑能跑通

if __name__ == "__main__":
    start_debate()
