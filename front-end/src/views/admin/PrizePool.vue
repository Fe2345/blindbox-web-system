<template>
  <div class="page-container">
    <div class="page-header"><h2>奖池概率配置</h2></div>

    <el-alert
      title="概率由系统按资产估值期望自动计算：长期资产估值接近单抽消耗，全部回收约返还一半；同一稀有度内按商品估值分配，估值越高概率越低。"
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

      <div class="add-prize-row">
        <el-select
          v-model="selectedProductIds[box.id]"
          filterable
          clearable
          placeholder="选择已上架商品加入奖池"
          style="width: 360px"
        >
          <el-option
            v-for="product in availableProducts(box)"
            :key="product.id"
            :label="`${product.name} / ${rarityLabel(product.rarity)} / 库存 ${product.stock || 0}`"
            :value="product.id"
          />
        </el-select>
        <el-button type="primary" plain @click="addProductToBox(box)">加入奖池</el-button>
      </div>

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
            <el-input-number :model-value="row.remainingQuantity" disabled size="small" style="width: 100px" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="90">
          <template #default="{ $index }">
            <el-button type="danger" link @click="box.prizes.splice($index, 1)">移除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pool-footer">
        <span>当前显示合计：{{ formatProbability(totalProb(box.prizes)) }}%；保存后系统会重算概率并自动更新封面</span>
        <el-button type="primary" size="small" @click="handleSave(box)">按规则重算并保存</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { useBlindBoxStore } from '@/stores/admin/blindbox'
import { useProductStore } from '@/stores/admin/product'
import { ElMessage } from 'element-plus'
import { rarityLabel, rarityColor, formatProbability } from '@/utils/format'

const blindBoxStore = useBlindBoxStore()
const productStore = useProductStore()
const selectedProductIds = reactive<Record<string, string>>({})

function totalProb(prizes: any[]) {
  return prizes.reduce((sum, p) => sum + Number(p.probability), 0)
}

function availableProducts(box: any) {
  const used = new Set(box.prizes.map((prize: any) => String(prize.productId || prize.product_id || '')))
  return productStore.list.filter((product) => {
    return product.status === 'approved' && product.image && !used.has(String(product.id))
  })
}

function addProductToBox(box: any) {
  const productId = selectedProductIds[box.id]
  const product = productStore.list.find((item) => String(item.id) === String(productId))
  if (!product) {
    ElMessage.warning('请先选择商品')
    return
  }
  box.prizes.push({
    productId: product.id,
    name: product.name,
    image: product.image,
    rarity: product.rarity,
    probability: 0,
    weight: 0,
    quantity: product.stock || 0,
    remainingQuantity: product.stock || 0,
    isActive: true,
    ipNameSnapshot: box.ipName || '',
    estimatedPoints: product.estimatedPoints,
  })
  selectedProductIds[box.id] = ''
}

async function handleSave(box: any) {
  if (!box.prizes.length) {
    ElMessage.warning('请先添加奖池商品')
    return
  }
  const res = await blindBoxStore.savePrizePool(box.id, box.prizes)
  if (res.code === 200) {
    ElMessage.success('奖池概率已按规则重算')
    await blindBoxStore.fetchList()
  } else {
    ElMessage.error(res.message)
  }
}

onMounted(async () => {
  await Promise.all([blindBoxStore.fetchList(), productStore.fetchList()])
})
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

.add-prize-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.prize-img {
  width: 36px;
  height: 36px;
  border-radius: 4px;
  object-fit: cover;
}
</style>
