<template>
  <div class="page-container">
    <div class="page-header"><h2>操作日志</h2></div>
    <el-table :data="logStore.logs" stripe>
      <el-table-column prop="operator" label="操作人" width="120" />
      <el-table-column prop="action" label="操作类型" width="120" />
      <el-table-column prop="target" label="操作对象" width="160" />
      <el-table-column prop="detail" label="操作详情" />
      <el-table-column label="时间" width="180"><template #default="{ row }">{{ row.createdAt }}</template></el-table-column>
    </el-table>
    <div v-if="!logStore.logs.length" class="empty-tip">暂无操作日志</div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useLogStore } from '@/stores/admin/log'

const logStore = useLogStore()
onMounted(() => logStore.fetchLogs())
</script>
