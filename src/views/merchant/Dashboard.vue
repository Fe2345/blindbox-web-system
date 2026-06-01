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
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMerchantDashboardStore } from '@/stores/merchant/dashboard'
import { Warning, ArrowRight, Goods, Box, Van, Document, Plus, List } from '@element-plus/icons-vue'

const router = useRouter()
const dashStore = useMerchantDashboardStore()
const dashData = computed(() => dashStore.data)

const statCards = computed(() => [
  { title: '已提交商品', value: dashData.value?.totalProducts || 0, color: '#409eff' },
  { title: '待审核商品', value: dashData.value?.pendingProducts || 0, color: '#e6a23c' },
  { title: '库存不足商品', value: dashData.value?.lowStockProducts || 0, color: '#f56c6c' },
  { title: '待发货任务', value: dashData.value?.pendingShipments || 0, color: '#67c23a' },
])

const quickLinks = [
  { label: '商品提交', icon: 'Plus', color: '#409eff', link: '/products/submit' },
  { label: '商品管理', icon: 'Goods', color: '#67c23a', link: '/products' },
  { label: '库存管理', icon: 'Box', color: '#e6a23c', link: '/inventory' },
  { label: '发货任务', icon: 'Van', color: '#f56c6c', link: '/shipments' },
  { label: '记录查询', icon: 'Document', color: '#909399', link: '/records' },
  { label: '商家资料', icon: 'List', color: '#409eff', link: '/profile' },
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
