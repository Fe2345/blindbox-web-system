<template>
  <div class="page-container">
    <div class="page-header">
      <h2>商品提交</h2>
    </div>

    <el-card>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" style="max-width: 650px">
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入商品名称" />
        </el-form-item>
        <el-form-item label="商品图片" prop="image">
          <div class="product-image-upload" @click="handleImageClick">
            <div v-if="imagePreview" class="image-preview-wrapper">
              <el-image :src="imagePreview" style="width: 120px; height: 120px; border-radius: 4px" fit="cover" />
              <div class="image-preview-overlay">重新上传</div>
            </div>
            <div v-else class="image-upload-placeholder">
              <span class="upload-icon">+</span>
              <span>点击上传图片</span>
            </div>
          </div>
          <span v-if="uploadingImage" style="margin-left: 8px; color: #909399">上传中...</span>
          <input
            ref="imageInputRef"
            type="file"
            accept="image/*"
            style="display: none"
            @change="handleImageChange"
          />
        </el-form-item>
        <el-form-item label="商品描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入商品描述" />
        </el-form-item>
        <el-form-item label="商品分类" prop="category">
          <el-select v-model="form.category" placeholder="请选择分类">
            <el-option label="动漫IP" value="动漫IP" />
            <el-option label="潮玩" value="潮玩" />
            <el-option label="数码" value="数码" />
            <el-option label="生活" value="生活" />
            <el-option label="美妆" value="美妆" />
            <el-option label="食品" value="食品" />
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
        <el-form-item label="初始库存" prop="stock">
          <el-input-number v-model="form.stock" :min="1" :max="99999" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">提交审核</el-button>
          <el-button @click="router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { useMerchantProductStore } from '@/stores/merchant/product'
import { uploadProductImage } from '@/api/merchant/product'

const router = useRouter()
const productStore = useMerchantProductStore()
const formRef = ref<FormInstance>()
const loading = ref(false)
const uploadingImage = ref(false)
const imagePreview = ref('')
const imageInputRef = ref<HTMLInputElement>()
const selectedImageFile = ref<File | null>(null)

const form = reactive({
  name: '',
  image: '',
  description: '',
  category: '',
  rarity: 'N',
  stock: 10,
})

const rules = {
  name: [{ required: true, message: '请输入商品名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入商品描述', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  rarity: [{ required: true, message: '请选择稀有度', trigger: 'change' }],
  stock: [{ required: true, message: '请输入库存数量', trigger: 'blur' }],
}

function handleImageClick() {
  imageInputRef.value?.click()
}

async function handleImageChange(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  const allowed = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
  if (!allowed.includes(file.type)) {
    ElMessage.error('仅支持 JPG、PNG、GIF、WebP 格式')
    input.value = ''
    return
  }

  if (file.size > 2 * 1024 * 1024) {
    ElMessage.error('文件大小不能超过 2MB')
    input.value = ''
    return
  }

  uploadingImage.value = true
  try {
    const res: any = await uploadProductImage(file)
    if (res.code === 200) {
      form.image = res.data.image
      imagePreview.value = res.data.image
      selectedImageFile.value = null
    } else {
      ElMessage.error(res.message)
    }
  } finally {
    uploadingImage.value = false
    input.value = ''
  }
}

async function handleSubmit() {
  await formRef.value?.validate()
  if (!form.image) {
    ElMessage.error('请上传商品图片')
    return
  }
  loading.value = true
  try {
    const res: any = await productStore.submit(form)
    if (res.code === 200) {
      ElMessage.success('商品已提交，等待管理员审核')
      router.push('/products')
    } else {
      ElMessage.error(res.message)
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.product-image-upload {
  cursor: pointer;
  display: inline-block;
}

.image-upload-placeholder {
  width: 120px;
  height: 120px;
  border: 1px dashed #dcdfe6;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
  font-size: 13px;
  transition: border-color 0.2s;
}

.image-upload-placeholder:hover {
  border-color: #409eff;
}

.upload-icon {
  font-size: 24px;
  line-height: 1;
  margin-bottom: 4px;
}

.image-preview-wrapper {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

.image-preview-wrapper .image-preview-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.45);
  color: #fff;
  font-size: 13px;
  border-radius: 4px;
  opacity: 0;
  transition: opacity 0.2s;
}

.image-preview-wrapper:hover .image-preview-overlay {
  opacity: 1;
}
</style>
