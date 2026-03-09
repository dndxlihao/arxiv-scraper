"""
用户认证相关API路由
"""

from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from typing import Optional

from database import get_db
from models import User
from schemas.auth import (
    UserCreate, UserResponse, UserUpdate, 
    Token, TokenData, LoginRequest
)
from services.auth import (
    verify_password, get_password_hash,
    create_access_token, create_refresh_token,
    verify_token, get_current_user
)
from utils.validators import validate_email, validate_password

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    用户注册
    
    参数:
    - email: 邮箱地址
    - username: 用户名
    - password: 密码
    - full_name: 全名（可选）
    """
    # 验证邮箱格式
    if not validate_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱格式不正确"
        )
    
    # 验证密码强度
    if not validate_password(user_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="密码必须至少8位，包含字母和数字"
        )
    
    # 检查邮箱是否已存在
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册"
        )
    
    # 检查用户名是否已存在
    result = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    existing_username = result.scalar_one_or_none()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户名已被使用"
        )
    
    # 创建新用户
    hashed_password = get_password_hash(user_data.password)
    
    user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hashed_password,
        full_name=user_data.full_name,
        interests=user_data.interests or [],
        categories=user_data.categories or [],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        interests=user.interests,
        categories=user.categories,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    用户登录
    
    参数:
    - username: 用户名或邮箱
    - password: 密码
    """
    # 查找用户（支持用户名或邮箱登录）
    result = await db.execute(
        select(User).where(
            (User.username == form_data.username) | 
            (User.email == form_data.username)
        )
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户账户已被禁用"
        )
    
    # 更新最后登录时间
    user.last_login_at = datetime.utcnow()
    await db.commit()
    
    # 创建访问令牌和刷新令牌
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=3600  # 1小时
    )

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    """
    刷新访问令牌
    
    参数:
    - refresh_token: 刷新令牌
    """
    try:
        payload = verify_token(refresh_token, is_refresh=True)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的刷新令牌"
            )
        
        # 验证用户是否存在且活跃
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在或已被禁用"
            )
        
        # 创建新的访问令牌
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,  # 刷新令牌不变
            token_type="bearer",
            expires_in=3600
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"令牌刷新失败: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户信息
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        interests=current_user.interests,
        categories=current_user.categories,
        avatar_url=current_user.avatar_url,
        bio=current_user.bio,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        last_login_at=current_user.last_login_at
    )

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新当前用户信息
    
    参数:
    - full_name: 全名（可选）
    - bio: 个人简介（可选）
    - interests: 兴趣标签（可选）
    - categories: 关注分类（可选）
    - notification_preferences: 通知偏好（可选）
    """
    # 更新用户信息
    update_data = user_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if hasattr(current_user, field):
            setattr(current_user, field, value)
    
    current_user.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(current_user)
    
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        interests=current_user.interests,
        categories=current_user.categories,
        avatar_url=current_user.avatar_url,
        bio=current_user.bio,
        notification_preferences=current_user.notification_preferences,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        last_login_at=current_user.last_login_at
    )

@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    用户登出
    
    注意：由于JWT是无状态的，客户端需要自行删除令牌。
    此端点主要用于记录登出事件。
    """
    # 这里可以记录登出日志或清除设备令牌
    # 在实际应用中，可能需要实现令牌黑名单
    
    return {"message": "登出成功"}

@router.post("/change-password")
async def change_password(
    current_password: str = Body(...),
    new_password: str = Body(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    修改密码
    
    参数:
    - current_password: 当前密码
    - new_password: 新密码
    """
    # 验证当前密码
    if not verify_password(current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前密码不正确"
        )
    
    # 验证新密码强度
    if not validate_password(new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="新密码必须至少8位，包含字母和数字"
        )
    
    # 更新密码
    current_user.password_hash = get_password_hash(new_password)
    current_user.updated_at = datetime.utcnow()
    
    await db.commit()
    
    return {"message": "密码修改成功"}

@router.post("/forgot-password")
async def forgot_password(
    email: str = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """
    忘记密码 - 发送重置邮件
    
    参数:
    - email: 注册邮箱
    """
    # 查找用户
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        # 出于安全考虑，不提示用户是否存在
        return {"message": "如果邮箱存在，重置链接已发送"}
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户账户已被禁用"
        )
    
    # 生成重置令牌（有效期1小时）
    reset_token = create_access_token(
        data={"sub": str(user.id), "type": "password_reset"},
        expires_delta=timedelta(hours=1)
    )
    
    # TODO: 发送重置邮件
    # 在实际应用中，这里应该发送包含重置链接的邮件
    
    return {
        "message": "重置链接已发送到邮箱",
        "reset_token": reset_token  # 开发环境返回，生产环境不返回
    }

@router.post("/reset-password")
async def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """
    重置密码
    
    参数:
    - token: 重置令牌
    - new_password: 新密码
    """
    try:
        # 验证重置令牌
        payload = verify_token(token)
        
        if payload.get("type") != "password_reset":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的重置令牌"
            )
        
        user_id = payload.get("sub")
        
        # 查找用户
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户不存在或已被禁用"
            )
        
        # 验证新密码强度
        if not validate_password(new_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="新密码必须至少8位，包含字母和数字"
            )
        
        # 更新密码
        user.password_hash = get_password_hash(new_password)
        user.updated_at = datetime.utcnow()
        
        await db.commit()
        
        return {"message": "密码重置成功"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"密码重置失败: {str(e)}"
        )

@router.post("/device-token")
async def register_device_token(
    device_token: str = Body(...),
    platform: str = Body(..., description="设备平台: ios, android"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    注册设备推送令牌
    
    参数:
    - device_token: 设备推送令牌
    - platform: 设备平台
    """
    if platform not in ["ios", "android"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="平台必须是 'ios' 或 'android'"
        )
    
    # 添加设备令牌到用户记录
    device_info = {
        "token": device_token,
        "platform": platform,
        "registered_at": datetime.utcnow().isoformat()
    }
    
    if not current_user.device_tokens:
        current_user.device_tokens = []
    
    # 检查是否已存在
    existing = False
    for device in current_user.device_tokens:
        if device.get("token") == device_token:
            existing = True
            break
    
    if not existing:
        current_user.device_tokens.append(device_info)
        current_user.updated_at = datetime.utcnow()
        await db.commit()
    
    return {"message": "设备令牌注册成功"}