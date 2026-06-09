<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-tabs">
        <span class="tab active">用户登录</span>
        <a class="tab" href="/merchant.html">商家登录</a>
        <a class="tab" href="/admin.html">管理员登录</a>
      </div>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="0" size="large">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" prefix-icon="Lock" show-password @keyup.enter="handleLogin" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" style="width: 100%" @click="handleLogin">登录</el-button>
        </el-form-item>
      </el-form>
      <div class="login-footer">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

onMounted(() => {
  if (route.query.msg === 'admin') {
    ElMessage.warning('请前往管理后台登录')
  } else if (route.query.msg === 'merchant') {
    ElMessage.warning('请前往商家中心登录')
  }
})

const form = reactive({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }, { min: 6, message: '密码至少6位', trigger: 'blur' }],
}

async function handleLogin() {
  await formRef.value?.validate()
  loading.value = true
  try {
    const res = await userStore.login(form.username, form.password, 'user')
    if (res.code === 200) {
      const role = res.data.user?.role
      if (role === 'admin') {
        ElMessage.error('该账号为管理员账号，请前往管理后台登录')
        return
      }
      if (role === 'merchant') {
        ElMessage.error('该账号为商家账号，请前往商家中心登录')
        return
      }
      if (role && role !== 'user') {
        ElMessage.error('该账号无权访问用户端')
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  background: #fff;
  border-radius: 12px;
  padding: 40px;
  width: 400px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

.login-tabs {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 30px;
}

.login-tabs .tab {
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 14px;
  color: #606266;
  background: #f4f4f5;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s;
}

.login-tabs .tab:hover {
  color: #409eff;
  background: #ecf5ff;
}

.login-tabs .tab.active {
  color: #fff;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-weight: 600;
}

.login-footer {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
  color: #909399;
}

.login-footer a {
  color: #409eff;
  text-decoration: none;
}
</style>
