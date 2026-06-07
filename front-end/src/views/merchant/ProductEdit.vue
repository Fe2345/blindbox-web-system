<template>
  <div class="page-container">
    <div class="page-header">
      <h2>修改商品</h2>
    </div>

    <el-card v-loading="pageLoading">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" style="max-width: 650px">
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入商品名称" maxlength="100" show-word-limit />
        </el-form-item>
        <el-form-item label="商品图片" prop="image">
          <el-input v-model="form.image" placeholder="请输入图片URL" />
          <div v-if="form.image" style="margin-top: 8px">
            <el-image :src="form.image" style="width: 100px; height: 100px; border-radius: 4px" fit="cover" />
          </div>
        </el-form-item>
        <el-form-item label="商品分类" prop="category">
          <el-select v-model="form.category" placeholder="请选择分类">
            <el-option label="动漫IP" value="动漫IP" />
            <el-option label="潮玩" value="潮玩" />
            <el-option label="数码" value="数码" />
            <el-option label="生活" value="生活" />
            <el-option label="美妆" value="美妆" />
            <el-option label="食品" value="食品" />
            <el-option label="服饰" value="服饰" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="稀有度" prop="rarity">
          <el-radio-group v-model="form.rarity">
            <el-radio value="N">普通 (N)</el-radio>
            <el-radio value="R">稀有 (R)</el-radio>
            <el-radio value="SR">超稀有 (SR)</el-radio>
            <el-radio value="SSR">传说 (SSR)</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="预估积分" prop="estimated_points">
          <el-input-number v-model="form.estimated_points" :min="0" :max="999999" />
        </el-form-item>
        <el-form-item label="商品描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="4" placeholder="请输入商品描述" maxlength="500" show-word-limit />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">保存修改</el-button>
          <el-button @click="router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { useMerchantProductStore } from '@/stores/merchant/product'

const route = useRoute()
const router = useRouter()
const productStore = useMerchantProductStore()
const formRef = ref<FormInstance>()
const loading = ref(false)
const pageLoading = ref(true)
const productId = Number(route.params.id)

const form = reactive({
  name: '',
  image: '',
  description: '',
  category: '',
  rarity: 'N',
  estimated_points: 0,
})

const rules = {
  name: [{ required: true, message: '请输入商品名称', trigger: 'blur' }],
  image: [{ required: true, message: '请输入商品图片URL', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  rarity: [{ required: true, message: '请选择稀有度', trigger: 'change' }],
}

async function loadProduct() {
  pageLoading.value = true
  const res: any = await productStore.fetchDetail(productId)
  if (res.code === 200 && res.data) {
    form.name = res.data.name
    form.image = res.data.image
    form.description = res.data.description || ''
    form.category = res.data.category
    form.rarity = res.data.rarity
    form.estimated_points = res.data.estimated_points
  }
  pageLoading.value = false
}

async function handleSubmit() {
  await formRef.value?.validate()
  loading.value = true
  try {
    const res: any = await productStore.update(productId, form)
    if (res.code === 200) {
      ElMessage.success('修改成功')
      router.push('/products')
    } else {
      ElMessage.error(res.message)
    }
  } catch {
    ElMessage.error('修改失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => loadProduct())
</script>
