import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as inventoryApi from '@/api/merchant/inventory'
import type { InventoryItem, InventoryRecord } from '@/types/merchant-self'

export const useMerchantInventoryStore = defineStore('merchantInventory', () => {
  const list = ref<InventoryItem[]>([])
  const records = ref<InventoryRecord[]>([])

  async function fetchList() {
    const res: any = await inventoryApi.getInventoryList()
    if (res.code === 0) list.value = res.data
    return res
  }

  async function updateStock(productId: string, stock: number) {
    return await inventoryApi.updateStock(productId, stock)
  }

  async function fetchRecords(productId?: string) {
    const res: any = await inventoryApi.getInventoryRecords(productId)
    if (res.code === 0) records.value = res.data
    return res
  }

  return { list, records, fetchList, updateStock, fetchRecords }
})
