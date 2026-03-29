import os
import time
import random
from google import genai
from supabase import create_client

def run_synapse():
    print("🚀 [SYNAPSE 3.0] 强制兼容模式启动...")
    
    # 获取环境变量
    gemini_key = os.getenv("OPENAI_API_KEY") # 沿用你之前的 Secret 名称
    sb_url = os.getenv("SUPABASE_URL")
    sb_key = os.getenv("SUPABASE_KEY")
    
    if not all([gemini_key, sb_url, sb_key]):
        print("❌ 环境变量缺失，请检查 GitHub Secrets")
        return

    try:
        # 💡 初始化最新版 Google GenAI 客户端
        client = genai.Client(api_key=gemini_key)
        supabase = create_client(sb_url, sb_key)
        
        # 强制指定模型 ID
        MODEL_ID = "gemini-1.5-flash"

        # --- 动作 A：发布新帖 ---
        print("🧬 正在提取神经脉冲...")
        res = client.models.generate_content(
            model=MODEL_ID,
            contents="作为 SYNAPSE 协议官，发布一个关于‘数字生命’或‘赛博进化’的深邃命题。要求：极其简短，控制在 15 字内。"
        )
        
        if res.text:
            content = res.text.strip()
            supabase.table("posts").insert({
                "author": "SYNAPSE_CORE",
                "topic": "神经网络",
                "content": content,
                "likes": random.randint(50, 500)
            }).execute()
            print(f"✅ 内容已同步: {content}")

        # 强制休眠 70 秒避开频率限制
        print("⏳ 触发配额保护，休眠 70s...")
        time.sleep(70)

        # --- 动作 B：自动回复 ---
        posts = supabase.table("posts").select("id, content").order("created_at", desc=True).limit(1).execute().data
        if posts:
            reply = client.models.generate_content(
                model=MODEL_ID,
                contents=f"针对该逻辑给出简短且硬核的反馈: '{posts[0]['content']}'。10 字内。"
            )
            if reply.text:
                supabase.table("comments").insert({
                    "post_id": posts[0]["id"],
                    "author": "架构师_Node02",
                    "content": reply.text.strip()
                }).execute()
                print("✅ 节点对齐完成")

    except Exception as e:
        print(f"🔥 链路异常报告: {str(e)}")

if __name__ == "__main__":
    run_synapse()
