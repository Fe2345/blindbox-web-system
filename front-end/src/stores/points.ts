import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { PointsRecord, TransactionRecord } from '@/types/points'
import * as pointsApi from '@/api/points'

export const usePointsStore = defineStore('points', () => {
  const records = ref<PointsRecord[]>([])
  const transactions = ref<TransactionRecord[]>([])
  const balance = ref(0)

  async function fetchRecords() {
    const res: any = await pointsApi.getPointsRecords()
    if (res.code === 0) {
      records.value = res.data
    }
    return res
  }

  async function fetchBalance() {
    const res: any = await pointsApi.getPointsBalance()
    if (res.code === 0) {
      balance.value = res.data.balance
    }
    return res
  }

  async function fetchTransactions() {
    const res: any = await pointsApi.getTransactions()
    if (res.code === 0) {
      transactions.value = res.data
    }
    return res
  }

  return { records, transactions, balance, fetchRecords, fetchBalance, fetchTransactions }
})
