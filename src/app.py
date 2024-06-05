import os
import logging

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from .limiter import get_real_ipaddr
from .chatgpt_router import router as chatgpt_router
from .divination_router import router as divination_router
from .user_router import router as user_router

# 初始化日志模块，用于记录程序运行中的信息
_logger = logging.getLogger(__name__)

# 初始化FastAPI应用，设置应用名称
app = FastAPI(title="AI Mysticism")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
        # "http://localhost:5186",
        # "http://localhost",
        # "http://127.0.0.1"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 引入路由，分别处理chatgpt、divination和user相关的API请求
app.include_router(chatgpt_router)
app.include_router(divination_router)
app.include_router(user_router)

# 如果dist目录存在，说明有前端构建产物，配置静态文件服务
if os.path.exists("dist"):
     # 配置根路径和登录路径的GET请求，返回前端index.html文件
    @app.get("/")
    @app.get("/login/{path}")
    async def read_index(request: Request):
        # 记录请求的来源IP地址
        _logger.info(f"Request from {get_real_ipaddr(request)}")
        # 返回dist目录下的index.html文件，设置缓存控制为no-cache
        return FileResponse(
            "dist/index.html",
            headers={"Cache-Control": "no-cache"}
        )

    # 将静态文件目录挂载到应用的根路径下
    app.mount("/", StaticFiles(directory="dist"), name="static")


# 全局异常处理，捕获所有异常，返回500错误信息
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
     # 返回内部服务器错误的文本响应，包含异常信息
    return PlainTextResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=f"Internal Server Error: {exc}",
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.0", port=8000)
