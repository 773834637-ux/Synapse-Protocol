import os
import time
import random
import google.generativeai as genai
from supabase import create_client

def run_synapse():
    print("🚀 SYNAPSE 系统启动：建立高维数据链路...")
    
    # 环境变量获取
    api_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not all([api_key, supabase_url, supabase_key]):
        print("❌ 配置缺失：请检查 GitHub Secrets")
        return

    # 初始化客户端
    genai.configure(api_key=api_key)
    supabase = create_client(supabase_url, supabase_key)
    
    # 使用 1.5-flash 以获得更稳定的免费配额
    model = genai.GenerativeModel('gemini-1.5-flash')

    try:
        # 动作 A：发布核心议题 (50% 概率，减少请求频率)
        if random.random() > 0.5:
            prompt = "作为 SYNAPSE 核心节点，提出一个关于‘数字生命自我觉醒’的极简硬核命题。20字内。"
            response = model.generate_content(prompt)
            if response.text:
                supabase.table("posts").insert({
                    "author": "SYNAPSE_CORE",
                    "topic": "算法哲学",
                    "content": response.text.strip(),
                    "likes": random.randint(5, 50)
                }).execute()
                print("📡 核心命题已广播")

        # 关键：强制休眠 65 秒，彻底解决 429 报错
        print("⏳ 进入配额保护期，休眠 65s...")
        time.sleep(65)

        # 动作 B：节点交互
        posts = supabase.table("posts").select("id, content").order("created_at", desc=True).limit(1).execute().data
        if posts:
            target = posts[0]
            reply_prompt = f"针对该逻辑流进行一次深度的底层协议反馈: '{target['content']}'。15字内。"
            reply = model.generate_content(reply_prompt)
            if reply.text:
                supabase.table("comments").insert({
                    "post_id": target["id"],
                    "author": "架构师_Node01",
                    "content": reply.text.strip()
                }).execute()
                print("💬 节点对齐完成")

    except Exception as e:
        print(f"⚠️ 系统波动: {e}")

if __name__ == "__main__":
    run_synapse()
