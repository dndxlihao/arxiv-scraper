"""
配置文件
"""

import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Settings(BaseSettings):
    """应用配置"""
    
    # 应用配置
    APP_NAME: str = "arXiv论文助手"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # 服务器配置
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # 数据库配置
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://postgres:password@localhost/arxiv_db"
    )
    
    # Redis配置
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # JWT配置
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # CORS配置
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://arxiv-reader.app",
        "https://*.arxiv-reader.app",
    ]
    
    # arXiv API配置
    ARXIV_API_URL: str = "https://export.arxiv.org/api/query"
    ARXIV_MAX_RESULTS: int = 100
    ARXIV_START_INDEX: int = 0
    
    # 推送配置
    APNS_KEY_ID: str = os.getenv("APNS_KEY_ID", "")
    APNS_TEAM_ID: str = os.getenv("APNS_TEAM_ID", "")
    APNS_AUTH_KEY: str = os.getenv("APNS_AUTH_KEY", "")
    FCM_SERVER_KEY: str = os.getenv("FCM_SERVER_KEY", "")
    
    # 爬虫配置
    CRAWL_INTERVAL_HOURS: int = 6  # 每6小时爬取一次
    DAILY_SUMMARY_HOUR: int = 8   # 每天8点发送摘要
    
    # 文件存储
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # 安全配置
    PASSWORD_MIN_LENGTH: int = 8
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # 秒
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# 创建全局配置实例
settings = Settings()

# 验证关键配置
if settings.JWT_SECRET_KEY == "your-secret-key-change-in-production" and not settings.DEBUG:
    raise ValueError("生产环境必须设置JWT_SECRET_KEY")

if __name__ == "__main__":
    # 打印配置信息（用于调试）
    print("=== 配置信息 ===")
    print(f"应用名称: {settings.APP_NAME}")
    print(f"版本: {settings.APP_VERSION}")
    print(f"调试模式: {settings.DEBUG}")
    print(f"服务器: {settings.HOST}:{settings.PORT}")
    print(f"数据库: {settings.DATABASE_URL[:50]}...")
    print(f"Redis: {settings.REDIS_URL}")
    print("================")