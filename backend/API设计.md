# arXiv论文助手 - 后端API设计

## 概述
为iOS APP提供完整的后端API服务，包括用户管理、论文爬取、推送通知等功能。

## 技术栈
- **框架**: FastAPI
- **数据库**: PostgreSQL
- **异步**: asyncio, aiohttp
- **认证**: JWT
- **部署**: Docker, Nginx

## API端点设计

### 认证相关
```
POST   /api/v1/auth/register      # 用户注册
POST   /api/v1/auth/login         # 用户登录
POST   /api/v1/auth/refresh       # 刷新令牌
GET    /api/v1/auth/me            # 获取当前用户信息
PUT    /api/v1/auth/me            # 更新用户信息
```

### 论文相关
```
GET    /api/v1/papers             # 获取论文列表
GET    /api/v1/papers/{id}        # 获取论文详情
POST   /api/v1/papers/search      # 搜索论文
GET    /api/v1/papers/recommended # 获取推荐论文
POST   /api/v1/papers/{id}/read   # 标记已读
POST   /api/v1/papers/{id}/save   # 收藏论文
GET    /api/v1/papers/saved       # 获取收藏论文
```

### 推送相关
```
GET    /api/v1/notifications      # 获取通知列表
POST   /api/v1/notifications/read # 标记通知已读
GET    /api/v1/notifications/unread # 未读通知数量
```

### 团队相关
```
GET    /api/v1/teams              # 获取团队列表
POST   /api/v1/teams              # 创建团队
GET    /api/v1/teams/{id}         # 获取团队详情
POST   /api/v1/teams/{id}/join    # 加入团队
POST   /api/v1/teams/{id}/invite  # 邀请成员
GET    /api/v1/teams/{id}/papers  # 团队论文
```

### 爬虫相关（内部）
```
POST   /internal/crawl/latest     # 爬取最新论文
POST   /internal/crawl/user/{id}  # 为用户爬取论文
GET    /internal/crawl/status     # 爬虫状态
```

## 数据模型

### 用户 (User)
```python
class User(BaseModel):
    id: UUID
    email: str
    username: str
    interests: List[str]  # 兴趣标签
    notification_preferences: Dict
    created_at: datetime
    updated_at: datetime
    device_tokens: List[str]  # 推送设备令牌
```

### 论文 (Paper)
```python
class Paper(BaseModel):
    id: UUID
    arxiv_id: str  # arXiv ID，如 "2106.09685"
    title: str
    authors: List[str]
    abstract: str
    categories: List[str]  # arXiv分类，如 ["cs.CV", "cs.LG"]
    published_date: datetime
    pdf_url: str
    source: str = "arxiv"
    created_at: datetime
    updated_at: datetime
```

### 用户论文关系 (UserPaper)
```python
class UserPaper(BaseModel):
    id: UUID
    user_id: UUID
    paper_id: UUID
    status: str  # "unread", "read", "saved"
    read_at: Optional[datetime]
    saved_at: Optional[datetime]
    created_at: datetime
```

### 通知 (Notification)
```python
class Notification(BaseModel):
    id: UUID
    user_id: UUID
    paper_id: UUID
    type: str  # "new_paper", "daily_summary", "team_share"
    title: str
    message: str
    sent_at: datetime
    read_at: Optional[datetime]
    data: Dict  # 附加数据
```

### 团队 (Team)
```python
class Team(BaseModel):
    id: UUID
    name: str
    description: str
    created_by: UUID
    created_at: datetime
    updated_at: datetime
```

### 团队成员 (TeamMember)
```python
class TeamMember(BaseModel):
    id: UUID
    team_id: UUID
    user_id: UUID
    role: str  # "owner", "admin", "member"
    joined_at: datetime
```

## 爬虫设计

### 定时任务
```python
# 每天执行的任务
1. 00:00 - 爬取arXiv最新论文
2. 01:00 - 为用户匹配论文
3. 02:00 - 发送推送通知
4. 08:00 - 发送每日摘要
```

### 爬取策略
```python
class ArxivCrawler:
    async def crawl_latest(self, categories=None, max_results=100):
        """爬取最新论文"""
        # 使用arXiv API
        # 过滤重复论文
        # 存储到数据库
        
    async def match_papers_for_user(self, user_id: UUID):
        """为用户匹配论文"""
        # 获取用户兴趣
        # 查询相关论文
        # 创建用户论文关系
        # 生成推送通知
```

### 推送服务
```python
class NotificationService:
    async def send_push_notification(self, user_id: UUID, notification: Notification):
        """发送推送通知"""
        # 获取用户设备令牌
        # 调用APNs/FCM
        # 记录发送状态
        
    async def send_daily_summary(self, user_id: UUID):
        """发送每日摘要"""
        # 获取用户今日论文
        # 生成摘要消息
        # 发送推送
```

## 数据库设计

### SQL Schema
```sql
-- 用户表
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    interests JSONB DEFAULT '[]',
    notification_preferences JSONB DEFAULT '{}',
    device_tokens JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 论文表
CREATE TABLE papers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    arxiv_id VARCHAR(50) UNIQUE NOT NULL,
    title TEXT NOT NULL,
    authors JSONB NOT NULL,
    abstract TEXT NOT NULL,
    categories JSONB NOT NULL,
    published_date TIMESTAMP NOT NULL,
    pdf_url VARCHAR(500),
    source VARCHAR(50) DEFAULT 'arxiv',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 用户论文关系表
CREATE TABLE user_papers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    paper_id UUID REFERENCES papers(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'unread',
    read_at TIMESTAMP,
    saved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, paper_id)
);

-- 索引
CREATE INDEX idx_user_papers_user ON user_papers(user_id);
CREATE INDEX idx_user_papers_paper ON user_papers(paper_id);
CREATE INDEX idx_papers_arxiv_id ON papers(arxiv_id);
CREATE INDEX idx_papers_published ON papers(published_date DESC);
```

## 认证和授权

### JWT认证
```python
# 生成令牌
def create_access_token(data: dict, expires_delta: timedelta = None):
    # 实现JWT令牌生成
    
# 验证令牌
def verify_token(token: str) -> Optional[dict]:
    # 验证JWT令牌
```

### 权限控制
```python
# 依赖注入
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # 获取当前用户
    
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    # 获取活跃用户
```

## 错误处理

### 自定义异常
```python
class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)

class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401)
```

### 全局异常处理器
```python
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )
```

## 性能优化

### 缓存策略
```python
# Redis缓存
CACHE_KEYS = {
    "user_papers": "user:papers:{user_id}",
    "paper_detail": "paper:{paper_id}",
    "recommendations": "rec:{user_id}"
}

# 缓存时间
CACHE_TTL = {
    "user_papers": 300,  # 5分钟
    "paper_detail": 3600,  # 1小时
    "recommendations": 1800  # 30分钟
}
```

### 数据库优化
1. 使用连接池
2. 添加合适索引
3. 分页查询
4. 批量操作

## 监控和日志

### 日志配置
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
```

### 监控指标
1. API响应时间
2. 错误率
3. 用户活跃度
4. 推送送达率

## 部署配置

### Docker配置
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 环境变量
```bash
# .env文件
DATABASE_URL=postgresql://user:password@localhost/arxiv_db
REDIS_URL=redis://localhost:6379
JWT_SECRET_KEY=your-secret-key
ARXIV_API_URL=https://export.arxiv.org/api/query
```

## 下一步开发

1. 创建FastAPI项目结构
2. 实现数据库模型
3. 创建API端点
4. 实现爬虫服务
5. 集成推送通知
6. 添加测试
7. 部署到服务器

---

**API版本**: v1.0.0
**设计时间**: 2026-03-09