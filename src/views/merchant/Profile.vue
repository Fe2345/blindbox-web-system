<template>
  <div class="page-container">
    <div class="page-header">
      <h2>商家资料</h2>
    </div>

    <el-card>
      <template #header><span>基础信息</span></template>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="商家名称">{{ info?.name }}</el-descriptions-item>
        <el-descriptions-item label="审核状态">
          <el-tag :type="statusType">{{ statusLabel }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="联系人">{{ info?.contactName }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ info?.phone }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ info?.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="信用评分">{{ info?.creditScore || 0 }}</el-descriptions-item>
        <el-descriptions-item label="供货数量">{{ info?.supplyCount || 0 }}</el-descriptions-item>
        <el-descriptions-item label="违规次数">{{ info?.violationCount || 0 }}</el-descriptions-item>
        <el-descriptions-item label="经营范围" :span="2">{{ info?.businessScope || '-' }}</el-descriptions-item>
        <el-descriptions-item label="供货说明" :span="2">{{ info?.supplyDescription || '-' }}</el-descriptions-item>
        <el-descriptions-item label="入驻时间">{{ info?.createdAt }}</el-descriptions-item>
        <el-descriptions-item label="审核时间">{{ info?.reviewedAt || '待审核' }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card v-if="info?.status === 'rejected' && info?.reviewNote" style="margin-top: 16px">
      <template #header><span>审核意见</span></template>
      <el-alert :title="info.reviewNote" type="error" show-icon :closable="false" />
    </el-card>

    <el-card v-if="info?.status === 'approved'" style="margin-top: 16px">
      <template #header><span>供货权限</span></template>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="商品提交">
          <el-tag type="success" size="small">已开通</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="库存管理">
          <el-tag type="success" size="small">已开通</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="发货处理">
          <el-tag type="success" size="small">已开通</el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useMerchantAuthStore } from '@/stores/merchant/auth'

const authStore = useMerchantAuthStore()
const info = computed(() => authStore.merchantInfo)

const statusLabel = computed(() => {
  const map: Record<string, string> = { pending: '待审核', approved: '已通过', rejected: '已驳回', frozen: '已冻结' }
  return map[info.value?.status] || ''
})

const statusType = computed(() => {
  const map: Record<string, string> = { pending: 'warning', approved: 'success', rejected: 'danger', frozen: 'info' }
  return map[info.value?.status] || 'info'
})

onMounted(() => authStore.fetchInfo())
</script>
