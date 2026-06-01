<template>
  <div class="page-container">
    <div class="page-header"><h2>用户管理</h2></div>
    <div class="filter-bar">
      <el-input v-model="searchKey" placeholder="搜索用户名或手机号" prefix-icon="Search" style="width: 250px" clearable />
      <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width: 150px">
        <el-option label="正常" value="active" />
        <el-option label="已冻结" value="frozen" />
      </el-select>
    </div>
    <el-table :data="filteredUsers" stripe>
      <el-table-column prop="username" label="用户名" width="120" />
      <el-table-column prop="phone" label="手机号" width="130" />
      <el-table-column prop="email" label="邮箱" width="180" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'danger'" size="small">{{ row.status === 'active' ? '正常' : '已冻结' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="积分" width="100"><template #default="{ row }">{{ row.points }}</template></el-table-column>
      <el-table-column label="资产数" width="80"><template #default="{ row }">{{ row.assetCount }}</template></el-table-column>
      <el-table-column label="订单数" width="80"><template #default="{ row }">{{ row.orderCount }}</template></el-table-column>
      <el-table-column label="注册时间" width="120"><template #default="{ row }">{{ row.createdAt }}</template></el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-popconfirm v-if="row.status === 'active'" title="确认冻结该用户？" @confirm="handleFreeze(row.id)">
            <template #reference><el-button type="danger" size="small">冻结</el-button></template>
          </el-popconfirm>
          <el-button v-if="row.status === 'frozen'" type="success" size="small" @click="handleUnfreeze(row.id)">解冻</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/admin/user'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const searchKey = ref('')
const filterStatus = ref('')

const filteredUsers = computed(() => {
  return userStore.list.filter((u) => {
    if (searchKey.value && !u.username.includes(searchKey.value) && !u.phone.includes(searchKey.value)) return false
    if (filterStatus.value && u.status !== filterStatus.value) return false
    return true
  })
})

async function handleFreeze(id: string) {
  const res = await userStore.updateStatus(id, 'frozen')
  if (res.code === 200) ElMessage.success('已冻结')
}
async function handleUnfreeze(id: string) {
  const res = await userStore.updateStatus(id, 'active')
  if (res.code === 200) ElMessage.success('已解冻')
}

onMounted(() => userStore.fetchList())
</script>
