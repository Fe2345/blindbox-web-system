import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as authApi from '@/api/admin/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('admin_token') || '')
  const adminInfo = ref<any>(null)
  const isLoggedIn = ref(!!token.value)

  async function login(username: string, password: string) {
    const res: any = await authApi.adminLogin({ username, password })
    if (res.code === 0) {
      token.value = res.data.token
      adminInfo.value = res.data.user
      isLoggedIn.value = true
      localStorage.setItem('admin_token', res.data.token)
    }
    return res
  }

  async function fetchInfo() {
    const res: any = await authApi.getAdminInfo()
    if (res.code === 0) adminInfo.value = res.data
    return res
  }

  function logout() {
    token.value = ''
    adminInfo.value = null
    isLoggedIn.value = false
    localStorage.removeItem('admin_token')
  }

  return { token, adminInfo, isLoggedIn, login, fetchInfo, logout }
})
