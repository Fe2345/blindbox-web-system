import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { BlindBox, DrawResult } from '@/types/blindbox'
import * as blindboxApi from '@/api/blindbox'

export const useBlindBoxStore = defineStore('blindbox', () => {
  const blindBoxes = ref<BlindBox[]>([])
  const currentBox = ref<BlindBox | null>(null)
  const drawResult = ref<DrawResult | null>(null)

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

  async function draw(id: string) {
    const res: any = await blindboxApi.drawBlindBox(id)
    if (res.code === 200) {
      drawResult.value = res.data
    }
    return res
  }

  return { blindBoxes, currentBox, drawResult, fetchBlindBoxes, fetchBlindBoxDetail, draw }
})
