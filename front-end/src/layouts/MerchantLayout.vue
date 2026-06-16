<template>
  <el-container class="merchant-layout">
    <el-aside width="220px" class="merchant-aside">
      <div class="aside-logo">乐抽盲盒 · 商家中心</div>
      <el-menu
        :default-active="activeMenu"
        router
        background-color="#0d2137"
        text-color="#ffffffb3"
        active-text-color="#409eff"
        :collapse="false"
      >
        <el-menu-item index="/">
          <el-icon><DataBoard /></el-icon>
          <span>工作台</span>
        </el-menu-item>

        <el-sub-menu index="application-group">
          <template #title>
            <el-icon><Document /></el-icon>
            <span>入驻与资料</span>
          </template>
          <el-menu-item index="/application">入驻申请</el-menu-item>
          <el-menu-item index="/profile">商家资料</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="product-group">
          <template #title>
            <el-icon><Goods /></el-icon>
            <span>商品管理</span>
          </template>
          <el-menu-item index="/products/submit">商品提交</el-menu-item>
          <el-menu-item index="/products">商品列表</el-menu-item>
        </el-sub-menu>

        <el-menu-item index="/inventory">
          <el-icon><Box /></el-icon>
          <span>库存管理</span>
        </el-menu-item>

        <el-menu-item index="/prize-stock">
          <el-icon><Present /></el-icon>
          <span>奖池库存</span>
        </el-menu-item>

        <el-menu-item index="/shipments">
          <el-icon><Van /></el-icon>
          <span>发货管理</span>
        </el-menu-item>

        <el-menu-item index="/orders">
          <el-icon><List /></el-icon>
          <span>订单管理</span>
        </el-menu-item>

        <el-menu-item index="/records">
          <el-icon><Notebook /></el-icon>
          <span>记录查询</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="merchant-header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-if="currentTitle">{{ currentTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-tag v-if="merchantInfo" :type="statusType" size="small" style="margin-right: 12px">
            {{ statusLabel }}
          </el-tag>
          <el-dropdown trigger="click">
            <span class="merchant-info">
              <el-icon><UserFilled /></el-icon>
              {{ merchantInfo?.name || '商家' }}
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="router.push('/profile')">商家资料</el-dropdown-item>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="merchant-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMerchantAuthStore } from '@/stores/merchant/auth'
import {
  DataBoard, Document, Goods, Box, Van, Notebook, Present,
  UserFilled, ArrowDown, List,
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const authStore = useMerchantAuthStore()

const merchantInfo = computed(() => authStore.merchantInfo)

const statusLabel = computed(() => {
  const map: Record<string, string> = { pending: '待审核', approved: '已通过', rejected: '已驳回' }
  return map[merchantInfo.value?.status] || ''
})

const statusType = computed(() => {
  const map: Record<string, string> = { pending: 'warning', approved: 'success', rejected: 'danger' }
  return map[merchantInfo.value?.status] || 'info'
})

const menuTitleMap: Record<string, string> = {
  '/application': '入驻申请',
  '/profile': '商家资料',
  '/products': '商品列表',
  '/products/submit': '商品提交',
  '/inventory': '库存管理',
  '/prize-stock': '奖池库存',
  '/shipments': '发货管理',
  '/orders': '订单管理',
  '/records': '记录查询',
}

const activeMenu = computed(() => route.path)
const currentTitle = computed(() => menuTitleMap[route.path] || '')

onMounted(() => {
  if (authStore.isLoggedIn) authStore.fetchInfo()
})

async function handleLogout() {
  await authStore.logout()
  window.location.href = '/login'
}
</script>

<style scoped>
.merchant-layout {
  min-height: 100vh;
}

.merchant-aside {
  background: #0d2137;
  overflow-y: auto;
}

.aside-logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 16px;
  font-weight: 700;
  border-bottom: 1px solid #ffffff1a;
}

.merchant-header {
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 60px !important;
}

.merchant-info {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  font-size: 14px;
  color: #606266;
}

.merchant-main {
  background: #f0f2f5;
  min-height: calc(100vh - 60px);
  padding: 0;
}

.el-aside .el-menu {
  border-right: none;
}
</style>
