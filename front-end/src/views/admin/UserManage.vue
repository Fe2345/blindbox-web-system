<template>
  <div class="page-container">
    <div class="page-header"><h2>用户管理</h2></div>
    <div class="filter-bar">
      <el-input v-model="searchKey" placeholder="搜索用户名或手机号" prefix-icon="Search" style="width: 250px" clearable />
      <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width: 150px">
        <el-option label="正常" value="active" />
        <el-option label="已冻结" value="inactive" />
      </el-select>
    </div>
    <el-table :data="filteredUsers" stripe>
      <el-table-column prop="username" label="用户名" width="120" />
      <el-table-column prop="phone" label="手机号" width="130" />
      <el-table-column label="角色" width="80"><template #default="{ row }">{{ row.role === 'admin' ? '管理员' : row.role === 'merchant' ? '商家' : '用户' }}</template></el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.isActive ? 'success' : 'danger'" size="small">{{ row.isActive ? '正常' : '已冻结' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="注册时间" width="170"><template #default="{ row }">{{ row.dateJoined }}</template></el-table-column>
      <el-table-column label="最后登录" width="170"><template #default="{ row }">{{ row.lastLogin || '从未登录' }}</template></el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-popconfirm v-if="row.isActive" title="确认冻结该用户？" @confirm="handleFreeze(row.id)">
            <template #reference><el-button type="danger" size="small">冻结</el-button></template>
          </el-popconfirm>
          <el-button v-else type="success" size="small" @click="handleUnfreeze(row.id)">解冻</el-button>
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
    if (filterStatus.value === 'active' && !u.isActive) return false
    if (filterStatus.value === 'inactive' && u.isActive) return false
    return true
  })
})

async function handleFreeze(id: string) {
  const res = await userStore.updateStatus(id, false)
  if (res.code === 200) ElMessage.success('已冻结')
}
async function handleUnfreeze(id: string) {
  const res = await userStore.updateStatus(id, true)
  if (res.code === 200) ElMessage.success('已解冻')
}

onMounted(() => userStore.fetchList())
</script>
