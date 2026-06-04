import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { AdminUser } from '@/types/user'
import * as api from '@/api/admin/user'

export const useUserStore = defineStore('user', () => {
  const list = ref<AdminUser[]>([])

  async function fetchList() {
    const res: any = await api.getUserList()
    if (res.code === 200) list.value = res.data
    return res
  }

  async function updateStatus(id: string, status: string) {
    const res: any = await api.updateUserStatus(id, status)
    if (res.code === 200) await fetchList()
    return res
  }

  return { list, fetchList, updateStatus }
})
