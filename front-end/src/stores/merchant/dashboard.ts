import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as dashboardApi from '@/api/merchant/dashboard'
import type { MerchantDashboard } from '@/types/merchant-self'

export const useMerchantDashboardStore = defineStore('merchantDashboard', () => {
  const data = ref<MerchantDashboard | null>(null)
  const loading = ref(false)

  async function fetchDashboard() {
    loading.value = true
    try {
      const res: any = await dashboardApi.getMerchantDashboard()
      if (res.code === 200) {
        data.value = res.data
      }
      return res
    } finally {
      loading.value = false
    }
  }

  return { data, loading, fetchDashboard }
})
