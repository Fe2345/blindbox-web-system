<template>
  <div class="login-page">
    <div class="bg-pattern"></div>
    <div class="login-container">
      <div class="left-panel">
        <div class="brand-content">
          <div class="brand-icon">
            <svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="merchantGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#fff;stop-opacity:0.9" />
                  <stop offset="100%" style="stop-color:#fff;stop-opacity:0.6" />
                </linearGradient>
              </defs>
              <rect x="5" y="5" width="70" height="70" rx="18" fill="url(#merchantGrad)" />
              <text x="40" y="50" text-anchor="middle" fill="#f0932b" font-size="28" font-weight="bold">商</text>
            </svg>
          </div>
          <h2>商家中心</h2>
          <p class="brand-desc">高效管理您的店铺</p>
          <div class="features">
            <div class="feature-item"><el-icon><Goods /></el-icon><span>商品管理</span></div>
            <div class="feature-item"><el-icon><Box /></el-icon><span>库存管理</span></div>
            <div class="feature-item"><el-icon><Van /></el-icon><span>发货管理</span></div>
          </div>
        </div>
      </div>
      <div class="right-panel">
        <div class="form-header">
          <h2>商家登录</h2>
          <p>登录商家后台，管理您的店铺</p>
        </div>
        <el-form ref="formRef" :model="form" :rules="rules" class="login-form">
          <el-form-item prop="username">
            <el-input v-model="form.username" placeholder="请输入商家账号" size="large" prefix-icon="User" />
          </el-form-item>
          <el-form-item prop="password">
            <el-input v-model="form.password" type="password" placeholder="请输入密码" size="large" prefix-icon="Lock" show-password @keyup.enter="handleLogin" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="loading" size="large" class="login-btn" @click="handleLogin">登录</el-button>
          </el-form-item>
        </el-form>
        <div class="switch-links">
          <a href="/" class="switch-link" @click.prevent="goTo('/')"><el-icon><HomeFilled /></el-icon><span>返回首页</span></a>
          <a href="/admin.html" class="switch-link"><el-icon><Setting /></el-icon><span>管理登录</span></a>
        </div>
        <div class="test-account">
          <el-divider>测试账号</el-divider>
          <p>用户名：<strong>merchant</strong> / 密码：<strong>merchant123</strong></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useMerchantAuthStore } from '@/stores/merchant/auth'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { Goods, Box, Van, User, Setting, HomeFilled } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useMerchantAuthStore()
const formRef = ref<FormInstance>()
const loading = ref(false)
const form = reactive({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入商家账号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

function goTo(path: string) {
  window.location.href = path
}

async function handleLogin() {
  await formRef.value?.validate()
  loading.value = true
  try {
    const username = form.username.trim()
    const password = form.password.trim()
    const res = await authStore.login(username, password)
    if (res.code === 200) {
      ElMessage.success('登录成功')
      router.push('/dashboard')
    } else {
      ElMessage.error(res.message || '登录失败')
    }
  } catch { ElMessage.error('登录失败，请检查网络连接') } finally { loading.value = false }
}
</script>

<style scoped>
.login-page { min-height: 100vh; background: linear-gradient(135deg, #f0932b 0%, #f57c00 50%, #ff9800 100%); display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; padding: 20px; }
.bg-pattern { position: absolute; inset: 0; background-image: radial-gradient(circle at 25% 25%, rgba(255,255,255,0.12) 0%, transparent 50%), radial-gradient(circle at 75% 75%, rgba(255,255,255,0.08) 0%, transparent 50%); }
.login-container { position: relative; z-index: 10; display: flex; border-radius: 24px; overflow: hidden; box-shadow: 0 40px 80px rgba(0,0,0,0.25); max-width: 900px; width: 100%; }
.left-panel { flex: 1; background: linear-gradient(135deg, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0.05) 100%); backdrop-filter: blur(20px); padding: 60px 40px; display: flex; align-items: center; justify-content: center; border-right: 1px solid rgba(255,255,255,0.15); }
.brand-content { text-align: center; color: #fff; }
.brand-icon { width: 80px; height: 80px; margin: 0 auto 20px; }
.brand-content h2 { font-size: 32px; font-weight: 800; margin: 0 0 8px; letter-spacing: 4px; }
.brand-desc { font-size: 16px; opacity: 0.85; margin: 0 0 40px; }
.features { display: flex; flex-direction: column; gap: 16px; }
.feature-item { display: flex; align-items: center; gap: 12px; padding: 14px 20px; background: rgba(255,255,255,0.12); border-radius: 12px; transition: all 0.3s; }
.feature-item:hover { background: rgba(255,255,255,0.22); transform: translateX(5px); }
.feature-item .el-icon { font-size: 22px; }
.right-panel { flex: 1; background: #fff; padding: 60px 40px; }
.form-header { margin-bottom: 40px; }
.form-header h2 { font-size: 28px; font-weight: 700; color: #1a1a2e; margin: 0 0 8px; }
.form-header p { font-size: 14px; color: #909399; margin: 0; }
.login-form { margin-bottom: 20px; }
.login-form :deep(.el-input__wrapper) { border-radius: 12px; padding: 8px 16px; }
.login-btn { width: 100%; border-radius: 12px; height: 48px; font-size: 16px; font-weight: 600; background: linear-gradient(135deg, #f0932b 0%, #f57c00 100%); border: none; }
.login-btn:hover { opacity: 0.9; transform: translateY(-2px); box-shadow: 0 8px 20px rgba(240,147,43,0.4); }
.switch-links { display: flex; justify-content: center; gap: 20px; margin-bottom: 24px; }
.switch-link { display: flex; align-items: center; gap: 4px; font-size: 13px; color: #909399; text-decoration: none; transition: all 0.3s; padding: 8px 12px; border-radius: 8px; }
.switch-link:hover { color: #f0932b; background: rgba(240,147,43,0.08); }
.test-account { text-align: center; }
.test-account p { font-size: 13px; color: #909399; margin: 0; }
.test-account strong { color: #f0932b; }
@media (max-width: 768px) { .login-container { flex-direction: column; } .left-panel { padding: 40px 20px; } .right-panel { padding: 40px 20px; } }
</style>
