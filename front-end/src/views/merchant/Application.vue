<template>
  <div class="page-container">
    <div class="page-header">
      <h2>商家入驻申请</h2>
    </div>

    <el-card v-if="existingApp && existingApp.status !== 'rejected'">
      <template #header><span>审核状态</span></template>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="商家名称">{{ existingApp.merchantName }}</el-descriptions-item>
        <el-descriptions-item label="审核状态">
          <el-tag :type="statusType(existingApp.status)">{{ statusLabel(existingApp.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="联系人">{{ existingApp.contactName }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ existingApp.phone }}</el-descriptions-item>
        <el-descriptions-item label="经营范围" :span="2">{{ existingApp.businessScope }}</el-descriptions-item>
        <el-descriptions-item label="供货说明" :span="2">{{ existingApp.supplyDescription }}</el-descriptions-item>
        <el-descriptions-item label="提交时间">{{ existingApp.createdAt }}</el-descriptions-item>
        <el-descriptions-item label="审核时间">{{ existingApp.reviewedAt || '待审核' }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card v-if="existingApp?.status === 'rejected'" style="margin-top: 16px">
      <template #header><span>驳回原因</span></template>
      <el-alert :title="existingApp.reviewNote" type="error" show-icon :closable="false" />
      <el-button type="primary" style="margin-top: 16px" @click="showForm = true">重新提交申请</el-button>
    </el-card>

    <el-card v-if="!existingApp || showForm" style="margin-top: 16px">
      <template #header><span>填写入驻信息</span></template>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" style="max-width: 600px">
        <el-form-item label="商家名称" prop="merchantName">
          <el-input v-model="form.merchantName" placeholder="请输入商家名称" />
        </el-form-item>
        <el-form-item label="联系人" prop="contactName">
          <el-input v-model="form.contactName" placeholder="请输入联系人姓名" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="经营范围" prop="businessScope">
          <el-input v-model="form.businessScope" type="textarea" :rows="3" placeholder="请描述经营范围" />
        </el-form-item>
        <el-form-item label="供货说明" prop="supplyDescription">
          <el-input v-model="form.supplyDescription" type="textarea" :rows="3" placeholder="请描述供货能力和产品特点" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">提交申请</el-button>
          <el-button @click="resetForm">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import * as applicationApi from '@/api/merchant/application'
import type { MerchantApplication } from '@/types/merchant-self'

const existingApp = ref<MerchantApplication | null>(null)
const showForm = ref(false)
const loading = ref(false)
const formRef = ref<FormInstance>()

const form = reactive({
  merchantName: '',
  contactName: '',
  phone: '',
  businessScope: '',
  supplyDescription: '',
})

const rules = {
  merchantName: [{ required: true, message: '请输入商家名称', trigger: 'blur' }],
  contactName: [{ required: true, message: '请输入联系人', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }, { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }],
  businessScope: [{ required: true, message: '请输入经营范围', trigger: 'blur' }],
  supplyDescription: [{ required: true, message: '请输入供货说明', trigger: 'blur' }],
}

function statusLabel(s: string) {
  const map: Record<string, string> = { pending: '待审核', approved: '已通过', rejected: '已驳回' }
  return map[s] || s
}

function statusType(s: string) {
  const map: Record<string, string> = { pending: 'warning', approved: 'success', rejected: 'danger' }
  return map[s] || 'info'
}

async function loadApplication() {
  const res: any = await applicationApi.getApplicationStatus()
  if (res.code === 0 && res.data) existingApp.value = res.data
}

async function handleSubmit() {
  await formRef.value?.validate()
  loading.value = true
  try {
    const res: any = await applicationApi.submitApplication(form)
    if (res.code === 0) {
      ElMessage.success('申请已提交，等待审核')
      showForm.value = false
      loadApplication()
    } else {
      ElMessage.error(res.message)
    }
  } catch {
    ElMessage.error('提交失败')
  } finally {
    loading.value = false
  }
}

function resetForm() {
  showForm.value = false
  formRef.value?.resetFields()
}

onMounted(() => loadApplication())
</script>
