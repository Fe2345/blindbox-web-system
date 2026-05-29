<template>
  <div class="page-container">
    <div class="page-header"><h2>商家审核</h2></div>

    <el-table :data="pendingList" stripe>
      <el-table-column prop="name" label="商家名称" width="150" />
      <el-table-column prop="contactName" label="联系人" width="100" />
      <el-table-column prop="phone" label="手机号" width="130" />
      <el-table-column prop="email" label="邮箱" width="180" />
      <el-table-column prop="license" label="营业执照" />
      <el-table-column label="申请时间" width="120">
        <template #default="{ row }">{{ row.createdAt }}</template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button type="success" size="small" @click="showReview(row, 'approve')">通过</el-button>
          <el-button type="danger" size="small" @click="showReview(row, 'reject')">驳回</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div v-if="!pendingList.length" class="empty-tip">暂无待审核商家</div>

    <el-dialog v-model="dialogVisible" :title="reviewAction === 'approve' ? '审核通过' : '审核驳回'" width="450px">
      <p style="margin-bottom: 12px">商家：{{ reviewTarget?.name }}</p>
      <el-input v-model="reviewNote" type="textarea" :rows="3" :placeholder="reviewAction === 'approve' ? '审核意见（选填）' : '请填写驳回原因'" />
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button :type="reviewAction === 'approve' ? 'success' : 'danger'" :loading="submitting" @click="handleReview">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useMerchantStore } from '@/stores/admin/merchant'
import { ElMessage } from 'element-plus'

const merchantStore = useMerchantStore()
const dialogVisible = ref(false)
const reviewAction = ref('')
const reviewTarget = ref<any>(null)
const reviewNote = ref('')
const submitting = ref(false)

const pendingList = computed(() => merchantStore.list.filter((m) => m.status === 'pending'))

function showReview(row: any, action: string) {
  reviewTarget.value = row
  reviewAction.value = action
  reviewNote.value = ''
  dialogVisible.value = true
}

async function handleReview() {
  if (reviewAction.value === 'reject' && !reviewNote.value.trim()) {
    ElMessage.warning('请填写驳回原因')
    return
  }
  submitting.value = true
  try {
    const res = await merchantStore.review(reviewTarget.value.id, reviewAction.value, reviewNote.value)
    if (res.code === 0) {
      ElMessage.success(reviewAction.value === 'approve' ? '已通过' : '已驳回')
      dialogVisible.value = false
    } else ElMessage.error(res.message)
  } catch { ElMessage.error('操作失败') } finally { submitting.value = false }
}

onMounted(() => merchantStore.fetchList())
</script>
