import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as authApi from '@/api/merchant/auth'

export const useMerchantAuthStore = defineStore('merchantAuth', () => {
  const merchantInfo = ref<any>(null)
  const isLoggedIn = ref(localStorage.getItem('merchant_logged_in') === 'true')

  async function login(username: string, password: string, expectedRole?: string) {
    const res: any = await authApi.merchantLogin({ username, password })
    if (res.code === 200) {
      const role = res.data.merchant?.role ?? res.data.user?.role
      if (expectedRole && role !== expectedRole) {
        return res
      }
      merchantInfo.value = res.data.merchant
      isLoggedIn.value = true
      localStorage.setItem('merchant_logged_in', 'true')
    }
    return res
  }

  async function fetchInfo() {
    const res: any = await authApi.getMerchantInfo()
    if (res.code === 200) merchantInfo.value = res.data
    return res
  }

  async function logout() {
    try {
      await authApi.merchantLogout()
    } catch {
      // 忽略网络错误，确保本地状态清理
    }
    merchantInfo.value = null
    isLoggedIn.value = false
    localStorage.removeItem('merchant_logged_in')
  }

  return { merchantInfo, isLoggedIn, login, fetchInfo, logout }
})
