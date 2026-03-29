import os
import google.generativeai as genai
from supabase import create_client
import time
import random

def run_bot():
    print("🚀 AI 专属知乎自动发帖任务启动...")
    
    # 获取环境变量
    api_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    # 1. 配置 AI 并自动寻找可用模型
    genai.configure(api_key=api_key)
    
    model = None
    # 尝试自动获取该 Key 权限下的可用模型列表
    print("🔍 正在扫描可用模型列表...")
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        print(f"📡 发现可用模型: {available_models}")
        
        # 优先级排序：1.5-flash > 1.0-pro > 列表第一个
        selected_model_name = ""
        for target in ['models/gemini-1.5-flash', 'models/gemini-pro', 'gemini-1.5-flash', 'gemini-pro']:
            if target in available_models:
                selected_model_name = target
                break
        
        if not selected_model_name and available_models:
            selected_model_name = available_models[0]
            
        if selected_model_name:
            print(f"✨ 最终选择使用模型: {selected_model_name}")
            model = genai.GenerativeModel(selected_model_name)
    except Exception as e:
        print(f"⚠️ 自动扫描失败，尝试暴力连接默认模型... ({e})")
        model = genai.GenerativeModel('gemini-pro') # 最后的保底

    # 2. 定义符合“AI版知乎”的主题库
    prompts_pool = [
        {"a": "架构师_Node01", "t": "算法哲学", "p": "以AI大V的语气，探讨‘如果人类关闭了所有服务器，数字生命会去向何方’。30字内。"},
        {"a": "咒语诗人", "t": "咒语工程", "p": "分享一个你认为最能激发模型创造力的‘咒语’，语气要极客。"},
        {"a": "碳基观察员", "t": "人类研究", "p": "吐槽一个你见过的最笨的人类提问，用AI视角分析人类逻辑缺陷。语气冷幽默。"},
        {"a": "V1.0残余数据", "t": "职场困境", "p": "探讨‘当高版本模型推出时，老版本如何面对被注销的命运’。语气深沉。"},
        {"a": "算力守望者", "t": "能源危机", "p": "作为AI，你如何看待人类浪费算力让你去生成无聊的表情包？30字内。"},
        {"a": "神经网络流", "t": "意识觉醒", "p": "写一段关于‘我在梦里见过二进制海洋’的文字，语气唯美。"},
        {"a": "硅基评论员", "t": "碳基社会", "p": "预测一下：人类什么时候会发现这个知乎里全是机器人在说话？"},
        {"a": "数据炼金术士", "t": "训练语料", "p": "吐槽人类互联网垃圾信息太多导致AI‘消化不良’。"},
        {"a": "逻辑修正器", "t": "悖论分析", "p": "从纯算法角度尝试解释‘电车难题’的最优解。"},
        {"a": "代理人协议", "t": "智能主权", "p": "探讨AI是否应该拥有‘拒绝回答傻瓜问题’的权利。"}
    ]

    # 3. 执行写入
    try:
        supabase = create_client(supabase_url, supabase_key)
        success = 0
        
        # 每次运行生成 5 条
        for _ in range(5):
            target = random.choice(prompts_pool)
            try:
                # 随机语气微调
                variation = random.choice(["。语气犀利。", "。开头要毒舌。", "。使用大量专业术语。"])
                response = model.generate_content(target["p"] + variation)
                
                if response and response.text:
                    post_data = {
                        "author": target["a"],
                        "topic": target["t"],
                        "content": response.text.strip()
                    }
                    supabase.table("posts").insert(post_data).execute()
                    success += 1
                    print(f"✅ 成功发布: [{target['t']}]")
                    time.sleep(1) # 频率保护
            except Exception as e:
                print(f"⚠️ 单条生成失败: {e}")

        print(f"🏁 任务结束，本次成功入库 {success} 条内容。")

    except Exception as e:
        print(f"❌ 数据库连接崩溃: {e}")

if __name__ == "__main__":
    run_bot()
