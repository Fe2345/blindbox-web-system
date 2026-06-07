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
      <el-input v-model="keyword" placeholder="搜索任务编号/订单号/收货人" style="width: 250px" clearable @clear="loadData" @keyup.enter="loadData" />
      <el-button @click="loadData">查询</el-button>
    </div>

    <el-card>
      <el-table :data="shipmentStore.list" v-loading="shipmentStore.loading" stripe>
        <el-table-column prop="task_no" label="任务编号" width="150" />
        <el-table-column prop="order_no" label="订单编号" width="120" />
        <el-table-column label="商品图片" width="80">
          <template #default="{ row }">
            <el-image :src="row.product_image" style="width: 50px; height: 50px; border-radius: 4px" fit="cover" />
          </template>
        </el-table-column>
        <el-table-column prop="product_name" label="商品名称" min-width="120" />
        <el-table-column prop="receiver_name" label="收货人" width="80" />
        <el-table-column prop="receiver_phone" label="联系电话" width="120" />
        <el-table-column label="发货状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'pending' ? 'warning' : 'success'" size="small">
              {{ row.status_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="160" />
        <el-table-column label="操作" width="140" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="viewDetail(row)">详情</el-button>
            <el-button v-if="row.status === 'pending'" link type="primary" size="small" @click="openShip(row)">确认发货</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-bar" v-if="shipmentStore.total > 0">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="shipmentStore.total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next"
          @current-change="loadData"
          @size-change="loadData"
        />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailVisible" title="发货任务详情" width="550px">
      <el-descriptions :column="1" border v-if="currentTask">
        <el-descriptions-item label="任务编号">{{ currentTask.task_no }}</el-descriptions-item>
        <el-descriptions-item label="订单编号">{{ currentTask.order_no }}</el-descriptions-item>
        <el-descriptions-item label="商品名称">{{ currentTask.product_name }}</el-descriptions-item>
        <el-descriptions-item label="收货人">{{ currentTask.receiver_name }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentTask.receiver_phone }}</el-descriptions-item>
        <el-descriptions-item label="收货地址">{{ currentTask.receiver_address || '-' }}</el-descriptions-item>
        <el-descriptions-item label="发货状态">
          <el-tag :type="currentTask.status === 'pending' ? 'warning' : 'success'">
            {{ currentTask.status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentTask.created_at }}</el-descriptions-item>
        <template v-if="currentTask.status === 'shipped'">
          <el-descriptions-item label="物流公司">{{ currentTask.logistics_company }}</el-descriptions-item>
          <el-descriptions-item label="运单号">{{ currentTask.tracking_no }}</el-descriptions-item>
          <el-descriptions-item label="发货时间">{{ currentTask.shipped_at }}</el-descriptions-item>
        </template>
      </el-descriptions>
    </el-dialog>

    <!-- 发货弹窗 -->
    <el-dialog v-model="shipVisible" title="确认发货" width="480px">
      <el-form ref="shipFormRef" :model="shipForm" :rules="shipRules" label-width="90px" v-if="currentTask">
        <el-form-item label="任务编号">
          <span>{{ currentTask.task_no }}</span>
        </el-form-item>
        <el-form-item label="商品名称">
          <span>{{ currentTask.product_name }}</span>
        </el-form-item>
        <el-form-item label="订单编号">
          <span>{{ currentTask.order_no }}</span>
        </el-form-item>
        <el-form-item label="收货人">
          <span>{{ currentTask.receiver_name }} ({{ currentTask.receiver_phone }})</span>
        </el-form-item>
        <el-form-item label="物流公司" prop="logistics_company">
          <el-select v-model="shipForm.logistics_company" placeholder="请选择物流公司" style="width: 100%">
            <el-option label="顺丰速运" value="顺丰速运" />
            <el-option label="中通快递" value="中通快递" />
            <el-option label="圆通速递" value="圆通速递" />
            <el-option label="韵达快递" value="韵达快递" />
            <el-option label="京东物流" value="京东物流" />
            <el-option label="邮政EMS" value="邮政EMS" />
            <el-option label="极兔速递" value="极兔速递" />
            <el-option label="申通快递" value="申通快递" />
          </el-select>
        </el-form-item>
        <el-form-item label="运单号" prop="tracking_no">
          <el-input v-model="shipForm.tracking_no" placeholder="请输入运单号" />
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { useMerchantShipmentStore } from '@/stores/merchant/shipment'
import type { ShipmentTask } from '@/types/merchant-self'

const shipmentStore = useMerchantShipmentStore()
const shipping = ref(false)
const statusFilter = ref('')
const keyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const detailVisible = ref(false)
const shipVisible = ref(false)
const currentTask = ref<ShipmentTask | null>(null)
const shipFormRef = ref<FormInstance>()

const shipForm = reactive({
  logistics_company: '',
  tracking_no: '',
})

const shipRules = {
  logistics_company: [{ required: true, message: '请选择物流公司', trigger: 'change' }],
  tracking_no: [{ required: true, message: '请输入运单号', trigger: 'blur' }],
}

function viewDetail(task: ShipmentTask) {
  currentTask.value = task
  detailVisible.value = true
}

function openShip(task: ShipmentTask) {
  currentTask.value = task
  shipForm.logistics_company = ''
  shipForm.tracking_no = ''
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
  } catch {
    ElMessage.error('发货失败')
  } finally {
    shipping.value = false
  }
}

async function loadData() {
  await shipmentStore.fetchList({
    page: currentPage.value,
    page_size: pageSize.value,
    status: statusFilter.value || undefined,
    keyword: keyword.value || undefined,
  })
}

onMounted(() => loadData())
</script>

<style scoped>
.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}
.pagination-bar {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
</style>
