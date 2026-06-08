import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { AdminOrder } from '@/types/order'
import * as api from '@/api/admin/order'

export const useOrderStore = defineStore('order', () => {
  const list = ref<AdminOrder[]>([])

  async function fetchList() {
    const res: any = await api.getOrderList()
    if (res.code === 200) list.value = res.data
    return res
  }

  async function ship(id: string, company: string, trackingNo: string) {
    const res: any = await api.shipOrder(id, { company, trackingNo })
    if (res.code === 200) await fetchList()
    return res
  }

  return { list, fetchList, ship }
})
