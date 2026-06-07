<template>
  <div class="page-container">
    <div class="page-header">
      <h2>商家入驻申请</h2>
    </div>

    <!-- 已有申请状态 -->
    <el-card v-if="existingApp && existingApp.status !== 'rejected'">
      <template #header><span>审核状态</span></template>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="商家名称">{{ existingApp.name }}</el-descriptions-item>
        <el-descriptions-item label="审核状态">
          <el-tag :type="statusType(existingApp.status)">{{ existingApp.status_display }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="联系人">{{ existingApp.contact_name }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ existingApp.phone }}</el-descriptions-item>
        <el-descriptions-item label="联系邮箱">{{ existingApp.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="营业执照">{{ existingApp.license || '-' }}</el-descriptions-item>
        <el-descriptions-item label="经营范围" :span="2">{{ existingApp.business_scope || '-' }}</el-descriptions-item>
        <el-descriptions-item label="供货说明" :span="2">{{ existingApp.supply_desc || '-' }}</el-descriptions-item>
        <el-descriptions-item label="提交时间">{{ existingApp.created_at }}</el-descriptions-item>
        <el-descriptions-item label="审核时间">{{ existingApp.reviewed_at || '待审核' }}</el-descriptions-item>
        <el-descriptions-item label="信用评分">{{ existingApp.credit_score }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 驳回原因 -->
    <el-card v-if="existingApp?.status === 'rejected'" style="margin-top: 16px">
      <template #header><span>驳回原因</span></template>
      <el-alert :title="existingApp.review_note || '未通过审核'" type="error" show-icon :closable="false" />
      <el-button type="primary" style="margin-top: 16px" @click="showForm = true">重新提交申请</el-button>
    </el-card>

    <!-- 申请表单 -->
    <el-card v-if="!existingApp || showForm" style="margin-top: 16px">
      <template #header><span>填写入驻信息</span></template>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" style="max-width: 600px">
        <el-form-item label="商家名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入商家名称" />
        </el-form-item>
        <el-form-item label="联系人" prop="contact_name">
          <el-input v-model="form.contact_name" placeholder="请输入联系人姓名" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="联系邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入联系邮箱（选填）" />
        </el-form-item>
        <el-form-item label="营业执照" prop="license">
          <el-input v-model="form.license" placeholder="请输入营业执照编号（选填）" />
        </el-form-item>
        <el-form-item label="经营范围" prop="business_scope">
          <el-input v-model="form.business_scope" type="textarea" :rows="3" placeholder="请描述经营范围" />
        </el-form-item>
        <el-form-item label="供货说明" prop="supply_desc">
          <el-input v-model="form.supply_desc" type="textarea" :rows="3" placeholder="请描述供货能力和产品特点" />
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
import type { MerchantInfo } from '@/types/merchant-self'

const existingApp = ref<MerchantInfo | null>(null)
const showForm = ref(false)
const loading = ref(false)
const formRef = ref<FormInstance>()

const form = reactive({
  name: '',
  contact_name: '',
  phone: '',
  email: '',
  license: '',
  business_scope: '',
  supply_desc: '',
})

const rules = {
  name: [{ required: true, message: '请输入商家名称', trigger: 'blur' }],
  contact_name: [{ required: true, message: '请输入联系人', trigger: 'blur' }],
  phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' },
  ],
  business_scope: [{ required: true, message: '请输入经营范围', trigger: 'blur' }],
}

function statusType(status: string) {
  const map: Record<string, string> = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger',
    frozen: 'info',
  }
  return map[status] || 'info'
}

async function loadApplication() {
  const res: any = await applicationApi.getApplicationStatus()
  if (res.code === 200 && res.data) {
    existingApp.value = res.data
  }
}

async function handleSubmit() {
  await formRef.value?.validate()
  loading.value = true
  try {
    const res: any = await applicationApi.submitApplication(form)
    if (res.code === 200) {
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
