<template>
  <div class="page-container">
    <div class="page-header"><h2>商家管理</h2></div>

    <div class="filter-bar">
      <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width: 150px">
        <el-option label="已通过" value="approved" />
        <el-option label="已驳回" value="rejected" />
        <el-option label="已冻结" value="frozen" />
      </el-select>
    </div>

    <el-table :data="filteredList" stripe>
      <el-table-column prop="name" label="商家名称" width="150" />
      <el-table-column prop="contactName" label="联系人" width="100" />
      <el-table-column prop="phone" label="手机号" width="130" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="merchantStatusType(row.status) as any" size="small">{{ merchantStatusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="信誉分" width="100">
        <template #default="{ row }">{{ row.creditScore }}</template>
      </el-table-column>
      <el-table-column label="供货数" width="80">
        <template #default="{ row }">{{ row.supplyCount }}</template>
      </el-table-column>
      <el-table-column label="违规数" width="80">
        <template #default="{ row }">
          <span :style="{ color: row.violationCount > 0 ? '#f56c6c' : '#303133' }">{{ row.violationCount }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="reviewNote" label="审核意见" />
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-popconfirm v-if="row.status === 'approved'" title="确认冻结该商家？" @confirm="handleFreeze(row.id)">
            <template #reference><el-button type="danger" size="small">冻结</el-button></template>
          </el-popconfirm>
          <el-button v-if="row.status === 'frozen'" type="success" size="small" @click="handleUnfreeze(row.id)">解冻</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useMerchantStore } from '@/stores/admin/merchant'
import { ElMessage } from 'element-plus'
import { merchantStatusLabel, merchantStatusType } from '@/utils/format'

const merchantStore = useMerchantStore()
const filterStatus = ref('')

const filteredList = computed(() => {
  if (!filterStatus.value) return merchantStore.list
  return merchantStore.list.filter((m) => m.status === filterStatus.value)
})

async function handleFreeze(id: string) {
  const res = await merchantStore.updateStatus(id, 'frozen')
  if (res.code === 0) ElMessage.success('已冻结')
}
async function handleUnfreeze(id: string) {
  const res = await merchantStore.updateStatus(id, 'approved')
  if (res.code === 0) ElMessage.success('已解冻')
}

onMounted(() => merchantStore.fetchList())
</script>
