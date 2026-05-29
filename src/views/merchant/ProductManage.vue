<template>
  <div class="page-container">
    <div class="page-header" style="display: flex; justify-content: space-between; align-items: center">
      <h2>商品管理</h2>
      <el-button type="primary" @click="router.push('/products/submit')">
        <el-icon><Plus /></el-icon> 提交商品
      </el-button>
    </div>

    <div class="filter-bar">
      <el-input v-model="keyword" placeholder="搜索商品名称" style="width: 200px" clearable @clear="loadData" @keyup.enter="loadData" />
      <el-select v-model="statusFilter" placeholder="审核状态" clearable style="width: 140px" @change="loadData">
        <el-option label="待审核" value="pending" />
        <el-option label="已通过" value="approved" />
        <el-option label="已驳回" value="rejected" />
        <el-option label="已下架" value="offline" />
      </el-select>
      <el-button @click="loadData">查询</el-button>
    </div>

    <el-card>
      <el-table :data="filtered" v-loading="loading" stripe>
        <el-table-column label="商品图片" width="80">
          <template #default="{ row }">
            <el-image :src="row.image" style="width: 50px; height: 50px; border-radius: 4px" fit="cover" />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="商品名称" min-width="140" />
        <el-table-column prop="category" label="分类" width="80" />
        <el-table-column label="稀有度" width="80">
          <template #default="{ row }">
            <span :style="{ color: rarityColor(row.rarity), fontWeight: 600 }">{{ rarityLabel(row.rarity) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="stock" label="库存" width="70" />
        <el-table-column label="审核状态" width="100">
          <template #default="{ row }">
            <el-tag :type="productStatusType(row.status)" size="small">{{ productStatusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createdAt" label="提交时间" width="110" />
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="viewDetail(row)">详情</el-button>
            <el-button link type="primary" size="small" @click="router.push(`/products/edit/${row.id}`)">修改</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="detailVisible" title="商品详情" width="500px">
      <el-descriptions :column="1" border v-if="currentProduct">
        <el-descriptions-item label="商品名称">{{ currentProduct.name }}</el-descriptions-item>
        <el-descriptions-item label="分类">{{ currentProduct.category }}</el-descriptions-item>
        <el-descriptions-item label="稀有度">
          <span :style="{ color: rarityColor(currentProduct.rarity), fontWeight: 600 }">{{ rarityLabel(currentProduct.rarity) }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="库存">{{ currentProduct.stock }}</el-descriptions-item>
        <el-descriptions-item label="审核状态">
          <el-tag :type="productStatusType(currentProduct.status)">{{ productStatusLabel(currentProduct.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="商品描述">{{ currentProduct.description }}</el-descriptions-item>
        <el-descriptions-item label="提交时间">{{ currentProduct.createdAt }}</el-descriptions-item>
      </el-descriptions>
      <el-alert v-if="currentProduct?.status === 'rejected' && currentProduct.reviewNote" :title="'驳回原因：' + currentProduct.reviewNote" type="error" show-icon :closable="false" style="margin-top: 12px" />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMerchantProductStore } from '@/stores/merchant/product'
import { Plus } from '@element-plus/icons-vue'
import type { MerchantProduct } from '@/types/merchant-self'

const router = useRouter()
const productStore = useMerchantProductStore()
const loading = ref(false)
const keyword = ref('')
const statusFilter = ref('')
const detailVisible = ref(false)
const currentProduct = ref<MerchantProduct | null>(null)

const filtered = computed(() => {
  let list = productStore.list
  if (statusFilter.value) list = list.filter((p) => p.status === statusFilter.value)
  if (keyword.value) list = list.filter((p) => p.name.includes(keyword.value))
  return list
})

function rarityLabel(r: string) {
  const map: Record<string, string> = { N: '普通', R: '稀有', SR: '超稀有', SSR: '传说' }
  return map[r] || r
}

function rarityColor(r: string) {
  const map: Record<string, string> = { N: '#909399', R: '#409EFF', SR: '#E6A23C', SSR: '#F56C6C' }
  return map[r] || '#909399'
}

function productStatusLabel(s: string) {
  const map: Record<string, string> = { pending: '待审核', approved: '审核通过', rejected: '审核驳回', offline: '已下架' }
  return map[s] || s
}

function productStatusType(s: string) {
  const map: Record<string, string> = { pending: 'warning', approved: 'success', rejected: 'danger', offline: 'info' }
  return map[s] || 'info'
}

function viewDetail(row: MerchantProduct) {
  currentProduct.value = row
  detailVisible.value = true
}

async function loadData() {
  loading.value = true
  await productStore.fetchList()
  loading.value = false
}

onMounted(() => loadData())
</script>
