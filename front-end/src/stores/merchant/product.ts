import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as productApi from '@/api/merchant/product'
import type { MerchantProduct } from '@/types/merchant-self'

export const useMerchantProductStore = defineStore('merchantProduct', () => {
  const list = ref<MerchantProduct[]>([])
  const current = ref<MerchantProduct | null>(null)

  async function fetchList(params?: { status?: string; keyword?: string }) {
    const res: any = await productApi.getMerchantProducts(params)
    if (res.code === 200) list.value = res.data
    return res
  }

  async function fetchDetail(id: string) {
    const res: any = await productApi.getMerchantProductDetail(id)
    if (res.code === 200) current.value = res.data
    return res
  }

  async function submit(data: {
    name: string
    image: string
    description: string
    category: string
    rarity: string
    stock: number
  }) {
    return await productApi.submitProduct(data)
  }

  async function update(id: string, data: {
    name?: string
    image?: string
    description?: string
    stock?: number
  }) {
    return await productApi.updateProduct(id, data)
  }

  return { list, current, fetchList, fetchDetail, submit, update }
})
