import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as productApi from '@/api/merchant/product'
import type { MerchantProduct, PaginatedResponse } from '@/types/merchant-self'

export const useMerchantProductStore = defineStore('merchantProduct', () => {
  const list = ref<MerchantProduct[]>([])
  const current = ref<MerchantProduct | null>(null)
  const total = ref(0)
  const loading = ref(false)

  async function fetchList(params?: productApi.ProductListParams) {
    loading.value = true
    try {
      const res: any = await productApi.getProductList(params)
      if (res.code === 200) {
        list.value = res.data.results
        total.value = res.data.count
      }
      return res
    } finally {
      loading.value = false
    }
  }

  async function fetchDetail(id: number) {
    loading.value = true
    try {
      const res: any = await productApi.getProductDetail(id)
      if (res.code === 200) {
        current.value = res.data
      }
      return res
    } finally {
      loading.value = false
    }
  }

  async function submit(data: productApi.ProductSubmitData) {
    return await productApi.submitProduct(data)
  }

  async function update(id: number, data: productApi.ProductSubmitData) {
    return await productApi.updateProduct(id, data)
  }

  return { list, current, total, loading, fetchList, fetchDetail, submit, update }
})
