<template>
  <div class="page-container">
    <el-skeleton v-if="loading" :rows="8" animated />

    <el-empty v-else-if="!box" description="盲盒不存在或加载失败">
      <el-button type="primary" @click="router.push('/blindbox')">返回列表</el-button>
    </el-empty>

    <template v-else>
      <el-page-header @back="router.push('/blindbox')" title="返回列表" :content="box.name" />

      <el-row :gutter="24" style="margin-top: 20px">
        <el-col :span="14">
          <el-card>
            <template #header>
              <span>盲盒信息</span>
            </template>
            <div class="box-info">
              <img :src="box.cover" :alt="box.name" class="box-cover" />
              <div class="box-detail">
                <h3>{{ box.name }}</h3>
                <p class="desc">{{ box.description }}</p>
                <div class="info-row"><span>分类：</span>{{ box.category }}</div>
                <div class="info-row"><span>活动时间：</span>{{ box.startTime }} ~ {{ box.endTime }}</div>
                <div class="info-row">
                  <span>单次消耗：</span>
                  <strong style="color: #e6a23c">{{ box.costPoints }} 积分</strong>
                </div>
                <div class="info-row">
                  <span>库存状态：</span>
                  <el-tag v-if="isOutOfStock" type="danger">待补货</el-tag>
                  <el-tag v-else type="success">可抽取</el-tag>
                </div>
              </div>
            </div>
          </el-card>

          <el-card style="margin-top: 16px">
            <template #header>
              <span>奖池商品</span>
            </template>
            <div class="prize-grid">
              <div v-for="prize in box.prizes" :key="prize.id" class="prize-item">
                <img :src="prize.image" :alt="prize.name" class="prize-img" />
                <div class="prize-name">{{ prize.name }}</div>
                <el-tag :color="rarityColor(prize.rarity)" style="color: #fff; border: none" size="small">
                  {{ rarityLabel(prize.rarity) }}
                </el-tag>
              </div>
            </div>
          </el-card>
        </el-col>

        <el-col :span="10">
          <el-card>
            <template #header>
              <span>概率说明</span>
            </template>
            <el-table :data="box.prizes" stripe size="small">
              <el-table-column prop="name" label="奖品" />
              <el-table-column label="稀有度" width="80">
                <template #default="{ row }">
                  <el-tag :style="{ color: rarityColor(row.rarity), borderColor: rarityColor(row.rarity) }" size="small" effect="plain">
                    {{ rarityLabel(row.rarity) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="概率" width="80">
                <template #default="{ row }">{{ formatProbability(row.probability) }}%</template>
              </el-table-column>
              <el-table-column label="估值" width="82">
                <template #default="{ row }">{{ row.estimatedPoints || 0 }} 积分</template>
              </el-table-column>
              <el-table-column label="回收" width="82">
                <template #default="{ row }">{{ row.recyclablePoints || 0 }} 积分</template>
              </el-table-column>
            </el-table>
            <div class="probability-note">
              概率按长期资产估值期望计算；稀有度越高总概率越低，同稀有度内估值越高概率越低。
            </div>
          </el-card>

          <el-card style="margin-top: 16px">
            <template #header>
              <span>抽取操作</span>
            </template>
            <div class="draw-section">
              <div class="points-info">
                <span>当前积分：</span>
                <strong>{{ pointsStore.balance }}</strong>
              </div>
              <div class="points-info">
                <span>本次消耗：</span>
                <strong style="color: #f56c6c">-{{ box.costPoints }}</strong>
              </div>
              <el-divider />
              <div class="draw-actions">
                <el-button
                  type="warning"
                  size="large"
                  :disabled="!canDraw(1)"
                  :loading="drawingCount === 1"
                  @click="handleDraw(1)"
                >
                  单抽
                </el-button>
                <el-button
                  type="warning"
                  size="large"
                  :disabled="!canDraw(5)"
                  :loading="drawingCount === 5"
                  @click="handleDraw(5)"
                >
                  五连抽
                </el-button>
                <el-button
                  type="danger"
                  size="large"
                  :disabled="!canDraw(10)"
                  :loading="drawingCount === 10"
                  @click="handleDraw(10)"
                >
                  十连抽
                </el-button>
              </div>
              <div v-if="pointsStore.balance < box.costPoints" class="warn-tip">积分不足，无法抽取</div>
              <div v-else-if="pointsStore.balance < box.costPoints * 5" class="warn-tip">积分不足，无法五连抽</div>
              <div v-else-if="pointsStore.balance < box.costPoints * 10" class="warn-tip">积分不足，无法十连抽</div>
              <div v-if="isOutOfStock" class="warn-tip">库存不足，请等待商家补货</div>
              <div v-if="box.status === 'ended'" class="warn-tip">活动已结束</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBlindBoxStore } from '@/stores/blindbox'
import { usePointsStore } from '@/stores/points'
import { ElMessage } from 'element-plus'
import { rarityLabel, rarityColor, formatProbability } from '@/utils/format'

const route = useRoute()
const router = useRouter()
const blindBoxStore = useBlindBoxStore()
const pointsStore = usePointsStore()
const drawingCount = ref(0)
const loading = ref(false)

const box = computed(() => blindBoxStore.currentBox)
const isOutOfStock = computed(() => {
  return (box.value?.prizes || []).every((p: any) => p.availableForShipping <= 0)
})
function canDraw(count: number) {
  if (!box.value) return false
  return box.value.status !== 'ended' && !isOutOfStock.value && pointsStore.balance >= box.value.costPoints * count
}

async function loadDetail(id: string) {
  loading.value = true
  blindBoxStore.currentBox = null
  try {
    const res = await blindBoxStore.fetchBlindBoxDetail(id)
    if (res.code !== 200) {
      ElMessage.error(res.message || '盲盒加载失败')
    }
    await pointsStore.fetchBalance()
  } finally {
    loading.value = false
  }
}

onMounted(() => loadDetail(route.params.id as string))

watch(
  () => route.params.id,
  (id) => {
    if (id) loadDetail(id as string)
  },
)

async function handleDraw(count: number) {
  if (!box.value || !canDraw(count)) return
  drawingCount.value = count
  try {
    const res = await blindBoxStore.draw(box.value.id, count)
    if (res.code === 200) {
      ElMessage.success('抽取成功')
      await pointsStore.fetchBalance()
      router.push('/draw-result')
    } else {
      ElMessage.error(res.message)
    }
  } finally {
    drawingCount.value = 0
  }
}
</script>

<style scoped>
.box-info {
  display: flex;
  gap: 20px;
}

.box-cover {
  width: 280px;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
}

.box-detail h3 {
  font-size: 20px;
  margin-bottom: 8px;
}

.box-detail .desc {
  color: #606266;
  margin-bottom: 12px;
}

.info-row {
  margin-bottom: 8px;
  font-size: 14px;
  color: #606266;
}

.info-row span {
  color: #909399;
}

.prize-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.prize-item {
  text-align: center;
  padding: 12px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
}

.prize-img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 8px;
}

.prize-name {
  font-size: 12px;
  margin-bottom: 4px;
  color: #303133;
}

.prize-stock {
  font-size: 11px;
  color: #909399;
  margin-top: 4px;
}

.draw-section {
  text-align: center;
}

.draw-actions {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.draw-actions .el-button {
  margin-left: 0;
}

.points-info {
  margin-bottom: 8px;
  font-size: 15px;
}

.warn-tip {
  margin-top: 8px;
  color: #f56c6c;
  font-size: 13px;
}

.probability-note {
  margin-top: 10px;
  color: #909399;
  font-size: 12px;
  line-height: 1.5;
}
</style>
