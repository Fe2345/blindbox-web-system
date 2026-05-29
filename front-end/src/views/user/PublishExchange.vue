<template>
  <div class="page-container">
    <el-page-header @back="router.back()" title="返回" content="发布换物" />

    <el-card style="margin-top: 20px; max-width: 600px">
      <el-form :model="form" label-width="80px" ref="formRef" :rules="rules">
        <el-form-item label="选择资产" prop="assetId">
          <el-select v-model="form.assetId" placeholder="请选择要交换的资产" style="width: 100%">
            <el-option v-for="a in availableAssets" :key="a.id" :label="a.productName" :value="a.id">
              <div style="display: flex; align-items: center; gap: 8px">
                <img :src="a.productImage" style="width: 30px; height: 30px; border-radius: 4px; object-fit: cover" />
                <span>{{ a.productName }}</span>
                <el-tag size="small" :style="{ color: rarityColor(a.rarity) }">{{ rarityLabel(a.rarity) }}</el-tag>
              </div>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item v-if="selectedAsset" label="资产预览">
          <div style="display: flex; gap: 12px; align-items: center">
            <img :src="selectedAsset.productImage" style="width: 80px; height: 80px; border-radius: 4px; object-fit: cover" />
            <div>
              <div style="font-weight: 600">{{ selectedAsset.productName }}</div>
              <el-tag :style="{ color: rarityColor(selectedAsset.rarity), borderColor: rarityColor(selectedAsset.rarity) }" effect="plain" size="small">
                {{ rarityLabel(selectedAsset.rarity) }}
              </el-tag>
              <div style="font-size: 13px; color: #909399; margin-top: 4px">估值：{{ selectedAsset.estimatedPoints }} 积分</div>
            </div>
          </div>
        </el-form-item>

        <el-form-item label="期望换取" prop="expectDescription">
          <el-input v-model="form.expectDescription" type="textarea" :rows="3" placeholder="请描述你希望换取的商品、角色、系列或稀有度" />
        </el-form-item>

        <el-form-item label="备注说明">
          <el-input v-model="form.remark" type="textarea" :rows="2" placeholder="补充商品状态、交换要求等（选填）" />
        </el-form-item>

        <el-form-item>
          <el-button type="warning" :loading="publishing" @click="handlePublish" style="width: 100%">发布换物</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAssetStore } from '@/stores/asset'
import { ElMessage } from 'element-plus'
import { rarityLabel, rarityColor } from '@/utils/format'
import type { FormInstance } from 'element-plus'

const router = useRouter()
const assetStore = useAssetStore()
const formRef = ref<FormInstance>()
const publishing = ref(false)

const form = ref({ assetId: '', expectDescription: '', remark: '' })

const rules = {
  assetId: [{ required: true, message: '请选择资产', trigger: 'change' }],
  expectDescription: [{ required: true, message: '请填写期望换取说明', trigger: 'blur' }],
}

const availableAssets = computed(() => assetStore.assets.filter((a) => a.status === 'available'))
const selectedAsset = computed(() => assetStore.assets.find((a) => a.id === form.value.assetId))

async function handlePublish() {
  await formRef.value?.validate()
  publishing.value = true
  try {
    const res = await assetStore.publishExchange(form.value.assetId, {
      expectDescription: form.value.expectDescription,
      remark: form.value.remark,
    })
    if (res.code === 0) {
      ElMessage.success('发布成功')
      router.push('/exchange')
    } else {
      ElMessage.error(res.message)
    }
  } catch {
    ElMessage.error('发布失败')
  } finally {
    publishing.value = false
  }
}

onMounted(() => assetStore.fetchAssets())
</script>
