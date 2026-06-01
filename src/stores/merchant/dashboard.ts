import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as dashboardApi from '@/api/merchant/dashboard'
import type { MerchantDashboard } from '@/types/merchant-self'

export const useMerchantDashboardStore = defineStore('merchantDashboard', () => {
  const data = ref<MerchantDashboard | null>(null)

  async function fetchDashboard() {
    const res: any = await dashboardApi.getMerchantDashboard()
    if (res.code === 0) data.value = res.data
    return res
  }

  return { data, fetchDashboard }
})
