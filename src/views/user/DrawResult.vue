<template>
  <div class="page-container">
    <div v-if="result" class="result-card">
      <div class="result-animation">
        <div class="glow" :style="{ borderColor: rarityColor(result.rarity) }">
          <img :src="result.prizeImage" :alt="result.prizeName" class="prize-image" />
        </div>
      </div>

      <h2 class="result-title">恭喜获得</h2>
      <h3 class="prize-name" :style="{ color: rarityColor(result.rarity) }">{{ result.prizeName }}</h3>
      <el-tag :style="{ color: rarityColor(result.rarity), borderColor: rarityColor(result.rarity) }" size="large" effect="plain">
        {{ rarityLabel(result.rarity) }}
      </el-tag>

      <div class="result-info">
        <div class="info-item">
          <span class="label">来源</span>
          <span class="value">{{ result.blindBoxName }}</span>
        </div>
        <div class="info-item">
          <span class="label">消耗积分</span>
          <span class="value" style="color: #f56c6c">-{{ result.costPoints }}</span>
        </div>
        <div class="info-item">
          <span class="label">剩余积分</span>
          <span class="value" style="color: #e6a23c">{{ result.remainingPoints }}</span>
        </div>
      </div>

      <el-alert title="商品已进入「我的资产」，可在资产页面查看详情" type="success" show-icon :closable="false" style="margin: 20px 0" />

      <div class="result-actions">
        <el-button type="primary" size="large" @click="router.push('/assets')">查看资产</el-button>
        <el-button size="large" @click="router.push(`/blindbox/${result.blindBoxId}`)">继续抽取</el-button>
        <el-button size="large" @click="router.push('/exchange')">去换物中心</el-button>
      </div>
    </div>

    <div v-else class="empty-tip">
      <p>暂无抽取结果</p>
      <el-button type="primary" @click="router.push('/blindbox')">去盲盒页面</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useBlindBoxStore } from '@/stores/blindbox'
import { rarityLabel, rarityColor } from '@/utils/format'

const router = useRouter()
const blindBoxStore = useBlindBoxStore()
const result = blindBoxStore.drawResult
</script>

<style scoped>
.result-card {
  max-width: 500px;
  margin: 40px auto;
  text-align: center;
  background: #fff;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
}

.result-animation {
  margin-bottom: 20px;
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
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
}

.result-title {
  font-size: 16px;
  color: #909399;
  margin-bottom: 8px;
}

.prize-name {
  font-size: 24px;
  margin-bottom: 12px;
}

.result-info {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-top: 20px;
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

.result-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}
</style>
