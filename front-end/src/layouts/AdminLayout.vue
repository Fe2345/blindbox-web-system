<template>
  <el-container class="admin-layout">
    <el-aside width="220px" class="admin-aside">
      <div class="aside-logo">乐抽盲盒 · 管理后台</div>
      <el-menu
        :default-active="activeMenu"
        router
        background-color="#001529"
        text-color="#ffffffb3"
        active-text-color="#409eff"
        :collapse="false"
      >
        <el-menu-item index="/">
          <el-icon><DataBoard /></el-icon>
          <span>工作台</span>
        </el-menu-item>

        <el-sub-menu index="merchant-group">
          <template #title>
            <el-icon><Shop /></el-icon>
            <span>商家管理</span>
          </template>
          <el-menu-item index="/merchant-review">商家审核</el-menu-item>
          <el-menu-item index="/merchant-manage">商家列表</el-menu-item>
        </el-sub-menu>

        <el-menu-item index="/user-manage">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>

        <el-sub-menu index="product-group">
          <template #title>
            <el-icon><Goods /></el-icon>
            <span>商品管理</span>
          </template>
          <el-menu-item index="/product-review">商品审核</el-menu-item>
          <el-menu-item index="/product-template">商品模板</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="blindbox-group">
          <template #title>
            <el-icon><Box /></el-icon>
            <span>盲盒管理</span>
          </template>
          <el-menu-item index="/blindbox-config">盲盒配置</el-menu-item>
          <el-menu-item index="/prize-pool">奖池概率</el-menu-item>
        </el-sub-menu>

        <el-menu-item index="/order-manage">
          <el-icon><Document /></el-icon>
          <span>订单管理</span>
        </el-menu-item>

        <el-menu-item index="/exchange-manage">
          <el-icon><Switch /></el-icon>
          <span>换物管理</span>
        </el-menu-item>

        <el-menu-item index="/rule-config">
          <el-icon><Setting /></el-icon>
          <span>规则配置</span>
        </el-menu-item>

        <el-sub-menu index="log-group">
          <template #title>
            <el-icon><Notebook /></el-icon>
            <span>日志与异常</span>
          </template>
          <el-menu-item index="/ledger">交易账本</el-menu-item>
          <el-menu-item index="/op-log">操作日志</el-menu-item>
          <el-menu-item index="/exception">异常处理</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="admin-header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-if="currentTitle">{{ currentTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-dropdown trigger="click">
            <span class="admin-info">
              <el-icon><UserFilled /></el-icon>
              {{ authStore.adminInfo?.username || '管理员' }}
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="admin-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/admin/auth'
import {
  DataBoard, Shop, User, Goods, Box, Document, Switch,
  Setting, Notebook, UserFilled, ArrowDown,
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const menuTitleMap: Record<string, string> = {
  '/merchant-review': '商家审核',
  '/merchant-manage': '商家管理',
  '/user-manage': '用户管理',
  '/product-review': '商品审核',
  '/product-template': '商品模板',
  '/blindbox-config': '盲盒配置',
  '/prize-pool': '奖池概率',
  '/order-manage': '订单管理',
  '/exchange-manage': '换物管理',
  '/rule-config': '规则配置',
  '/ledger': '交易账本',
  '/op-log': '操作日志',
  '/exception': '异常处理',
}

const activeMenu = computed(() => route.path)
const currentTitle = computed(() => menuTitleMap[route.path] || '')

function handleLogout() {
  authStore.logout()
  window.location.href = '/login'
}
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
}

.admin-aside {
  background: #001529;
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

.admin-header {
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 60px !important;
}

.admin-info {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  font-size: 14px;
  color: #606266;
}

.admin-main {
  background: #f0f2f5;
  min-height: calc(100vh - 60px);
  padding: 0;
}

.el-aside .el-menu {
  border-right: none;
}
</style>
