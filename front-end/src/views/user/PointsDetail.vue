<template>
  <div class="page-container">
    <el-page-header @back="router.back()" title="返回" content="积分明细" />

    <el-card style="margin-top: 20px">
      <div class="balance-card">
        <div>
          <span class="balance-label">当前积分余额</span>
          <span class="balance-value">{{ balance }}</span>
          <span class="rate-tip">1 元 = 100 积分</span>
        </div>
        <el-button type="primary" @click="rechargeDialogVisible = true">充值积分</el-button>
      </div>
    </el-card>

    <div class="filter-bar" style="margin-top: 16px">
      <el-select v-model="filterType" placeholder="类型筛选" clearable style="width: 160px">
        <el-option label="盲盒消费" value="blindbox_consume" />
        <el-option label="回收返还" value="recycle_return" />
        <el-option label="积分充值" value="recharge" />
        <el-option label="系统调整" value="system_adjust" />
      </el-select>
    </div>

    <el-table :data="filteredRecords" stripe style="margin-top: 12px">
      <el-table-column label="时间" width="180">
        <template #default="{ row }">{{ formatDate(row.createdAt) }}</template>
      </el-table-column>
      <el-table-column label="类型" width="120">
        <template #default="{ row }">
          <el-tag :type="pointsTagType(row.type)" size="small">
            {{ pointsTypeLabel(row.type) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="说明" />
      <el-table-column label="变动积分" width="120">
        <template #default="{ row }">
          <span :style="{ color: row.amount > 0 ? '#67c23a' : '#f56c6c' }">
            {{ row.amount > 0 ? '+' : '' }}{{ row.amount }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="变动后余额" width="120">
        <template #default="{ row }">{{ row.balance }}</template>
      </el-table-column>
    </el-table>

    <div v-if="!filteredRecords.length" class="empty-tip">暂无积分记录</div>

    <el-dialog v-model="rechargeDialogVisible" title="充值积分" width="420px">
      <div class="recharge-panel">
        <div class="preset-grid">
          <button
            v-for="amount in presetAmounts"
            :key="amount"
            class="preset-button"
            :class="{ active: rechargeAmount === amount }"
            @click="rechargeAmount = amount"
          >
            <span>¥{{ amount }}</span>
            <small>{{ amount * 100 }} 积分</small>
          </button>
        </div>
        <el-input-number v-model="rechargeAmount" :min="1" :max="9999" :precision="2" :step="10" style="width: 100%" />
        <div class="recharge-summary">
          预计到账 <strong>{{ Math.floor(rechargeAmount * 100) }}</strong> 积分
        </div>
      </div>
      <template #footer>
        <el-button @click="rechargeDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="recharging" @click="handleRecharge">确认充值</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { usePointsStore } from '@/stores/points'
import { formatDate, pointsTypeLabel } from '@/utils/format'

const router = useRouter()
const pointsStore = usePointsStore()
const filterType = ref('')
const rechargeDialogVisible = ref(false)
const recharging = ref(false)
const rechargeAmount = ref(30)
const presetAmounts = [6, 30, 68, 128, 328]
const balance = computed(() => pointsStore.balance)

const filteredRecords = computed(() => {
  if (!filterType.value) return pointsStore.records
  return pointsStore.records.filter((r) => r.type === filterType.value)
})

function pointsTagType(type: string) {
  if (type === 'blindbox_consume') return 'danger'
  if (type === 'recycle_return' || type === 'recharge') return 'success'
  return 'info'
}

async function handleRecharge() {
  if (!rechargeAmount.value || rechargeAmount.value <= 0) {
    ElMessage.warning('请输入正确的充值金额')
    return
  }
  recharging.value = true
  try {
    const res: any = await pointsStore.recharge(rechargeAmount.value)
    if (res.code === 200) {
      ElMessage.success(`充值成功，到账 ${res.data.points} 积分`)
      rechargeDialogVisible.value = false
      await pointsStore.fetchBalance()
    }
  } finally {
    recharging.value = false
  }
}

onMounted(async () => {
  await pointsStore.fetchBalance()
  await pointsStore.fetchRecords()
})
</script>

<style scoped>
.balance-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.balance-label {
  display: block;
  font-size: 14px;
  color: #606266;
}

.balance-value {
  display: inline-block;
  margin-top: 6px;
  font-size: 32px;
  font-weight: 700;
  color: #e6a23c;
}

.rate-tip {
  margin-left: 12px;
  color: #909399;
  font-size: 13px;
}

.recharge-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.preset-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.preset-button {
  height: 64px;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  background: #fff;
  color: #303133;
  cursor: pointer;
}

.preset-button.active {
  color: #409eff;
  border-color: #409eff;
  background: #ecf5ff;
}

.preset-button span,
.preset-button small {
  display: block;
}

.preset-button span {
  font-size: 18px;
  font-weight: 700;
}

.preset-button small {
  margin-top: 4px;
  color: #909399;
}

.recharge-summary {
  padding: 10px 12px;
  border-radius: 6px;
  background: #f5f7fa;
  color: #606266;
}
</style>
