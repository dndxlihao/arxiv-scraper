#!/usr/bin/env python3
"""
arXiv推荐APP - 后端API服务
基于FastAPI + SQLite
"""

import aiosqlite
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import datetime

# 数据库文件路径
DATABASE = "arxiv_app.db"

# 创建FastAPI应用
app = FastAPI(title="arXiv推荐API", version="1.0.0")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class UserRegister(BaseModel):
    username: str
    email: str
    interests: List[str] = []

class PaperSearch(BaseModel):
    query: str
    limit: int = 10

class TeamCreate(BaseModel):
    name: str
    description: str = ""
    creator: str

class ReadingTask(BaseModel):
    user_id: int
    paper_id: str
    status: str = "pending"
    deadline: Optional[str] = None
    notes: str = ""

# 初始化数据库
async def init_db():
    async with aiosqlite.connect(DATABASE) as db:
        # 创建用户表
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                interests TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建论文表
        await db.execute('''
            CREATE TABLE IF NOT EXISTS papers (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                authors TEXT,
                abstract TEXT,
                categories TEXT,
                published TEXT,
                updated TEXT,
                pdf_url TEXT,
                arxiv_url TEXT
            )
        ''')
        
        # 创建收藏表
        await db.execute('''
            CREATE TABLE IF NOT EXISTS collections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                paper_id TEXT NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (paper_id) REFERENCES papers (id)
            )
        ''')
        
        # 创建团队表
        await db.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                creator_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (creator_id) REFERENCES users (id)
            )
        ''')
        
        # 创建团队成员表
        await db.execute('''
            CREATE TABLE IF NOT EXISTS team_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                role TEXT DEFAULT 'member',
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id) REFERENCES teams (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # 创建团队推荐表
        await db.execute('''
            CREATE TABLE IF NOT EXISTS team_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                recommender_id INTEGER,
                paper_id TEXT NOT NULL,
                note TEXT,
                recommended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id) REFERENCES teams (id),
                FOREIGN KEY (recommender_id) REFERENCES users (id),
                FOREIGN KEY (paper_id) REFERENCES papers (id)
            )
        ''')
        
        # 创建阅读任务表
        await db.execute('''
            CREATE TABLE IF NOT EXISTS reading_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                paper_id TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                deadline TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (paper_id) REFERENCES papers (id)
            )
        ''')
        
        await db.commit()

# 启动时初始化数据库
@app.on_event("startup")
async def startup_event():
    await init_db()
    print("✅ 数据库初始化完成")

# 根路径
@app.get("/")
async def root():
    return {"message": "arXiv推荐API服务运行中", "version": "1.0.0"}

# 用户注册
@app.post("/users/register")
async def register_user(user: UserRegister):
    """用户注册"""
    async with aiosqlite.connect(DATABASE) as db:
        try:
            interests_str = ",".join(user.interests) if user.interests else ""
            await db.execute(
                "INSERT INTO users (username, email, interests) VALUES (?, ?, ?)",
                (user.username, user.email, interests_str)
            )
            await db.commit()
            
            # 获取新用户ID
            cursor = await db.execute("SELECT last_insert_rowid()")
            user_id = (await cursor.fetchone())[0]
            
            return {"user_id": user_id, "message": "用户注册成功"}
        except aiosqlite.IntegrityError:
            raise HTTPException(status_code=400, detail="用户名或邮箱已存在")

# 获取用户个性化推荐
@app.get("/users/{username}/recommendations")
async def get_user_recommendations(username: str, limit: int = 10):
    """获取用户个性化推荐"""
    async with aiosqlite.connect(DATABASE) as db:
        # 获取用户兴趣
        cursor = await db.execute(
            "SELECT interests FROM users WHERE username = ?",
            (username,)
        )
        row = await cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        interests = row[0] or ""
        
        # 简单推荐逻辑：根据兴趣关键词匹配论文标题
        if interests:
            interest_list = interests.split(",")
            query_conditions = " OR ".join([f"title LIKE '%{interest}%'" for interest in interest_list])
            query = f"SELECT * FROM papers WHERE {query_conditions} LIMIT ?"
            cursor = await db.execute(query, (limit,))
        else:
            # 如果没有兴趣，返回最新论文
            cursor = await db.execute(
                "SELECT * FROM papers ORDER BY published DESC LIMIT ?",
                (limit,)
            )
        
        papers = await cursor.fetchall()
        
        # 转换为字典列表
        result = []
        for paper in papers:
            result.append({
                "id": paper[0],
                "title": paper[1],
                "authors": paper[2],
                "abstract": paper[3][:200] + "..." if paper[3] and len(paper[3]) > 200 else paper[3],
                "categories": paper[4],
                "published": paper[5],
                "pdf_url": paper[7],
                "arxiv_url": paper[8]
            })
        
        return {"username": username, "recommendations": result}

# 搜索论文
@app.get("/papers/search")
async def search_papers(query: str, limit: int = 10):
    """搜索论文"""
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute(
            "SELECT * FROM papers WHERE title LIKE ? OR abstract LIKE ? LIMIT ?",
            (f"%{query}%", f"%{query}%", limit)
        )
        papers = await cursor.fetchall()
        
        result = []
        for paper in papers:
            result.append({
                "id": paper[0],
                "title": paper[1],
                "authors": paper[2],
                "abstract": paper[3][:150] + "..." if paper[3] and len(paper[3]) > 150 else paper[3],
                "categories": paper[4],
                "published": paper[5],
                "pdf_url": paper[7]
            })
        
        return {"query": query, "results": result}

# 获取论文详情
@app.get("/papers/{paper_id}")
async def get_paper_details(paper_id: str):
    """获取论文详情"""
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute(
            "SELECT * FROM papers WHERE id = ?",
            (paper_id,)
        )
        paper = await cursor.fetchone()
        
        if not paper:
            raise HTTPException(status_code=404, detail="论文不存在")
        
        return {
            "id": paper[0],
            "title": paper[1],
            "authors": paper[2],
            "abstract": paper[3],
            "categories": paper[4],
            "published": paper[5],
            "updated": paper[6],
            "pdf_url": paper[7],
            "arxiv_url": paper[8]
        }

# 收藏论文
@app.post("/users/{username}/collect/{paper_id}")
async def collect_paper(username: str, paper_id: str):
    """收藏论文"""
    async with aiosqlite.connect(DATABASE) as db:
        # 获取用户ID
        cursor = await db.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        )
        user_row = await cursor.fetchone()
        
        if not user_row:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        user_id = user_row[0]
        
        # 检查论文是否存在
        cursor = await db.execute(
            "SELECT id FROM papers WHERE id = ?",
            (paper_id,)
        )
        paper_row = await cursor.fetchone()
        
        if not paper_row:
            raise HTTPException(status_code=404, detail="论文不存在")
        
        # 检查是否已收藏
        cursor = await db.execute(
            "SELECT id FROM collections WHERE user_id = ? AND paper_id = ?",
            (user_id, paper_id)
        )
        existing = await cursor.fetchone()
        
        if existing:
            raise HTTPException(status_code=400, detail="论文已收藏")
        
        # 添加收藏
        await db.execute(
            "INSERT INTO collections (user_id, paper_id) VALUES (?, ?)",
            (user_id, paper_id)
        )
        await db.commit()
        
        return {"message": "收藏成功"}

# 获取收藏列表
@app.get("/users/{username}/collections")
async def get_collections(username: str):
    """获取用户收藏列表"""
    async with aiosqlite.connect(DATABASE) as db:
        # 获取用户ID
        cursor = await db.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        )
        user_row = await cursor.fetchone()
        
        if not user_row:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        user_id = user_row[0]
        
        # 获取收藏的论文
        cursor = await db.execute('''
            SELECT p.*, c.added_at 
            FROM papers p
            JOIN collections c ON p.id = c.paper_id
            WHERE c.user_id = ?
            ORDER BY c.added_at DESC
        ''', (user_id,))
        
        papers = await cursor.fetchall()
        
        result = []
        for paper in papers:
            result.append({
                "id": paper[0],
                "title": paper[1],
                "authors": paper[2],
                "abstract": paper[3][:150] + "..." if paper[3] and len(paper[3]) > 150 else paper[3],
                "categories": paper[4],
                "published": paper[5],
                "pdf_url": paper[7],
                "added_at": paper[9]
            })
        
        return {"username": username, "collections": result}

# 创建团队
@app.post("/teams/create")
async def create_team(team: TeamCreate):
    """创建团队"""
    async with aiosqlite.connect(DATABASE) as db:
        try:
            # 获取创建者ID
            cursor = await db.execute(
                "SELECT id FROM users WHERE username = ?",
                (team.creator,)
            )
            creator_row = await cursor.fetchone()
            
            if not creator_row:
                raise HTTPException(status_code=404, detail="创建者不存在")
            
            creator_id = creator_row[0]
            
            # 创建团队
            await db.execute(
                "INSERT INTO teams (name, description, creator_id) VALUES (?, ?, ?)",
                (team.name, team.description, creator_id)
            )
            
            await db.commit()
            
            # 获取团队ID
            cursor = await db.execute("SELECT last_insert_rowid()")
            team_id = (await cursor.fetchone())[0]
            
            # 添加创建者为管理员
            await db.execute(
                "INSERT INTO team_members (team_id, user_id, role) VALUES (?, ?, ?)",
                (team_id, creator_id, "admin")
            )
            await db.commit()
            
            return {"team_id": team_id, "message": "团队创建成功"}
        except aiosqlite.IntegrityError:
            raise HTTPException(status_code=400, detail="团队名称已存在")

# 向团队推荐文章
@app.post("/teams/{team_id}/recommend")
async def recommend_to_team(team_id: int, paper_id: str, note: str = "", recommender: str = ""):
    """向团队推荐文章"""
    async with aiosqlite.connect(DATABASE) as db:
        # 获取推荐人ID
        recommender_id = None
        if recommender:
            cursor = await db.execute(
                "SELECT id FROM users WHERE username = ?",
                (recommender,)
            )
            row = await cursor.fetchone()
            if row:
                recommender_id = row[0]
        
        # 确保论文存在
        await get_paper_details(paper_id)
        
        # 添加推荐
        await db.execute(
            "INSERT INTO team_recommendations (team_id, recommender_id, paper_id, note) VALUES (?, ?, ?, ?)",
            (team_id, recommender_id, paper_id, note)
        )
        await db.commit()
        
        return {"message": "推荐成功"}

# 创建阅读任务
@app.post("/reading-tasks/create")
async def create_reading_task(task: ReadingTask):
    """创建阅读任务"""
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''
            INSERT INTO reading_tasks (user_id, paper_id, status, deadline, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (task.user_id, task.paper_id, task.status, task.deadline, task.notes))
        
        await db.commit()
        
        cursor = await db.execute("SELECT last_insert_rowid()")
        task_id = (await cursor.fetchone())[0]
        
        return {"task_id": task_id, "message": "阅读任务创建成功"}

# 获取每日简报
@app.get("/daily-digest/{username}")
async def get_daily_digest(username: str):
    """获取用户每日简报"""
    # 获取当前日期
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    async with aiosqlite.connect(DATABASE) as db:
        # 获取用户兴趣
        cursor = await db.execute(
            "SELECT interests FROM users WHERE username = ?",
            (username,)
        )
        row = await cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        interests = row[0] or ""
        
        # 获取推荐论文（基于兴趣或最新论文）
        if interests:
            interest_list = interests.split(",")
            query_conditions = " OR ".join([f"title LIKE '%{interest}%'" for interest in interest_list])
            query = f"SELECT * FROM papers WHERE {query_conditions} ORDER BY published DESC LIMIT 10"
            cursor = await db.execute(query)
        else:
            cursor = await db.execute(
                "SELECT * FROM papers ORDER BY published DESC LIMIT 10"
            )
        
        papers = await cursor.fetchall()
        
        # 获取待办任务
        cursor = await db.execute('''
            SELECT rt.*, p.title, p.authors
            FROM reading_tasks rt
            JOIN papers p ON rt.paper_id = p.id
            JOIN users u ON rt.user_id = u.id
            WHERE u.username = ? AND rt.status = 'pending'
            ORDER BY rt.deadline ASC
            LIMIT 5
        ''', (username,))
        
        tasks = await cursor.fetchall()
        
        # 格式化结果
        recommendations = []
        for paper in papers:
            recommendations.append({
                "id": paper[0],
                "title": paper[1],
                "authors": paper[2],
                "abstract": paper[3][:100] + "..." if paper[3] and len(paper[3]) > 100 else paper[3],
                "categories": paper[4]
            })
        
        pending_tasks = []
        for task in tasks:
            pending_tasks.append({
                "task_id": task[0],
                "paper_title": task[8],
                "paper_authors": task[9],
                "deadline": task[4],
                "notes": task[5]
            })
        
        return {
            "date": today,
            "username": username,
            "recommendations": recommendations,
            "pending_tasks": pending_tasks,
            "message": f"早安，{username}！这是您今天的arXiv简报"
        }

# 运行服务
if __name__ == "__main__":
    port = 8001  # 使用8001端口避免冲突
    print("🚀 启动arXiv推荐API服务...")
    print(f"📚 访问 http://localhost:{port}")
    print(f"📖 API文档: http://localhost:{port}/docs")
    uvicorn.run(app, host="0.0.0.0", port=port)