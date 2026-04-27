# 完整可运行代码
from openai import OpenAI
from fastapi import FastAPI

# 初始化 FastAPI
app = FastAPI()

# 初始化 OpenAI 客户端（已填入你的 API Key）
client = OpenAI(
    api_key="sk-c5595e788c1446c586363d5960b35675"
)

# 测试接口
@app.get("/")
def home():
    return {"message": "服务启动成功！OpenAI 已正常连接"}

# 调用 OpenAI 接口示例
@app.get("/chat")
def chat(prompt: str = "你好"):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return {
        "prompt": prompt,
        "reply": response.choices[0].message.content
    }
    return {"reply": completion.choices[0].message.content}

# Railway 必须的启动配置
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
