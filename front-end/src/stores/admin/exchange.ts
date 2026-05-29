import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { AdminExchange } from '@/types/exchange'
import * as api from '@/api/admin/exchange'

export const useExchangeStore = defineStore('exchange', () => {
  const list = ref<AdminExchange[]>([])

  async function fetchList() {
    const res: any = await api.getExchangeList()
    if (res.code === 0) list.value = res.data
    return res
  }

  async function resolve(id: string, action: string, note: string) {
    const res: any = await api.resolveException(id, { action, note })
    if (res.code === 0) await fetchList()
    return res
  }

  return { list, fetchList, resolve }
})
