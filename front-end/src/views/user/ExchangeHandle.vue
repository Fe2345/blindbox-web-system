<template>
  <div class="page-container">
    <el-page-header @back="router.back()" title="返回" content="换物申请处理" />

    <div v-if="loading" v-loading="true" style="min-height: 200px; margin-top: 20px"></div>
    <div v-else-if="applications.length" style="margin-top: 20px">
      <el-card v-for="app in applications" :key="app.id" style="margin-bottom: 16px">
        <div class="app-card">
          <div class="asset-side">
            <h4>我方商品</h4>
            <div class="asset-info">
              <img :src="app.postAssetImage" class="asset-img" />
              <div>
                <div class="asset-name">{{ app.postAssetName }}</div>
                <el-tag :style="{ color: rarityColor(app.postAssetRarity), borderColor: rarityColor(app.postAssetRarity) }" size="small" effect="plain">
                  {{ rarityLabel(app.postAssetRarity) }}
                </el-tag>
              </div>
            </div>
          </div>

          <div class="exchange-arrow">
            <el-icon :size="24"><Switch /></el-icon>
          </div>

          <div class="asset-side">
            <h4>对方商品</h4>
            <div class="asset-info">
              <img :src="app.applicantAssetImage" class="asset-img" />
              <div>
                <div class="asset-name">{{ app.applicantAssetName }}</div>
                <el-tag :style="{ color: rarityColor(app.applicantAssetRarity), borderColor: rarityColor(app.applicantAssetRarity) }" size="small" effect="plain">
                  {{ rarityLabel(app.applicantAssetRarity) }}
                </el-tag>
                <div class="applicant-name">申请人：{{ app.applicantName }}</div>
              </div>
            </div>
          </div>

          <div class="app-meta">
            <div v-if="app.remark" class="remark">备注：{{ app.remark }}</div>
            <div class="status">
              <el-tag :type="app.status === 'pending' ? 'warning' : app.status === 'accepted' ? 'success' : 'danger'">
                {{ app.status === 'pending' ? '待处理' : app.status === 'accepted' ? '已接受' : '已拒绝' }}
              </el-tag>
            </div>
          </div>

          <div v-if="app.status === 'pending'" class="app-actions">
            <el-popconfirm title="接受后双方资产将进入锁定状态，确认接受？" @confirm="handleAccept(app.id)">
              <template #reference>
                <el-button type="success">接受</el-button>
              </template>
            </el-popconfirm>
            <el-button type="danger" @click="handleReject(app.id)">拒绝</el-button>
          </div>
        </div>
      </el-card>
    </div>
    <div v-else class="empty-tip" style="margin-top: 40px">暂无换物申请</div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useExchangeStore } from '@/stores/exchange'
import { useAssetStore } from '@/stores/asset'
import { ElMessage } from 'element-plus'
import { rarityLabel, rarityColor } from '@/utils/format'
import { Switch } from '@element-plus/icons-vue'

const router = useRouter()
const exchangeStore = useExchangeStore()
const assetStore = useAssetStore()
const applications = computed(() => exchangeStore.applications)

async function handleAccept(id: string) {
  const res = await exchangeStore.acceptApp(id)
  if (res.code === 200) {
    ElMessage.success('???')
    await assetStore.fetchAssets()
  } else {
    ElMessage.error(res.message)
  }
}

async function handleReject(id: string) {
  const res = await exchangeStore.rejectApp(id)
  if (res.code === 200) {
    ElMessage.success('???')
    await assetStore.fetchAssets()
  } else {
    ElMessage.error(res.message)
  }
}

onMounted(async () => {
  try {
    const res = await exchangeStore.fetchApplications()
    if (res.code !== 200) {
      ElMessage.error(res.message || '获取换物申请失败')
    }
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.app-card {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: center;
}

.asset-side {
  flex: 1;
  min-width: 200px;
}

.asset-side h4 {
  margin-bottom: 8px;
  color: #606266;
}

.asset-info {
  display: flex;
  gap: 12px;
  align-items: center;
}

.asset-img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.asset-name {
  font-weight: 600;
  margin-bottom: 4px;
}

.applicant-name {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}

.exchange-arrow {
  color: #409eff;
}

.app-meta {
  min-width: 150px;
}

.remark {
  font-size: 13px;
  color: #606266;
  margin-bottom: 8px;
}

.app-actions {
  display: flex;
  gap: 8px;
}
</style>
