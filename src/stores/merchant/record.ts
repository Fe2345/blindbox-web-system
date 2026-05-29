import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as recordApi from '@/api/merchant/record'
import type { MerchantRecord } from '@/types/merchant-self'

export const useMerchantRecordStore = defineStore('merchantRecord', () => {
  const list = ref<MerchantRecord[]>([])

  async function fetchList(params?: {
    type?: string
    keyword?: string
    startDate?: string
    endDate?: string
  }) {
    const res: any = await recordApi.getMerchantRecords(params)
    if (res.code === 0) list.value = res.data
    return res
  }

  return { list, fetchList }
})
