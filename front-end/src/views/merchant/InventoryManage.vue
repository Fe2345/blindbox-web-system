<template>
  <div class="page-container">
    <div class="page-header">
      <h2>库存管理</h2>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-bar">
      <el-input v-model="keyword" placeholder="搜索商品名称" style="width: 200px" clearable @clear="loadData" @keyup.enter="loadData" />
      <el-select v-model="stockStatus" placeholder="库存状态" clearable style="width: 140px" @change="loadData">
        <el-option label="正常" value="normal" />
        <el-option label="库存不足" value="low" />
        <el-option label="已售罄" value="out" />
      </el-select>
      <el-button @click="loadData">查询</el-button>
    </div>

    <el-card>
      <el-table :data="inventoryStore.list" v-loading="inventoryStore.loading" stripe>
        <el-table-column label="商品图片" width="80">
          <template #default="{ row }">
            <el-image :src="row.product_image" style="width: 50px; height: 50px; border-radius: 4px" fit="cover" />
          </template>
        </el-table-column>
        <el-table-column prop="product_name" label="商品名称" min-width="140" />
        <el-table-column prop="product_category" label="分类" width="80" />
        <el-table-column label="稀有度" width="80">
          <template #default="{ row }">
            <span :style="{ color: rarityColor(row.product_rarity), fontWeight: 600 }">{{ row.product_rarity }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="current_stock" label="当前库存" width="100">
          <template #default="{ row }">
            <span :style="{ color: row.current_stock < 10 ? '#F56C6C' : '' }">{{ row.current_stock }}</span>
          </template>
        </el-table-column>
        <el-table-column label="库存状态" width="100">
          <template #default="{ row }">
            <el-tag :type="stockStatusType(row.current_stock)" size="small">{{ stockStatusLabel(row.current_stock) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="updated_at" label="更新时间" width="160" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openUpdate(row)">更新库存</el-button>
            <el-button link type="primary" size="small" @click="viewRecords(row)">库存记录</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-bar" v-if="inventoryStore.total > 0">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="inventoryStore.total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next"
          @current-change="loadData"
          @size-change="loadData"
        />
      </div>
    </el-card>

    <!-- 更新库存弹窗 -->
    <el-dialog v-model="updateVisible" title="更新库存" width="500px">
      <el-form label-width="100px" v-if="currentItem">
        <el-form-item label="商品名称">
          <span>{{ currentItem.product_name }}</span>
        </el-form-item>
        <el-form-item label="当前库存">
          <span>{{ currentItem.current_stock }}</span>
        </el-form-item>
        <el-form-item label="变动类型">
          <el-radio-group v-model="updateForm.change_type">
            <el-radio value="increase">入库</el-radio>
            <el-radio value="decrease">出库</el-radio>
            <el-radio value="modify">调整为</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item :label="updateForm.change_type === 'modify' ? '调整为' : '变动数量'">
          <el-input-number v-model="updateForm.quantity" :min="0" :max="99999" />
          <span v-if="updateForm.change_type !== 'modify'" style="margin-left: 8px; color: #909399">
            {{ updateForm.change_type === 'increase' ? '入库后库存: ' + (currentItem.current_stock + updateForm.quantity) : '出库后库存: ' + Math.max(0, currentItem.current_stock - updateForm.quantity) }}
          </span>
        </el-form-item>
        <el-form-item label="变动原因">
          <el-input v-model="updateForm.reason" placeholder="请输入变动原因（选填）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="updateVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleUpdate">确认更新</el-button>
      </template>
    </el-dialog>

    <!-- 库存记录弹窗 -->
    <el-dialog v-model="recordsVisible" title="库存变动记录" width="700px">
      <el-table :data="inventoryStore.records" stripe>
        <el-table-column prop="product_name" label="商品名称" min-width="120" />
        <el-table-column label="类型" width="80">
          <template #default="{ row }">
            <el-tag :type="recordTypeColor(row.type)" size="small">{{ row.type_display }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="变化" width="140">
          <template #default="{ row }">
            <span>{{ row.before_stock }}</span>
            <el-icon style="margin: 0 4px"><ArrowRight /></el-icon>
            <span :style="{ color: row.after_stock > row.before_stock ? '#67C23A' : row.after_stock < row.before_stock ? '#F56C6C' : '' }">{{ row.after_stock }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="reason" label="原因" min-width="100" />
        <el-table-column prop="created_at" label="时间" width="160" />
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowRight } from '@element-plus/icons-vue'
import { useMerchantInventoryStore } from '@/stores/merchant/inventory'
import type { InventoryItem } from '@/types/merchant-self'

const inventoryStore = useMerchantInventoryStore()
const keyword = ref('')
const stockStatus = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const submitting = ref(false)
const updateVisible = ref(false)
const recordsVisible = ref(false)
const currentItem = ref<InventoryItem | null>(null)

const updateForm = reactive({
  change_type: 'increase' as 'increase' | 'decrease' | 'modify',
  quantity: 0,
  reason: '',
})

function rarityColor(r: string) {
  const map: Record<string, string> = { N: '#909399', R: '#409EFF', SR: '#E6A23C', SSR: '#F56C6C' }
  return map[r] || '#909399'
}

function stockStatusLabel(stock: number) {
  if (stock === 0) return '已售罄'
  if (stock < 10) return '库存不足'
  return '正常'
}

function stockStatusType(stock: number) {
  if (stock === 0) return 'danger'
  if (stock < 10) return 'warning'
  return 'success'
}

function recordTypeColor(t: string) {
  const map: Record<string, string> = { increase: 'success', decrease: 'danger', modify: 'warning' }
  return map[t] || 'info'
}

function openUpdate(item: InventoryItem) {
  currentItem.value = item
  updateForm.change_type = 'increase'
  updateForm.quantity = 0
  updateForm.reason = ''
  updateVisible.value = true
}

async function handleUpdate() {
  if (!currentItem.value) return

  const actionLabel = updateForm.change_type === 'increase' ? '入库' : updateForm.change_type === 'decrease' ? '出库' : '调整'
  await ElMessageBox.confirm(
    `确认对「${currentItem.value.product_name}」执行${actionLabel}操作？`,
    '确认更新',
    { type: 'warning' }
  )

  submitting.value = true
  try {
    const res: any = await inventoryStore.updateStock(currentItem.value.id, {
      change_type: updateForm.change_type,
      quantity: updateForm.quantity,
      reason: updateForm.reason,
    })
    if (res.code === 200) {
      ElMessage.success('库存已更新')
      updateVisible.value = false
      loadData()
    } else {
      ElMessage.error(res.message)
    }
  } catch {
    ElMessage.error('更新失败')
  } finally {
    submitting.value = false
  }
}

async function viewRecords(item: InventoryItem) {
  await inventoryStore.fetchRecords({ product_id: item.product })
  recordsVisible.value = true
}

async function loadData() {
  await inventoryStore.fetchList({
    page: currentPage.value,
    page_size: pageSize.value,
    keyword: keyword.value || undefined,
    stock_status: stockStatus.value || undefined,
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
