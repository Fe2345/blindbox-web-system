import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { AdminBlindBox } from '@/types/blindbox'
import * as api from '@/api/admin/blindbox'

export const useBlindBoxStore = defineStore('blindbox', () => {
  const list = ref<AdminBlindBox[]>([])

  async function fetchList() {
    const res: any = await api.getBlindBoxList()
    if (res.code === 200) list.value = res.data
    return res
  }

  async function updateStatus(id: string, status: string) {
    const res: any = await api.updateBlindBoxStatus(id, status)
    if (res.code === 200) await fetchList()
    return res
  }

  async function savePrizePool(blindboxId: string, prizes: any[]) {
    const res: any = await api.savePrizePool(blindboxId, prizes)
    if (res.code === 200) await fetchList()
    return res
  }

  return { list, fetchList, updateStatus, savePrizePool }
})
