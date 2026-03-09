"""
数据库模型定义
"""

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, 
    ForeignKey, JSON, UUID, Float, Index
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID as PGUUID
import uuid
from datetime import datetime

Base = declarative_base()

def generate_uuid():
    """生成UUID"""
    return str(uuid.uuid4())

class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # 用户信息
    full_name = Column(String(200), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    
    # 兴趣和偏好
    interests = Column(JSON, default=list)  # 兴趣标签列表
    categories = Column(JSON, default=list)  # 关注的arXiv分类
    notification_preferences = Column(JSON, default=dict)  # 通知偏好
    
    # 设备信息
    device_tokens = Column(JSON, default=list)  # 推送设备令牌
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)
    
    # 状态
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # 关系
    papers = relationship("UserPaper", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    teams = relationship("TeamMember", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"

class Paper(Base):
    """论文模型"""
    __tablename__ = "papers"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    arxiv_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # 论文信息
    title = Column(Text, nullable=False)
    authors = Column(JSON, nullable=False)  # 作者列表
    abstract = Column(Text, nullable=False)
    categories = Column(JSON, nullable=False)  # arXiv分类列表
    
    # 元数据
    published_date = Column(DateTime, nullable=False, index=True)
    updated_date = Column(DateTime, nullable=True)
    pdf_url = Column(String(500), nullable=True)
    source_url = Column(String(500), nullable=True)  # arXiv页面URL
    
    # 统计信息
    citation_count = Column(Integer, default=0)
    download_count = Column(Integer, default=0)
    
    # 来源
    source = Column(String(50), default="arxiv")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user_papers = relationship("UserPaper", back_populates="paper", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="paper", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Paper(id={self.id}, arxiv_id={self.arxiv_id}, title={self.title[:50]}...)>"

class UserPaper(Base):
    """用户-论文关系模型"""
    __tablename__ = "user_papers"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    paper_id = Column(PGUUID(as_uuid=True), ForeignKey("papers.id", ondelete="CASCADE"), nullable=False)
    
    # 状态
    status = Column(String(20), default="unread")  # unread, reading, read, saved
    is_recommended = Column(Boolean, default=False)  # 是否推荐
    
    # 用户操作
    read_at = Column(DateTime, nullable=True)
    saved_at = Column(DateTime, nullable=True)
    rating = Column(Integer, nullable=True)  # 评分 1-5
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="papers")
    paper = relationship("Paper", back_populates="user_papers")
    
    # 复合唯一索引
    __table_args__ = (
        Index('idx_user_paper_unique', 'user_id', 'paper_id', unique=True),
        Index('idx_user_status', 'user_id', 'status'),
        Index('idx_paper_status', 'paper_id', 'status'),
    )
    
    def __repr__(self):
        return f"<UserPaper(user_id={self.user_id}, paper_id={self.paper_id}, status={self.status})>"

class Notification(Base):
    """通知模型"""
    __tablename__ = "notifications"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    paper_id = Column(PGUUID(as_uuid=True), ForeignKey("papers.id", ondelete="CASCADE"), nullable=True)
    
    # 通知内容
    type = Column(String(50), nullable=False)  # new_paper, daily_summary, team_share, system
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    data = Column(JSON, default=dict)  # 附加数据
    
    # 状态
    is_read = Column(Boolean, default=False)
    is_sent = Column(Boolean, default=False)
    
    # 时间戳
    sent_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="notifications")
    paper = relationship("Paper", back_populates="notifications")
    
    # 索引
    __table_args__ = (
        Index('idx_notification_user', 'user_id', 'created_at'),
        Index('idx_notification_type', 'type', 'created_at'),
        Index('idx_notification_read', 'is_read', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type={self.type})>"

class Team(Base):
    """团队模型"""
    __tablename__ = "teams"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # 创建者
    created_by = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # 设置
    is_public = Column(Boolean, default=False)
    join_code = Column(String(50), unique=True, nullable=True)  # 加入代码
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
    papers = relationship("TeamPaper", back_populates="team", cascade="all, delete-orphan")
    creator = relationship("User", foreign_keys=[created_by])
    
    def __repr__(self):
        return f"<Team(id={self.id}, name={self.name})>"

class TeamMember(Base):
    """团队成员模型"""
    __tablename__ = "team_members"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_id = Column(PGUUID(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # 角色
    role = Column(String(20), default="member")  # owner, admin, member
    
    # 时间戳
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="teams")
    
    # 复合唯一索引
    __table_args__ = (
        Index('idx_team_member_unique', 'team_id', 'user_id', unique=True),
    )
    
    def __repr__(self):
        return f"<TeamMember(team_id={self.team_id}, user_id={self.user_id}, role={self.role})>"

class TeamPaper(Base):
    """团队论文模型"""
    __tablename__ = "team_papers"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_id = Column(PGUUID(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    paper_id = Column(PGUUID(as_uuid=True), ForeignKey("papers.id", ondelete="CASCADE"), nullable=False)
    added_by = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # 备注
    note = Column(Text, nullable=True)
    
    # 时间戳
    added_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    team = relationship("Team", back_populates="papers")
    paper = relationship("Paper")
    adder = relationship("User", foreign_keys=[added_by])
    
    # 复合唯一索引
    __table_args__ = (
        Index('idx_team_paper_unique', 'team_id', 'paper_id', unique=True),
    )
    
    def __repr__(self):
        return f"<TeamPaper(team_id={self.team_id}, paper_id={self.paper_id})>"

class CrawlLog(Base):
    """爬虫日志模型"""
    __tablename__ = "crawl_logs"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # 爬取信息
    task_type = Column(String(50), nullable=False)  # latest, user, category
    categories = Column(JSON, nullable=True)
    
    # 结果
    papers_found = Column(Integer, default=0)
    papers_added = Column(Integer, default=0)
    users_notified = Column(Integer, default=0)
    
    # 状态
    status = Column(String(20), default="pending")  # pending, running, completed, failed
    error_message = Column(Text, nullable=True)
    
    # 时间戳
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<CrawlLog(id={self.id}, task_type={self.task_type}, status={self.status})>"