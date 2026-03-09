"""
认证服务模块
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from config import settings
from database import get_db
from models import User

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2方案
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """获取密码哈希值"""
    return pwd_context.hash(password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET_KEY, 
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt

def create_refresh_token(data: Dict[str, Any]) -> str:
    """创建刷新令牌"""
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET_KEY, 
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt

def verify_token(token: str, is_refresh: bool = False) -> Dict[str, Any]:
    """验证令牌"""
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # 检查令牌类型
        token_type = payload.get("type")
        if is_refresh and token_type != "refresh":
            raise JWTError("不是刷新令牌")
        elif not is_refresh and token_type != "access" and token_type != "password_reset":
            raise JWTError("不是访问令牌")
        
        return payload
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"令牌验证失败: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(token)
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    # 从数据库获取用户
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户账户已被禁用"
        )
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """获取当前活跃用户"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="用户未激活")
    return current_user

async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """获取当前管理员用户"""
    # 这里可以根据需要添加管理员检查逻辑
    # 例如：检查用户角色或权限
    return current_user

def create_password_reset_token(user_id: str) -> str:
    """创建密码重置令牌"""
    data = {
        "sub": user_id,
        "type": "password_reset",
        "iat": datetime.utcnow()
    }
    
    return create_access_token(data, expires_delta=timedelta(hours=1))

def verify_password_reset_token(token: str) -> Optional[str]:
    """验证密码重置令牌"""
    try:
        payload = verify_token(token)
        
        if payload.get("type") != "password_reset":
            return None
        
        user_id = payload.get("sub")
        return user_id
        
    except JWTError:
        return None

def create_email_verification_token(user_id: str) -> str:
    """创建邮箱验证令牌"""
    data = {
        "sub": user_id,
        "type": "email_verification",
        "iat": datetime.utcnow()
    }
    
    return create_access_token(data, expires_delta=timedelta(days=7))

def verify_email_verification_token(token: str) -> Optional[str]:
    """验证邮箱验证令牌"""
    try:
        payload = verify_token(token)
        
        if payload.get("type") != "email_verification":
            return None
        
        user_id = payload.get("sub")
        return user_id
        
    except JWTError:
        return None

# 权限检查函数
async def check_user_permission(
    user: User,
    required_permission: str,
    resource_id: Optional[str] = None
) -> bool:
    """
    检查用户权限
    
    参数:
    - user: 用户对象
    - required_permission: 需要的权限
    - resource_id: 资源ID（可选）
    
    返回: 是否有权限
    """
    # 这里可以实现具体的权限检查逻辑
    # 例如：基于角色、基于资源所有权等
    
    # 简单实现：所有活跃用户都有基本权限
    if not user.is_active:
        return False
    
    # 可以根据需要添加更复杂的权限检查
    return True

# 用户操作审计
async def log_user_action(
    db: AsyncSession,
    user_id: str,
    action: str,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    details: Optional[Dict] = None
):
    """
    记录用户操作日志
    
    在实际应用中，可以记录到专门的审计日志表
    """
    # TODO: 实现用户操作日志记录
    pass

# 安全相关工具函数
def sanitize_user_input(input_str: str) -> str:
    """清理用户输入，防止XSS等攻击"""
    import html
    
    # HTML转义
    sanitized = html.escape(input_str)
    
    # 移除危险字符
    dangerous_chars = ['<', '>', '"', "'", '&', ';']
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()

def validate_session_token(token: str) -> bool:
    """验证会话令牌（用于额外的安全检查）"""
    try:
        payload = verify_token(token)
        
        # 检查令牌是否在黑名单中（需要实现令牌黑名单功能）
        # TODO: 检查令牌黑名单
        
        return True
        
    except JWTError:
        return False

# 速率限制相关（可以在中间件中实现）
class RateLimiter:
    """简单的速率限制器"""
    
    def __init__(self):
        self.requests = {}
    
    def is_allowed(self, user_id: str, limit: int = 100, window: int = 60) -> bool:
        """
        检查是否允许请求
        
        参数:
        - user_id: 用户ID
        - limit: 时间窗口内允许的请求数
        - window: 时间窗口（秒）
        """
        import time
        
        current_time = time.time()
        window_start = current_time - window
        
        # 清理过期的请求记录
        if user_id in self.requests:
            self.requests[user_id] = [
                req_time for req_time in self.requests[user_id]
                if req_time > window_start
            ]
        else:
            self.requests[user_id] = []
        
        # 检查请求数
        if len(self.requests[user_id]) >= limit:
            return False
        
        # 记录本次请求
        self.requests[user_id].append(current_time)
        return True

# 创建全局速率限制器实例
rate_limiter = RateLimiter()