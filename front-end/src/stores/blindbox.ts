import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { BlindBox, DrawBatchResult, DrawResult } from '@/types/blindbox'
import * as blindboxApi from '@/api/blindbox'

export const useBlindBoxStore = defineStore('blindbox', () => {
  const blindBoxes = ref<BlindBox[]>([])
  const currentBox = ref<BlindBox | null>(null)
  const drawResult = ref<DrawResult | null>(null)
  const drawBatchResult = ref<DrawBatchResult | null>(null)

  async function fetchBlindBoxes() {
    const res: any = await blindboxApi.getBlindBoxes()
    if (res.code === 200) {
      blindBoxes.value = res.data
    }
    return res
  }

  async function fetchBlindBoxDetail(id: string) {
    const res: any = await blindboxApi.getBlindBoxDetail(id)
    if (res.code === 200) {
      currentBox.value = res.data
    }
    return res
  }

  async function draw(id: string, count = 1) {
    const res: any = await blindboxApi.drawBlindBox(id, count)
    if (res.code === 200) {
      if (count === 1) {
        drawResult.value = res.data
        drawBatchResult.value = {
          batchNo: res.data.batchNo,
          count: 1,
          totalCostPoints: res.data.costPoints,
          remainingPoints: res.data.remainingPoints,
          blindBoxId: res.data.blindBoxId,
          blindBoxName: res.data.blindBoxName,
          results: [res.data],
        }
      } else {
        drawBatchResult.value = res.data
        drawResult.value = res.data.results?.[0] || null
      }
    }
    return res
  }

  return { blindBoxes, currentBox, drawResult, drawBatchResult, fetchBlindBoxes, fetchBlindBoxDetail, draw }
})
