<template>
  <div class="page-container" v-if="box">
    <el-page-header @back="router.push('/blindbox')" :title="'返回列表'" :content="box.name" />

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
              <div class="info-row"><span>单次消耗：</span><strong style="color: #e6a23c">{{ box.costPoints }} 积分</strong></div>
              <div class="info-row"><span>剩余库存：</span>{{ box.prizes.reduce((s, p) => s + p.remainingQuantity, 0) }}</div>
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
              <div class="prize-stock">库存：{{ prize.remainingQuantity }}</div>
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
              <template #default="{ row }">{{ row.probability }}%</template>
            </el-table-column>
          </el-table>
        </el-card>

        <el-card style="margin-top: 16px">
          <template #header>
            <span>抽取操作</span>
          </template>
          <div class="draw-section">
            <div class="points-info">
              <span>当前积分：</span>
              <strong>{{ userStore.userInfo?.points || 0 }}</strong>
            </div>
            <div class="points-info">
              <span>本次消耗：</span>
              <strong style="color: #f56c6c">-{{ box.costPoints }}</strong>
            </div>
            <el-divider />
            <el-button
              type="warning"
              size="large"
              style="width: 100%"
              :disabled="box.status === 'ended' || box.prizes.reduce((s, p) => s + p.remainingQuantity, 0) <= 0 || (userStore.userInfo?.points || 0) < box.costPoints"
              :loading="drawing"
              @click="handleDraw"
            >
              立即抽取
            </el-button>
            <div v-if="(userStore.userInfo?.points || 0) < box.costPoints" class="warn-tip">积分不足，无法抽取</div>
            <div v-if="box.prizes.reduce((s, p) => s + p.remainingQuantity, 0) <= 0" class="warn-tip">库存不足</div>
            <div v-if="box.status === 'ended'" class="warn-tip">活动已结束</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBlindBoxStore } from '@/stores/blindbox'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { rarityLabel, rarityColor } from '@/utils/format'

const route = useRoute()
const router = useRouter()
const blindBoxStore = useBlindBoxStore()
const userStore = useUserStore()
const drawing = ref(false)

const box = blindBoxStore.currentBox

onMounted(async () => {
  const id = route.params.id as string
  await blindBoxStore.fetchBlindBoxDetail(id)
  if (!userStore.userInfo) {
    await userStore.fetchUserInfo()
  }
})

async function handleDraw() {
  if (!box) return
  drawing.value = true
  try {
    const res = await blindBoxStore.draw(box.id)
    if (res.code === 0) {
      ElMessage.success('抽取成功！')
      router.push('/draw-result')
    } else {
      ElMessage.error(res.message)
    }
  } finally {
    drawing.value = false
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

.points-info {
  margin-bottom: 8px;
  font-size: 15px;
}

.warn-tip {
  margin-top: 8px;
  color: #f56c6c;
  font-size: 13px;
}
</style>
