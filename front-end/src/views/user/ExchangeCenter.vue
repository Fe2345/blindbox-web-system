<template>
  <div class="page-container">
    <div class="page-header" style="display: flex; justify-content: space-between; align-items: center">
      <h2>换物中心</h2>
      <el-button type="warning" @click="router.push('/exchange/publish')">发布换物</el-button>
    </div>

    <div class="filter-bar">
      <el-select v-model="filterCategory" placeholder="分类筛选" clearable style="width: 150px">
        <el-option v-for="c in categories" :key="c" :label="c" :value="c" />
      </el-select>
      <el-select v-model="filterRarity" placeholder="稀有度筛选" clearable style="width: 150px">
        <el-option label="普通(N)" value="N" />
        <el-option label="稀有(R)" value="R" />
        <el-option label="超稀有(SR)" value="SR" />
        <el-option label="传说(SSR)" value="SSR" />
      </el-select>
      <el-input v-model="searchKey" placeholder="搜索商品名称或期望说明" prefix-icon="Search" style="width: 280px" clearable />
    </div>

    <div v-if="loading" v-loading="true" style="min-height: 200px"></div>
    <div v-else-if="filteredPosts.length" class="card-grid">
      <div v-for="post in filteredPosts" :key="post.id" class="item-card">
        <img :src="post.assetImage" :alt="post.assetName" class="card-image" />
        <div class="card-body">
          <div class="card-title">{{ post.assetName }}</div>
          <div class="card-meta">
            <el-tag :style="{ color: rarityColor(post.assetRarity), borderColor: rarityColor(post.assetRarity) }" size="small" effect="plain">
              {{ rarityLabel(post.assetRarity) }}
            </el-tag>
            <el-tag size="small" type="info">{{ post.assetCategory }}</el-tag>
          </div>
          <div class="card-meta">发布者：{{ post.username }}</div>
          <div class="card-meta expect">期望：{{ post.expectDescription }}</div>
          <div class="card-meta">发布时间：{{ formatDate(post.createdAt) }}</div>
        </div>
        <div class="card-actions">
          <el-tag :type="post.status === 'published' ? 'success' : 'info'" size="small">
            {{ post.status === 'published' ? '展示中' : post.status === 'locked' ? '已锁定' : '已完成' }}
          </el-tag>
          <el-tag v-if="post.pendingCount > 0" type="warning" size="small">{{ post.pendingCount }}条申请</el-tag>
          <template v-if="isMyPost(post)">
            <el-button v-if="post.pendingCount > 0" size="small" type="success" @click="router.push('/exchange/handle')">处理申请</el-button>
          </template>
          <template v-else>
            <el-button v-if="post.status === 'published'" size="small" type="primary" @click="showApplyDialog(post)">申请换物</el-button>
          </template>
        </div>
      </div>
    </div>
    <div v-else class="empty-tip">暂无换物信息</div>

    <!-- 申请换物弹窗 -->
    <el-dialog v-model="applyDialogVisible" title="申请换物" width="500px">
      <div v-if="currentPost">
        <h4 style="margin-bottom: 12px">对方商品</h4>
        <div style="display: flex; gap: 12px; margin-bottom: 16px">
          <img :src="currentPost.assetImage" style="width: 80px; height: 80px; border-radius: 4px; object-fit: cover" />
          <div>
            <div style="font-weight: 600">{{ currentPost.assetName }}</div>
            <el-tag :style="{ color: rarityColor(currentPost.assetRarity), borderColor: rarityColor(currentPost.assetRarity) }" size="small" effect="plain">
              {{ rarityLabel(currentPost.assetRarity) }}
            </el-tag>
            <div style="font-size: 13px; color: #909399; margin-top: 4px">期望：{{ currentPost.expectDescription }}</div>
          </div>
        </div>

        <el-divider />

        <h4 style="margin-bottom: 12px">我的商品</h4>
        <el-select v-model="applyForm.assetId" placeholder="选择要交换的资产" style="width: 100%">
          <el-option v-for="a in myAvailableAssets" :key="a.id" :label="a.productName" :value="a.id">
            <span>{{ a.productName }}</span>
            <el-tag size="small" effect="plain" :style="{ color: rarityColor(a.rarity), borderColor: rarityColor(a.rarity), marginLeft: '8px' }">{{ rarityLabel(a.rarity) }}</el-tag>
          </el-option>
        </el-select>

        <el-input v-model="applyForm.remark" type="textarea" :rows="3" placeholder="申请说明（选填）" style="margin-top: 12px" />
      </div>
      <template #footer>
        <el-button @click="applyDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="applying" @click="handleApply">提交申请</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useExchangeStore } from '@/stores/exchange'
import { useAssetStore } from '@/stores/asset'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { formatDate, rarityLabel, rarityColor } from '@/utils/format'
import type { ExchangePost } from '@/types/exchange'

const router = useRouter()
const exchangeStore = useExchangeStore()
const assetStore = useAssetStore()
const userStore = useUserStore()

function isMyPost(post: ExchangePost) {
  return String(post.userId) === String(userStore.userInfo?.id)
}

const filterCategory = ref('')
const filterRarity = ref('')
const searchKey = ref('')
const loading = ref(true)
const applyDialogVisible = ref(false)
const applying = ref(false)
const currentPost = ref<ExchangePost | null>(null)
const applyForm = ref({ assetId: '', remark: '' })

const categories = computed(() => [...new Set(exchangeStore.posts.map((p) => p.assetCategory))])

const filteredPosts = computed(() => {
  return exchangeStore.posts.filter((p) => {
    // 只显示展示中和已锁定的帖子，隐藏已完成和已取消的
    if (p.status !== 'published' && p.status !== 'locked') return false
    if (filterCategory.value && p.assetCategory !== filterCategory.value) return false
    if (filterRarity.value && p.assetRarity !== filterRarity.value) return false
    if (searchKey.value && !p.assetName.includes(searchKey.value) && !p.expectDescription.includes(searchKey.value)) return false
    return true
  })
})

const myAvailableAssets = computed(() => assetStore.assets.filter((a) => a.status === 'available'))

function showApplyDialog(post: ExchangePost) {
  currentPost.value = post
  applyForm.value = { assetId: '', remark: '' }
  applyDialogVisible.value = true
}

async function handleApply() {
  if (!applyForm.value.assetId) {
    ElMessage.warning('请选择要交换的资产')
    return
  }
  if (!currentPost.value) return
  applying.value = true
  try {
    const res = await exchangeStore.applyForExchange(currentPost.value.id, applyForm.value)
    if (res.code === 200) {
      ElMessage.success('申请已提交')
      applyDialogVisible.value = false
    } else {
      ElMessage.error(res.message)
    }
  } finally {
    applying.value = false
  }
}

onMounted(async () => {
  try {
    const results = await Promise.allSettled([
      exchangeStore.fetchPosts(),
      assetStore.fetchAssets(),
      userStore.fetchUserInfo(),
    ])
    // 如果换物帖子加载失败，显示错误
    const postsResult = results[0]
    if (postsResult.status === 'fulfilled' && postsResult.value?.code !== 200) {
      ElMessage.error(postsResult.value?.message || '获取换物信息失败')
    } else if (postsResult.status === 'rejected') {
      ElMessage.error('获取换物信息失败')
    }
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.expect {
  color: #e6a23c;
  font-style: italic;
}
</style>
