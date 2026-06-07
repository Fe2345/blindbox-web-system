<template>
  <div class="login-page">
    <div class="bg-pattern"></div>
    <div class="login-container">
      <div class="left-panel">
        <div class="brand-content">
          <div class="brand-icon">
            <svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="adminGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#fff;stop-opacity:0.9" />
                  <stop offset="100%" style="stop-color:#fff;stop-opacity:0.6" />
                </linearGradient>
              </defs>
              <rect x="5" y="5" width="70" height="70" rx="18" fill="url(#adminGrad)" />
              <text x="40" y="50" text-anchor="middle" fill="#2e86de" font-size="28" font-weight="bold">管</text>
            </svg>
          </div>
          <h2>管理后台</h2>
          <p class="brand-desc">平台运营管理中心</p>
          <div class="features">
            <div class="feature-item"><el-icon><DataAnalysis /></el-icon><span>数据统计</span></div>
            <div class="feature-item"><el-icon><UserFilled /></el-icon><span>用户管理</span></div>
            <div class="feature-item"><el-icon><Checked /></el-icon><span>审核管理</span></div>
          </div>
        </div>
      </div>
      <div class="right-panel">
        <div class="form-header">
          <h2>管理员登录</h2>
          <p>登录管理后台，掌控平台运营</p>
        </div>
        <el-form ref="formRef" :model="form" :rules="rules" class="login-form">
          <el-form-item prop="username">
            <el-input v-model="form.username" placeholder="请输入管理员账号" size="large" prefix-icon="User" />
          </el-form-item>
          <el-form-item prop="password">
            <el-input v-model="form.password" type="password" placeholder="请输入密码" size="large" prefix-icon="Lock" show-password @keyup.enter="handleLogin" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="loading" size="large" class="login-btn" @click="handleLogin">登录</el-button>
          </el-form-item>
        </el-form>
        <div class="switch-links">
          <a href="/" class="switch-link"><el-icon><HomeFilled /></el-icon><span>返回首页</span></a>
          <a href="/merchant.html" class="switch-link"><el-icon><Shop /></el-icon><span>商户登录</span></a>
        </div>
        <div class="test-account">
          <el-divider>测试账号</el-divider>
          <p>用户名：<strong>admin</strong> / 密码：<strong>admin123</strong></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/admin/auth'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { DataAnalysis, UserFilled, Checked, User, Shop, HomeFilled } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()
const formRef = ref<FormInstance>()
const loading = ref(false)
const form = reactive({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入管理员账号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

async function handleLogin() {
  await formRef.value?.validate()
  loading.value = true
  try {
    const res = await authStore.login(form.username.trim(), form.password.trim())
    if (res.code === 0) {
      ElMessage.success('登录成功')
      router.push('/dashboard')
    } else {
      ElMessage.error(res.message)
    }
  } catch { ElMessage.error('登录失败') } finally { loading.value = false }
}
</script>

<style scoped>
.login-page { min-height: 100vh; background: linear-gradient(135deg, #0c2461 0%, #1e3799 50%, #2e86de 100%); display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; padding: 20px; }
.bg-pattern { position: absolute; inset: 0; background-image: radial-gradient(circle at 25% 25%, rgba(255,255,255,0.08) 0%, transparent 50%), radial-gradient(circle at 75% 75%, rgba(255,255,255,0.05) 0%, transparent 50%); }
.login-container { position: relative; z-index: 10; display: flex; border-radius: 24px; overflow: hidden; box-shadow: 0 40px 80px rgba(0,0,0,0.35); max-width: 900px; width: 100%; }
.left-panel { flex: 1; background: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.03) 100%); backdrop-filter: blur(20px); padding: 60px 40px; display: flex; align-items: center; justify-content: center; border-right: 1px solid rgba(255,255,255,0.1); }
.brand-content { text-align: center; color: #fff; }
.brand-icon { width: 80px; height: 80px; margin: 0 auto 20px; }
.brand-content h2 { font-size: 32px; font-weight: 800; margin: 0 0 8px; letter-spacing: 4px; }
.brand-desc { font-size: 16px; opacity: 0.8; margin: 0 0 40px; }
.features { display: flex; flex-direction: column; gap: 16px; }
.feature-item { display: flex; align-items: center; gap: 12px; padding: 14px 20px; background: rgba(255,255,255,0.1); border-radius: 12px; transition: all 0.3s; }
.feature-item:hover { background: rgba(255,255,255,0.18); transform: translateX(5px); }
.feature-item .el-icon { font-size: 22px; }
.right-panel { flex: 1; background: #fff; padding: 60px 40px; }
.form-header { margin-bottom: 40px; }
.form-header h2 { font-size: 28px; font-weight: 700; color: #1a1a2e; margin: 0 0 8px; }
.form-header p { font-size: 14px; color: #909399; margin: 0; }
.login-form { margin-bottom: 20px; }
.login-form :deep(.el-input__wrapper) { border-radius: 12px; padding: 8px 16px; }
.login-btn { width: 100%; border-radius: 12px; height: 48px; font-size: 16px; font-weight: 600; background: linear-gradient(135deg, #2e86de 0%, #1e3799 100%); border: none; }
.login-btn:hover { opacity: 0.9; transform: translateY(-2px); box-shadow: 0 8px 20px rgba(46,134,222,0.4); }
.switch-links { display: flex; justify-content: center; gap: 20px; margin-bottom: 24px; }
.switch-link { display: flex; align-items: center; gap: 4px; font-size: 13px; color: #909399; text-decoration: none; transition: all 0.3s; padding: 8px 12px; border-radius: 8px; }
.switch-link:hover { color: #2e86de; background: rgba(46,134,222,0.08); }
.test-account { text-align: center; }
.test-account p { font-size: 13px; color: #909399; margin: 0; }
.test-account strong { color: #2e86de; }
@media (max-width: 768px) { .login-container { flex-direction: column; } .left-panel { padding: 40px 20px; } .right-panel { padding: 40px 20px; } }
</style>
