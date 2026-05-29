import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ExchangePost, ExchangeApplication } from '@/types/exchange'
import * as exchangeApi from '@/api/exchange'

export const useExchangeStore = defineStore('exchange', () => {
  const posts = ref<ExchangePost[]>([])
  const applications = ref<ExchangeApplication[]>([])

  async function fetchPosts() {
    const res: any = await exchangeApi.getExchangePosts()
    if (res.code === 0) {
      posts.value = res.data
    }
    return res
  }

  async function applyForExchange(postId: string, data: { assetId: string; remark: string }) {
    const res: any = await exchangeApi.applyExchange(postId, data)
    return res
  }

  async function fetchApplications() {
    const res: any = await exchangeApi.getExchangeApplications()
    if (res.code === 0) {
      applications.value = res.data
    }
    return res
  }

  async function acceptApp(id: string) {
    const res: any = await exchangeApi.acceptApplication(id)
    if (res.code === 0) {
      await fetchApplications()
    }
    return res
  }

  async function rejectApp(id: string) {
    const res: any = await exchangeApi.rejectApplication(id)
    if (res.code === 0) {
      await fetchApplications()
    }
    return res
  }

  return { posts, applications, fetchPosts, applyForExchange, fetchApplications, acceptApp, rejectApp }
})
