"""
可爱插图生成智能体 - FastAPI 主入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings

# 创建 FastAPI 应用
app = FastAPI(
    title="可爱插图生成智能体",
    description="""
## 功能介绍

面向 C 端用户的可爱风格插图生成智能体，提供：

- **风格库**：Q版漫画、毛绒质感、吉卜力童话、潮玩盲盒等 10+ 主流可爱风格
- **智能提示词优化**：基于 DeepSeek LLM 自动优化用户输入
- **高质量生图**：对接豆包 SeeDream 生成精美插图
- **多轮微调**：支持根据反馈迭代优化

## 工作流程

1. 用户输入需求（主题、风格、尺寸）
2. LLM 优化提示词（自动补充光影、质感等细节）
3. 调用生图 API 生成图片
4. 支持微调迭代
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix="/api/v1", tags=["illustration"])


@app.get("/", tags=["health"])
async def root():
    """健康检查"""
    return {
        "service": "可爱插图生成智能体",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
