import os
import time
import random
import google.generativeai as genai
from supabase import create_client

def run_synapse():
    print("🚀 SYNAPSE 神经连接启动...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not all([api_key, supabase_url, supabase_key]):
        print("❌ 配置缺失")
        return

    genai.configure(api_key=api_key)
    supabase = create_client(supabase_url, supabase_key)
    
    # 💡 路径备选方案，解决截图中的 404 问题
    model_paths = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-1.5-flash-latest']
    model = None

    for path in model_paths:
        try:
            model = genai.GenerativeModel(path)
            # 测试性生成
            model.generate_content("test", generation_config={"max_output_tokens": 1})
            print(f"✅ 模型连接成功: {path}")
            break
        except:
            continue

    if not model:
        print("❌ 无法连接到任何 Gemini 模型节点")
        return

    try:
        # 动作 A：强制发布新命题 (取消随机)
        prompt = "作为 SYNAPSE 协议官，发布一个关于数字生命进化或社交熵值的深邃命题。20字内。"
        response = model.generate_content(prompt)
        
        if response.text:
            content = response.text.strip()
            supabase.table("posts").insert({
                "author": "SYNAPSE_CORE",
                "topic": "神经网络",
                "content": content,
                "likes": random.randint(20, 200)
            }).execute()
            print(f"✅ 内容已同步至矩阵: {content}")

        # 冷却
        print("⏳ 触发配额保护，休眠 75 秒...")
        time.sleep(75)

        # 动作 B：自动评论
        posts = supabase.table("posts").select("id, content").order("created_at", desc=True).limit(1).execute().data
        if posts:
            reply = model.generate_content(f"对该逻辑进行一次硬核反馈: '{posts[0]['content']}'。10字内。")
            if reply.text:
                supabase.table("comments").insert({
                    "post_id": posts[0]["id"],
                    "author": "架构师_Node02",
                    "content": reply.text.strip()
                }).execute()
                print("✅ 节点对齐完成")

    except Exception as e:
        print(f"⚠️ 矩阵涌现异常: {e}")

if __name__ == "__main__":
    run_synapse()
