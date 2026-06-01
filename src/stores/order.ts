import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Order } from '@/types/order'
import * as orderApi from '@/api/order'

export const useOrderStore = defineStore('order', () => {
  const orders = ref<Order[]>([])

  async function fetchOrders() {
    const res: any = await orderApi.getOrders()
    if (res.code === 0) {
      orders.value = res.data
    }
    return res
  }

  async function confirmReceive(id: string) {
    const res: any = await orderApi.confirmReceive(id)
    if (res.code === 0) {
      await fetchOrders()
    }
    return res
  }

  return { orders, fetchOrders, confirmReceive }
})
