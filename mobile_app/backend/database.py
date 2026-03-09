"""
数据库连接和会话管理
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator

from config import settings

logger = logging.getLogger(__name__)

# 创建异步引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # 调试模式下显示SQL
    pool_size=20,  # 连接池大小
    max_overflow=10,  # 最大溢出连接数
    pool_pre_ping=True,  # 连接前ping检查
    pool_recycle=3600,  # 连接回收时间（秒）
)

# 创建会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# 获取数据库会话的依赖
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库会话的依赖函数
    使用示例：
        async def some_endpoint(db: AsyncSession = Depends(get_db)):
            # 使用db会话
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"数据库会话错误: {e}")
            raise
        finally:
            await session.close()

@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """
    上下文管理器方式获取数据库会话
    使用示例：
        async with get_db_context() as db:
            # 使用db会话
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"数据库会话错误: {e}")
            raise
        finally:
            await session.close()

async def test_connection():
    """测试数据库连接"""
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        logger.info("数据库连接测试成功")
        return True
    except Exception as e:
        logger.error(f"数据库连接测试失败: {e}")
        return False

async def create_tables():
    """创建所有表（开发环境使用）"""
    from models import Base
    
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("数据库表创建成功")
        return True
    except Exception as e:
        logger.error(f"创建数据库表失败: {e}")
        return False

async def drop_tables():
    """删除所有表（开发环境使用）"""
    from models import Base
    
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.info("数据库表删除成功")
        return True
    except Exception as e:
        logger.error(f"删除数据库表失败: {e}")
        return False

# 数据库工具函数
class DatabaseUtils:
    """数据库工具类"""
    
    @staticmethod
    async def get_or_create(session: AsyncSession, model, **kwargs):
        """
        获取或创建记录
        返回: (instance, created)
        """
        try:
            # 尝试获取
            query = session.query(model).filter_by(**kwargs)
            result = await session.execute(query)
            instance = result.scalar_one_or_none()
            
            if instance:
                return instance, False
            
            # 创建新记录
            instance = model(**kwargs)
            session.add(instance)
            await session.flush()
            return instance, True
            
        except Exception as e:
            logger.error(f"获取或创建记录失败: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def bulk_insert(session: AsyncSession, model, data_list):
        """
        批量插入数据
        """
        try:
            instances = [model(**data) for data in data_list]
            session.add_all(instances)
            await session.flush()
            logger.info(f"批量插入 {len(instances)} 条记录到 {model.__tablename__}")
            return instances
        except Exception as e:
            logger.error(f"批量插入失败: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def execute_raw_sql(session: AsyncSession, sql: str, params: dict = None):
        """
        执行原始SQL
        """
        try:
            result = await session.execute(sql, params or {})
            return result
        except Exception as e:
            logger.error(f"执行SQL失败: {e}")
            raise

# 数据库健康检查
async def check_database_health() -> dict:
    """
    检查数据库健康状况
    返回: {
        "status": "healthy" | "unhealthy",
        "details": {...}
    }
    """
    try:
        # 测试连接
        connection_ok = await test_connection()
        
        if not connection_ok:
            return {
                "status": "unhealthy",
                "details": {"error": "数据库连接失败"}
            }
        
        # 检查表数量
        from models import Base
        table_count = len(Base.metadata.tables)
        
        return {
            "status": "healthy",
            "details": {
                "connection": "ok",
                "tables": table_count,
                "url": settings.DATABASE_URL.split("@")[-1] if "@" in settings.DATABASE_URL else "local"
            }
        }
        
    except Exception as e:
        logger.error(f"数据库健康检查失败: {e}")
        return {
            "status": "unhealthy",
            "details": {"error": str(e)}
        }

# 数据库统计信息
async def get_database_stats(session: AsyncSession) -> dict:
    """
    获取数据库统计信息
    """
    try:
        stats = {}
        
        # 获取各表记录数
        from models import User, Paper, Notification, Team
        
        tables = [
            ("users", User),
            ("papers", Paper),
            ("notifications", Notification),
            ("teams", Team),
            ("user_papers", None),  # 需要单独处理
        ]
        
        for table_name, model in tables:
            if model:
                query = session.query(model)
                result = await session.execute(query)
                count = len(result.scalars().all())
                stats[table_name] = count
            else:
                # 对于没有直接模型的表
                sql = f"SELECT COUNT(*) FROM {table_name}"
                result = await session.execute(sql)
                count = result.scalar()
                stats[table_name] = count
        
        return stats
        
    except Exception as e:
        logger.error(f"获取数据库统计信息失败: {e}")
        return {"error": str(e)}

# 初始化数据库（开发环境使用）
async def init_database():
    """初始化数据库"""
    logger.info("开始初始化数据库...")
    
    # 测试连接
    if not await test_connection():
        logger.error("数据库连接失败，无法初始化")
        return False
    
    # 创建表
    if not await create_tables():
        logger.error("创建表失败")
        return False
    
    logger.info("数据库初始化完成")
    return True

if __name__ == "__main__":
    import asyncio
    
    async def main():
        """测试数据库连接"""
        print("=== 测试数据库连接 ===")
        
        # 测试连接
        success = await test_connection()
        if success:
            print("✅ 数据库连接成功")
            
            # 检查健康状况
            health = await check_database_health()
            print(f"健康状态: {health['status']}")
            print(f"详细信息: {health['details']}")
        else:
            print("❌ 数据库连接失败")
        
        print("=====================")
    
    asyncio.run(main())