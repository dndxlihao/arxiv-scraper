"""
认证相关的数据模型（Pydantic Schema）
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
import uuid

class UserBase(BaseModel):
    """用户基础模型"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, regex=r'^[a-zA-Z0-9_]+$')
    full_name: Optional[str] = Field(None, max_length=100)

class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(..., min_length=8)
    interests: Optional[List[str]] = Field(default_factory=list)
    categories: Optional[List[str]] = Field(default_factory=list)
    
    @validator('password')
    def validate_password_strength(cls, v):
        """验证密码强度"""
        if len(v) < 8:
            raise ValueError('密码必须至少8位')
        if not any(c.isalpha() for c in v):
            raise ValueError('密码必须包含字母')
        if not any(c.isdigit() for c in v):
            raise ValueError('密码必须包含数字')
        return v
    
    @validator('username')
    def validate_username(cls, v):
        """验证用户名"""
        if v.lower() in ['admin', 'root', 'system', 'test']:
            raise ValueError('该用户名不可用')
        return v

class UserUpdate(BaseModel):
    """用户更新模型"""
    full_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = Field(None, max_length=500)
    interests: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    notification_preferences: Optional[dict] = None
    
    class Config:
        extra = "forbid"  # 禁止额外字段

class UserResponse(UserBase):
    """用户响应模型"""
    id: uuid.UUID
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    interests: List[str] = Field(default_factory=list)
    categories: List[str] = Field(default_factory=list)
    notification_preferences: dict = Field(default_factory=dict)
    is_verified: bool = False
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # 允许从ORM对象转换

class Token(BaseModel):
    """令牌响应模型"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # 过期时间（秒）

class TokenData(BaseModel):
    """令牌数据模型"""
    sub: Optional[str] = None  # 用户ID
    type: Optional[str] = None  # 令牌类型
    exp: Optional[int] = None  # 过期时间

class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str  # 支持用户名或邮箱
    password: str

class PasswordResetRequest(BaseModel):
    """密码重置请求模型"""
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    """密码重置确认模型"""
    token: str
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def validate_password_strength(cls, v):
        """验证密码强度"""
        if len(v) < 8:
            raise ValueError('密码必须至少8位')
        if not any(c.isalpha() for c in v):
            raise ValueError('密码必须包含字母')
        if not any(c.isdigit() for c in v):
            raise ValueError('密码必须包含数字')
        return v

class DeviceTokenRegister(BaseModel):
    """设备令牌注册模型"""
    device_token: str
    platform: str = Field(..., regex='^(ios|android)$')

class NotificationPreferences(BaseModel):
    """通知偏好设置模型"""
    new_paper: bool = True  # 新论文通知
    daily_summary: bool = True  # 每日摘要
    team_updates: bool = True  # 团队更新
    system_notices: bool = True  # 系统通知
    
    # 推送时间偏好
    quiet_start: Optional[int] = Field(None, ge=0, le=23)  # 安静时段开始
    quiet_end: Optional[int] = Field(None, ge=0, le=23)  # 安静时段结束
    
    class Config:
        json_schema_extra = {
            "example": {
                "new_paper": True,
                "daily_summary": True,
                "team_updates": True,
                "system_notices": False,
                "quiet_start": 22,
                "quiet_end": 8
            }
        }

class UserPreferencesUpdate(BaseModel):
    """用户偏好更新模型"""
    notification_preferences: Optional[NotificationPreferences] = None
    interests: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "notification_preferences": {
                    "new_paper": True,
                    "daily_summary": True,
                    "team_updates": False
                },
                "interests": ["machine learning", "computer vision"],
                "categories": ["cs.CV", "cs.LG"]
            }
        }

# 响应模型别名，用于API文档
UserDetail = UserResponse
UserList = List[UserResponse]

# 错误响应模型
class ErrorResponse(BaseModel):
    """错误响应模型"""
    detail: str
    error_code: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "用户不存在",
                "error_code": "USER_NOT_FOUND"
            }
        }

class ValidationError(BaseModel):
    """验证错误模型"""
    loc: List[str]
    msg: str
    type: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "loc": ["body", "password"],
                "msg": "密码必须至少8位",
                "type": "value_error"
            }
        }

class HTTPValidationError(BaseModel):
    """HTTP验证错误模型"""
    detail: List[ValidationError]