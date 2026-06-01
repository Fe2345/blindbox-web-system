<template>
  <div class="page-container">
    <el-page-header @back="router.back()" title="返回" content="交易记录" />

    <div class="filter-bar" style="margin-top: 20px">
      <el-select v-model="filterType" placeholder="类型筛选" clearable style="width: 150px">
        <el-option label="盲抽记录" value="blindbox_draw" />
        <el-option label="回收记录" value="recycle" />
        <el-option label="发货记录" value="shipment" />
        <el-option label="换物记录" value="exchange" />
      </el-select>
      <el-date-picker v-model="dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" style="width: 300px" />
    </div>

    <el-table :data="filteredRecords" stripe style="margin-top: 12px">
      <el-table-column label="类型" width="120">
        <template #default="{ row }">
          <el-tag :type="typeTagType(row.type)" size="small">{{ transactionTypeLabel(row.type) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="说明" />
      <el-table-column prop="relatedAssetName" label="关联商品" width="180" />
      <el-table-column prop="statusChange" label="状态变化" width="150" />
      <el-table-column label="时间" width="180">
        <template #default="{ row }">{{ formatDate(row.createdAt) }}</template>
      </el-table-column>
    </el-table>

    <div v-if="!filteredRecords.length" class="empty-tip">暂无交易记录</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePointsStore } from '@/stores/points'
import { formatDate, transactionTypeLabel } from '@/utils/format'

const router = useRouter()
const pointsStore = usePointsStore()
const filterType = ref('')
const dateRange = ref<[Date, Date] | null>(null)

function typeTagType(type: string) {
  const map: Record<string, string> = { blindbox_draw: 'primary', recycle: 'warning', shipment: 'success', exchange: 'info' }
  return map[type] || 'info'
}

const filteredRecords = computed(() => {
  return pointsStore.transactions.filter((t) => {
    if (filterType.value && t.type !== filterType.value) return false
    if (dateRange.value) {
      const d = new Date(t.createdAt)
      if (d < dateRange.value[0] || d > dateRange.value[1]) return false
    }
    return true
  })
})

onMounted(() => pointsStore.fetchTransactions())
</script>
