<template>
  <div class="page-container">
    <div class="page-header">
      <h2>盲盒抽取</h2>
    </div>

    <div class="filter-bar">
      <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width: 150px">
        <el-option label="进行中" value="active" />
        <el-option label="已下架" value="inactive" />
        <el-option label="已结束" value="ended" />
      </el-select>
      <el-input v-model="searchKey" placeholder="搜索感兴趣的动漫IP" prefix-icon="Search" style="width: 250px" clearable />
    </div>

    <div v-if="filteredBoxes.length" class="card-grid">
      <div v-for="box in filteredBoxes" :key="box.id" class="item-card" @click="router.push(`/blindbox/${box.id}`)">
        <img :src="box.cover" :alt="box.name" class="card-image" />
        <div class="card-body">
          <div class="card-title">{{ box.name }}</div>
          <div class="card-meta">分类：{{ box.category }}</div>
          <div class="card-meta">消耗积分：{{ box.costPoints }}</div>
          <div class="card-meta">
            <el-tag v-if="isOutOfStock(box)" type="danger" size="small">待补货</el-tag>
            <el-tag v-else type="success" size="small">可抽取</el-tag>
          </div>
        </div>
        <div class="card-actions">
          <el-tag :type="box.status === 'active' ? 'success' : box.status === 'inactive' ? 'warning' : 'info'" size="small">
            {{ box.status === 'active' ? '进行中' : box.status === 'inactive' ? '已下架' : '已结束' }}
          </el-tag>
          <el-button size="small" type="primary" @click.stop="router.push(`/blindbox/${box.id}`)">查看详情</el-button>
        </div>
      </div>
    </div>
    <div v-else class="empty-tip">当前暂无可抽取盲盒，请稍后查看</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBlindBoxStore } from '@/stores/blindbox'

const router = useRouter()
const blindBoxStore = useBlindBoxStore()

const filterStatus = ref('')
const searchKey = ref('')

function isOutOfStock(box: any) {
  return box.prizes.every((p: any) => p.availableForShipping <= 0)
}

const filteredBoxes = computed(() => {
  return blindBoxStore.blindBoxes.filter((b) => {
    if (filterStatus.value && b.status !== filterStatus.value) return false
    if (searchKey.value && !b.name.includes(searchKey.value)) return false
    return true
  })
})

onMounted(() => blindBoxStore.fetchBlindBoxes())
</script>
