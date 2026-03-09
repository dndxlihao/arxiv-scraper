                    0]
                    await db.execute(
                        "INSERT INTO team_members (team_id, user_id, role) VALUES (?, ?, ?)",
                        (team_id, user_id, "admin")
                    )
                    await db.commit()
            
            return {"team_id": team_id, "message": "团队创建成功"}
        except aiosqlite.IntegrityError:
            raise HTTPException(status_code=400, detail="团队名称已存在")

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

@app.get("/daily-digest/{username}")
async def get_daily_digest(username: str):
    """获取每日简报"""
    # 获取用户兴趣
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute(
            "SELECT interests FROM users WHERE username = ?",
            (username,)
        )
        row = await cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        interests = json.loads(row[0]) if row[0] else ["machine learning", "AI"]
    
    # 爬取今日论文（限制10篇）
    papers = await scrape_arxiv(interests, max_results=10)
    
    # 生成简报
    digest = DailyDigest(
        date=datetime.now().strftime("%Y-%m-%d"),
        papers=papers,
        user_id=username
    )
    
    return digest

# 定时任务（简化版）
async def scheduled_daily_crawl():
    """定时爬取任务（每天9点执行）"""
    while True:
        now = datetime.now()
        
        # 检查是否是9点
        if now.hour == 9 and now.minute == 0:
            print(f"[{now}] 开始每日arXiv爬取...")
            
            # 这里可以添加：为所有用户生成简报并发送通知
            # 简化实现：只打印日志
            print("每日爬取完成")
            
            # 等待1小时，避免重复执行
            await asyncio.sleep(3600)
        else:
            # 每分钟检查一次
            await asyncio.sleep(60)

@app.on_event("startup")
async def start_scheduler():
    """启动定时任务"""
    asyncio.create_task(scheduled_daily_crawl())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)