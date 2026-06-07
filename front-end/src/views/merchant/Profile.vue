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
          <el-tag :type="statusType">{{ info?.status_display }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="联系人">{{ info?.contact_name }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ info?.phone }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ info?.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="信用评分">
          <el-tag :type="(info?.credit_score ?? 0) >= 80 ? 'success' : (info?.credit_score ?? 0) >= 60 ? 'warning' : 'danger'">
            {{ info?.credit_score ?? 0 }} 分
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="营业执照">{{ info?.license || '-' }}</el-descriptions-item>
        <el-descriptions-item label="经营范围" :span="2">{{ info?.business_scope || '-' }}</el-descriptions-item>
        <el-descriptions-item label="供货说明" :span="2">{{ info?.supply_desc || '-' }}</el-descriptions-item>
        <el-descriptions-item label="入驻时间">{{ info?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="审核时间">{{ info?.reviewed_at || '待审核' }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card v-if="info?.status === 'rejected' && info?.review_note" style="margin-top: 16px">
      <template #header><span>审核意见</span></template>
      <el-alert :title="info.review_note" type="error" show-icon :closable="false" />
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
        <el-descriptions-item label="记录查询">
          <el-tag type="success" size="small">已开通</el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card v-if="info?.status === 'frozen'" style="margin-top: 16px">
      <template #header><span>账号状态</span></template>
      <el-alert title="您的商家账号已被冻结，请联系管理员解冻" type="warning" show-icon :closable="false" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import * as applicationApi from '@/api/merchant/application'
import type { MerchantInfo } from '@/types/merchant-self'

const info = ref<MerchantInfo | null>(null)

const statusType = computed(() => {
  const map: Record<string, string> = { pending: 'warning', approved: 'success', rejected: 'danger', frozen: 'info' }
  return map[info.value?.status || ''] || 'info'
})

async function loadInfo() {
  const res: any = await applicationApi.getMerchantInfo()
  if (res.code === 200) {
    info.value = res.data
  }
}

onMounted(() => loadInfo())
</script>
