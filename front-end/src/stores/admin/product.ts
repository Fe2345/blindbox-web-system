import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Product } from '@/types/product'
import * as api from '@/api/admin/product'

export const useProductStore = defineStore('product', () => {
  const list = ref<Product[]>([])

  async function fetchList() {
    const res: any = await api.getProductList()
    if (res.code === 200) list.value = res.data
    return res
  }

  async function review(id: string, action: string, note: string) {
    const res: any = await api.reviewProduct(id, { action, note })
    if (res.code === 200) await fetchList()
    return res
  }

  async function offline(id: string) {
    const res: any = await api.offlineProduct(id)
    if (res.code === 200) await fetchList()
    return res
  }

  return { list, fetchList, review, offline }
})
