import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { UserInfo, Address } from '@/types/user'
import * as userApi from '@/api/user'

export const useUserStore = defineStore('user', () => {
  const userInfo = ref<UserInfo | null>(null)
  const addresses = ref<Address[]>([])
  const isLoggedIn = ref(localStorage.getItem('isLoggedIn') === 'true')

  async function login(username: string, password: string) {
    const res: any = await userApi.login({ username, password })
    if (res.code === 200) {
      userInfo.value = res.data.user
      isLoggedIn.value = true
      localStorage.setItem('isLoggedIn', 'true')
    }
    return res
  }

  async function register(username: string, phone: string, password: string) {
    const res: any = await userApi.register({ username, phone, password })
    return res
  }

  async function fetchUserInfo() {
    const res: any = await userApi.getUserInfo()
    if (res.code === 200) {
      userInfo.value = res.data
    }
    return res
  }

  async function updateUserInfo(data: Partial<UserInfo>) {
    const res: any = await userApi.updateUserInfo(data)
    if (res.code === 0 && userInfo.value) {
      Object.assign(userInfo.value, data)
    }
    return res
  }

  async function fetchAddresses() {
    const res: any = await userApi.getAddresses()
    if (res.code === 200) {
      addresses.value = res.data
    }
    return res
  }

  async function addAddress(data: Omit<Address, 'id'>) {
    const res: any = await userApi.addAddress(data)
    if (res.code === 200) {
      await fetchAddresses()
    }
    return res
  }

  async function updateAddress(id: string, data: Partial<Address>) {
    const res: any = await userApi.updateAddress(id, data)
    if (res.code === 200) {
      await fetchAddresses()
    }
    return res
  }

  async function deleteAddress(id: string) {
    const res: any = await userApi.deleteAddress(id)
    if (res.code === 200) {
      await fetchAddresses()
    }
    return res
  }

  async function logout() {
    try {
      await userApi.logout()
    } catch {
      // 忽略网络错误，确保本地状态清理
    }
    userInfo.value = null
    isLoggedIn.value = false
    localStorage.removeItem('isLoggedIn')
  }

  return {
    userInfo, addresses, isLoggedIn,
    login, register, fetchUserInfo, updateUserInfo,
    fetchAddresses, addAddress, updateAddress, deleteAddress, logout,
  }
})
