<template>
  <div class="page-container">
    <div class="page-header">
      <h2>修改商品</h2>
    </div>

    <el-card v-loading="pageLoading">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" style="max-width: 650px">
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入商品名称" />
        </el-form-item>
        <el-form-item label="商品图片" prop="image">
          <el-input v-model="form.image" placeholder="请输入图片URL" />
          <div v-if="form.image" style="margin-top: 8px">
            <el-image :src="form.image" style="width: 100px; height: 100px; border-radius: 4px" fit="cover" />
          </div>
        </el-form-item>
        <el-form-item label="商品描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入商品描述" />
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
const productId = route.params.id as string

const form = reactive({
  name: '',
  image: '',
  description: '',
})

const rules = {
  name: [{ required: true, message: '请输入商品名称', trigger: 'blur' }],
  image: [{ required: true, message: '请输入商品图片', trigger: 'blur' }],
  description: [{ required: true, message: '请输入商品描述', trigger: 'blur' }],
}

async function loadProduct() {
  pageLoading.value = true
  const res: any = await productStore.fetchDetail(productId)
  if (res.code === 0 && res.data) {
    form.name = res.data.name
    form.image = res.data.image
    form.description = res.data.description
  }
  pageLoading.value = false
}

async function handleSubmit() {
  await formRef.value?.validate()
  loading.value = true
  try {
    const res: any = await productStore.update(productId, form)
    if (res.code === 0) {
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
