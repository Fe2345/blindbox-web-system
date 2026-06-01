<template>
  <div class="page-container">
    <div class="page-header">
      <h2>个人中心</h2>
    </div>

    <el-tabs v-model="activeTab">
      <!-- 基本资料 -->
      <el-tab-pane label="基本资料" name="profile">
        <el-card style="max-width: 600px">
          <div class="avatar-section">
            <el-avatar :size="80" :src="profileForm.avatar || undefined">
              {{ profileForm.username?.charAt(0) }}
            </el-avatar>
          </div>
          <el-form :model="profileForm" label-width="80px" style="margin-top: 20px">
            <el-form-item label="用户名">
              <el-input v-model="profileForm.username" />
            </el-form-item>
            <el-form-item label="手机号">
              <el-input v-model="profileForm.phone" />
            </el-form-item>
            <el-form-item label="注册时间">
              <el-input :model-value="profileForm.createdAt" disabled />
            </el-form-item>
            <el-form-item label="账号状态">
              <el-tag :type="profileForm.status === 'active' ? 'success' : 'danger'">
                {{ profileForm.status === 'active' ? '正常' : '冻结' }}
              </el-tag>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="saving" @click="handleSaveProfile">保存修改</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- 收货地址 -->
      <el-tab-pane label="收货地址" name="address">
        <div style="margin-bottom: 16px">
          <el-button type="primary" @click="showAddressDialog(null)">新增地址</el-button>
        </div>

        <el-card v-for="addr in userStore.addresses" :key="addr.id" style="margin-bottom: 12px; max-width: 600px">
          <div class="address-card">
            <div class="address-info">
              <div>
                <strong>{{ addr.receiver_name }}</strong>
                <span style="margin-left: 12px; color: #909399">{{ addr.receiver_phone }}</span>
                <el-tag v-if="addr.is_default" type="success" size="small" style="margin-left: 8px">默认</el-tag>
              </div>
              <div style="color: #606266; margin-top: 4px">
                {{ addr.province?.name }}{{ addr.city?.name }}{{ addr.district?.name }}{{ addr.detail }}
              </div>
            </div>
            <div class="address-actions">
              <el-button size="small" @click="showAddressDialog(addr)">编辑</el-button>
              <el-button v-if="!addr.is_default" size="small" type="success" @click="handleSetDefault(addr)">设为默认</el-button>
              <el-popconfirm title="确认删除该地址？" @confirm="handleDeleteAddress(addr.id)">
                <template #reference>
                  <el-button size="small" type="danger">删除</el-button>
                </template>
              </el-popconfirm>
            </div>
          </div>
        </el-card>

        <div v-if="!userStore.addresses.length" class="empty-tip">暂无收货地址</div>
      </el-tab-pane>

      <!-- 账号安全 -->
      <el-tab-pane label="账号安全" name="security">
        <el-card style="max-width: 600px">
          <el-alert title="密码修改功能暂未开放，敬请期待" type="info" show-icon :closable="false" />
          <el-descriptions :column="1" border style="margin-top: 16px">
            <el-descriptions-item label="登录状态">
              <el-tag type="success">已登录</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="Token有效期">会话期间有效</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-tab-pane>
    </el-tabs>

    <!-- 地址编辑弹窗 -->
    <el-dialog v-model="addressDialogVisible" :title="editingAddress ? '编辑地址' : '新增地址'" width="500px">
      <el-form :model="addressForm" label-width="80px" ref="addressFormRef" :rules="addressRules">
        <el-form-item label="收货人" prop="receiver_name">
          <el-input v-model="addressForm.receiver_name" />
        </el-form-item>
        <el-form-item label="手机号" prop="receiver_phone">
          <el-input v-model="addressForm.receiver_phone" />
        </el-form-item>
        <el-form-item label="省份代码" prop="province_code">
          <el-input v-model="addressForm.province_code" />
        </el-form-item>
        <el-form-item label="城市代码" prop="city_code">
          <el-input v-model="addressForm.city_code" />
        </el-form-item>
        <el-form-item label="区县代码" prop="district_code">
          <el-input v-model="addressForm.district_code" />
        </el-form-item>
        <el-form-item label="街道" prop="street">
          <el-input v-model="addressForm.street" />
        </el-form-item>
        <el-form-item label="详细地址" prop="detail">
          <el-input v-model="addressForm.detail" />
        </el-form-item>
        <el-form-item label="设为默认">
          <el-switch v-model="addressForm.is_default" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="addressDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="savingAddress" @click="handleSaveAddress">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import type { Address } from '@/types/user'

const userStore = useUserStore()
const activeTab = ref('profile')
const saving = ref(false)
const savingAddress = ref(false)
const addressDialogVisible = ref(false)
const editingAddress = ref<Address | null>(null)
const addressFormRef = ref<FormInstance>()

const profileForm = reactive({
  username: '',
  phone: '',
  avatar: '',
  createdAt: '',
  status: 'active' as string,
})

const addressForm = reactive({
  receiver_name: '',
  receiver_phone: '',
  province_code: '',
  city_code: '',
  district_code: '',
  street: '',
  detail: '',
  is_default: false,
})

const addressRules = {
  receiver_name: [{ required: true, message: '请输入收货人', trigger: 'blur' }],
  receiver_phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }],
  province_code: [{ required: true, message: '请输入省份代码', trigger: 'blur' }],
  city_code: [{ required: true, message: '请输入城市代码', trigger: 'blur' }],
  district_code: [{ required: true, message: '请输入区县代码', trigger: 'blur' }],
  detail: [{ required: true, message: '请输入详细地址', trigger: 'blur' }],
}

async function handleSaveProfile() {
  saving.value = true
  try {
    const res = await userStore.updateUserInfo({ username: profileForm.username, phone: profileForm.phone })
    if (res.code === 200) ElMessage.success('保存成功')
    else ElMessage.error(res.message)
  } finally {
    saving.value = false
  }
}

function showAddressDialog(addr: Address | null) {
  editingAddress.value = addr
  if (addr) {
    Object.assign(addressForm, {
      receiver_name: addr.receiver_name,
      receiver_phone: addr.receiver_phone,
      province_code: addr.province?.code || '',
      city_code: addr.city?.code || '',
      district_code: addr.district?.code || '',
      street: addr.street,
      detail: addr.detail,
      is_default: addr.is_default,
    })
  } else {
    Object.assign(addressForm, {
      receiver_name: '', receiver_phone: '',
      province_code: '', city_code: '', district_code: '',
      street: '', detail: '', is_default: false,
    })
  }
  addressDialogVisible.value = true
}

async function handleSaveAddress() {
  await addressFormRef.value?.validate()
  savingAddress.value = true
  try {
    let res
    if (editingAddress.value) {
      res = await userStore.updateAddress(editingAddress.value.id, { ...addressForm })
    } else {
      res = await userStore.addAddress({ ...addressForm })
    }
    if (res.code === 200) {
      ElMessage.success(editingAddress.value ? '修改成功' : '添加成功')
      addressDialogVisible.value = false
    } else {
      ElMessage.error(res.message)
    }
  } finally {
    savingAddress.value = false
  }
}

async function handleSetDefault(addr: Address) {
  const res = await userStore.updateAddress(addr.id, { is_default: true })
  if (res.code === 200) ElMessage.success('设置成功')
  else ElMessage.error(res.message)
}

async function handleDeleteAddress(id: string) {
  const res = await userStore.deleteAddress(id)
  if (res.code === 200) ElMessage.success('删除成功')
  else ElMessage.error(res.message)
}

onMounted(async () => {
  await userStore.fetchUserInfo()
  await userStore.fetchAddresses()
  if (userStore.userInfo) {
    Object.assign(profileForm, userStore.userInfo)
  }
})
</script>

<style scoped>
.avatar-section {
  text-align: center;
}

.address-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.address-actions {
  display: flex;
  gap: 8px;
}
</style>
