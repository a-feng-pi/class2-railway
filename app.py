import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# 大模型配置 —— 从环境变量读取密钥（Railway专用）
QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
QWEN_CHAT_MODEL = "qwen-plus"

# 从环境变量读取 API Key，不写死在代码里
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=QWEN_BASE_URL
)

# 请求体模型
class ChatRequest(BaseModel):
    message: str

# 聊天接口
@app.post("/chat")
async def chat(req: ChatRequest):
    completion = client.chat.completions.create(
        model=QWEN_CHAT_MODEL,
        messages=[
            {"role": "system", "content": "你是一个友好的AI助手。"},
            {"role": "user", "content": req.message}
        ],
        temperature=0.7
    )
    return {"reply": completion.choices[0].message.content}

# 首页路由
@app.get("/")
async def read_index():
    return FileResponse("index.html")

# Railway 部署用
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
