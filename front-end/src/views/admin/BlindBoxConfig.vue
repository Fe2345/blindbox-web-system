<template>
  <div class="page-container">
    <div class="page-header" style="display: flex; justify-content: space-between; align-items: center">
      <h2>盲盒配置</h2>
      <el-button type="primary" @click="showAdd">新增盲盒</el-button>
    </div>

    <el-table :data="blindBoxStore.list" stripe>
      <el-table-column label="封面" width="80">
        <template #default="{ row }">
          <img :src="row.cover" class="cover-img" />
        </template>
      </el-table-column>
      <el-table-column prop="name" label="盲盒名称" width="160" />
      <el-table-column prop="category" label="分类" width="100" />
      <el-table-column label="消耗积分" width="100">
        <template #default="{ row }">{{ row.costPoints }}</template>
      </el-table-column>
      <el-table-column label="剩余库存" width="100">
        <template #default="{ row }">{{ row.prizes.reduce((s: number, p: any) => s + p.remainingQuantity, 0) }}</template>
      </el-table-column>
      <el-table-column label="奖品数" width="80">
        <template #default="{ row }">{{ row.prizes.length }}</template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : row.status === 'inactive' ? 'warning' : 'info'" size="small">
            {{ row.status === 'active' ? '上架中' : row.status === 'inactive' ? '已下架' : '已结束' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="活动时间">
        <template #default="{ row }">{{ row.startTime }} ~ {{ row.endTime }}</template>
      </el-table-column>
      <el-table-column label="操作" width="250" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="showEdit(row)">编辑</el-button>
          <el-button v-if="row.status === 'active'" type="warning" size="small" @click="handleToggle(row.id, 'inactive')">下架</el-button>
          <el-button v-if="row.status === 'inactive'" type="success" size="small" @click="handleToggle(row.id, 'active')">上架</el-button>
          <el-popconfirm title="确认删除该盲盒？删除后奖池也会删除。" @confirm="handleDelete(row.id)">
            <template #reference>
              <el-button type="danger" size="small">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑盲盒' : '新增盲盒'" width="760px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="盲盒名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.category" placeholder="请选择分类" style="width: 100%">
            <el-option label="动漫IP" value="动漫IP" />
            <el-option label="潮玩" value="潮玩" />
            <el-option label="数码" value="数码" />
            <el-option label="生活" value="生活" />
            <el-option label="美妆" value="美妆" />
            <el-option label="食品" value="食品" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" /></el-form-item>
        <el-form-item label="消耗积分"><el-input-number v-model="form.costPoints" :min="1" /></el-form-item>
        <el-form-item label="活动时间">
          <el-date-picker
            v-model="form.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始"
            end-placeholder="结束"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="奖池商品">
          <div class="prize-picker">
            <el-select v-model="selectedProductId" filterable clearable placeholder="选择已上架商品加入奖池" style="width: 100%">
              <el-option
                v-for="product in availableProducts"
                :key="product.id"
                :label="`${product.name} / ${rarityLabel(product.rarity)} / 库存 ${product.stock || 0}`"
                :value="product.id"
              />
            </el-select>
            <el-button type="primary" plain @click="addPrize">加入</el-button>
          </div>
        </el-form-item>
      </el-form>

      <el-table v-if="form.prizes.length" :data="form.prizes" size="small" border>
        <el-table-column label="图片" width="58">
          <template #default="{ row }"><img :src="row.image" class="prize-img" /></template>
        </el-table-column>
        <el-table-column prop="name" label="商品" min-width="160" />
        <el-table-column label="稀有度" width="88">
          <template #default="{ row }">{{ rarityLabel(row.rarity) }}</template>
        </el-table-column>
        <el-table-column label="库存" width="112">
          <template #default="{ row }">
            <el-input-number :model-value="row.remainingQuantity" disabled size="small" style="width: 92px" />
          </template>
        </el-table-column>
        <el-table-column label="概率" width="82">
          <template #default="{ row }">{{ row.probability ? `${formatProbability(row.probability)}%` : '保存后' }}</template>
        </el-table-column>
        <el-table-column label="操作" width="70">
          <template #default="{ $index }">
            <el-button type="danger" link @click="form.prizes.splice($index, 1)">移除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useBlindBoxStore } from '@/stores/admin/blindbox'
import { useProductStore } from '@/stores/admin/product'
import { ElMessage } from 'element-plus'
import { formatProbability, rarityLabel } from '@/utils/format'

const blindBoxStore = useBlindBoxStore()
const productStore = useProductStore()
const dialogVisible = ref(false)
const isEdit = ref(false)
const selectedProductId = ref('')
const form = ref<any>(emptyForm())

const availableProducts = computed(() => {
  const used = new Set(form.value.prizes.map((prize: any) => String(prize.productId || prize.product_id || '')))
  return productStore.list.filter((product) => product.status === 'approved' && product.image && !used.has(String(product.id)))
})

function emptyForm() {
  return {
    id: '',
    name: '',
    cover: '',
    category: '',
    description: '',
    costPoints: 100,
    startTime: '',
    endTime: '',
    dateRange: null,
    prizes: [],
  }
}

function showAdd() {
  isEdit.value = false
  form.value = emptyForm()
  selectedProductId.value = ''
  dialogVisible.value = true
}

function showEdit(row: any) {
  isEdit.value = true
  form.value = { ...row, dateRange: null, prizes: [...(row.prizes || [])] }
  selectedProductId.value = ''
  dialogVisible.value = true
}

function addPrize() {
  const product = productStore.list.find((item) => String(item.id) === String(selectedProductId.value))
  if (!product) {
    ElMessage.warning('请先选择商品')
    return
  }
  form.value.prizes.push({
    productId: product.id,
    name: product.name,
    image: product.image,
    rarity: product.rarity,
    probability: 0,
    weight: 0,
    quantity: product.stock || 0,
    remainingQuantity: product.stock || 0,
    isActive: true,
    ipNameSnapshot: form.value.ipName || '',
    estimatedPoints: product.estimatedPoints,
  })
  selectedProductId.value = ''
}

async function handleSave() {
  if (!form.value.name || !form.value.category) {
    ElMessage.warning('请填写盲盒名称和分类')
    return
  }
  const dateRange = form.value.dateRange as any[] | null
  const { dateRange: _dateRange, prizes, ...basePayload } = form.value
  const payload = {
    ...basePayload,
    startTime: dateRange?.[0] || form.value.startTime || null,
    endTime: dateRange?.[1] || form.value.endTime || null,
  }
  let res
  if (isEdit.value) {
    res = await blindBoxStore.update(form.value.id, payload)
  } else {
    res = await blindBoxStore.save(payload)
  }
  if (res.code !== 200) {
    ElMessage.error(res.message)
    return
  }

  const boxId = res.data?.id || form.value.id
  if (boxId) {
    const prizeRes = await blindBoxStore.savePrizePool(boxId, prizes)
    if (prizeRes.code !== 200) {
      ElMessage.error(prizeRes.message || '盲盒已保存，但奖池保存失败')
      return
    }
  }

  ElMessage.success(isEdit.value ? '修改成功' : '添加成功')
  dialogVisible.value = false
}

async function handleToggle(id: string, status: string) {
  const res = await blindBoxStore.updateStatus(id, status)
  if (res.code === 200) ElMessage.success(status === 'active' ? '已上架' : '已下架')
}

async function handleDelete(id: string) {
  const res = await blindBoxStore.remove(id)
  if (res.code === 200) ElMessage.success('删除成功')
  else ElMessage.error(res.message)
}

onMounted(async () => {
  await Promise.all([blindBoxStore.fetchList(), productStore.fetchList()])
})
</script>

<style scoped>
.cover-img {
  width: 50px;
  height: 40px;
  border-radius: 4px;
  object-fit: cover;
}

.prize-picker {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 10px;
  width: 100%;
}

.prize-img {
  width: 36px;
  height: 36px;
  border-radius: 4px;
  object-fit: cover;
}
</style>
