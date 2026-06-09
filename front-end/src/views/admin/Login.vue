<template>
  <div class="login-page">
    <div class="login-card">
      <h2>管理后台登录</h2>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="0" size="large">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="管理员账号" prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" style="width: 100%" @click="handleLogin">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/admin/auth'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

onMounted(() => {
  if (route.query.msg === 'merchant') {
    ElMessage.warning('请前往商家中心登录')
  } else if (route.query.msg === 'user') {
    ElMessage.warning('请前往用户端登录')
  }
})

const form = reactive({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

async function handleLogin() {
  await formRef.value?.validate()
  loading.value = true
  try {
    const res = await authStore.login(form.username, form.password, 'admin')
    if (res.code === 200) {
      const role = res.data.user?.role
      if (role === 'user') {
        ElMessage.error('该账号为普通用户，请前往用户端登录')
        return
      }
      if (role === 'merchant') {
        ElMessage.error('该账号为商家账号，请前往商家中心登录')
        return
      }
      if (role && role !== 'admin') {
        ElMessage.error('该账号无权访问管理后台')
        return
      }
      ElMessage.success('登录成功')
      router.push('/')
    } else {
      ElMessage.error(res.message)
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
  background: #001529;
}
.login-card {
  background: #fff;
  border-radius: 12px;
  padding: 40px;
  width: 400px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}
.login-card h2 { text-align: center; margin-bottom: 30px; color: #303133; font-size: 22px; }
</style>
