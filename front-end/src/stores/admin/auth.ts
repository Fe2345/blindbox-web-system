import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as authApi from '@/api/admin/auth'

export const useAuthStore = defineStore('auth', () => {
  const adminInfo = ref<any>(null)
  const isLoggedIn = ref(localStorage.getItem('admin_logged_in') === 'true')

  async function login(username: string, password: string) {
    const res: any = await authApi.adminLogin({ username, password })
    if (res.code === 200) {
      adminInfo.value = res.data.user
      isLoggedIn.value = true
      localStorage.setItem('admin_logged_in', 'true')
    }
    return res
  }

  async function fetchInfo() {
    const res: any = await authApi.getAdminInfo()
    if (res.code === 200) adminInfo.value = res.data
    return res
  }

  async function logout() {
    try {
      await authApi.adminLogout()
    } catch {
      // 忽略网络错误，确保本地状态清理
    }
    adminInfo.value = null
    isLoggedIn.value = false
    localStorage.removeItem('admin_logged_in')
  }

  return { adminInfo, isLoggedIn, login, fetchInfo, logout }
})
