<template>
  <div class="page-container">
    <div class="page-header">
      <h2>发货任务</h2>
    </div>

    <div class="filter-bar">
      <el-radio-group v-model="statusFilter" @change="loadData">
        <el-radio-button value="">全部</el-radio-button>
        <el-radio-button value="pending">待发货</el-radio-button>
        <el-radio-button value="shipped">已发货</el-radio-button>
      </el-radio-group>
    </div>

    <el-card>
      <el-table :data="filtered" v-loading="loading" stripe>
        <el-table-column prop="taskNo" label="任务编号" width="150" />
        <el-table-column label="商品图片" width="80">
          <template #default="{ row }">
            <el-image :src="row.productImage" style="width: 50px; height: 50px; border-radius: 4px" fit="cover" />
          </template>
        </el-table-column>
        <el-table-column prop="productName" label="商品名称" min-width="120" />
        <el-table-column prop="receiverName" label="收货人" width="80" />
        <el-table-column prop="receiverPhone" label="联系电话" width="120" />
        <el-table-column prop="receiverAddress" label="收货地址" min-width="180" show-overflow-tooltip />
        <el-table-column label="发货状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'pending' ? 'warning' : 'success'" size="small">
              {{ row.status === 'pending' ? '待发货' : '已发货' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createdAt" label="申请时间" width="110" />
        <el-table-column label="操作" width="140" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="viewDetail(row)">详情</el-button>
            <el-button v-if="row.status === 'pending'" link type="primary" size="small" @click="openShip(row)">确认发货</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="detailVisible" title="发货任务详情" width="550px">
      <el-descriptions :column="1" border v-if="currentTask">
        <el-descriptions-item label="任务编号">{{ currentTask.taskNo }}</el-descriptions-item>
        <el-descriptions-item label="订单编号">{{ currentTask.orderNo }}</el-descriptions-item>
        <el-descriptions-item label="商品名称">{{ currentTask.productName }}</el-descriptions-item>
        <el-descriptions-item label="收货人">{{ currentTask.receiverName }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentTask.receiverPhone }}</el-descriptions-item>
        <el-descriptions-item label="收货地址">{{ currentTask.receiverAddress }}</el-descriptions-item>
        <el-descriptions-item label="发货状态">
          <el-tag :type="currentTask.status === 'pending' ? 'warning' : 'success'">
            {{ currentTask.status === 'pending' ? '待发货' : '已发货' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="申请时间">{{ currentTask.createdAt }}</el-descriptions-item>
        <template v-if="currentTask.status === 'shipped'">
          <el-descriptions-item label="物流公司">{{ currentTask.logisticsCompany }}</el-descriptions-item>
          <el-descriptions-item label="运单号">{{ currentTask.trackingNo }}</el-descriptions-item>
          <el-descriptions-item label="发货时间">{{ currentTask.shippedAt }}</el-descriptions-item>
        </template>
      </el-descriptions>
    </el-dialog>

    <el-dialog v-model="shipVisible" title="确认发货" width="480px">
      <el-form ref="shipFormRef" :model="shipForm" :rules="shipRules" label-width="90px" v-if="currentTask">
        <el-form-item label="商品名称">
          <span>{{ currentTask.productName }}</span>
        </el-form-item>
        <el-form-item label="订单编号">
          <span>{{ currentTask.orderNo }}</span>
        </el-form-item>
        <el-form-item label="物流公司" prop="logisticsCompany">
          <el-select v-model="shipForm.logisticsCompany" placeholder="请选择物流公司" style="width: 100%">
            <el-option label="顺丰速运" value="顺丰速运" />
            <el-option label="中通快递" value="中通快递" />
            <el-option label="圆通速递" value="圆通速递" />
            <el-option label="韵达快递" value="韵达快递" />
            <el-option label="京东物流" value="京东物流" />
            <el-option label="邮政EMS" value="邮政EMS" />
          </el-select>
        </el-form-item>
        <el-form-item label="运单号" prop="trackingNo">
          <el-input v-model="shipForm.trackingNo" placeholder="请输入运单号" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="shipVisible = false">取消</el-button>
        <el-button type="primary" :loading="shipping" @click="handleShip">确认发货</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { useMerchantShipmentStore } from '@/stores/merchant/shipment'
import type { ShipmentTask } from '@/types/merchant-self'

const shipmentStore = useMerchantShipmentStore()
const loading = ref(false)
const shipping = ref(false)
const statusFilter = ref('')
const detailVisible = ref(false)
const shipVisible = ref(false)
const currentTask = ref<ShipmentTask | null>(null)
const shipFormRef = ref<FormInstance>()

const shipForm = reactive({
  logisticsCompany: '',
  trackingNo: '',
})

const shipRules = {
  logisticsCompany: [{ required: true, message: '请选择物流公司', trigger: 'change' }],
  trackingNo: [{ required: true, message: '请输入运单号', trigger: 'blur' }],
}

const filtered = computed(() => {
  if (!statusFilter.value) return shipmentStore.list
  return shipmentStore.list.filter((s) => s.status === statusFilter.value)
})

function viewDetail(task: ShipmentTask) {
  currentTask.value = task
  detailVisible.value = true
}

function openShip(task: ShipmentTask) {
  currentTask.value = task
  shipForm.logisticsCompany = ''
  shipForm.trackingNo = ''
  shipVisible.value = true
}

async function handleShip() {
  await shipFormRef.value?.validate()
  if (!currentTask.value) return
  shipping.value = true
  try {
    const res: any = await shipmentStore.confirmShip(currentTask.value.id, shipForm)
    if (res.code === 200) {
      ElMessage.success('发货成功')
      shipVisible.value = false
      loadData()
    } else {
      ElMessage.error(res.message)
    }
  } finally {
    shipping.value = false
  }
}

async function loadData() {
  loading.value = true
  await shipmentStore.fetchList()
  loading.value = false
}

onMounted(() => loadData())
</script>
