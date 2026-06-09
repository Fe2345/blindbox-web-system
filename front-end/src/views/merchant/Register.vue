<template>
  <div class="login-page">
    <div class="login-card">
      <h2>商家注册</h2>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="0" size="large">
        <el-form-item prop="username">
          <el-input v-model.trim="form.username" placeholder="登录账号" prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="merchantName">
          <el-input v-model.trim="form.merchantName" placeholder="商家名称" prefix-icon="Shop" />
        </el-form-item>
        <el-form-item prop="contactName">
          <el-input v-model.trim="form.contactName" placeholder="联系人姓名" prefix-icon="UserFilled" />
        </el-form-item>
        <el-form-item prop="phone">
          <el-input v-model.trim="form.phone" placeholder="手机号码" prefix-icon="Phone" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input v-model="form.confirmPassword" type="password" placeholder="确认密码" prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" class="submit-btn" @click="handleRegister">注册</el-button>
        </el-form-item>
      </el-form>
      <div class="login-tip">
        已有账号？<router-link to="/login">去登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { merchantRegister } from '@/api/merchant/auth'

const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  username: '',
  merchantName: '',
  contactName: '',
  phone: '',
  password: '',
  confirmPassword: '',
})

const validateConfirmPassword = (_rule: unknown, value: string, callback: (error?: Error) => void) => {
  if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
    return
  }
  callback()
}

const rules: FormRules = {
  username: [
    { required: true, message: '请输入登录账号', trigger: 'blur' },
    { min: 3, max: 150, message: '账号长度为 3-150 个字符', trigger: 'blur' },
  ],
  merchantName: [{ required: true, message: '请输入商家名称', trigger: 'blur' }],
  contactName: [{ required: true, message: '请输入联系人姓名', trigger: 'blur' }],
  phone: [
    { required: true, message: '请输入手机号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号码格式不正确', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 128, message: '密码长度为 6-128 个字符', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: ['blur', 'change'] },
  ],
}

async function handleRegister() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    const res: any = await merchantRegister({
      username: form.username,
      merchantName: form.merchantName,
      contactName: form.contactName,
      phone: form.phone,
      password: form.password,
    })
    if (res.code === 200) {
      ElMessage.success('注册成功，请登录后完善入驻申请')
      router.push('/login')
    } else {
      ElMessage.error(res.message || '注册失败')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0d2137;
  padding: 24px;
}

.login-card {
  width: min(420px, 100%);
  background: #fff;
  border-radius: 8px;
  padding: 36px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.login-card h2 {
  text-align: center;
  margin: 0 0 28px;
  color: #303133;
  font-size: 22px;
  font-weight: 600;
}

.submit-btn {
  width: 100%;
}

.login-tip {
  text-align: center;
  margin-top: 12px;
  color: #909399;
  font-size: 13px;
}

.login-tip a {
  color: #409eff;
  text-decoration: none;
}
</style>
