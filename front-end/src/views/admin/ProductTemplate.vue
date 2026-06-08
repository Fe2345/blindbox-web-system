<template>
  <div class="page-container">
    <div class="page-header" style="display: flex; justify-content: space-between; align-items: center">
      <h2>商品模板管理</h2>
      <el-button type="primary" @click="showAdd">新增商品</el-button>
    </div>
    <div class="filter-bar">
      <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width: 150px">
        <el-option label="已上架" value="approved" />
        <el-option label="已下架" value="offline" />
        <el-option label="待审核" value="pending" />
      </el-select>
    </div>
    <el-table :data="filteredProducts" stripe>
      <el-table-column label="图片" width="70"><template #default="{ row }"><img :src="row.image" style="width: 40px; height: 40px; border-radius: 4px; object-fit: cover" /></template></el-table-column>
      <el-table-column prop="name" label="商品名称" width="160" />
      <el-table-column prop="category" label="分类" width="100" />
      <el-table-column label="稀有度" width="80"><template #default="{ row }"><el-tag :style="{ color: rarityColor(row.rarity), borderColor: rarityColor(row.rarity) }" size="small" effect="plain">{{ rarityLabel(row.rarity) }}</el-tag></template></el-table-column>
      <el-table-column prop="merchantName" label="商家" width="120" />
      <el-table-column label="库存" width="80"><template #default="{ row }">{{ row.stock }}</template></el-table-column>
      <el-table-column label="估值" width="80"><template #default="{ row }">{{ row.estimatedPoints }}</template></el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }"><el-tag :type="row.status === 'approved' ? 'success' : row.status === 'offline' ? 'info' : 'warning'" size="small">{{ row.status === 'approved' ? '已上架' : row.status === 'offline' ? '已下架' : '待审核' }}</el-tag></template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="showEdit(row)">编辑</el-button>
          <el-popconfirm v-if="row.status === 'approved'" title="确认下架？" @confirm="handleOffline(row.id)">
            <template #reference><el-button type="danger" size="small">下架</el-button></template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑商品' : '新增商品'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="商品名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="分类"><el-input v-model="form.category" /></el-form-item>
        <el-form-item label="稀有度">
          <el-select v-model="form.rarity" style="width: 100%">
            <el-option label="普通(N)" value="N" /><el-option label="稀有(R)" value="R" />
            <el-option label="超稀有(SR)" value="SR" /><el-option label="传说(SSR)" value="SSR" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" /></el-form-item>
        <el-form-item label="库存"><el-input-number v-model="form.stock" :min="0" /></el-form-item>
        <el-form-item label="估值积分"><el-input-number v-model="form.estimatedPoints" :min="0" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useProductStore } from '@/stores/admin/product'
import { ElMessage } from 'element-plus'
import { rarityLabel, rarityColor } from '@/utils/format'

const productStore = useProductStore()
const filterStatus = ref('')
const dialogVisible = ref(false)
const isEdit = ref(false)
const form = ref({ id: '', name: '', category: '', rarity: 'N', description: '', stock: 0, estimatedPoints: 0 })

const filteredProducts = computed(() => {
  if (!filterStatus.value) return productStore.list
  return productStore.list.filter((p) => p.status === filterStatus.value)
})

function showAdd() { isEdit.value = false; form.value = { id: '', name: '', category: '', rarity: 'N', description: '', stock: 0, estimatedPoints: 0 }; dialogVisible.value = true }
function showEdit(row: any) { isEdit.value = true; form.value = { ...row }; dialogVisible.value = true }
async function handleSave() {
  if (!form.value.name || !form.value.category) {
    ElMessage.warning('请填写商品名称和分类')
    return
  }
  let res
  if (isEdit.value) {
    res = await productStore.update(form.value.id, form.value)
  } else {
    res = await productStore.save(form.value)
  }
  if (res.code === 200) {
    ElMessage.success(isEdit.value ? '修改成功' : '添加成功')
    dialogVisible.value = false
  }
}
async function handleOffline(id: string) {
  const res = await productStore.offline(id)
  if (res.code === 200) ElMessage.success('已下架')
}

onMounted(() => productStore.fetchList())
</script>
