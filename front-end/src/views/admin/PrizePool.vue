<template>
  <div class="page-container">
    <div class="page-header"><h2>奖池概率配置</h2></div>

    <el-alert
      title="概率由系统按稀有度自动计算：传说 SSR 固定 6.6%，同一奖池内同稀有度奖品概率一致。"
      type="info"
      show-icon
      :closable="false"
      style="margin-bottom: 16px"
    />

    <el-card v-for="box in blindBoxStore.list" :key="box.id" style="margin-bottom: 16px">
      <template #header>
        <div class="card-header">
          <span>{{ box.name }} <el-tag size="small" type="info">{{ box.category }}</el-tag></span>
          <el-tag :type="box.status === 'active' ? 'success' : 'info'" size="small">
            {{ box.status === 'active' ? '上架中' : '未上架' }}
          </el-tag>
        </div>
      </template>

      <el-table :data="box.prizes" stripe size="small">
        <el-table-column label="图片" width="60">
          <template #default="{ row }">
            <img :src="row.image" class="prize-img" />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="奖品名称" width="180" />
        <el-table-column label="稀有度" width="90">
          <template #default="{ row }">
            <el-tag :style="{ color: rarityColor(row.rarity), borderColor: rarityColor(row.rarity) }" size="small" effect="plain">
              {{ rarityLabel(row.rarity) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="概率" width="100">
          <template #default="{ row }">{{ formatProbability(row.probability) }}%</template>
        </el-table-column>
        <el-table-column label="剩余库存" width="130">
          <template #default="{ row }">
            <el-input-number v-model="row.remainingQuantity" :min="0" size="small" style="width: 100px" />
          </template>
        </el-table-column>
      </el-table>

      <div class="pool-footer">
        <span>显示合计：{{ formatProbability(totalProb(box.prizes)) }}%</span>
        <el-button type="primary" size="small" @click="handleSave(box)">按规则重算并保存</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useBlindBoxStore } from '@/stores/admin/blindbox'
import { ElMessage } from 'element-plus'
import { rarityLabel, rarityColor, formatProbability } from '@/utils/format'

const blindBoxStore = useBlindBoxStore()

function totalProb(prizes: any[]) {
  return prizes.reduce((sum, p) => sum + Number(p.probability), 0)
}

async function handleSave(box: any) {
  const res = await blindBoxStore.savePrizePool(box.id, box.prizes)
  if (res.code === 200) {
    ElMessage.success('奖池概率已按规则重算')
    await blindBoxStore.fetchList()
  } else {
    ElMessage.error(res.message)
  }
}

onMounted(() => blindBoxStore.fetchList())
</script>

<style scoped>
.card-header,
.pool-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.pool-footer {
  margin-top: 12px;
  color: #606266;
}

.prize-img {
  width: 36px;
  height: 36px;
  border-radius: 4px;
  object-fit: cover;
}
</style>
