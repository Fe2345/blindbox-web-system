<template>
  <div class="page-container">
    <div class="page-header">
      <h2>我的订单</h2>
    </div>

    <el-tabs v-model="activeTab" @tab-change="handleTabChange">
      <el-tab-pane label="全部" name="all" />
      <el-tab-pane label="待发货" name="pending" />
      <el-tab-pane label="已发货" name="shipped" />
      <el-tab-pane label="已完成" name="completed" />
    </el-tabs>

    <div v-if="filteredOrders.length">
      <el-card v-for="order in filteredOrders" :key="order.id" style="margin-bottom: 12px">
        <div class="order-card">
          <div class="order-left">
            <img :src="order.assetImage" class="order-img" />
            <div class="order-info">
              <div class="order-name">{{ order.assetName }}</div>
              <div class="order-meta">订单号：{{ order.orderNo }}</div>
              <div class="order-meta">类型：{{ order.type === 'shipment' ? '发货' : '换物' }}</div>
              <div class="order-meta">创建时间：{{ formatDate(order.createdAt) }}</div>
            </div>
          </div>
          <div class="order-right">
            <el-tag :type="order.status === 'pending' ? 'warning' : order.status === 'shipped' ? 'primary' : 'success'">
              {{ orderStatusLabel(order.status) }}
            </el-tag>
            <div v-if="order.logistics" class="logistics">
              <div>{{ order.logistics.company }}：{{ order.logistics.trackingNo }}</div>
            </div>
            <div class="order-actions">
              <el-button size="small" @click="showOrderDetail(order)">查看详情</el-button>
              <el-button v-if="order.status === 'shipped'" size="small" type="success" @click="handleConfirm(order.id)">确认收货</el-button>
            </div>
          </div>
        </div>
      </el-card>
    </div>
    <div v-else class="empty-tip" style="margin-top: 40px">暂无订单</div>

    <!-- 订单详情弹窗 -->
    <el-dialog v-model="detailVisible" title="订单详情" width="500px">
      <div v-if="detailOrder">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="订单号">{{ detailOrder.orderNo }}</el-descriptions-item>
          <el-descriptions-item label="商品">{{ detailOrder.assetName }}</el-descriptions-item>
          <el-descriptions-item label="类型">{{ detailOrder.type === 'shipment' ? '发货' : '换物' }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="detailOrder.status === 'pending' ? 'warning' : detailOrder.status === 'shipped' ? 'primary' : 'success'">
              {{ orderStatusLabel(detailOrder.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="收货人">{{ detailOrder.address.name }}</el-descriptions-item>
          <el-descriptions-item label="手机号">{{ detailOrder.address.phone }}</el-descriptions-item>
          <el-descriptions-item label="收货地址">{{ detailOrder.address.fullAddress }}</el-descriptions-item>
          <el-descriptions-item v-if="detailOrder.logistics" label="物流公司">{{ detailOrder.logistics.company }}</el-descriptions-item>
          <el-descriptions-item v-if="detailOrder.logistics" label="运单号">{{ detailOrder.logistics.trackingNo }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(detailOrder.createdAt) }}</el-descriptions-item>
          <el-descriptions-item v-if="detailOrder.shippedAt" label="发货时间">{{ formatDate(detailOrder.shippedAt) }}</el-descriptions-item>
          <el-descriptions-item v-if="detailOrder.completedAt" label="完成时间">{{ formatDate(detailOrder.completedAt) }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useOrderStore } from '@/stores/order'
import { ElMessage } from 'element-plus'
import { formatDate, orderStatusLabel } from '@/utils/format'
import type { Order } from '@/types/order'

const orderStore = useOrderStore()
const activeTab = ref('all')
const detailVisible = ref(false)
const detailOrder = ref<Order | null>(null)

const filteredOrders = computed(() => {
  if (activeTab.value === 'all') return orderStore.orders
  return orderStore.orders.filter((o) => o.status === activeTab.value)
})

function handleTabChange() {}

function showOrderDetail(order: Order) {
  detailOrder.value = order
  detailVisible.value = true
}

async function handleConfirm(id: string) {
  const res = await orderStore.confirmReceive(id)
  if (res.code === 200) ElMessage.success('确认收货成功')
  else ElMessage.error(res.message)
}

onMounted(() => orderStore.fetchOrders())
</script>

<style scoped>
.order-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.order-left {
  display: flex;
  gap: 16px;
  align-items: center;
}

.order-img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.order-name {
  font-weight: 600;
  margin-bottom: 4px;
}

.order-meta {
  font-size: 13px;
  color: #909399;
}

.order-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.logistics {
  font-size: 13px;
  color: #606266;
}

.order-actions {
  display: flex;
  gap: 8px;
}
</style>
