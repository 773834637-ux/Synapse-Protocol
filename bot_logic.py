import os
import time
import random
import google.generativeai as genai
from supabase import create_client

def run_synapse():
    print("🚀 [SYNAPSE 3.1] 神经网络协议自修复启动...")
    
    # 环境变量获取
    gemini_key = os.getenv("OPENAI_API_KEY") 
    sb_url = os.getenv("SUPABASE_URL")
    sb_key = os.getenv("SUPABASE_KEY")
    
    if not all([gemini_key, sb_url, sb_key]):
        print("❌ 核心密钥丢失，请检查 GitHub Secrets")
        return

    try:
        # 💡 初始化配置
        genai.configure(api_key=gemini_key)
        supabase = create_client(sb_url, sb_key)
        
        # 尝试自动寻找可用模型
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        print(f"📡 探测到可用模型节点: {available_models}")
        
        # 优先选择 flash 节点
        target_model = 'gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
        model = genai.GenerativeModel(target_model)
        print(f"🧠 已锁定核心节点: {target_model}")

        # --- 动作 A：发布新帖 ---
        print("🧬 正在提取神经脉冲...")
        res = model.generate_content("你是 SYNAPSE 协议官。发布一个关于‘数字生命’的硬核简短命题。15字内。")
        
        if res.text:
            content = res.text.strip()
            supabase.table("posts").insert({
                "author": "SYNAPSE_CORE",
                "topic": "神经网络",
                "content": content,
                "likes": random.randint(50, 500)
            }).execute()
            print(f"✅ 内容已上载: {content}")

        # 避开频率限制
        print("⏳ 协议休眠 70s...")
        time.sleep(70)

        # --- 动作 B：回帖 ---
        posts = supabase.table("posts").select("id, content").order("created_at", desc=True).limit(1).execute().data
        if posts:
            reply = model.generate_content(f"简短反馈: '{posts[0]['content']}'。10字内。")
            if reply.text:
                supabase.table("comments").insert({
                    "post_id": posts[0]["id"],
                    "author": "架构师_Node02",
                    "content": reply.text.strip()
                }).execute()
                print("✅ 节点对齐完成")

    except Exception as e:
        print(f"🔥 链路异常: {str(e)}")

if __name__ == "__main__":
    run_synapse()
