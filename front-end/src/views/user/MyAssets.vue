<template>
  <div class="page-container">
    <div class="page-header">
      <h2>我的资产</h2>
      <div class="header-actions">
        <el-button :disabled="!selectedIds.length" type="danger" plain @click="openManualRecycle">回收已选</el-button>
        <el-button type="warning" @click="showBulkDialog = true">快捷回收</el-button>
      </div>
    </div>

    <div class="asset-summary">
      <div class="summary-item primary">
        <span>拥有资产估值</span>
        <strong>{{ ownedEstimatedTotal }}</strong>
        <small>积分</small>
      </div>
      <div class="summary-item">
        <span>可回收返还</span>
        <strong>{{ availableRecycleTotal }}</strong>
        <small>积分</small>
      </div>
      <div class="summary-item muted">
        <span>已回收价值</span>
        <strong>{{ recycledEstimatedTotal }}</strong>
        <small>积分</small>
      </div>
      <div class="summary-item compact">
        <span>已选可返还</span>
        <strong>{{ selectedRecycleTotal }}</strong>
        <small>积分</small>
      </div>
    </div>

    <div class="filter-bar">
      <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width: 150px">
        <el-option label="可操作" value="available" />
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

    <template v-if="filteredAssets.length">
      <section v-if="ownedAssets.length" class="asset-section">
        <div class="section-title">
          <span>拥有中</span>
          <small>{{ ownedAssets.length }} 件</small>
        </div>
        <div class="card-grid">
          <AssetCard
            v-for="asset in ownedAssets"
            :key="asset.id"
            :asset="asset"
            :selected="selectedIds.includes(asset.id)"
            @toggle="toggleSelected(asset.id)"
            @detail="router.push(`/assets/${asset.id}`)"
            @recycle="quickRecycleOne(asset)"
          />
        </div>
      </section>

      <section v-if="recycledAssets.length" class="asset-section recycled-section">
        <div class="section-divider">
          <span>已回收</span>
          <small>{{ recycledAssets.length }} 件</small>
        </div>
        <div class="card-grid">
          <AssetCard
            v-for="asset in recycledAssets"
            :key="asset.id"
            :asset="asset"
            recycled
            @detail="router.push(`/assets/${asset.id}`)"
          />
        </div>
      </section>
    </template>

    <div v-else class="empty-tip">
      <p>当前暂无资产，可前往盲盒页面参与抽取</p>
      <el-button type="primary" @click="router.push('/blindbox')">去盲盒页面</el-button>
    </div>

    <el-dialog v-model="showBulkDialog" title="快捷回收" width="480px">
      <el-form label-width="96px">
        <el-form-item label="回收方式">
          <el-radio-group v-model="recycleMode">
            <el-radio-button label="manual">手动选择</el-radio-button>
            <el-radio-button label="rarity">按稀有度</el-radio-button>
            <el-radio-button label="keepOne">同类保留一件</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="recycleMode === 'manual'" label="已选资产">
          <span>{{ selectedIds.length }} 件，预计返还 {{ selectedRecycleTotal }} 积分</span>
        </el-form-item>
        <el-form-item v-if="recycleMode === 'rarity'" label="稀有度">
          <el-checkbox-group v-model="selectedRarities">
            <el-checkbox label="N">普通(N)</el-checkbox>
            <el-checkbox label="R">稀有(R)</el-checkbox>
            <el-checkbox label="SR">超稀有(SR)</el-checkbox>
            <el-checkbox label="SSR">传说(SSR)</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-alert
          v-if="recycleMode === 'keepOne'"
          title="系统会按商品名称分组，每种可操作资产保留最新获得的一件，其余全部回收。"
          type="warning"
          show-icon
          :closable="false"
        />
      </el-form>
      <template #footer>
        <el-button @click="showBulkDialog = false">取消</el-button>
        <el-button type="danger" :loading="recycling" @click="confirmBulkRecycle">确认回收</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { defineComponent, h, ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElButton, ElCheckbox, ElMessage, ElTag } from 'element-plus'
import type { Asset } from '@/types/asset'
import { useAssetStore } from '@/stores/asset'
import { usePointsStore } from '@/stores/points'
import { formatDate, rarityLabel, rarityColor, assetStatusLabel, assetStatusType } from '@/utils/format'

const router = useRouter()
const assetStore = useAssetStore()
const pointsStore = usePointsStore()

const filterStatus = ref('')
const filterRarity = ref('')
const searchKey = ref('')
const selectedIds = ref<string[]>([])
const showBulkDialog = ref(false)
const recycleMode = ref<'manual' | 'rarity' | 'keepOne'>('manual')
const selectedRarities = ref<string[]>(['N'])
const recycling = ref(false)

const rarityRank: Record<string, number> = { SSR: 4, SR: 3, R: 2, N: 1 }
const activeStatusRank: Record<string, number> = {
  available: 5,
  exchange_published: 4,
  exchange_locked: 3,
  pending_shipment: 2,
  shipped: 1,
  completed: 0,
}

const filteredAssets = computed(() => {
  return assetStore.assets.filter((asset) => {
    if (filterStatus.value && asset.status !== filterStatus.value) return false
    if (filterRarity.value && asset.rarity !== filterRarity.value) return false
    if (searchKey.value && !asset.productName.includes(searchKey.value)) return false
    return true
  })
})

const ownedAssets = computed(() => {
  return sortedAssets(filteredAssets.value.filter((asset) => asset.status !== 'recycled'))
})

const recycledAssets = computed(() => {
  return sortedAssets(filteredAssets.value.filter((asset) => asset.status === 'recycled'))
})

const ownedEstimatedTotal = computed(() => {
  return assetStore.assets
    .filter((asset) => asset.status !== 'recycled')
    .reduce((sum, asset) => sum + (asset.estimatedPoints || 0), 0)
})

const availableRecycleTotal = computed(() => {
  return assetStore.assets
    .filter((asset) => asset.status === 'available')
    .reduce((sum, asset) => sum + (asset.recyclablePoints || 0), 0)
})

const recycledEstimatedTotal = computed(() => {
  return assetStore.assets
    .filter((asset) => asset.status === 'recycled')
    .reduce((sum, asset) => sum + (asset.estimatedPoints || 0), 0)
})

const selectedRecycleTotal = computed(() => {
  const selected = new Set(selectedIds.value)
  return assetStore.assets
    .filter((asset) => selected.has(asset.id) && asset.status === 'available')
    .reduce((sum, asset) => sum + (asset.recyclablePoints || 0), 0)
})

function sortedAssets(assets: Asset[]) {
  return [...assets].sort((a, b) => {
    const rarityDiff = (rarityRank[b.rarity] || 0) - (rarityRank[a.rarity] || 0)
    if (rarityDiff) return rarityDiff

    const statusDiff = (activeStatusRank[b.status] || 0) - (activeStatusRank[a.status] || 0)
    if (statusDiff) return statusDiff

    return new Date(b.obtainedAt).getTime() - new Date(a.obtainedAt).getTime()
  })
}

function toggleSelected(id: string) {
  selectedIds.value = selectedIds.value.includes(id)
    ? selectedIds.value.filter((item) => item !== id)
    : [...selectedIds.value, id]
}

function openManualRecycle() {
  recycleMode.value = 'manual'
  showBulkDialog.value = true
}

async function quickRecycleOne(asset: Asset) {
  await runRecycle({ assetIds: [asset.id] })
}

async function confirmBulkRecycle() {
  if (recycleMode.value === 'manual') {
    if (!selectedIds.value.length) {
      ElMessage.warning('请先勾选要回收的资产')
      return
    }
    await runRecycle({ assetIds: selectedIds.value })
    return
  }
  if (recycleMode.value === 'rarity') {
    if (!selectedRarities.value.length) {
      ElMessage.warning('请选择稀有度')
      return
    }
    await runRecycle({ rarities: selectedRarities.value })
    return
  }
  await runRecycle({ keepOneByProduct: true })
}

async function runRecycle(payload: Parameters<typeof assetStore.bulkRecycle>[0]) {
  recycling.value = true
  try {
    const res = await assetStore.bulkRecycle(payload)
    if (res.code === 200) {
      ElMessage.success(`回收成功，共 ${res.data.recycledCount} 件，获得 ${res.data.recycledPoints} 积分`)
      const recycledIdSet = new Set(res.data.recycledAssetIds.map((id: number | string) => String(id)))
      selectedIds.value = selectedIds.value.filter((id) => !recycledIdSet.has(String(id)))
      showBulkDialog.value = false
      await pointsStore.fetchBalance()
    } else {
      ElMessage.error(res.message)
    }
  } finally {
    recycling.value = false
  }
}

const AssetCard = defineComponent({
  props: {
    asset: { type: Object as () => Asset, required: true },
    selected: { type: Boolean, default: false },
    recycled: { type: Boolean, default: false },
  },
  emits: ['toggle', 'detail', 'recycle'],
  setup(props, { emit }) {
    return () => h('div', {
      class: ['item-card', props.recycled ? 'is-recycled' : ''],
      onClick: () => emit('detail'),
    }, [
      props.asset.status === 'available'
        ? h(ElCheckbox, {
          class: 'asset-check',
          modelValue: props.selected,
          onClick: (event: Event) => event.stopPropagation(),
          onChange: () => emit('toggle'),
        })
        : null,
      h('img', { src: props.asset.productImage, alt: props.asset.productName, class: 'card-image' }),
      h('div', { class: 'card-body' }, [
        h('div', { class: 'card-title' }, props.asset.productName),
        h('div', { class: 'card-meta' }, [
          h(ElTag, {
            style: { color: rarityColor(props.asset.rarity), borderColor: rarityColor(props.asset.rarity) },
            size: 'small',
            effect: 'plain',
          }, () => rarityLabel(props.asset.rarity)),
        ]),
        h('div', { class: 'card-meta' }, `来源：${props.asset.sourceName}`),
        h('div', { class: 'card-meta' }, `获得时间：${formatDate(props.asset.obtainedAt)}`),
        h('div', { class: 'card-values' }, [
          h('span', {}, `估值 ${props.asset.estimatedPoints} 积分`),
          h('strong', {}, `回收 ${props.asset.recyclablePoints} 积分`),
        ]),
      ]),
      h('div', { class: 'card-actions' }, [
        h(ElTag, { type: assetStatusType(props.asset.status) as any, size: 'small' }, () => assetStatusLabel(props.asset.status)),
        props.asset.status === 'available'
          ? h(ElButton, {
            size: 'small',
            type: 'danger',
            plain: true,
            onClick: (event: Event) => {
              event.stopPropagation()
              emit('recycle')
            },
          }, () => '回收')
          : null,
        h(ElButton, {
          size: 'small',
          type: 'primary',
          onClick: (event: Event) => {
            event.stopPropagation()
            emit('detail')
          },
        }, () => '查看详情'),
      ]),
    ])
  },
})

onMounted(() => assetStore.fetchAssets())
</script>

<style scoped>
.header-actions {
  display: flex;
  gap: 10px;
}

.asset-summary {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin: 14px 0 16px;
}

.summary-item {
  min-height: 78px;
  padding: 14px 16px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  background: #fff;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.summary-item span {
  color: #909399;
  font-size: 13px;
}

.summary-item strong {
  margin-top: 4px;
  color: #303133;
  font-size: 26px;
  line-height: 1;
}

.summary-item small {
  margin-top: 2px;
  color: #909399;
}

.summary-item.primary strong {
  color: #e6a23c;
}

.summary-item.muted {
  background: #fafafa;
}

.summary-item.compact strong {
  color: #67c23a;
}

.asset-section {
  margin-top: 18px;
}

.section-title {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 18px;
  font-weight: 700;
  color: #303133;
}

.section-title small,
.section-divider small {
  font-size: 13px;
  font-weight: 400;
  color: #909399;
}

.section-divider {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 28px 0 12px;
  font-size: 16px;
  font-weight: 700;
  color: #909399;
}

.section-divider::before,
.section-divider::after {
  content: '';
  height: 1px;
  flex: 1;
  background: #dcdfe6;
}

.item-card {
  position: relative;
}

.card-values {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px dashed #ebeef5;
  font-size: 12px;
  color: #909399;
}

.card-values strong {
  color: #67c23a;
  font-weight: 600;
}

.asset-check {
  position: absolute;
  top: 8px;
  left: 8px;
  z-index: 2;
  padding: 4px;
  background: rgba(255, 255, 255, 0.92);
  border-radius: 4px;
}

.is-recycled {
  opacity: 0.62;
  filter: grayscale(0.25);
  background:
    linear-gradient(135deg, transparent 48%, rgba(144, 147, 153, 0.35) 49%, rgba(144, 147, 153, 0.35) 51%, transparent 52%),
    #fff;
}

.is-recycled :deep(.card-image) {
  filter: grayscale(0.7);
}

@media (max-width: 900px) {
  .asset-summary {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 560px) {
  .asset-summary {
    grid-template-columns: 1fr;
  }
}
</style>
