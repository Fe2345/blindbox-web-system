<template>
  <div class="page-container">
    <div class="page-header"><h2>换物管理</h2></div>
    <div class="filter-bar">
      <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width: 150px">
        <el-option label="锁定中" value="locked" /><el-option label="已完成" value="completed" /><el-option label="异常" value="exception" />
      </el-select>
    </div>
    <el-table :data="filteredExchanges" stripe>
      <el-table-column prop="publisherName" label="发布方" width="120" />
      <el-table-column prop="publisherAssetName" label="发布方商品" width="160" />
      <el-table-column prop="applicantName" label="申请方" width="120" />
      <el-table-column prop="applicantAssetName" label="申请方商品" width="160" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }"><el-tag :type="exchangeStatusType(row.status) as any" size="small">{{ exchangeStatusLabel(row.status) }}</el-tag></template>
      </el-table-column>
      <el-table-column label="时间" width="120"><template #default="{ row }">{{ row.createdAt }}</template></el-table-column>
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button v-if="row.status === 'exception'" type="warning" size="small" @click="showResolve(row)">处理</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="处理换物异常" width="420px">
      <p style="margin-bottom: 12px">发布方：{{ target?.publisherName }} / 申请方：{{ target?.applicantName }}</p>
      <el-input v-model="result" type="textarea" :rows="3" placeholder="处理说明" />
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleResolve">确认处理</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useExchangeStore } from '@/stores/admin/exchange'
import { ElMessage } from 'element-plus'
import { exchangeStatusLabel } from '@/utils/format'

const exchangeStore = useExchangeStore()
const filterStatus = ref('')
const dialogVisible = ref(false)
const target = ref<any>(null)
const result = ref('')

function exchangeStatusType(status: string) {
  const map: Record<string, string> = { locked: 'warning', completed: 'success', exception: 'danger' }
  return map[status] || 'info'
}

const filteredExchanges = computed(() => {
  if (!filterStatus.value) return exchangeStore.list
  return exchangeStore.list.filter((e) => e.status === filterStatus.value)
})

function showResolve(row: any) { target.value = row; result.value = ''; dialogVisible.value = true }

async function handleResolve() {
  const res = await exchangeStore.resolve(target.value.id, 'resolve', result.value)
  if (res.code === 0) { ElMessage.success('已处理'); dialogVisible.value = false }
  else ElMessage.error(res.message)
}

onMounted(() => exchangeStore.fetchList())
</script>
