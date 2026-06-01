<template>
  <div class="page-container">
    <div class="page-header"><h2>奖池概率配置</h2></div>

    <el-card v-for="box in blindBoxStore.list" :key="box.id" style="margin-bottom: 16px">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span>{{ box.name }} <el-tag size="small" type="info">{{ box.category }}</el-tag></span>
          <el-tag :type="box.status === 'active' ? 'success' : 'info'" size="small">{{ box.status === 'active' ? '上架中' : '未上架' }}</el-tag>
        </div>
      </template>

      <el-table :data="box.prizes" stripe size="small">
        <el-table-column label="图片" width="60"><template #default="{ row }"><img :src="row.image" style="width: 36px; height: 36px; border-radius: 4px; object-fit: cover" /></template></el-table-column>
        <el-table-column prop="name" label="奖品名称" width="160" />
        <el-table-column label="稀有度" width="80">
          <template #default="{ row }"><el-tag :style="{ color: rarityColor(row.rarity), borderColor: rarityColor(row.rarity) }" size="small" effect="plain">{{ rarityLabel(row.rarity) }}</el-tag></template>
        </el-table-column>
        <el-table-column label="概率(%)" width="120">
          <template #default="{ row }"><el-input-number v-model="row.probability" :min="0" :max="100" size="small" style="width: 90px" /></template>
        </el-table-column>
        <el-table-column label="剩余库存" width="120">
          <template #default="{ row }"><el-input-number v-model="row.remainingQuantity" :min="0" size="small" style="width: 90px" /></template>
        </el-table-column>
      </el-table>

      <div style="margin-top: 12px; display: flex; justify-content: space-between; align-items: center">
        <span :style="{ color: totalProb(box.prizes) === 100 ? '#67c23a' : '#f56c6c' }">
          概率合计：{{ totalProb(box.prizes) }}% {{ totalProb(box.prizes) === 100 ? '✓' : '(需等于100%)' }}
        </span>
        <el-button type="primary" size="small" :disabled="totalProb(box.prizes) !== 100" @click="handleSave(box)">保存配置</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useBlindBoxStore } from '@/stores/admin/blindbox'
import { ElMessage } from 'element-plus'
import { rarityLabel, rarityColor } from '@/utils/format'

const blindBoxStore = useBlindBoxStore()

function totalProb(prizes: any[]) {
  return prizes.reduce((sum, p) => sum + p.probability, 0)
}

async function handleSave(box: any) {
  const res = await blindBoxStore.savePrizePool(box.id, box.prizes)
  if (res.code === 0) ElMessage.success('保存成功')
  else ElMessage.error(res.message)
}

onMounted(() => blindBoxStore.fetchList())
</script>
