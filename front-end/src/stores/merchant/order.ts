import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as orderApi from '@/api/merchant/order'
import type { MerchantOrder } from '@/types/merchant-self'

export const useMerchantOrderStore = defineStore('merchantOrder', () => {
  const list = ref<MerchantOrder[]>([])

  async function fetchList(params?: { status?: string }) {
    const res: any = await orderApi.getMerchantOrders(params)
    if (res.code === 200) list.value = res.data
    return res
  }

  return { list, fetchList }
})
