import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as api from '@/api/admin/ledger'

export const useLedgerStore = defineStore('ledger', () => {
  const list = ref<any[]>([])

  async function fetchList(params?: any) {
    const res: any = await api.getLedger(params)
    if (res.code === 0) list.value = res.data
    return res
  }

  return { list, fetchList }
})
