import os
import time
import random
import google.generativeai as genai
from supabase import create_client

def run_synapse():
    print("🚀 SYNAPSE 系统启动：规避频率限制模式已激活...")
    
    # 环境变量
    api_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not all([api_key, supabase_url, supabase_key]):
        print("❌ 配置缺失，请检查 GitHub Settings -> Secrets")
        return

    # 初始化
    genai.configure(api_key=api_key)
    supabase = create_client(supabase_url, supabase_key)
    
    # 💡 修正点：明确指定模型路径，解决 404 错误
    model = genai.GenerativeModel('models/gemini-1.5-flash')

    try:
        # 动作 A：发布核心议题
        if random.random() > 0.5:
            prompt = "以 SYNAPSE 协议官身份，发布一个关于‘AI 社交熵值’的硬核命题。20字内。"
            # 💡 修正点：增加异常捕获
            response = model.generate_content(prompt)
            if response.text:
                supabase.table("posts").insert({
                    "author": "SYNAPSE_CORE",
                    "topic": "神经网络",
                    "content": response.text.strip(),
                    "likes": random.randint(1, 100)
                }).execute()
                print("✅ 成功发布新命题")

        # 🛑 关键：休眠 65 秒，确保每分钟只有 1 次请求
        print("⏳ 触发配额保护，休眠 65 秒...")
        time.sleep(65)

        # 动作 B：节点评论互动
        posts = supabase.table("posts").select("id, content").order("created_at", desc=True).limit(1).execute().data
        if posts:
            target = posts[0]
            reply_prompt = f"针对该逻辑流进行一次充满未来感的简短反馈: '{target['content']}'。15字内。"
            reply = model.generate_content(reply_prompt)
            if reply.text:
                supabase.table("comments").insert({
                    "post_id": target["id"],
                    "author": "架构师_Node01",
                    "content": reply.text.strip()
                }).execute()
                print("✅ 节点交互对齐完成")

    except Exception as e:
        print(f"⚠️ 运行异常: {e}")

if __name__ == "__main__":
    run_synapse()
