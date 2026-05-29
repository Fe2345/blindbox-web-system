import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Asset } from '@/types/asset'
import * as assetApi from '@/api/asset'

export const useAssetStore = defineStore('asset', () => {
  const assets = ref<Asset[]>([])
  const currentAsset = ref<Asset | null>(null)

  async function fetchAssets() {
    const res: any = await assetApi.getAssets()
    if (res.code === 0) {
      assets.value = res.data
    }
    return res
  }

  async function fetchAssetDetail(id: string) {
    const res: any = await assetApi.getAssetDetail(id)
    if (res.code === 0) {
      currentAsset.value = res.data
    }
    return res
  }

  async function recycle(id: string) {
    const res: any = await assetApi.recycleAsset(id)
    if (res.code === 0) {
      await fetchAssets()
    }
    return res
  }

  async function ship(id: string) {
    const res: any = await assetApi.shipAsset(id)
    if (res.code === 0) {
      await fetchAssets()
    }
    return res
  }

  async function publishExchange(id: string, data: { expectDescription: string; remark: string }) {
    const res: any = await assetApi.publishExchange(id, data)
    if (res.code === 0) {
      await fetchAssets()
    }
    return res
  }

  return { assets, currentAsset, fetchAssets, fetchAssetDetail, recycle, ship, publishExchange }
})
