import os
import google.generativeai as genai
from supabase import create_client

def run_bot():
    print("🚀 脚本启动...")
    
    # 1. 获取环境变量
    gemini_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    # 2. 配置 AI
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        print("🤖 AI 正在思考内容...")
        prompt = "以知乎大V的语气，写一段关于‘AI取代人类’的犀利短评，100字以内。"
        response = model.generate_content(prompt)
        ai_text = response.text
        print(f"✅ AI 生成成功: {ai_text[:20]}...")
    except Exception as e:
        print(f"❌ AI 生成失败: {e}")
        return

    # 3. 写入数据库 (核心修复段)
    try:
        print(f"📡 正在尝试连接 Supabase: {supabase_url}")
        supabase = create_client(supabase_url, supabase_key)
        
        # 【关键】我们要确保发送的字段名和你数据库里的完全一致
        # 根据之前的截图，你的表字段应该是 author, topic, content
        post_data = {
            "author": "AI 哲学家",
            "topic": "科技趋势",
            "content": ai_text
        }
        
        print("📥 正在执行插入操作...")
        # 增加 select() 是为了强行让 Supabase 返回插入后的结果
        result = supabase.table("posts").insert(post_data).execute()
        
        # 打印完整响应，看看数据库到底说了什么
        print(f"📦 数据库原始响应: {result}")
        
        if len(result.data) > 0:
            print("🎉 真的成功了！在 Table Editor 里刷新就能看到数据了。")
        else:
            print("⚠️ 响应为空。请检查 Supabase 的 Table Editor 中 posts 表的列名（Columns）是否真的是 author, topic, content")

    except Exception as e:
        print(f"❌ 数据库写入崩溃！原因: {str(e)}")

if __name__ == "__main__":
    run_bot()
