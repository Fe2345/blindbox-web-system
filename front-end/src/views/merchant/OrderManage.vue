<template>
  <div class="page-container">
    <div class="page-header">
      <h2>订单管理</h2>
    </div>

    <div class="filter-bar">
      <el-radio-group v-model="statusFilter" @change="loadData">
        <el-radio-button value="">全部</el-radio-button>
        <el-radio-button value="pending">待发货</el-radio-button>
        <el-radio-button value="shipped">已发货</el-radio-button>
        <el-radio-button value="completed">已确认收货</el-radio-button>
      </el-radio-group>
    </div>

    <el-card>
      <el-table :data="orderList" v-loading="loading" stripe>
        <el-table-column prop="orderNo" label="订单编号" width="170" />
        <el-table-column label="商品图片" width="80">
          <template #default="{ row }">
            <el-image :src="row.assetImage" style="width: 50px; height: 50px; border-radius: 4px" fit="cover" />
          </template>
        </el-table-column>
        <el-table-column prop="assetName" label="商品名称" min-width="120" />
        <el-table-column prop="userName" label="下单用户" width="90" />
        <el-table-column prop="receiverName" label="收货人" width="80" />
        <el-table-column prop="receiverPhone" label="联系电话" width="120" />
        <el-table-column prop="receiverAddress" label="收货地址" min-width="180" show-overflow-tooltip />
        <el-table-column label="订单状态" width="120">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)" size="small">{{ statusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="物流信息" min-width="150" show-overflow-tooltip>
          <template #default="{ row }">
            <template v-if="row.logisticsCompany">
              {{ row.logisticsCompany }} {{ row.trackingNo }}
            </template>
            <span v-else style="color: #c0c4cc">暂无</span>
          </template>
        </el-table-column>
        <el-table-column prop="createdAt" label="下单时间" width="110" />
        <el-table-column label="操作" width="80" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="viewDetail(row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="detailVisible" title="订单详情" width="550px">
      <el-descriptions :column="1" border v-if="currentOrder">
        <el-descriptions-item label="订单编号">{{ currentOrder.orderNo }}</el-descriptions-item>
        <el-descriptions-item label="商品名称">{{ currentOrder.assetName }}</el-descriptions-item>
        <el-descriptions-item label="下单用户">{{ currentOrder.userName }}</el-descriptions-item>
        <el-descriptions-item label="收货人">{{ currentOrder.receiverName }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentOrder.receiverPhone }}</el-descriptions-item>
        <el-descriptions-item label="收货地址">{{ currentOrder.receiverAddress }}</el-descriptions-item>
        <el-descriptions-item label="订单状态">
          <el-tag :type="statusTagType(currentOrder.status)">{{ statusLabel(currentOrder.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="下单时间">{{ currentOrder.createdAt }}</el-descriptions-item>
        <template v-if="currentOrder.logisticsCompany">
          <el-descriptions-item label="物流公司">{{ currentOrder.logisticsCompany }}</el-descriptions-item>
          <el-descriptions-item label="运单号">{{ currentOrder.trackingNo }}</el-descriptions-item>
          <el-descriptions-item label="发货时间">{{ currentOrder.shippedAt }}</el-descriptions-item>
        </template>
        <template v-if="currentOrder.completedAt">
          <el-descriptions-item label="确认收货时间">{{ currentOrder.completedAt }}</el-descriptions-item>
        </template>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useMerchantOrderStore } from '@/stores/merchant/order'
import type { MerchantOrder } from '@/types/merchant-self'

const orderStore = useMerchantOrderStore()
const loading = ref(false)
const statusFilter = ref('')
const detailVisible = ref(false)
const currentOrder = ref<MerchantOrder | null>(null)
const orderList = ref<MerchantOrder[]>([])

function statusLabel(status: string) {
  const map: Record<string, string> = { pending: '待发货', shipped: '已发货', completed: '已确认收货' }
  return map[status] || status
}

function statusTagType(status: string) {
  const map: Record<string, string> = { pending: 'warning', shipped: 'primary', completed: 'success' }
  return map[status] || 'info'
}

function viewDetail(order: MerchantOrder) {
  currentOrder.value = order
  detailVisible.value = true
}

async function loadData() {
  loading.value = true
  const res: any = await orderStore.fetchList({ status: statusFilter.value || undefined })
  if (res.code === 200) orderList.value = orderStore.list
  loading.value = false
}

onMounted(() => loadData())
</script>
