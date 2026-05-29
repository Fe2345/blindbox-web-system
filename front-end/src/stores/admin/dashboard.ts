import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as api from '@/api/admin/dashboard'

export const useDashboardStore = defineStore('dashboard', () => {
  const data = ref<any>(null)

  async function fetchDashboard() {
    const res: any = await api.getDashboard()
    if (res.code === 0) data.value = res.data
    return res
  }

  return { data, fetchDashboard }
})
