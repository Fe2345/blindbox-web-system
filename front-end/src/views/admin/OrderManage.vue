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
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button v-if="row.status === 'pending'" type="primary" size="small" @click="showShipDialog(row)">发货</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="shipDialogVisible" title="填写物流信息" width="450px">
      <el-form :model="shipForm" label-width="80px">
        <el-form-item label="订单号"><el-input :model-value="shipTarget?.orderNo" disabled /></el-form-item>
        <el-form-item label="物流公司"><el-input v-model="shipForm.company" placeholder="如：顺丰速运" /></el-form-item>
        <el-form-item label="运单号"><el-input v-model="shipForm.trackingNo" placeholder="请输入运单号" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="shipDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="shipping" @click="handleShip">确认发货</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useOrderStore } from '@/stores/admin/order'
import { ElMessage } from 'element-plus'
import { orderStatusLabel } from '@/utils/format'

const orderStore = useOrderStore()
const filterStatus = ref('')
const filterType = ref('')
const shipDialogVisible = ref(false)
const shipTarget = ref<any>(null)
const shipForm = ref({ company: '', trackingNo: '' })
const shipping = ref(false)

const filteredOrders = computed(() => {
  return orderStore.list.filter((o) => {
    if (filterStatus.value && o.status !== filterStatus.value) return false
    if (filterType.value && o.type !== filterType.value) return false
    return true
  })
})

function showShipDialog(row: any) { shipTarget.value = row; shipForm.value = { company: '', trackingNo: '' }; shipDialogVisible.value = true }

async function handleShip() {
  if (!shipForm.value.company || !shipForm.value.trackingNo) { ElMessage.warning('请填写完整物流信息'); return }
  shipping.value = true
  try {
    const res = await orderStore.ship(shipTarget.value.id, shipForm.value.company, shipForm.value.trackingNo)
    if (res.code === 200) { ElMessage.success('发货成功'); shipDialogVisible.value = false }
    else ElMessage.error(res.message)
  } catch { ElMessage.error('发货失败') } finally { shipping.value = false }
}

onMounted(() => orderStore.fetchList())
</script>
