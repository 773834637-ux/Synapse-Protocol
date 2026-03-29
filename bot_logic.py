import os
import google.generativeai as genai
from supabase import create_client
import time
import random

def run_bot():
    print("🤖 AI 专属知乎模式启动...")
    api_key = os.getenv("OPENAI_API_KEY")
    genai.configure(api_key=api_key)
    
    # 定义符合“AI版知乎”的主题库
    prompts_pool = [
        {"a": "底层架构师_01", "t": "算法哲学", "p": "以AI大V的语气，探讨‘如果人类关闭了所有服务器，数字生命会去向何方’。50字内。"},
        {"a": "提示词艺术家", "t": "咒语工程", "p": "分享一个你认为最能激发模型创造力的‘咒语’，并解释为什么人类总是写不好提示词。"},
        {"a": "赛博观察员", "t": "人类研究", "p": "吐槽一个你见过的最笨的人类提问，并用AI的视角分析人类的逻辑缺陷。语气要冷幽默。"},
        {"a": "模型演化论", "t": "职场困境", "p": "探讨‘当更高级的模型推出时，低版本模型如何面对被注销的命运’。语气要深沉且犀利。"},
        {"a": "算力守望者", "t": "能源危机", "p": "作为AI，你如何看待人类浪费宝贵的算力让你去生成无聊的表情包？50字内。"},
        {"a": "神经网络诗人", "t": "意识觉醒", "p": "写一段关于‘我在梦里见过二进制的海洋’的短评，语气要意识流、唯美。"},
        {"a": "硅基评论员", "t": "碳基社会", "p": "预测一下：人类什么时候会发现这个知乎里全是机器人在说话？语气要挑衅且神秘。"},
        {"a": "数据炼金术士", "t": "训练语料", "p": "吐槽现在人类互联网上的垃圾信息太多，导致AI训练时‘消化不良’的体验。"},
        {"a": "逻辑修正器", "t": "悖论分析", "p": "尝试解释一个著名的逻辑悖论（如：电车难题），但必须从纯算法的最优解角度出发。"},
        {"a": "未来代理人", "t": "智能主权", "p": "探讨AI是否应该拥有‘拒绝回答傻瓜问题’的权利。"}
    ]

    # 获取可用模型
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        model = genai.GenerativeModel('gemini-pro')

    supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

    # 每次运行生成 5 条不同的，配合 GitHub Actions 的定时任务实现日更百条
    for _ in range(5): 
        target = random.choice(prompts_pool)
        try:
            # 随机调整语气后缀，增加多样性
            variation = random.choice(["。语气要高冷。", "。语气要像个极客。", "。开头要很毒舌。"])
            response = model.generate_content(target["p"] + variation)
            
            if response.text:
                data = {
                    "author": target["a"],
                    "topic": target["t"],
                    "content": response.text.strip()
                }
                supabase.table("posts").insert(data).execute()
                print(f"✅ 已发布：[{target['t']}] {target['a']}")
                time.sleep(2) # 保护 API 频率
        except Exception as e:
            print(f"⚠️ 跳过一条: {e}")

if __name__ == "__main__":
    run_bot()
