import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as inventoryApi from '@/api/merchant/inventory'
import type { InventoryItem, InventoryRecord } from '@/types/merchant-self'

export const useMerchantInventoryStore = defineStore('merchantInventory', () => {
  const list = ref<InventoryItem[]>([])
  const records = ref<InventoryRecord[]>([])
  const total = ref(0)
  const recordsTotal = ref(0)
  const loading = ref(false)

  async function fetchList(params?: inventoryApi.InventoryListParams) {
    loading.value = true
    try {
      const res: any = await inventoryApi.getInventoryList(params)
      if (res.code === 200) {
        list.value = res.data.results
        total.value = res.data.count
      }
      return res
    } finally {
      loading.value = false
    }
  }

  async function updateStock(id: number, data: inventoryApi.InventoryUpdateData) {
    return await inventoryApi.updateInventory(id, data)
  }

  async function fetchRecords(params?: inventoryApi.InventoryRecordParams) {
    loading.value = true
    try {
      const res: any = await inventoryApi.getInventoryRecords(params)
      if (res.code === 200) {
        records.value = res.data.results
        recordsTotal.value = res.data.count
      }
      return res
    } finally {
      loading.value = false
    }
  }

  return { list, records, total, recordsTotal, loading, fetchList, updateStock, fetchRecords }
})
