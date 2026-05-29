<template>
  <div class="page-container">
    <div class="page-header"><h2>交易账本</h2></div>
    <div class="filter-bar">
      <el-select v-model="filterType" placeholder="类型筛选" clearable style="width: 150px">
        <el-option label="盲抽" value="blindbox_draw" /><el-option label="回收" value="recycle" />
        <el-option label="发货" value="shipment" /><el-option label="换物" value="exchange" />
        <el-option label="系统" value="system" />
      </el-select>
      <el-date-picker v-model="dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" style="width: 300px" />
    </div>
    <el-table :data="filteredLedger" stripe>
      <el-table-column label="类型" width="100">
        <template #default="{ row }"><el-tag :type="typeTag(row.type)" size="small">{{ typeLabel(row.type) }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="description" label="说明" />
      <el-table-column label="积分变动" width="120">
        <template #default="{ row }"><span :style="{ color: row.amount > 0 ? '#67c23a' : row.amount < 0 ? '#f56c6c' : '#909399' }">{{ row.amount === 0 ? '-' : (row.amount > 0 ? '+' : '') + row.amount }}</span></template>
      </el-table-column>
      <el-table-column label="时间" width="180"><template #default="{ row }">{{ row.createdAt }}</template></el-table-column>
    </el-table>
    <div v-if="!filteredLedger.length" class="empty-tip">暂无记录</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useLedgerStore } from '@/stores/admin/ledger'

const ledgerStore = useLedgerStore()
const filterType = ref('')
const dateRange = ref<[Date, Date] | null>(null)

function typeLabel(type: string) {
  const map: Record<string, string> = { blindbox_draw: '盲抽', recycle: '回收', shipment: '发货', exchange: '换物', system: '系统' }
  return map[type] || type
}
function typeTag(type: string) {
  const map: Record<string, string> = { blindbox_draw: 'primary', recycle: 'warning', shipment: 'success', exchange: 'info', system: 'danger' }
  return map[type] || 'info'
}

const filteredLedger = computed(() => {
  return ledgerStore.list.filter((l) => {
    if (filterType.value && l.type !== filterType.value) return false
    if (dateRange.value) {
      const d = new Date(l.createdAt)
      if (d < dateRange.value[0] || d > dateRange.value[1]) return false
    }
    return true
  })
})

onMounted(() => ledgerStore.fetchList())
</script>
