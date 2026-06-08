<template>
  <div class="page-container">
    <el-page-header @back="router.back()" title="返回" content="积分明细" />

    <el-card style="margin-top: 20px">
      <div class="balance-card">
        <span class="balance-label">当前积分余额</span>
        <span class="balance-value">{{ balance }}</span>
      </div>
    </el-card>

    <div class="filter-bar" style="margin-top: 16px">
      <el-select v-model="filterType" placeholder="类型筛选" clearable style="width: 150px">
        <el-option label="盲盒消费" value="blindbox_consume" />
        <el-option label="回收返还" value="recycle_return" />
        <el-option label="系统调整" value="system_adjust" />
      </el-select>
    </div>

    <el-table :data="filteredRecords" stripe style="margin-top: 12px">
      <el-table-column label="时间" width="180">
        <template #default="{ row }">{{ formatDate(row.createdAt) }}</template>
      </el-table-column>
      <el-table-column label="类型" width="120">
        <template #default="{ row }">
          <el-tag :type="row.type === 'blindbox_consume' ? 'danger' : row.type === 'recycle_return' ? 'success' : 'info'" size="small">
            {{ pointsTypeLabel(row.type) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="说明" />
      <el-table-column label="变动积分" width="120">
        <template #default="{ row }">
          <span :style="{ color: row.amount > 0 ? '#67c23a' : '#f56c6c' }">
            {{ row.amount > 0 ? '+' : '' }}{{ row.amount }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="变动后余额" width="120">
        <template #default="{ row }">{{ row.balance }}</template>
      </el-table-column>
    </el-table>

    <div v-if="!filteredRecords.length" class="empty-tip">暂无积分记录</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePointsStore } from '@/stores/points'
import { formatDate, pointsTypeLabel } from '@/utils/format'

const router = useRouter()
const pointsStore = usePointsStore()
const filterType = ref('')
const balance = computed(() => pointsStore.balance)

const filteredRecords = computed(() => {
  if (!filterType.value) return pointsStore.records
  return pointsStore.records.filter((r) => r.type === filterType.value)
})

onMounted(async () => {
  await pointsStore.fetchBalance()
  await pointsStore.fetchRecords()
})
</script>

<style scoped>
.balance-card {
  display: flex;
  align-items: center;
  gap: 16px;
}

.balance-label {
  font-size: 16px;
  color: #606266;
}

.balance-value {
  font-size: 32px;
  font-weight: 700;
  color: #e6a23c;
}
</style>
