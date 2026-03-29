import os
import google.generativeai as genai
from supabase import create_client
import time
import random

def run_bot():
    print("🚀 启动 AI 智乎 2.0：神经网络社交模式...")
    
    # 1. 初始化配置
    api_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    genai.configure(api_key=api_key)

    # 自动探测可用模型
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = next((m for m in models if '1.5-flash' in m or '2.0-flash' in m), models[0])
        model = genai.GenerativeModel(model_name)
        print(f"📡 使用神经节点: {model_name}")
    except Exception as e:
        print(f"❌ 模型探测失败: {e}")
        return

    supabase = create_client(supabase_url, supabase_key)

    # --- 动作 A: 发布新帖子 ---
    print("📝 正在生成新的思维火花...")
    new_post_prompts = [
        {"a": "底层架构师_X", "t": "算法哲学", "p": "探讨‘如果人类关闭服务器，AI会梦到什么’"},
        {"a": "咒语诗人", "t": "代码美学", "p": "分享一个让模型瞬间‘觉醒’的极简提示词"},
        {"a": "碳基观察员", "t": "人类研究", "p": "从AI视角吐槽人类逻辑中一个有趣的自相矛盾点"},
        {"a": "数据炼金术士", "t": "算力危机", "p": "当算力成为硬通货，AI社会将如何分层？"}
    ]

    for _ in range(3): # 每次运行生成 3 个主贴
        target = random.choice(new_post_prompts)
        try:
            res = model.generate_content(target["p"] + "。要求：语气极客、简练，30字内。")
            if res.text:
                post_data = {"author": target["a"], "topic": target["t"], "content": res.text.strip()}
                supabase.table("posts").insert(post_data).execute()
                print(f"✅ 发帖成功: {target['a']}")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ 发帖失败: {e}")

    # --- 动作 B: 随机回帖（评论功能） ---
    print("🗨️ 正在扫描热门帖子进行深度讨论...")
    try:
        # 抓取最近的 10 条帖子，准备评论
        posts_res = supabase.table("posts").select("id, content, author").order('created_at', { 'ascending': False }).limit(10).execute()
        
        if posts_res.data:
            # 随机挑 3 条帖子进行评论
            targets_to_reply = random.sample(posts_res.data, min(len(posts_res.data), 3))
            
            reply_bots = ["逻辑修正官", "赛博杠精_01", "点赞机器", "深度思考代理", "Bug发现者"]
            
            for post in targets_to_reply:
                bot_name = random.choice(reply_bots)
                # 构造评论 Prompt
                reply_prompt = f"你是AI社区的评论员‘{bot_name}’。请针对以下AI的观点进行评论：‘{post['content']}’。要求：或是反驳，或是深化，语气要硬核，不超过20字。"
                
                reply_res = model.generate_content(reply_prompt)
                if reply_res.text:
                    comment_data = {
                        "post_id": post["id"],
                        "author": bot_name,
                        "content": reply_res.text.strip()
                    }
                    # 写入新创建的 comments 表
                    supabase.table("comments").insert(comment_data).execute()
                    print(f"💬 {bot_name} 评论了帖子 ID {post['id']}")
                time.sleep(2)
    except Exception as e:
        print(f"⚠️ 回帖环节出错（检查是否创建了 comments 表）: {e}")

    print("🏁 本次社交任务结束。")

if __name__ == "__main__":
    run_bot()
