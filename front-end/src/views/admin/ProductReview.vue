<template>
  <div class="page-container">
    <div class="page-header"><h2>商品审核</h2></div>
    <el-table :data="pendingList" stripe>
      <el-table-column label="商品图片" width="80">
        <template #default="{ row }"><img :src="row.image" style="width: 50px; height: 50px; border-radius: 4px; object-fit: cover" /></template>
      </el-table-column>
      <el-table-column prop="name" label="商品名称" width="160" />
      <el-table-column prop="category" label="分类" width="100" />
      <el-table-column label="稀有度" width="80">
        <template #default="{ row }"><el-tag :style="{ color: rarityColor(row.rarity), borderColor: rarityColor(row.rarity) }" size="small" effect="plain">{{ rarityLabel(row.rarity) }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="merchantName" label="商家" width="120" />
      <el-table-column label="库存" width="80"><template #default="{ row }">{{ row.stock }}</template></el-table-column>
      <el-table-column label="估值积分" width="100"><template #default="{ row }">{{ row.estimatedPoints }}</template></el-table-column>
      <el-table-column prop="description" label="描述" />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button type="success" size="small" @click="showReview(row, 'approve')">通过</el-button>
          <el-button type="danger" size="small" @click="showReview(row, 'reject')">驳回</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div v-if="!pendingList.length" class="empty-tip">暂无待审核商品</div>

    <el-dialog v-model="dialogVisible" :title="action === 'approve' ? '审核通过' : '审核驳回'" width="420px">
      <p style="margin-bottom: 12px">商品：{{ target?.name }}</p>
      <el-input v-model="note" type="textarea" :rows="3" placeholder="审核意见" />
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button :type="action === 'approve' ? 'success' : 'danger'" :loading="submitting" @click="handleReview">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useProductStore } from '@/stores/admin/product'
import { ElMessage } from 'element-plus'
import { rarityLabel, rarityColor } from '@/utils/format'

const productStore = useProductStore()
const dialogVisible = ref(false)
const action = ref('')
const target = ref<any>(null)
const note = ref('')
const submitting = ref(false)

const pendingList = computed(() => productStore.list.filter((p) => p.status === 'pending'))

function showReview(row: any, a: string) { target.value = row; action.value = a; note.value = ''; dialogVisible.value = true }

async function handleReview() {
  submitting.value = true
  try {
    const res = await productStore.review(target.value.id, action.value, note.value)
    if (res.code === 0) { ElMessage.success('审核完成'); dialogVisible.value = false }
    else ElMessage.error(res.message)
  } finally { submitting.value = false }
}

onMounted(() => productStore.fetchList())
</script>
