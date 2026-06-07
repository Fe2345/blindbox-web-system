import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as shipmentApi from '@/api/merchant/shipment'
import type { ShipmentTask } from '@/types/merchant-self'

export const useMerchantShipmentStore = defineStore('merchantShipment', () => {
  const list = ref<ShipmentTask[]>([])
  const current = ref<ShipmentTask | null>(null)
  const total = ref(0)
  const loading = ref(false)

  async function fetchList(params?: shipmentApi.ShipmentListParams) {
    loading.value = true
    try {
      const res: any = await shipmentApi.getShipmentList(params)
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
      const res: any = await shipmentApi.getShipmentDetail(id)
      if (res.code === 200) {
        current.value = res.data
      }
      return res
    } finally {
      loading.value = false
    }
  }

  async function confirmShip(id: number, data: shipmentApi.ShipmentShipData) {
    return await shipmentApi.confirmShipment(id, data)
  }

  return { list, current, total, loading, fetchList, fetchDetail, confirmShip }
})
