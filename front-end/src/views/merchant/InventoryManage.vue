<template>
  <div class="page-container">
    <div class="page-header">
      <h2>库存管理</h2>
    </div>

    <el-card>
      <el-table :data="inventoryStore.list" v-loading="loading" stripe>
        <el-table-column label="商品图片" width="80">
          <template #default="{ row }">
            <el-image :src="row.productImage" style="width: 50px; height: 50px; border-radius: 4px" fit="cover" />
          </template>
        </el-table-column>
        <el-table-column prop="productName" label="商品名称" min-width="160" />
        <el-table-column prop="currentStock" label="当前库存" width="100" />
        <el-table-column label="库存状态" width="100">
          <template #default="{ row }">
            <el-tag :type="stockStatusType(row.stockStatus)" size="small">{{ stockStatusLabel(row.stockStatus) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openUpdate(row)">更新库存</el-button>
            <el-button link type="primary" size="small" @click="viewRecords(row)">库存记录</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="updateVisible" title="更新库存" width="400px">
      <el-form label-width="80px" v-if="currentItem">
        <el-form-item label="商品名称">
          <span>{{ currentItem.productName }}</span>
        </el-form-item>
        <el-form-item label="当前库存">
          <span>{{ currentItem.currentStock }}</span>
        </el-form-item>
        <el-form-item label="新库存">
          <el-input-number v-model="newStock" :min="0" :max="99999" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="updateVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleUpdate">确认更新</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="recordsVisible" title="库存记录" width="700px">
      <el-table :data="inventoryStore.records" stripe>
        <el-table-column prop="productName" label="商品名称" min-width="120" />
        <el-table-column label="类型" width="80">
          <template #default="{ row }">
            <el-tag :type="recordTypeColor(row.type)" size="small">{{ recordTypeLabel(row.type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="变化" width="140">
          <template #default="{ row }">
            {{ row.beforeStock }} → {{ row.afterStock }}
          </template>
        </el-table-column>
        <el-table-column prop="reason" label="原因" min-width="100" />
        <el-table-column prop="createdAt" label="时间" width="160" />
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useMerchantInventoryStore } from '@/stores/merchant/inventory'
import type { InventoryItem } from '@/types/merchant-self'

const inventoryStore = useMerchantInventoryStore()
const loading = ref(false)
const submitting = ref(false)
const updateVisible = ref(false)
const recordsVisible = ref(false)
const currentItem = ref<InventoryItem | null>(null)
const newStock = ref(0)

function stockStatusLabel(s: string) {
  const map: Record<string, string> = { normal: '正常', low: '库存不足', empty: '库存为零' }
  return map[s] || s
}

function stockStatusType(s: string) {
  const map: Record<string, string> = { normal: 'success', low: 'warning', empty: 'danger' }
  return map[s] || 'info'
}

function recordTypeLabel(t: string) {
  const map: Record<string, string> = { increase: '增加', decrease: '减少', modify: '修改' }
  return map[t] || t
}

function recordTypeColor(t: string) {
  const map: Record<string, string> = { increase: 'success', decrease: 'danger', modify: 'warning' }
  return map[t] || 'info'
}

function openUpdate(item: InventoryItem) {
  currentItem.value = item
  newStock.value = item.currentStock
  updateVisible.value = true
}

async function handleUpdate() {
  if (!currentItem.value) return
  await ElMessageBox.confirm(`确认将「${currentItem.value.productName}」库存更新为 ${newStock.value}？`, '确认更新', { type: 'warning' })
  submitting.value = true
  try {
    const res: any = await inventoryStore.updateStock(currentItem.value.productId, newStock.value)
    if (res.code === 0) {
      ElMessage.success('库存已更新')
      updateVisible.value = false
      inventoryStore.fetchList()
    } else {
      ElMessage.error(res.message)
    }
  } finally {
    submitting.value = false
  }
}

async function viewRecords(item: InventoryItem) {
  await inventoryStore.fetchRecords(item.productId)
  recordsVisible.value = true
}

onMounted(() => {
  loading.value = true
  inventoryStore.fetchList().finally(() => { loading.value = false })
})
</script>
