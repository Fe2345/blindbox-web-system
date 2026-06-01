import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { RuleConfig } from '@/types/rule'
import * as api from '@/api/admin/rule'

export const useRuleStore = defineStore('rule', () => {
  const rules = ref<RuleConfig | null>(null)

  async function fetchRules() {
    const res: any = await api.getRules()
    if (res.code === 200) rules.value = res.data
    return res
  }

  async function saveRules(data: Partial<RuleConfig>) {
    const res: any = await api.saveRules(data)
    if (res.code === 200) await fetchRules()
    return res
  }

  return { rules, fetchRules, saveRules }
})
