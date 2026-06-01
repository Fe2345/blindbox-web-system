<template>
  <div class="page-container" v-if="asset">
    <el-page-header @back="router.push('/assets')" :title="'返回资产列表'" :content="asset.productName" />

    <el-row :gutter="24" style="margin-top: 20px">
      <el-col :span="10">
        <el-card>
          <img :src="asset.productImage" :alt="asset.productName" style="width: 100%; border-radius: 8px" />
        </el-card>
      </el-col>
      <el-col :span="14">
        <el-card>
          <template #header><span>商品信息</span></template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="商品名称">{{ asset.productName }}</el-descriptions-item>
            <el-descriptions-item label="分类">{{ asset.category }}</el-descriptions-item>
            <el-descriptions-item label="稀有度">
              <el-tag :style="{ color: rarityColor(asset.rarity), borderColor: rarityColor(asset.rarity) }" effect="plain">
                {{ rarityLabel(asset.rarity) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="当前状态">
              <el-tag :type="assetStatusType(asset.status) as any">{{ assetStatusLabel(asset.status) }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="来源类型">{{ asset.sourceType === 'blindbox' ? '盲盒抽取' : '换物获得' }}</el-descriptions-item>
            <el-descriptions-item label="来源">{{ asset.sourceName }}</el-descriptions-item>
            <el-descriptions-item label="获得时间">{{ formatDate(asset.obtainedAt) }}</el-descriptions-item>
            <el-descriptions-item label="估值积分" :span="2">
              <span style="color: #e6a23c; font-weight: 600">{{ asset.estimatedPoints }}</span>
            </el-descriptions-item>
          </el-descriptions>
          <p style="margin-top: 12px; color: #606266">{{ asset.description }}</p>
        </el-card>

        <el-card style="margin-top: 16px">
          <template #header><span>价值信息</span></template>
          <div class="value-info">
            <div class="value-item">
              <span class="label">估值积分</span>
              <span class="value" style="color: #e6a23c">{{ asset.estimatedPoints }}</span>
            </div>
            <div class="value-item">
              <span class="label">回收可返还</span>
              <span class="value" style="color: #67c23a">{{ asset.recyclablePoints }}</span>
            </div>
          </div>
        </el-card>

        <el-card style="margin-top: 16px">
          <template #header><span>可执行操作</span></template>
          <div class="action-buttons">
            <el-button v-if="asset.canRecycle" type="danger" @click="showRecycleDialog = true">回收</el-button>
            <el-button v-if="asset.canShip" type="primary" @click="handleShip">申请发货</el-button>
            <el-button v-if="asset.canExchange" type="warning" @click="showExchangeDialog = true">发布换物</el-button>
            <el-button v-if="asset.status === 'exchange_published'" type="info" @click="router.push('/exchange/handle')">查看换物申请</el-button>
            <el-button v-if="asset.status === 'pending_shipment'" type="info" @click="router.push('/orders')">查看订单</el-button>
            <el-button v-if="asset.status === 'shipped'" type="info" @click="router.push('/orders')">查看物流</el-button>
          </div>
          <el-alert v-if="!asset.canRecycle && !asset.canShip && !asset.canExchange" title="当前状态下无可执行操作" type="info" show-icon :closable="false" />
        </el-card>
      </el-col>
    </el-row>

    <!-- 回收确认弹窗 -->
    <el-dialog v-model="showRecycleDialog" title="确认回收" width="420px">
      <div class="recycle-dialog">
        <div class="recycle-item">
          <img :src="asset.productImage" :alt="asset.productName" class="recycle-img" />
          <div>
            <div style="font-weight: 600">{{ asset.productName }}</div>
            <el-tag :style="{ color: rarityColor(asset.rarity), borderColor: rarityColor(asset.rarity) }" size="small" effect="plain">
              {{ rarityLabel(asset.rarity) }}
            </el-tag>
          </div>
        </div>
        <el-divider />
        <div class="recycle-points">
          <span>预计返还积分：</span>
          <strong style="color: #67c23a; font-size: 20px">{{ asset.recyclablePoints }}</strong>
        </div>
        <el-alert title="回收后资产状态将变为已回收，不能再发货或换物，且不可撤销" type="warning" show-icon :closable="false" />
      </div>
      <template #footer>
        <el-button @click="showRecycleDialog = false">取消</el-button>
        <el-button type="danger" :loading="recycling" @click="handleRecycle">确认回收</el-button>
      </template>
    </el-dialog>

    <!-- 发布换物弹窗 -->
    <el-dialog v-model="showExchangeDialog" title="发布换物" width="500px">
      <el-form :model="exchangeForm" label-width="80px">
        <el-form-item label="商品">
          <div style="display: flex; align-items: center; gap: 8px">
            <img :src="asset.productImage" style="width: 40px; height: 40px; border-radius: 4px; object-fit: cover" />
            <span>{{ asset.productName }}</span>
          </div>
        </el-form-item>
        <el-form-item label="期望换取" required>
          <el-input v-model="exchangeForm.expectDescription" type="textarea" :rows="3" placeholder="请描述你希望换取的商品、角色、系列或稀有度" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="exchangeForm.remark" type="textarea" :rows="2" placeholder="补充商品状态、交换要求等" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showExchangeDialog = false">取消</el-button>
        <el-button type="warning" :loading="publishing" @click="handlePublishExchange">发布</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAssetStore } from '@/stores/asset'
import { ElMessage } from 'element-plus'
import { formatDate, rarityLabel, rarityColor, assetStatusLabel, assetStatusType } from '@/utils/format'

const route = useRoute()
const router = useRouter()
const assetStore = useAssetStore()

const showRecycleDialog = ref(false)
const showExchangeDialog = ref(false)
const recycling = ref(false)
const publishing = ref(false)
const exchangeForm = ref({ expectDescription: '', remark: '' })

const asset = assetStore.currentAsset

onMounted(async () => {
  await assetStore.fetchAssetDetail(route.params.id as string)
})

async function handleRecycle() {
  if (!asset) return
  recycling.value = true
  try {
    const res = await assetStore.recycle(asset.id)
    if (res.code === 0) {
      ElMessage.success(`回收成功，获得 ${res.data.recycledPoints} 积分`)
      showRecycleDialog.value = false
      await assetStore.fetchAssetDetail(asset.id)
    } else {
      ElMessage.error(res.message)
    }
  } finally {
    recycling.value = false
  }
}

async function handleShip() {
  if (!asset) return
  const res = await assetStore.ship(asset.id)
  if (res.code === 0) {
    ElMessage.success('发货申请已提交')
    await assetStore.fetchAssetDetail(asset.id)
  } else {
    ElMessage.error(res.message)
  }
}

async function handlePublishExchange() {
  if (!asset) return
  if (!exchangeForm.value.expectDescription.trim()) {
    ElMessage.warning('请填写期望换取说明')
    return
  }
  publishing.value = true
  try {
    const res = await assetStore.publishExchange(asset.id, exchangeForm.value)
    if (res.code === 0) {
      ElMessage.success('发布成功')
      showExchangeDialog.value = false
      await assetStore.fetchAssetDetail(asset.id)
    } else {
      ElMessage.error(res.message)
    }
  } finally {
    publishing.value = false
  }
}
</script>

<style scoped>
.value-info {
  display: flex;
  gap: 40px;
}

.value-item .label {
  display: block;
  font-size: 13px;
  color: #909399;
  margin-bottom: 4px;
}

.value-item .value {
  font-size: 24px;
  font-weight: 600;
}

.action-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.recycle-dialog {
  text-align: center;
}

.recycle-item {
  display: flex;
  align-items: center;
  gap: 12px;
  justify-content: center;
}

.recycle-img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.recycle-points {
  margin: 16px 0;
  font-size: 16px;
}
</style>
