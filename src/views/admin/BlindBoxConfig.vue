<template>
  <div class="page-container">
    <div class="page-header" style="display: flex; justify-content: space-between; align-items: center">
      <h2>盲盒配置</h2>
      <el-button type="primary" @click="showAdd">新增盲盒</el-button>
    </div>

    <el-table :data="blindBoxStore.list" stripe>
      <el-table-column label="封面" width="80"><template #default="{ row }"><img :src="row.cover" style="width: 50px; height: 40px; border-radius: 4px; object-fit: cover" /></template></el-table-column>
      <el-table-column prop="name" label="盲盒名称" width="160" />
      <el-table-column prop="category" label="分类" width="100" />
      <el-table-column label="消耗积分" width="100"><template #default="{ row }">{{ row.costPoints }}</template></el-table-column>
      <el-table-column label="库存" width="80"><template #default="{ row }">{{ row.stock }}</template></el-table-column>
      <el-table-column label="奖品数" width="80"><template #default="{ row }">{{ row.prizes.length }}</template></el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : row.status === 'inactive' ? 'warning' : 'info'" size="small">
            {{ row.status === 'active' ? '上架中' : row.status === 'inactive' ? '已下架' : '已结束' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="活动时间"><template #default="{ row }">{{ row.startTime }} ~ {{ row.endTime }}</template></el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="showEdit(row)">编辑</el-button>
          <el-button v-if="row.status === 'active'" type="warning" size="small" @click="handleToggle(row.id, 'inactive')">下架</el-button>
          <el-button v-if="row.status === 'inactive'" type="success" size="small" @click="handleToggle(row.id, 'active')">上架</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑盲盒' : '新增盲盒'" width="550px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="盲盒名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="分类"><el-input v-model="form.category" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" /></el-form-item>
        <el-form-item label="消耗积分"><el-input-number v-model="form.costPoints" :min="1" /></el-form-item>
        <el-form-item label="库存"><el-input-number v-model="form.stock" :min="0" /></el-form-item>
        <el-form-item label="活动时间"><el-date-picker v-model="form.dateRange" type="daterange" range-separator="至" start-placeholder="开始" end-placeholder="结束" style="width: 100%" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="dialogVisible = false">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useBlindBoxStore } from '@/stores/admin/blindbox'
import { ElMessage } from 'element-plus'

const blindBoxStore = useBlindBoxStore()
const dialogVisible = ref(false)
const isEdit = ref(false)
const form = ref({ name: '', category: '', description: '', costPoints: 100, stock: 0, dateRange: null })

function showAdd() { isEdit.value = false; form.value = { name: '', category: '', description: '', costPoints: 100, stock: 0, dateRange: null }; dialogVisible.value = true }
function showEdit(row: any) { isEdit.value = true; form.value = { ...row, dateRange: null }; dialogVisible.value = true }

async function handleToggle(id: string, status: string) {
  const res = await blindBoxStore.updateStatus(id, status)
  if (res.code === 0) ElMessage.success(status === 'active' ? '已上架' : '已下架')
}

onMounted(() => blindBoxStore.fetchList())
</script>
