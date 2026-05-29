<template>
  <div class="page-container">
    <h2 style="margin-bottom: 20px">工作台</h2>

    <el-row :gutter="16" style="margin-bottom: 20px">
      <el-col :span="6" v-for="card in statCards" :key="card.title">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-value" :style="{ color: card.color }">{{ card.value }}</div>
            <div class="stat-title">{{ card.title }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16">
      <el-col :span="14">
        <el-card>
          <template #header><span>待办事项</span></template>
          <div v-if="dashData?.todos?.length">
            <div v-for="todo in dashData.todos" :key="todo.id" class="todo-item" @click="router.push(todo.link)">
              <el-icon :size="16"><Warning /></el-icon>
              <span>{{ todo.title }}</span>
              <el-icon class="arrow"><ArrowRight /></el-icon>
            </div>
          </div>
          <div v-else class="empty-tip">暂无待办事项</div>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card>
          <template #header><span>快捷入口</span></template>
          <div class="quick-grid">
            <div class="quick-item" v-for="q in quickLinks" :key="q.label" @click="router.push(q.link)">
              <el-icon :size="24" :color="q.color"><component :is="q.icon" /></el-icon>
              <span>{{ q.label }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDashboardStore } from '@/stores/admin/dashboard'
import { Warning, ArrowRight, Shop, User, Goods, Box, Document, Switch, Setting, Notebook } from '@element-plus/icons-vue'

const router = useRouter()
const dashStore = useDashboardStore()
const dashData = computed(() => dashStore.data)

const statCards = computed(() => [
  { title: '注册用户', value: dashData.value?.userCount || 0, color: '#409eff' },
  { title: '待审核商家', value: dashData.value?.pendingMerchants || 0, color: '#e6a23c' },
  { title: '待审核商品', value: dashData.value?.pendingProducts || 0, color: '#f56c6c' },
  { title: '待处理订单', value: dashData.value?.pendingOrders || 0, color: '#67c23a' },
])

const quickLinks = [
  { label: '商家审核', icon: 'Shop', color: '#409eff', link: '/merchant-review' },
  { label: '商品审核', icon: 'Goods', color: '#67c23a', link: '/product-review' },
  { label: '盲盒配置', icon: 'Box', color: '#e6a23c', link: '/blindbox-config' },
  { label: '订单管理', icon: 'Document', color: '#f56c6c', link: '/order-manage' },
  { label: '用户管理', icon: 'User', color: '#909399', link: '/user-manage' },
  { label: '异常处理', icon: 'Warning', color: '#f56c6c', link: '/exception' },
]

onMounted(() => dashStore.fetchDashboard())
</script>

<style scoped>
.stat-card { text-align: center; }
.stat-value { font-size: 28px; font-weight: 700; }
.stat-title { font-size: 14px; color: #909399; margin-top: 4px; }
.todo-item { display: flex; align-items: center; gap: 8px; padding: 12px 0; border-bottom: 1px solid #ebeef5; cursor: pointer; }
.todo-item:hover { color: #409eff; }
.todo-item .arrow { margin-left: auto; color: #c0c4cc; }
.quick-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.quick-item { display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 16px; border: 1px solid #ebeef5; border-radius: 8px; cursor: pointer; transition: all 0.2s; }
.quick-item:hover { border-color: #409eff; background: #f0f7ff; }
.quick-item span { font-size: 13px; color: #606266; }
</style>
