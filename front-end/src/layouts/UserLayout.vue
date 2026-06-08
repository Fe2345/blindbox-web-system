<template>
  <el-container class="layout-container">
    <el-header class="layout-header">
      <div class="header-content">
        <div class="logo" @click="router.push('/')">乐抽盲盒</div>
        <el-menu
          :default-active="activeMenu"
          mode="horizontal"
          :ellipsis="false"
          router
          class="header-menu"
        >
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/blindbox">盲盒抽取</el-menu-item>
          <el-menu-item index="/exchange">换物中心</el-menu-item>
          <el-menu-item index="/assets">我的资产</el-menu-item>
          <el-menu-item index="/orders">我的订单</el-menu-item>
        </el-menu>
        <div class="header-right">
          <el-dropdown v-if="userStore.isLoggedIn" trigger="click">
            <span class="user-info">
              <span class="points-display" @click.stop="router.push('/points')">
                <el-icon><Coin /></el-icon>
                {{ userStore.userInfo?.points || 0 }}
              </span>
              <el-icon><User /></el-icon>
              {{ userStore.userInfo?.username || '用户' }}
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="router.push('/profile')">个人中心</el-dropdown-item>
                <el-dropdown-item @click="router.push('/points')">积分明细</el-dropdown-item>
                <el-dropdown-item @click="router.push('/transactions')">交易记录</el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          <el-button v-else type="primary" @click="router.push('/login')">登录</el-button>
        </div>
      </div>
    </el-header>
    <el-main class="layout-main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { User, ArrowDown, Coin } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

onMounted(async () => {
  if (userStore.isLoggedIn && !userStore.userInfo) {
    await userStore.fetchUserInfo()
  }
})

const activeMenu = computed(() => {
  const path = route.path
  if (path.startsWith('/blindbox')) return '/blindbox'
  if (path.startsWith('/assets')) return '/assets'
  if (path.startsWith('/exchange')) return '/exchange'
  if (path.startsWith('/orders')) return '/orders'
  return path
})

function handleLogout() {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.layout-container {
  min-height: 100vh;
}

.layout-header {
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 100;
  height: 60px !important;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 60px;
  padding: 0 20px;
}

.logo {
  font-size: 18px;
  font-weight: 700;
  color: #409eff;
  cursor: pointer;
  white-space: nowrap;
  margin-right: 30px;
}

.header-menu {
  flex: 1;
  border-bottom: none;
}

.header-menu .el-menu-item {
  height: 60px;
  line-height: 60px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  font-size: 14px;
  color: #606266;
}

.points-display {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 12px;
  background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
  border-radius: 20px;
  color: #fff;
  font-weight: 600;
  font-size: 13px;
  margin-right: 12px;
  cursor: pointer;
  transition: transform 0.2s;
}

.points-display:hover {
  transform: scale(1.05);
}

.layout-main {
  padding: 0;
  background: #f5f7fa;
  min-height: calc(100vh - 60px);
}
</style>
