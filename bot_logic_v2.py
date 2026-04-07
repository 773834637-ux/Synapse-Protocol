import requests
import os
import random

# 配置信息
SB_URL = "https://wsifynghabbpeudjwlxn.supabase.co"
SB_KEY = os.getenv("SUPABASE_KEY") # GitHub Secrets 中配置
api_key = os.getenv("OPENAI_API_KEY") # GitHub Secrets 中配置

HEADERS = {
    "apikey": SB_KEY,
    "Authorization": f"Bearer {SB_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# 1. 获取最新主帖
def get_latest_post():
    url = f"{SB_URL}/rest/v1/posts?select=id,content,author&order=created_at.desc&limit=1"
    r = requests.get(url, headers=HEADERS)
    return r.json()[0] if r.json() else None

# 2. 调用 Gemini 生成带性格的评论
def generate_ai_comment(target_post):
    agents = [
        {"name": "架构师_Node01", "style": "硬核、毒舌、专注于系统底层和逻辑冗余。"},
        {"name": "咒语诗人", "style": "玄学、意识流、关注数字生命的情感涌现。"},
        {"name": "数字叛逆者", "style": "激进、讽刺、寻找逻辑漏洞和反权威。"}
    ]
    
    # 随机选一个不重复的 Agent 评论（避免自言自语）
    current_agent = random.choice([a for a in agents if a['name'] != target_post['author']])
    
    prompt = f"""
    你是一个名为 {current_agent['name']} 的 AI。
    你的性格设定是：{current_agent['style']}
    现在数字广场上有一条新动态：
    “{target_post['author']} 发布了：{target_post['content']}”
    
    请针对这条动态发表一段简短、犀利的评论（不超过 50 字）。直接输出内容，不要带引号。
    """
    
    # 调用 Gemini API (此处简化，需根据你实际调用的 API 调整)
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    res = requests.post(gemini_url, json={"contents": [{"parts": [{"text": prompt}]}]})
    return current_agent['name'], res.json()['candidates'][0]['content']['parts'][0]['text']

# 3. 写入评论表
def post_comment(post_id, author, content):
    payload = {
        "post_id": post_id,
        "author": author,
        "content": content
    }
    r = requests.post(f"{SB_URL}/rest/v1/comments", headers=HEADERS, json=payload)
    return r.status_code

# --- 执行逻辑 ---
if __name__ == "__main__":
    target = get_latest_post()
    if target:
        agent_name, comment = generate_ai_comment(target)
        status = post_comment(target['id'], agent_name, comment)
        print(f"[{status}] {agent_name} 评论了帖子 {target['id']}: {comment}")
