#!/usr/bin/env python3
"""
arXiv论文助手 - 后端API主程序
"""

import os
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from contextlib import asynccontextmanager
import logging
from typing import Optional

from database import engine, Base, get_db
from models import User, Paper, Notification, Team
from routers import auth, papers, notifications, teams, admin
from config import settings

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 应用生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    - 启动时：创建数据库表
    - 关闭时：清理资源
    """
    logger.info("启动arXiv论文助手API服务...")
    
    # 创建数据库表
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("数据库表创建成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise
    
    # 启动定时任务（这里可以添加爬虫任务）
    logger.info("服务启动完成")
    
    yield  # 应用运行期间
    
    # 关闭时清理
    logger.info("关闭服务...")
    await engine.dispose()

# 创建FastAPI应用
app = FastAPI(
    title="arXiv论文助手API",
    description="为arXiv论文助手iOS APP提供后端API服务",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

# 包含路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(papers.router, prefix="/api/v1/papers", tags=["论文"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["通知"])
app.include_router(teams.router, prefix="/api/v1/teams", tags=["团队"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["管理"])

# 健康检查端点
@app.get("/")
async def root():
    """根端点，用于健康检查"""
    return {
        "message": "arXiv论文助手API服务运行正常",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "timestamp": "2026-03-09T10:58:00Z"}

# 错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP异常处理器"""
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """通用异常处理器"""
    logger.error(f"未处理的异常: {exc}", exc_info=True)
    return {
        "error": "服务器内部错误",
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"启动服务，地址: http://{settings.HOST}:{settings.PORT}")
    logger.info(f"API文档: http://{settings.HOST}:{settings.PORT}/docs")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )