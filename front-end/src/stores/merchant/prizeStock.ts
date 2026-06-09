import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as prizeStockApi from '@/api/merchant/prizeStock'

export interface PrizeStockItem {
  id: string
  name: string
  image: string
  rarity: string
  blindboxId: string
  blindboxName: string
  productId: string
  productName: string
  remainingQuantity: number
  availableForShipping: number
  pendingShipmentCount: number
}

export interface ShipmentOrder {
  id: string
  userId: string
  username: string
  prizeId: string
  prizeName: string
  prizeImage: string
  rarity: string
  blindboxName: string
  batchNo: string
  createdAt: string
}

export const useMerchantPrizeStockStore = defineStore('merchantPrizeStock', () => {
  const prizeList = ref<PrizeStockItem[]>([])
  const shipmentOrders = ref<ShipmentOrder[]>([])

  async function fetchPrizeList() {
    const res: any = await prizeStockApi.getPrizeStockList()
    if (res.code === 200) prizeList.value = res.data
    return res
  }

  async function replenishStock(prizeId: string, quantity: number) {
    return await prizeStockApi.replenishPrizeStock(prizeId, quantity)
  }

  async function fetchShipmentOrders() {
    const res: any = await prizeStockApi.getShipmentOrders()
    if (res.code === 200) shipmentOrders.value = res.data
    return res
  }

  async function confirmShip(recordId: string) {
    return await prizeStockApi.confirmShip(recordId)
  }

  return {
    prizeList,
    shipmentOrders,
    fetchPrizeList,
    replenishStock,
    fetchShipmentOrders,
    confirmShip
  }
})
