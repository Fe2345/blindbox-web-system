<template>
  <div class="page-container">
    <!-- 轮播区 -->
    <el-carousel height="280px" class="home-carousel">
      <el-carousel-item v-for="item in carouselItems" :key="item.title">
        <div class="carousel-card" :style="{ background: item.bg }">
          <div class="carousel-text">
            <h3>{{ item.title }}</h3>
            <p>{{ item.desc }}</p>
            <el-button type="primary" @click="router.push(item.link)">立即查看</el-button>
          </div>
        </div>
      </el-carousel-item>
    </el-carousel>

    <!-- 用户信息区 -->
    <el-card v-if="userStore.isLoggedIn && userStore.userInfo" class="user-summary">
      <div class="summary-content">
        <div class="summary-item">
          <span class="label">欢迎回来</span>
          <span class="value">{{ userStore.userInfo.username }}</span>
        </div>
        <div class="summary-item">
          <span class="label">积分余额</span>
          <span class="value points">{{ userStore.userInfo.points }}</span>
        </div>
        <div class="summary-item">
          <span class="label">待处理订单</span>
          <span class="value">{{ pendingOrders }}</span>
        </div>
        <div class="summary-item">
          <span class="label">换物申请</span>
          <span class="value">{{ pendingExchange }}</span>
        </div>
      </div>
    </el-card>

    <!-- 快捷入口 -->
    <div class="quick-actions">
      <div class="action-item" @click="router.push('/blindbox')">
        <el-icon :size="32" color="#409eff"><Box /></el-icon>
        <span>立即抽取</span>
      </div>
      <div class="action-item" @click="router.push('/assets')">
        <el-icon :size="32" color="#67c23a"><Present /></el-icon>
        <span>我的资产</span>
      </div>
      <div class="action-item" @click="router.push('/exchange/publish')">
        <el-icon :size="32" color="#e6a23c"><Switch /></el-icon>
        <span>发布换物</span>
      </div>
      <div class="action-item" @click="router.push('/orders')">
        <el-icon :size="32" color="#f56c6c"><Document /></el-icon>
        <span>查看订单</span>
      </div>
    </div>

    <!-- 热门盲盒 -->
    <div class="section">
      <div class="section-header">
        <h3>热门盲盒</h3>
        <el-button text @click="router.push('/blindbox')">查看全部</el-button>
      </div>
      <div class="card-grid">
        <div v-for="box in hotBoxes" :key="box.id" class="item-card" @click="router.push(`/blindbox/${box.id}`)">
          <img :src="box.cover" :alt="box.name" class="card-image" />
          <div class="card-body">
            <div class="card-title">{{ box.name }}</div>
            <div class="card-meta">消耗积分：{{ box.costPoints }}</div>
            <div class="card-meta">剩余库存：{{ box.prizes.reduce((s, p) => s + p.remainingQuantity, 0) }}</div>
          </div>
          <div class="card-actions">
            <el-tag :type="box.status === 'active' ? 'success' : box.status === 'inactive' ? 'warning' : 'info'" size="small">
              {{ box.status === 'active' ? '进行中' : box.status === 'inactive' ? '已下架' : '已结束' }}
            </el-tag>
          </div>
        </div>
      </div>
    </div>

    <!-- 换物推荐 -->
    <div class="section">
      <div class="section-header">
        <h3>换物推荐</h3>
        <el-button text @click="router.push('/exchange')">查看全部</el-button>
      </div>
      <div class="card-grid">
        <div v-for="post in exchangePosts" :key="post.id" class="item-card" @click="router.push('/exchange')">
          <img :src="post.assetImage" :alt="post.assetName" class="card-image" />
          <div class="card-body">
            <div class="card-title">{{ post.assetName }}</div>
            <div class="card-meta">
              <el-tag :style="{ color: rarityColor(post.assetRarity), borderColor: rarityColor(post.assetRarity) }" size="small" effect="plain">
                {{ rarityLabel(post.assetRarity) }}
              </el-tag>
            </div>
            <div class="card-meta">期望：{{ post.expectDescription }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useBlindBoxStore } from '@/stores/blindbox'
import { useExchangeStore } from '@/stores/exchange'
import { Box, Present, Switch, Document } from '@element-plus/icons-vue'
import { rarityLabel, rarityColor } from '@/utils/format'

const router = useRouter()
const userStore = useUserStore()
const blindBoxStore = useBlindBoxStore()
const exchangeStore = useExchangeStore()

const pendingOrders = ref(0)
const pendingExchange = ref(0)
const hotBoxes = ref<any[]>([])
const exchangePosts = ref<any[]>([])

const carouselItems = [
  { title: '原神角色盲盒', desc: '原神人气角色周边，限定挂件、立牌、手办等你来抽', bg: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', link: '/blindbox/bb001' },
  { title: 'MOLLY城市盲盒', desc: '泡泡玛特MOLLY城市系列，隐藏款概率惊喜', bg: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', link: '/blindbox/bb002' },
  { title: '换物中心', desc: '闲置好物换起来，找到你心仪的宝贝', bg: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', link: '/exchange' },
]

onMounted(async () => {
  await blindBoxStore.fetchBlindBoxes()
  hotBoxes.value = blindBoxStore.blindBoxes.filter((b) => b.status !== 'ended').slice(0, 4)
  await exchangeStore.fetchPosts()
  exchangePosts.value = exchangeStore.posts.filter((p) => p.status === 'published').slice(0, 3)
})
</script>

<style scoped>
.home-carousel {
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
}

.carousel-card {
  height: 280px;
  display: flex;
  align-items: center;
  padding: 0 60px;
}

.carousel-text {
  color: #fff;
}

.carousel-text h3 {
  font-size: 28px;
  margin-bottom: 12px;
}

.carousel-text p {
  font-size: 16px;
  margin-bottom: 20px;
  opacity: 0.9;
}

.user-summary {
  margin-bottom: 20px;
}

.summary-content {
  display: flex;
  justify-content: space-around;
}

.summary-item {
  text-align: center;
}

.summary-item .label {
  display: block;
  font-size: 13px;
  color: #909399;
  margin-bottom: 4px;
}

.summary-item .value {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.summary-item .value.points {
  color: #e6a23c;
}

.quick-actions {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.action-item {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s;
}

.action-item:hover {
  transform: translateY(-2px);
}

.action-item span {
  font-size: 14px;
  color: #606266;
}

.section {
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h3 {
  font-size: 18px;
  color: #303133;
}
</style>
