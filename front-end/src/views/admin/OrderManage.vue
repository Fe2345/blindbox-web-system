<template>
  <div class="page-container">
    <div class="page-header"><h2>订单管理</h2></div>
    <div class="filter-bar">
      <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width: 150px">
        <el-option label="待发货" value="pending" /><el-option label="已发货" value="shipped" /><el-option label="已完成" value="completed" />
      </el-select>
      <el-select v-model="filterType" placeholder="类型筛选" clearable style="width: 150px">
        <el-option label="发货订单" value="shipment" /><el-option label="换物订单" value="exchange" />
      </el-select>
    </div>

    <el-table :data="filteredOrders" stripe>
      <el-table-column prop="orderNo" label="订单号" width="160" />
      <el-table-column label="商品" width="160">
        <template #default="{ row }"><div style="display: flex; align-items: center; gap: 8px"><img :src="row.assetImage" style="width: 36px; height: 36px; border-radius: 4px; object-fit: cover" /><span>{{ row.assetName }}</span></div></template>
      </el-table-column>
      <el-table-column label="类型" width="80"><template #default="{ row }"><el-tag size="small">{{ row.type === 'shipment' ? '发货' : '换物' }}</el-tag></template></el-table-column>
      <el-table-column prop="username" label="用户" width="100" />
      <el-table-column label="状态" width="100"><template #default="{ row }"><el-tag :type="row.status === 'pending' ? 'warning' : row.status === 'shipped' ? 'primary' : 'success'" size="small">{{ orderStatusLabel(row.status) }}</el-tag></template></el-table-column>
      <el-table-column label="收货地址"><template #default="{ row }">{{ row.address.fullAddress }}</template></el-table-column>
      <el-table-column label="物流"><template #default="{ row }">{{ row.logistics ? `${row.logistics.company} ${row.logistics.trackingNo}` : '-' }}</template></el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useOrderStore } from '@/stores/admin/order'
import { orderStatusLabel } from '@/utils/format'

const orderStore = useOrderStore()
const filterStatus = ref('')
const filterType = ref('')

const filteredOrders = computed(() => {
  return orderStore.list.filter((o) => {
    if (filterStatus.value && o.status !== filterStatus.value) return false
    if (filterType.value && o.type !== filterType.value) return false
    return true
  })
})

onMounted(() => orderStore.fetchList())
</script>
