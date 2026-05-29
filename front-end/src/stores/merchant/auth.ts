import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as authApi from '@/api/merchant/auth'

export const useMerchantAuthStore = defineStore('merchantAuth', () => {
  const token = ref(localStorage.getItem('merchant_token') || '')
  const merchantInfo = ref<any>(null)
  const isLoggedIn = ref(!!token.value)

  async function login(username: string, password: string) {
    const res: any = await authApi.merchantLogin({ username, password })
    if (res.code === 0) {
      token.value = res.data.token
      merchantInfo.value = res.data.merchant
      isLoggedIn.value = true
      localStorage.setItem('merchant_token', res.data.token)
    }
    return res
  }

  async function fetchInfo() {
    const res: any = await authApi.getMerchantInfo()
    if (res.code === 0) merchantInfo.value = res.data
    return res
  }

  function logout() {
    token.value = ''
    merchantInfo.value = null
    isLoggedIn.value = false
    localStorage.removeItem('merchant_token')
  }

  return { token, merchantInfo, isLoggedIn, login, fetchInfo, logout }
})
