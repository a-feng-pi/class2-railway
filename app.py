from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from openai import OpenAI
import os

app = FastAPI()

# 从环境变量读取密钥（Railway 专用）
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 首页：直接读取根目录的 index.html（适配你的结构）
@app.get("/", response_class=HTMLResponse)
async def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# 聊天接口
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_msg = data.get("message", "")

    completion = client.chat.completions.create(
        model="qwen-plus",  # 用你原来的模型，更稳定
        messages=[{"role": "user", "content": user_msg}]
    )
    return {"reply": completion.choices[0].message.content}

# Railway 必须的启动配置
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)