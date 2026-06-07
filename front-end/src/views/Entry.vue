<template>
  <div class="entry-page">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="floating-box box-1"></div>
      <div class="floating-box box-2"></div>
      <div class="floating-box box-3"></div>
      <div class="floating-box box-4"></div>
      <div class="floating-box box-5"></div>
    </div>

    <!-- 主内容 -->
    <div class="entry-content">
      <!-- Logo 和标题 -->
      <div class="logo-section">
        <div class="logo-icon">
          <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#667eea" />
                <stop offset="100%" style="stop-color:#764ba2" />
              </linearGradient>
            </defs>
            <rect x="10" y="10" width="80" height="80" rx="20" fill="url(#logoGrad)" />
            <text x="50" y="62" text-anchor="middle" fill="white" font-size="40" font-weight="bold">?</text>
          </svg>
        </div>
        <h1 class="main-title">乐抽盲盒</h1>
        <p class="sub-title">惊喜无限 · 乐趣无穷</p>
      </div>

      <!-- 入口卡片 -->
      <div class="entry-cards">
        <div class="entry-card user-card" @click="goTo('/user-login')">
          <div class="card-icon">
            <el-icon :size="48"><User /></el-icon>
          </div>
          <h3>用户端</h3>
          <p>探索盲盒世界，抽取惊喜好物</p>
          <div class="card-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>

        <div class="entry-card merchant-card" @click="goTo('/merchant-login')">
          <div class="card-icon">
            <el-icon :size="48"><Shop /></el-icon>
          </div>
          <h3>商户端</h3>
          <p>管理商品库存，处理发货订单</p>
          <div class="card-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>

        <div class="entry-card admin-card" @click="goTo('/admin-login')">
          <div class="card-icon">
            <el-icon :size="48"><Setting /></el-icon>
          </div>
          <h3>管理端</h3>
          <p>平台运营管理，数据统计分析</p>
          <div class="card-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>
      </div>

      <!-- 底部信息 -->
      <div class="footer-info">
        <p>© 2026 乐抽盲盒平台 - 您的盲盒购物首选</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { User, Shop, Setting, ArrowRight } from '@element-plus/icons-vue'

const router = useRouter()

function goTo(path: string) {
  router.push(path)
}
</script>

<style scoped>
.entry-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0c1445 0%, #1a237e 30%, #283593 60%, #3949ab 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

/* 背景装饰 */
.bg-decoration {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.floating-box {
  position: absolute;
  border-radius: 20px;
  opacity: 0.1;
  animation: float 15s infinite ease-in-out;
}

.box-1 {
  width: 200px;
  height: 200px;
  background: linear-gradient(45deg, #ff6b6b, #feca57);
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.box-2 {
  width: 150px;
  height: 150px;
  background: linear-gradient(45deg, #48dbfb, #0abde3);
  top: 60%;
  right: 15%;
  animation-delay: 3s;
}

.box-3 {
  width: 180px;
  height: 180px;
  background: linear-gradient(45deg, #ff9ff3, #f368e0);
  bottom: 20%;
  left: 20%;
  animation-delay: 6s;
}

.box-4 {
  width: 120px;
  height: 120px;
  background: linear-gradient(45deg, #54a0ff, #2e86de);
  top: 30%;
  right: 30%;
  animation-delay: 9s;
}

.box-5 {
  width: 160px;
  height: 160px;
  background: linear-gradient(45deg, #5f27cd, #341f97);
  bottom: 10%;
  right: 40%;
  animation-delay: 12s;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  25% { transform: translateY(-30px) rotate(5deg); }
  50% { transform: translateY(0) rotate(-5deg); }
  75% { transform: translateY(30px) rotate(3deg); }
}

/* 主内容 */
.entry-content {
  position: relative;
  z-index: 10;
  text-align: center;
  padding: 40px;
}

/* Logo */
.logo-section {
  margin-bottom: 60px;
}

.logo-icon {
  width: 100px;
  height: 100px;
  margin: 0 auto 20px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.main-title {
  font-size: 48px;
  font-weight: 800;
  color: #fff;
  margin: 0 0 10px;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  letter-spacing: 4px;
}

.sub-title {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  letter-spacing: 8px;
}

/* 入口卡片 */
.entry-cards {
  display: flex;
  gap: 30px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 60px;
}

.entry-card {
  width: 240px;
  padding: 40px 30px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.entry-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0) 100%);
  transition: opacity 0.3s;
  opacity: 0;
}

.entry-card:hover {
  transform: translateY(-15px) scale(1.02);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.3);
}

.entry-card:hover::before {
  opacity: 1;
}

.user-card {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.8) 0%, rgba(118, 75, 162, 0.8) 100%);
}

.merchant-card {
  background: linear-gradient(135deg, rgba(240, 147, 43, 0.8) 0%, rgba(245, 135, 55, 0.8) 100%);
}

.admin-card {
  background: linear-gradient(135deg, rgba(46, 134, 222, 0.8) 0%, rgba(43, 119, 191, 0.8) 100%);
}

.card-icon {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 20px;
}

.entry-card h3 {
  font-size: 24px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 12px;
}

.entry-card p {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  margin: 0 0 20px;
  line-height: 1.6;
}

.card-arrow {
  color: rgba(255, 255, 255, 0.6);
  transition: all 0.3s;
}

.entry-card:hover .card-arrow {
  color: #fff;
  transform: translateX(5px);
}

/* 底部信息 */
.footer-info {
  color: rgba(255, 255, 255, 0.5);
  font-size: 14px;
}

.footer-info p {
  margin: 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .entry-cards {
    flex-direction: column;
    align-items: center;
  }

  .entry-card {
    width: 100%;
    max-width: 300px;
  }

  .main-title {
    font-size: 36px;
  }
}
</style>
