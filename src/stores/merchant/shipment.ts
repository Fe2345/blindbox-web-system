import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as shipmentApi from '@/api/merchant/shipment'
import type { ShipmentTask } from '@/types/merchant-self'

export const useMerchantShipmentStore = defineStore('merchantShipment', () => {
  const list = ref<ShipmentTask[]>([])
  const current = ref<ShipmentTask | null>(null)

  async function fetchList(params?: { status?: string }) {
    const res: any = await shipmentApi.getShipmentTasks(params)
    if (res.code === 0) list.value = res.data
    return res
  }

  async function fetchDetail(id: string) {
    const res: any = await shipmentApi.getShipmentDetail(id)
    if (res.code === 0) current.value = res.data
    return res
  }

  async function confirmShip(id: string, data: { logisticsCompany: string; trackingNo: string }) {
    return await shipmentApi.confirmShipment(id, data)
  }

  return { list, current, fetchList, fetchDetail, confirmShip }
})
