import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as recordApi from '@/api/merchant/record'
import type { MerchantRecord } from '@/types/merchant-self'

export const useMerchantRecordStore = defineStore('merchantRecord', () => {
  const list = ref<MerchantRecord[]>([])
  const total = ref(0)
  const loading = ref(false)

  async function fetchList(params?: recordApi.RecordListParams) {
    loading.value = true
    try {
      const res: any = await recordApi.getMerchantRecords(params)
      if (res.code === 200) {
        list.value = res.data.results
        total.value = res.data.count
      }
      return res
    } finally {
      loading.value = false
    }
  }

  return { list, total, loading, fetchList }
})
