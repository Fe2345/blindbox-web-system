import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { OpLog, ExceptionRecord } from '@/types/log'
import * as api from '@/api/admin/log'

export const useLogStore = defineStore('log', () => {
  const logs = ref<OpLog[]>([])
  const exceptions = ref<ExceptionRecord[]>([])

  async function fetchLogs() {
    const res: any = await api.getOpLogs()
    if (res.code === 0) logs.value = res.data
    return res
  }

  async function fetchExceptions() {
    const res: any = await api.getExceptions()
    if (res.code === 0) exceptions.value = res.data
    return res
  }

  async function resolveException(id: string, result: string) {
    const res: any = await api.resolveException(id, { result })
    if (res.code === 0) await fetchExceptions()
    return res
  }

  return { logs, exceptions, fetchLogs, fetchExceptions, resolveException }
})
