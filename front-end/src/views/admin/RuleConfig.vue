<template>
  <div class="page-container">
    <div class="page-header"><h2>规则配置</h2></div>
    <el-card style="max-width: 600px" v-if="ruleStore.rules">
      <el-form :model="form" label-width="140px">
        <el-form-item label="回收返还比例(%)">
          <el-input-number v-model="form.recycleRate" :min="0" :max="100" />
          <span style="margin-left: 8px; color: #909399">用户回收商品时返还估值积分的百分比</span>
        </el-form-item>
        <el-form-item label="新用户赠送积分">
          <el-input-number v-model="form.newUserPoints" :min="0" />
        </el-form-item>
        <el-form-item label="每日抽取上限">
          <el-input-number v-model="form.maxDrawPerDay" :min="1" />
        </el-form-item>
        <el-form-item label="最低抽取积分">
          <el-input-number v-model="form.minPointsToDraw" :min="0" />
        </el-form-item>
        <el-form-item label="订单自动确认天数">
          <el-input-number v-model="form.orderAutoConfirmDays" :min="1" />
          <span style="margin-left: 8px; color: #909399">发货后N天自动确认收货</span>
        </el-form-item>
        <el-form-item label="换物锁定时长(小时)">
          <el-input-number v-model="form.exchangeLockHours" :min="1" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="saving" @click="handleSave">保存配置</el-button>
        </el-form-item>
      </el-form>
      <div style="color: #909399; font-size: 13px; margin-top: 12px">
        上次修改：{{ ruleStore.rules.updatedAt }} by {{ ruleStore.rules.updatedBy }}
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { useRuleStore } from '@/stores/admin/rule'
import { ElMessage } from 'element-plus'

const ruleStore = useRuleStore()
const saving = ref(false)
const form = reactive({
  recycleRate: 30, newUserPoints: 500, maxDrawPerDay: 20,
  minPointsToDraw: 60, orderAutoConfirmDays: 7, exchangeLockHours: 48,
})

watch(() => ruleStore.rules, (r) => {
  if (r) Object.assign(form, r)
}, { immediate: true })

async function handleSave() {
  saving.value = true
  try {
    const res = await ruleStore.saveRules({ ...form })
    if (res.code === 200) ElMessage.success('保存成功')
    else ElMessage.error(res.message)
  } catch { ElMessage.error('保存失败') } finally { saving.value = false }
}

onMounted(() => ruleStore.fetchRules())
</script>
