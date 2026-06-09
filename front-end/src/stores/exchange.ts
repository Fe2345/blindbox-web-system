import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ExchangePost, ExchangeApplication } from '@/types/exchange'
import * as exchangeApi from '@/api/exchange'

export const useExchangeStore = defineStore('exchange', () => {
  const posts = ref<ExchangePost[]>([])
  const applications = ref<ExchangeApplication[]>([])

  async function fetchPosts() {
    try {
      const res: any = await exchangeApi.getExchangePosts()
      if (res.code === 200) {
        posts.value = res.data || []
      }
      return res
    } catch (e: any) {
      console.error('[exchange] fetchPosts failed:', e)
      const msg = e?.response?.data?.message || e?.message || '获取换物帖子失败'
      return { code: -1, message: msg, data: [] }
    }
  }

  async function applyForExchange(postId: string, data: { assetId: string; remark: string }) {
    const res: any = await exchangeApi.applyExchange(postId, data)
    if (res.code === 200) {
      await fetchPosts()
    }
    return res
  }

  async function fetchApplications() {
    try {
      const res: any = await exchangeApi.getExchangeApplications()
      if (res.code === 200) {
        applications.value = res.data || []
      }
      return res
    } catch (e: any) {
      console.error('[exchange] fetchApplications failed:', e)
      const msg = e?.response?.data?.message || e?.message || '获取换物申请失败'
      return { code: -1, message: msg, data: [] }
    }
  }

  async function acceptApp(id: string) {
    const res: any = await exchangeApi.acceptApplication(id)
    if (res.code === 200) {
      await fetchApplications()
    }
    return res
  }

  async function rejectApp(id: string) {
    const res: any = await exchangeApi.rejectApplication(id)
    if (res.code === 200) {
      await fetchApplications()
    }
    return res
  }

  return { posts, applications, fetchPosts, applyForExchange, fetchApplications, acceptApp, rejectApp }
})
