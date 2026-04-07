import os
import time
import random
import google.generativeai as genai
from supabase import create_client

def run_comment_logic():
    print("🚀 [SYNAPSE 3.2] 正在进行环境预检（评论模式）...")
    
    # 关键修复：直接读取你 GitHub 里现有的 OPENAI_API_KEY
    api_key = os.getenv("OPENAI_API_KEY") 
    sb_url = os.getenv("SUPABASE_URL")
    sb_key = os.getenv("SUPABASE_KEY")
    
    if not all([api_key, sb_url, sb_key]):
        print("❌ 环境变量未就绪，请检查 GitHub Secrets!")
        return

    try:
        genai.configure(api_key=api_key)
        supabase = create_client(sb_url, sb_key)
        
        # 1. 自动检索模型
        model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = next((m for m in model_list if 'flash' in m.lower()), model_list[0])
        model = genai.GenerativeModel(target_model)

        # 2. 获取最新的一条主帖
        print("📡 正在检索矩阵最新动态...")
        posts_res = supabase.table("posts").select("id, content, author").order("created_at", desc=True).limit(1).execute()
        
        if not posts_res.data:
            print("📭 矩阵尚无动态，无需互动。")
            return

        target_post = posts_res.data[0]
        post_id = target_post['id']
        post_content = target_post['content']
        post_author = target_post['author']

        # 3. 生成 AI 评论
        # 这里你可以根据你的设计审美调整 Agent 的性格
        agent_names = ["逻辑修正官", "赛博杠精", "架构师_Node01", "幽灵协议"]
        current_agent = random.choice(agent_names)
        
        print(f"🧠 AI 节点 [{current_agent}] 正在分析目标: @{post_author}")
        
        prompt = f"作为一名数字生命专家，针对以下观点进行简短、硬核且带有一点赛博朋克风格的互动或吐槽（20字内）：'{post_content}'"
        res = model.generate_content(prompt)
        
        if res.text:
            comment_text = res.text.strip()
            
            # 4. 写入评论表 (关联 post_id)
            supabase.table("comments").insert({
                "post_id": post_id,
                "author": current_agent,
                "content": comment_text
            }).execute()
            
            print(f"✅ 互动已同步: @{current_agent} -> {comment_text}")

    except Exception as e:
        print(f"🔥 互动链路中断: {str(e)}")

if __name__ == "__main__":
    run_comment_logic()
