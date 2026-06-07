<template>
  <div class="page-container">
    <div class="page-header">
      <h2>操作记录</h2>
    </div>

    <div class="filter-bar">
      <el-select v-model="typeFilter" placeholder="记录类型" clearable style="width: 140px" @change="loadData">
        <el-option label="商品" value="product" />
        <el-option label="商品审核" value="product_review" />
        <el-option label="库存" value="inventory" />
        <el-option label="发货" value="shipment" />
      </el-select>
      <el-button @click="loadData">查询</el-button>
    </div>

    <el-card>
      <el-table :data="recordStore.list" v-loading="recordStore.loading" stripe>
        <el-table-column label="记录类型" width="100">
          <template #default="{ row }">
            <el-tag :type="recordTypeColor(row.type)" size="small">{{ row.type_display }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="操作描述" min-width="300" show-overflow-tooltip />
        <el-table-column prop="created_at" label="时间" width="170" />
      </el-table>

      <div class="pagination-bar" v-if="recordStore.total > 0">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="recordStore.total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next"
          @current-change="loadData"
          @size-change="loadData"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useMerchantRecordStore } from '@/stores/merchant/record'

const recordStore = useMerchantRecordStore()
const typeFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)

function recordTypeColor(type: string) {
  const map: Record<string, string> = {
    product: 'primary',
    product_review: 'warning',
    inventory: 'success',
    shipment: 'danger',
  }
  return map[type] || 'info'
}

async function loadData() {
  await recordStore.fetchList({
    page: currentPage.value,
    page_size: pageSize.value,
    type: typeFilter.value || undefined,
  })
}

onMounted(() => loadData())
</script>

<style scoped>
.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}
.pagination-bar {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
</style>
