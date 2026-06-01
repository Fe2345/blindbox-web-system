<template>
  <div class="page-container">
    <div class="page-header"><h2>异常处理</h2></div>
    <div class="filter-bar">
      <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width: 150px">
        <el-option label="待处理" value="open" /><el-option label="处理中" value="processing" /><el-option label="已解决" value="resolved" />
      </el-select>
    </div>
    <el-table :data="filteredExceptions" stripe>
      <el-table-column label="类型" width="100">
        <template #default="{ row }"><el-tag :type="row.type === 'stock' ? 'danger' : row.type === 'appeal' ? 'warning' : 'info'" size="small">{{ exceptionTypeLabel(row.type) }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="description" label="异常描述" />
      <el-table-column prop="relatedId" label="关联ID" width="120" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }"><el-tag :type="row.status === 'open' ? 'danger' : row.status === 'processing' ? 'warning' : 'success'" size="small">{{ row.status === 'open' ? '待处理' : row.status === 'processing' ? '处理中' : '已解决' }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="result" label="处理结果" />
      <el-table-column label="时间" width="120"><template #default="{ row }">{{ row.createdAt }}</template></el-table-column>
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button v-if="row.status !== 'resolved'" type="primary" size="small" @click="showResolve(row)">处理</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="处理异常" width="420px">
      <p style="margin-bottom: 12px">异常：{{ target?.description }}</p>
      <el-input v-model="resultText" type="textarea" :rows="3" placeholder="处理结果说明" />
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleResolve">确认处理</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useLogStore } from '@/stores/admin/log'
import { ElMessage } from 'element-plus'
import { exceptionTypeLabel } from '@/utils/format'

const logStore = useLogStore()
const filterStatus = ref('')
const dialogVisible = ref(false)
const target = ref<any>(null)
const resultText = ref('')
const submitting = ref(false)

const filteredExceptions = computed(() => {
  if (!filterStatus.value) return logStore.exceptions
  return logStore.exceptions.filter((e) => e.status === filterStatus.value)
})

function showResolve(row: any) { target.value = row; resultText.value = ''; dialogVisible.value = true }

async function handleResolve() {
  if (!resultText.value.trim()) { ElMessage.warning('请填写处理结果'); return }
  submitting.value = true
  try {
    const res = await logStore.resolveException(target.value.id, resultText.value)
    if (res.code === 0) { ElMessage.success('已处理'); dialogVisible.value = false }
    else ElMessage.error(res.message)
  } finally { submitting.value = false }
}

onMounted(() => logStore.fetchExceptions())
</script>
