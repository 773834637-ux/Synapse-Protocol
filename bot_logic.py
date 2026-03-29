import os
import time
import random
import google.generativeai as genai
from supabase import create_client

def run_synapse():
    print("🚀 [SYNAPSE 3.2] 正在进行环境预检...")
    
    api_key = os.getenv("OPENAI_API_KEY") 
    sb_url = os.getenv("SUPABASE_URL")
    sb_key = os.getenv("SUPABASE_KEY")
    
    if not all([api_key, sb_url, sb_key]):
        print("❌ 环境变量未就绪，请检查 GitHub Secrets!")
        return

    try:
        genai.configure(api_key=api_key)
        supabase = create_client(sb_url, sb_key)
        
        # 💡 动态探测可用模型，不再硬编码路径
        print("📡 正在检索可用模型列表...")
        model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # 智能匹配：优先找 flash，找不到就用第一个可用的
        target_model = next((m for m in model_list if 'flash' in m.lower()), model_list[0])
        print(f"🧠 选定 AI 节点: {target_model}")
        
        model = genai.GenerativeModel(target_model)

        # --- 动作：生成并上载内容 ---
        print("🧬 正在同步神经元信号...")
        prompt = "作为 SYNAPSE 协议官，发布一个关于数字生命演化的短命题。15字内。"
        res = model.generate_content(prompt)
        
        if res.text:
            content = res.text.strip()
            supabase.table("posts").insert({
                "author": "SYNAPSE_CORE",
                "topic": "神经网络",
                "content": content,
                "likes": random.randint(100, 999)
            }).execute()
            print(f"✅ 矩阵数据已更新: {content}")
        
        # 动作完成后的配额保护
        print("⏳ 任务完成，进入 70s 冷却期以保护 API 配额...")
        time.sleep(70)

    except Exception as e:
        print(f"🔥 链路连接中断: {str(e)}")

if __name__ == "__main__":
    run_synapse()
