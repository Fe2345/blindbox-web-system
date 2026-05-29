<template>
  <div class="page-container">
    <div class="page-header">
      <h2>我的资产</h2>
    </div>

    <div class="filter-bar">
      <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width: 150px">
        <el-option label="可回收" value="available" />
        <el-option label="换物发布中" value="exchange_published" />
        <el-option label="交换锁定中" value="exchange_locked" />
        <el-option label="待发货" value="pending_shipment" />
        <el-option label="已发货" value="shipped" />
        <el-option label="已回收" value="recycled" />
        <el-option label="已完成" value="completed" />
      </el-select>
      <el-select v-model="filterRarity" placeholder="稀有度筛选" clearable style="width: 150px">
        <el-option label="普通(N)" value="N" />
        <el-option label="稀有(R)" value="R" />
        <el-option label="超稀有(SR)" value="SR" />
        <el-option label="传说(SSR)" value="SSR" />
      </el-select>
      <el-input v-model="searchKey" placeholder="搜索商品名称" prefix-icon="Search" style="width: 250px" clearable />
    </div>

    <div v-if="filteredAssets.length" class="card-grid">
      <div v-for="asset in filteredAssets" :key="asset.id" class="item-card" @click="router.push(`/assets/${asset.id}`)">
        <img :src="asset.productImage" :alt="asset.productName" class="card-image" />
        <div class="card-body">
          <div class="card-title">{{ asset.productName }}</div>
          <div class="card-meta">
            <el-tag :style="{ color: rarityColor(asset.rarity), borderColor: rarityColor(asset.rarity) }" size="small" effect="plain">
              {{ rarityLabel(asset.rarity) }}
            </el-tag>
          </div>
          <div class="card-meta">来源：{{ asset.sourceName }}</div>
          <div class="card-meta">获得时间：{{ formatDate(asset.obtainedAt) }}</div>
        </div>
        <div class="card-actions">
          <el-tag :type="assetStatusType(asset.status) as any" size="small">{{ assetStatusLabel(asset.status) }}</el-tag>
          <el-button size="small" type="primary" @click.stop="router.push(`/assets/${asset.id}`)">查看详情</el-button>
        </div>
      </div>
    </div>
    <div v-else class="empty-tip">
      <p>当前暂无资产，可前往盲盒页面参与抽取</p>
      <el-button type="primary" @click="router.push('/blindbox')">去盲盒页面</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAssetStore } from '@/stores/asset'
import { formatDate, rarityLabel, rarityColor, assetStatusLabel, assetStatusType } from '@/utils/format'

const router = useRouter()
const assetStore = useAssetStore()

const filterStatus = ref('')
const filterRarity = ref('')
const searchKey = ref('')

const filteredAssets = computed(() => {
  return assetStore.assets.filter((a) => {
    if (filterStatus.value && a.status !== filterStatus.value) return false
    if (filterRarity.value && a.rarity !== filterRarity.value) return false
    if (searchKey.value && !a.productName.includes(searchKey.value)) return false
    return true
  })
})

onMounted(() => assetStore.fetchAssets())
</script>
