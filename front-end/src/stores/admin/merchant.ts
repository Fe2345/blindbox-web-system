import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Merchant } from '@/types/merchant'
import * as api from '@/api/admin/merchant'

export const useMerchantStore = defineStore('merchant', () => {
  const list = ref<Merchant[]>([])

  async function fetchList() {
    const res: any = await api.getMerchantList()
    if (res.code === 200) list.value = res.data
    return res
  }

  async function review(id: string, action: string, note: string) {
    const res: any = await api.reviewMerchant(id, { action, note })
    if (res.code === 200) await fetchList()
    return res
  }

  async function updateStatus(id: string, status: string) {
    const res: any = await api.updateMerchantStatus(id, status)
    if (res.code === 200) await fetchList()
    return res
  }

  return { list, fetchList, review, updateStatus }
})
