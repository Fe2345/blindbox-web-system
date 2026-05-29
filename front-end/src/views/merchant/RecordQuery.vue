<template>
  <div class="page-container">
    <div class="page-header">
      <h2>记录查询</h2>
    </div>

    <div class="filter-bar">
      <el-input v-model="keyword" placeholder="搜索商品名称" style="width: 180px" clearable @clear="loadData" @keyup.enter="loadData" />
      <el-select v-model="typeFilter" placeholder="记录类型" clearable style="width: 140px" @change="loadData">
        <el-option label="库存记录" value="inventory" />
        <el-option label="发货记录" value="shipment" />
        <el-option label="状态变化" value="status_change" />
      </el-select>
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        style="width: 260px"
        @change="loadData"
      />
      <el-button @click="loadData">查询</el-button>
    </div>

    <el-card>
      <el-table :data="filtered" v-loading="loading" stripe>
        <el-table-column label="记录类型" width="100">
          <template #default="{ row }">
            <el-tag :type="recordTypeColor(row.type)" size="small">{{ recordTypeLabel(row.type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="productName" label="商品名称" min-width="140" />
        <el-table-column prop="description" label="描述" min-width="120" />
        <el-table-column prop="detail" label="详情" min-width="200" show-overflow-tooltip />
        <el-table-column prop="createdAt" label="时间" width="170" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useMerchantRecordStore } from '@/stores/merchant/record'

const recordStore = useMerchantRecordStore()
const loading = ref(false)
const keyword = ref('')
const typeFilter = ref('')
const dateRange = ref<[Date, Date] | null>(null)

const filtered = computed(() => {
  let list = recordStore.list
  if (typeFilter.value) list = list.filter((r) => r.type === typeFilter.value)
  if (keyword.value) list = list.filter((r) => r.productName.includes(keyword.value))
  if (dateRange.value) {
    const [start, end] = dateRange.value
    list = list.filter((r) => {
      const d = new Date(r.createdAt)
      return d >= start && d <= new Date(end.getTime() + 86400000)
    })
  }
  return list
})

function recordTypeLabel(t: string) {
  const map: Record<string, string> = { inventory: '库存记录', shipment: '发货记录', status_change: '状态变化' }
  return map[t] || t
}

function recordTypeColor(t: string) {
  const map: Record<string, string> = { inventory: 'primary', shipment: 'success', status_change: 'warning' }
  return map[t] || 'info'
}

async function loadData() {
  loading.value = true
  await recordStore.fetchList()
  loading.value = false
}

onMounted(() => loadData())
</script>
