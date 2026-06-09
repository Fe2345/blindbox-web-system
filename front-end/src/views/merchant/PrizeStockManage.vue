<template>
  <div class="page-container">
    <div class="page-header">
      <h2>奖池库存管理</h2>
    </div>

    <el-tabs v-model="activeTab">
      <!-- 奖池库存 -->
      <el-tab-pane label="奖池库存" name="stock">
        <div v-loading="stockLoading">
          <el-table :data="prizeStockStore.prizeList" stripe>
            <el-table-column label="奖品图片" width="80">
              <template #default="{ row }">
                <img :src="row.image" class="prize-img" />
              </template>
            </el-table-column>
            <el-table-column prop="name" label="奖品名称" min-width="150" />
            <el-table-column label="稀有度" width="80">
              <template #default="{ row }">
                <el-tag :style="{ color: rarityColor(row.rarity), borderColor: rarityColor(row.rarity) }" size="small" effect="plain">
                  {{ rarityLabel(row.rarity) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="blindboxName" label="所属盲盒" min-width="120" />
            <el-table-column prop="availableForShipping" label="可发货库存" width="100" />
            <el-table-column prop="pendingShipmentCount" label="待发货" width="80" />
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="showReplenishDialog(row)">补充库存</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>

      <!-- 待发货订单 -->
      <el-tab-pane label="待发货订单" name="orders">
        <div v-loading="ordersLoading">
          <el-table :data="prizeStockStore.shipmentOrders" stripe>
            <el-table-column label="奖品图片" width="80">
              <template #default="{ row }">
                <img :src="row.prizeImage" class="prize-img" />
              </template>
            </el-table-column>
            <el-table-column prop="prizeName" label="奖品名称" min-width="120" />
            <el-table-column label="稀有度" width="80">
              <template #default="{ row }">
                <el-tag :style="{ color: rarityColor(row.rarity), borderColor: rarityColor(row.rarity) }" size="small" effect="plain">
                  {{ rarityLabel(row.rarity) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="username" label="用户" width="100" />
            <el-table-column prop="blindboxName" label="盲盒" width="120" />
            <el-table-column prop="batchNo" label="批次号" width="160" />
            <el-table-column prop="createdAt" label="抽奖时间" width="160" />
            <el-table-column label="操作" width="100">
              <template #default="{ row }">
                <el-popconfirm title="确认已发货？" @confirm="handleShip(row.id)">
                  <template #reference>
                    <el-button type="success" size="small">确认发货</el-button>
                  </template>
                </el-popconfirm>
              </template>
            </el-table-column>
          </el-table>
          <el-empty v-if="!prizeStockStore.shipmentOrders.length" description="暂无待发货订单" />
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 补充库存弹窗 -->
    <el-dialog v-model="replenishDialogVisible" title="补充库存" width="400px">
      <div v-if="currentPrize">
        <p>奖品：{{ currentPrize.name }}</p>
        <p>当前可发货库存：{{ currentPrize.availableForShipping }}</p>
        <el-form-item label="补充数量" style="margin-top: 16px">
          <el-input-number v-model="replenishQuantity" :min="1" style="width: 100%" />
        </el-form-item>
      </div>
      <template #footer>
        <el-button @click="replenishDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="replenishLoading" @click="handleReplenish">确认补充</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useMerchantPrizeStockStore, type PrizeStockItem } from '@/stores/merchant/prizeStock'
import { ElMessage } from 'element-plus'
import { rarityLabel, rarityColor } from '@/utils/format'

const prizeStockStore = useMerchantPrizeStockStore()
const activeTab = ref('stock')
const stockLoading = ref(false)
const ordersLoading = ref(false)

// 补充库存相关
const replenishDialogVisible = ref(false)
const replenishLoading = ref(false)
const currentPrize = ref<PrizeStockItem | null>(null)
const replenishQuantity = ref(10)

async function loadPrizeList() {
  stockLoading.value = true
  try {
    const res = await prizeStockStore.fetchPrizeList()
    if (res.code !== 200) {
      ElMessage.error(res.message || '获取奖池库存失败')
    }
  } finally {
    stockLoading.value = false
  }
}

async function loadShipmentOrders() {
  ordersLoading.value = true
  try {
    const res = await prizeStockStore.fetchShipmentOrders()
    if (res.code !== 200) {
      ElMessage.error(res.message || '获取待发货订单失败')
    }
  } finally {
    ordersLoading.value = false
  }
}

function showReplenishDialog(prize: PrizeStockItem) {
  currentPrize.value = prize
  replenishQuantity.value = 10
  replenishDialogVisible.value = true
}

async function handleReplenish() {
  if (!currentPrize.value) return
  replenishLoading.value = true
  try {
    const res = await prizeStockStore.replenishStock(currentPrize.value.id, replenishQuantity.value)
    if (res.code === 200) {
      ElMessage.success('补充成功')
      replenishDialogVisible.value = false
      await loadPrizeList()
    } else {
      ElMessage.error(res.message)
    }
  } finally {
    replenishLoading.value = false
  }
}

async function handleShip(recordId: string) {
  const res = await prizeStockStore.confirmShip(recordId)
  if (res.code === 200) {
    ElMessage.success('发货成功')
    await Promise.all([loadShipmentOrders(), loadPrizeList()])
  } else {
    ElMessage.error(res.message)
  }
}

onMounted(() => {
  loadPrizeList()
  loadShipmentOrders()
})
</script>

<style scoped>
.prize-img {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 4px;
}
</style>
