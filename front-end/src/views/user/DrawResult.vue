<template>
  <div class="page-container">
    <div v-if="batch" class="result-card">
      <h2 class="result-title">恭喜获得</h2>
      <div class="batch-subtitle">
        {{ batch.blindBoxName }} · {{ batch.count > 1 ? `${batch.count} 连抽` : '单抽' }}
      </div>

      <div :class="['prize-grid', { single: batch.results.length === 1 }]">
        <div v-for="item in batch.results" :key="item.id" class="prize-card">
          <el-checkbox
            class="result-check"
            :disabled="recycledIds.includes(String(item.assetId))"
            :model-value="selectedAssetIds.includes(String(item.assetId))"
            @change="toggleSelected(String(item.assetId))"
          />
          <div class="glow" :style="{ borderColor: rarityColor(item.rarity) }">
            <img :src="item.prizeImage" :alt="item.prizeName" class="prize-image" />
          </div>
          <h3 class="prize-name" :style="{ color: rarityColor(item.rarity) }">{{ item.prizeName }}</h3>
          <el-tag :style="{ color: rarityColor(item.rarity), borderColor: rarityColor(item.rarity) }" size="large" effect="plain">
            {{ rarityLabel(item.rarity) }}
          </el-tag>
        </div>
      </div>

      <div class="result-info">
        <div class="info-item">
          <span class="label">消耗积分</span>
          <span class="value" style="color: #f56c6c">-{{ batch.totalCostPoints }}</span>
        </div>
        <div class="info-item">
          <span class="label">剩余积分</span>
          <span class="value" style="color: #e6a23c">{{ batch.remainingPoints }}</span>
        </div>
        <div class="info-item">
          <span class="label">批次号</span>
          <span class="value small">{{ batch.batchNo }}</span>
        </div>
      </div>

      <el-alert title="商品已进入“我的资产”，可在资产页面查看详情" type="success" show-icon :closable="false" style="margin: 20px 0" />

      <div class="result-actions">
        <el-button type="primary" size="large" @click="router.push('/assets')">查看资产</el-button>
        <el-button type="danger" size="large" :loading="recycling" @click="recycleAll">一键回收</el-button>
        <el-button type="warning" size="large" @click="showRecycleDialog = true">选择回收</el-button>
        <el-button size="large" @click="continueDraw">继续抽取</el-button>
        <el-button size="large" @click="router.push('/exchange')">去换物中心</el-button>
      </div>
    </div>

    <div v-else class="empty-tip">
      <p>暂无抽取结果</p>
      <el-button type="primary" @click="router.push('/blindbox')">去盲盒页面</el-button>
    </div>

    <el-dialog v-model="showRecycleDialog" title="选择回收" width="500px">
      <el-form label-width="96px">
        <el-form-item label="回收方式">
          <el-radio-group v-model="recycleMode">
            <el-radio-button label="manual">手动选择</el-radio-button>
            <el-radio-button label="rarity">按稀有度</el-radio-button>
            <el-radio-button label="keepOne">同类保留一件</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="recycleMode === 'manual'" label="已选资产">
          <span>{{ selectedAssetIds.length }} 件</span>
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
          title="只在本次抽取结果中按同类商品保留一件，其余回收。"
          type="warning"
          show-icon
          :closable="false"
        />
      </el-form>
      <template #footer>
        <el-button @click="showRecycleDialog = false">取消</el-button>
        <el-button type="danger" :loading="recycling" @click="confirmRecycle">确认回收</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useBlindBoxStore } from '@/stores/blindbox'
import { useAssetStore } from '@/stores/asset'
import { usePointsStore } from '@/stores/points'
import { rarityLabel, rarityColor } from '@/utils/format'

const router = useRouter()
const blindBoxStore = useBlindBoxStore()
const assetStore = useAssetStore()
const pointsStore = usePointsStore()
const batch = computed(() => blindBoxStore.drawBatchResult)
const selectedAssetIds = ref<string[]>([])
const recycledIds = ref<string[]>([])
const selectedRarities = ref<string[]>(['N'])
const recycleMode = ref<'manual' | 'rarity' | 'keepOne'>('manual')
const showRecycleDialog = ref(false)
const recycling = ref(false)

watch(
  batch,
  (value) => {
    selectedAssetIds.value = (value?.results || []).map((item) => String(item.assetId)).filter(Boolean)
    recycledIds.value = []
  },
  { immediate: true },
)

function toggleSelected(assetId: string) {
  selectedAssetIds.value = selectedAssetIds.value.includes(assetId)
    ? selectedAssetIds.value.filter((id) => id !== assetId)
    : [...selectedAssetIds.value, assetId]
}

function continueDraw() {
  if (batch.value?.blindBoxId) {
    router.push(`/blindbox/${batch.value.blindBoxId}`)
  } else {
    router.push('/blindbox')
  }
}

async function recycleAll() {
  const ids = availableResultAssetIds.value
  if (!ids.length) {
    ElMessage.warning('没有可回收的本次抽取资产')
    return
  }
  await runRecycle({ assetIds: ids })
}

async function confirmRecycle() {
  if (!batch.value) return
  if (recycleMode.value === 'manual') {
    const ids = selectedAssetIds.value.filter((id) => !recycledIds.value.includes(id))
    if (!ids.length) {
      ElMessage.warning('请先选择要回收的资产')
      return
    }
    await runRecycle({ assetIds: ids })
    return
  }
  if (recycleMode.value === 'rarity') {
    if (!selectedRarities.value.length) {
      ElMessage.warning('请选择稀有度')
      return
    }
    const ids = batch.value.results
      .filter((item) => selectedRarities.value.includes(item.rarity))
      .map((item) => String(item.assetId))
      .filter((id) => !recycledIds.value.includes(id))
    if (!ids.length) {
      ElMessage.warning('当前稀有度没有可回收资产')
      return
    }
    await runRecycle({ assetIds: ids })
    return
  }
  await runRecycle({ assetIds: availableResultAssetIds.value, keepOneByProduct: true })
}

const availableResultAssetIds = computed(() => {
  return (batch.value?.results || [])
    .map((item) => String(item.assetId))
    .filter((id) => id && !recycledIds.value.includes(id))
})

async function runRecycle(payload: Parameters<typeof assetStore.bulkRecycle>[0]) {
  recycling.value = true
  try {
    const res = await assetStore.bulkRecycle(payload)
    if (res.code === 200) {
      const ids = res.data.recycledAssetIds.map((id: number | string) => String(id))
      recycledIds.value = Array.from(new Set([...recycledIds.value, ...ids]))
      selectedAssetIds.value = selectedAssetIds.value.filter((id) => !recycledIds.value.includes(id))
      showRecycleDialog.value = false
      await pointsStore.fetchBalance()
      ElMessage.success(`回收成功，共 ${res.data.recycledCount} 件，获得 ${res.data.recycledPoints} 积分`)
    } else {
      ElMessage.error(res.message)
    }
  } finally {
    recycling.value = false
  }
}
</script>

<style scoped>
.result-card {
  max-width: 900px;
  margin: 40px auto;
  text-align: center;
  background: #fff;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
}

.result-title {
  font-size: 18px;
  color: #909399;
  margin-bottom: 8px;
}

.batch-subtitle {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 24px;
}

.prize-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 18px;
}

.prize-grid.single {
  display: flex;
  justify-content: center;
}

.prize-card {
  min-width: 0;
  position: relative;
}

.result-check {
  position: absolute;
  top: 0;
  left: 50%;
  z-index: 2;
  transform: translateX(-70px);
  padding: 4px;
  background: rgba(255, 255, 255, 0.92);
  border-radius: 4px;
}

.glow {
  display: inline-block;
  padding: 8px;
  border: 3px solid;
  border-radius: 12px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 10px rgba(102, 126, 234, 0.3); }
  50% { box-shadow: 0 0 30px rgba(102, 126, 234, 0.6); }
}

.prize-image {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 8px;
}

.prize-name {
  font-size: 15px;
  margin: 10px 0 8px;
  word-break: break-word;
}

.result-info {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-top: 24px;
  flex-wrap: wrap;
}

.info-item .label {
  display: block;
  font-size: 13px;
  color: #909399;
}

.info-item .value {
  font-size: 18px;
  font-weight: 600;
}

.info-item .value.small {
  font-size: 13px;
}

.result-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .result-card {
    padding: 24px;
  }

  .prize-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
