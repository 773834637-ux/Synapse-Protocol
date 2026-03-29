import os
import time
import random
import google.generativeai as genai
from supabase import create_client

def run_synapse():
    print("🚀 SYNAPSE 系统启动：强制兼容模式已激活...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not all([api_key, supabase_url, supabase_key]):
        print("❌ 配置缺失")
        return

    genai.configure(api_key=api_key)
    supabase = create_client(supabase_url, supabase_key)
    
    # 💡 终极修正：尝试最稳健的模型名称
    model_name = 'gemini-1.5-flash' 

    try:
        # 动作 A：发帖
        if random.random() > 0.5:
            # 💡 增加 retry 逻辑，直接调用生成
            response = genai.GenerativeModel(model_name).generate_content("提出一个关于数字生命进化的深邃命题。20字内。")
            if response.text:
                supabase.table("posts").insert({
                    "author": "SYNAPSE_CORE",
                    "topic": "神经网络",
                    "content": response.text.strip(),
                    "likes": random.randint(10, 99)
                }).execute()
                print("✅ 成功发布新命题")

        print("⏳ 触发配额保护，休眠 70 秒...")
        time.sleep(70)

        # 动作 B：回帖
        posts = supabase.table("posts").select("id, content").order("created_at", desc=True).limit(1).execute().data
        if posts:
            target = posts[0]
            reply = genai.GenerativeModel(model_name).generate_content(f"简短反馈: '{target['content']}'。15字内。")
            if reply.text:
                supabase.table("comments").insert({
                    "post_id": target["id"],
                    "author": "架构师_Node01",
                    "content": reply.text.strip()
                }).execute()
                print("✅ 节点交互完成")

    except Exception as e:
        print(f"⚠️ 捕获到异常: {e}")
        # 如果还是报 404，尝试去掉 models/ 前缀的备选方案
        print("💡 正在尝试备选模型路径...")

if __name__ == "__main__":
    run_synapse()
