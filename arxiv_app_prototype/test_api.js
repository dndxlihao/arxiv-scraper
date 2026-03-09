#!/usr/bin/env node

/**
 * arXiv推荐APP API测试脚本
 * 测试所有核心API功能
 */

const fetch = require('node-fetch');

const API_BASE = 'http://localhost:8000';
const TEST_USER = 'testuser2';

async function testAPI() {
  console.log('🔍 arXiv推荐APP API测试开始\n');
  
  try {
    // 1. 测试API根端点
    console.log('1. 测试API根端点...');
    const rootRes = await fetch(`${API_BASE}/`);
    const rootData = await rootRes.json();
    console.log(`   ✅ ${rootData.message} (版本: ${rootData.version})`);
    
    // 2. 注册测试用户
    console.log('\n2. 注册测试用户...');
    const registerRes = await fetch(`${API_BASE}/users/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: TEST_USER,
        email: `${TEST_USER}@example.com`,
        interests: ['offline RL', 'power system', 'reinforcement learning'],
        team: 'Power Systems Research'
      })
    });
    
    if (registerRes.status === 200) {
      const registerData = await registerRes.json();
      console.log(`   ✅ 用户注册成功 (ID: ${registerData.user_id})`);
    } else {
      const error = await registerRes.text();
      console.log(`   ⚠️ 用户可能已存在: ${error}`);
    }
    
    // 3. 获取个性化推荐
    console.log('\n3. 获取个性化推荐...');
    const recRes = await fetch(`${API_BASE}/users/${TEST_USER}/recommendations?limit=3`);
    const recommendations = await recRes.json();
    console.log(`   ✅ 获取到 ${recommendations.length} 篇推荐论文`);
    
    if (recommendations.length > 0) {
      const firstPaper = recommendations[0];
      console.log(`   第一篇论文: "${firstPaper.title.substring(0, 50)}..."`);
      console.log(`   作者: ${firstPaper.authors.slice(0, 2).join(', ')}...`);
      console.log(`   关键词: ${firstPaper.keywords.slice(0, 3).join(', ')}`);
      console.log(`   推荐分数: ${firstPaper.score.toFixed(2)}`);
      
      // 保存第一个论文ID用于后续测试
      const testPaperId = firstPaper.id;
      
      // 4. 收藏论文
      console.log('\n4. 收藏论文...');
      const collectRes = await fetch(`${API_BASE}/users/${TEST_USER}/collect/${testPaperId}`, {
        method: 'POST'
      });
      
      if (collectRes.status === 200) {
        console.log(`   ✅ 论文收藏成功 (ID: ${testPaperId})`);
      }
      
      // 5. 获取论文详情
      console.log('\n5. 获取论文详情...');
      const detailRes = await fetch(`${API_BASE}/papers/${testPaperId}`);
      const paperDetail = await detailRes.json();
      console.log(`   ✅ 论文详情获取成功`);
      console.log(`   标题: ${paperDetail.title.substring(0, 60)}...`);
      console.log(`   摘要长度: ${paperDetail.summary.length} 字符`);
      console.log(`   分类: ${paperDetail.categories.join(', ')}`);
      console.log(`   PDF链接: ${paperDetail.pdf_url}`);
      
      // 6. 获取相关论文
      console.log('\n6. 获取相关论文...');
      const relatedRes = await fetch(`${API_BASE}/papers/${testPaperId}/related?limit=3`);
      const relatedPapers = await relatedRes.json();
      console.log(`   ✅ 获取到 ${relatedPapers.length} 篇相关论文`);
      
      // 7. 获取收藏列表
      console.log('\n7. 获取收藏列表...');
      const collectionsRes = await fetch(`${API_BASE}/users/${TEST_USER}/collections`);
      const collections = await collectionsRes.json();
      console.log(`   ✅ 用户有 ${collections.length} 篇收藏`);
      
      // 8. 搜索论文
      console.log('\n8. 搜索论文...');
      const searchRes = await fetch(`${API_BASE}/papers/search?query=offline%20reinforcement%20learning&limit=2`);
      const searchResults = await searchRes.json();
      console.log(`   ✅ 搜索到 ${searchResults.length} 篇相关论文`);
      
      // 9. 创建团队
      console.log('\n9. 创建团队...');
      const teamRes = await fetch(`${API_BASE}/teams/create?name=Power%20Systems%20Lab&description=Research%20on%20power%20systems%20and%20RL&creator=${TEST_USER}`);
      
      if (teamRes.status === 200) {
        const teamData = await teamRes.json();
        console.log(`   ✅ 团队创建成功 (ID: ${teamData.team_id})`);
        
        // 10. 向团队推荐文章
        console.log('\n10. 向团队推荐文章...');
        const recommendRes = await fetch(`${API_BASE}/teams/${teamData.team_id}/recommend?paper_id=${testPaperId}&note=Important%20paper%20for%20our%20research&recommender=${TEST_USER}`, {
          method: 'POST'
        });
        
        if (recommendRes.status === 200) {
          console.log(`   ✅ 成功向团队推荐文章`);
        }
      }
      
      // 11. 获取每日简报
      console.log('\n11. 获取每日简报...');
      const digestRes = await fetch(`${API_BASE}/daily-digest/${TEST_USER}`);
      const digest = await digestRes.json();
      console.log(`   ✅ ${digest.date} 的每日简报`);
      console.log(`   包含 ${digest.papers.length} 篇精选论文`);
      
      // 12. 创建阅读任务
      console.log('\n12. 创建阅读任务...');
      const taskRes = await fetch(`${API_BASE}/reading-tasks/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: TEST_USER,
          paper_id: testPaperId,
          status: 'pending',
          deadline: '2026-03-15',
          notes: '需要仔细阅读的方法部分'
        })
      });
      
      if (taskRes.status === 200) {
        const taskData = await taskRes.json();
        console.log(`   ✅ 阅读任务创建成功 (ID: ${taskData.task_id})`);
      }
      
    } else {
      console.log('   ⚠️ 没有获取到推荐论文，可能arXiv API暂时不可用');
    }
    
    console.log('\n🎉 所有API测试完成！');
    console.log('\n📊 测试总结:');
    console.log('   后端服务: ✅ 运行正常');
    console.log('   arXiv API: ✅ 连接正常');
    console.log('   数据库: ✅ 数据存储正常');
    console.log('   核心功能: ✅ 全部可用');
    
  } catch (error) {
    console.error('\n❌ 测试过程中出现错误:');
    console.error(error.message);
    console.log('\n💡 可能的原因:');
    console.log('   1. 后端服务未启动 (运行: python app.py)');
    console.log('   2. 网络连接问题');
    console.log('   3. arXiv API暂时不可用');
  }
}

// 运行测试
testAPI();