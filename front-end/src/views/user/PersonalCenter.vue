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
                <strong>{{ addr.receiverName }}</strong>
                <span style="margin-left: 12px; color: #909399">{{ addr.receiverPhone }}</span>
                <el-tag v-if="addr.isDefault" type="success" size="small" style="margin-left: 8px">默认</el-tag>
              </div>
              <div style="color: #606266; margin-top: 4px">
                {{ addr.province?.name }}{{ addr.city?.name }}{{ addr.district?.name }}{{ addr.detail }}
              </div>
            </div>
            <div class="address-actions">
              <el-button size="small" @click="showAddressDialog(addr)">编辑</el-button>
              <el-button v-if="!addr.isDefault" size="small" type="success" @click="handleSetDefault(addr)">设为默认</el-button>
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
          <el-form :model="passwordForm" label-width="100px" ref="passwordFormRef" :rules="passwordRules">
            <el-form-item label="原密码" prop="oldPassword">
              <el-input v-model="passwordForm.oldPassword" type="password" show-password />
            </el-form-item>
            <el-form-item label="新密码" prop="newPassword">
              <el-input v-model="passwordForm.newPassword" type="password" show-password />
            </el-form-item>
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="changingPassword" @click="handleChangePassword">修改密码</el-button>
            </el-form-item>
          </el-form>
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
        <el-form-item label="收货人" prop="receiverName">
          <el-input v-model="addressForm.receiverName" />
        </el-form-item>
        <el-form-item label="手机号" prop="receiverPhone">
          <el-input v-model="addressForm.receiverPhone" />
        </el-form-item>
        <el-form-item label="所在地区" required>
          <el-select v-model="addressForm.provinceCode" placeholder="请选择省份" @change="onProvinceChange" style="width:100%">
            <el-option v-for="d in provinces" :key="d.code" :label="d.name" :value="d.code" />
          </el-select>
        </el-form-item>
        <el-form-item label="" prop="cityCode">
          <el-select v-model="addressForm.cityCode" placeholder="请选择城市" @change="onCityChange" :disabled="!addressForm.provinceCode" style="width:100%">
            <el-option v-for="d in cities" :key="d.code" :label="d.name" :value="d.code" />
          </el-select>
        </el-form-item>
        <el-form-item label="" prop="districtCode">
          <el-select v-model="addressForm.districtCode" placeholder="请选择区县" :disabled="!addressForm.cityCode" style="width:100%">
            <el-option v-for="d in districts" :key="d.code" :label="d.name" :value="d.code" />
          </el-select>
        </el-form-item>
        <el-form-item label="街道" prop="street">
          <el-input v-model="addressForm.street" />
        </el-form-item>
        <el-form-item label="详细地址" prop="detail">
          <el-input v-model="addressForm.detail" />
        </el-form-item>
        <el-form-item label="设为默认">
          <el-switch v-model="addressForm.isDefault" />
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
import { getDivisions, changePassword } from '@/api/user'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import type { Address } from '@/types/user'

interface DivisionOption {
  code: string
  name: string
  level: number
}

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
  receiverName: '',
  receiverPhone: '',
  provinceCode: '',
  cityCode: '',
  districtCode: '',
  street: '',
  detail: '',
  isDefault: false,
})

const addressRules = {
  receiverName: [{ required: true, message: '请输入收货人', trigger: 'blur' }],
  receiverPhone: [{ required: true, message: '请输入手机号', trigger: 'blur' }],
  provinceCode: [{ required: true, message: '请选择省份', trigger: 'change' }],
  cityCode: [{ required: true, message: '请选择城市', trigger: 'change' }],
  districtCode: [{ required: true, message: '请选择区县', trigger: 'change' }],
  detail: [{ required: true, message: '请输入详细地址', trigger: 'blur' }],
}

const provinces = ref<DivisionOption[]>([])
const cities = ref<DivisionOption[]>([])
const districts = ref<DivisionOption[]>([])

async function loadProvinces() {
  const res: any = await getDivisions()
  if (res.code === 200) provinces.value = res.data
}

async function onProvinceChange() {
  addressForm.cityCode = ''
  addressForm.districtCode = ''
  cities.value = []
  districts.value = []
  if (!addressForm.provinceCode) return
  const res: any = await getDivisions(addressForm.provinceCode)
  if (res.code === 200) cities.value = res.data
}

async function onCityChange() {
  addressForm.districtCode = ''
  districts.value = []
  if (!addressForm.cityCode) return
  const res: any = await getDivisions(addressForm.cityCode)
  if (res.code === 200) districts.value = res.data
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

async function showAddressDialog(addr: Address | null) {
  editingAddress.value = addr
  cities.value = []
  districts.value = []

  if (addr) {
    addressForm.receiverName = addr.receiverName
    addressForm.receiverPhone = addr.receiverPhone
    addressForm.provinceCode = addr.province?.code || ''
    addressForm.cityCode = addr.city?.code || ''
    addressForm.districtCode = addr.district?.code || ''
    addressForm.street = addr.street
    addressForm.detail = addr.detail
    addressForm.isDefault = addr.isDefault

    if (addr.province?.code) {
      const cityRes: any = await getDivisions(addr.province.code)
      if (cityRes.code === 200) cities.value = cityRes.data
    }
    if (addr.city?.code) {
      const distRes: any = await getDivisions(addr.city.code)
      if (distRes.code === 200) districts.value = distRes.data
    }
  } else {
    addressForm.receiverName = ''
    addressForm.receiverPhone = ''
    addressForm.provinceCode = ''
    addressForm.cityCode = ''
    addressForm.districtCode = ''
    addressForm.street = ''
    addressForm.detail = ''
    addressForm.isDefault = false
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
  const res = await userStore.updateAddress(addr.id, { isDefault: true })
  if (res.code === 200) ElMessage.success('设置成功')
  else ElMessage.error(res.message)
}

const passwordFormRef = ref<FormInstance>()
const changingPassword = ref(false)
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: '',
})

const validateConfirm = (_rule: any, value: string, callback: any) => {
  if (value !== passwordForm.newPassword) callback(new Error('两次密码不一致'))
  else callback()
}

const passwordRules = {
  oldPassword: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
  newPassword: [{ required: true, message: '请输入新密码', trigger: 'blur' }, { min: 6, message: '密码至少6位', trigger: 'blur' }],
  confirmPassword: [{ required: true, message: '请确认新密码', trigger: 'blur' }, { validator: validateConfirm, trigger: 'blur' }],
}

async function handleChangePassword() {
  await passwordFormRef.value?.validate()
  changingPassword.value = true
  try {
    const res: any = await changePassword({ oldPassword: passwordForm.oldPassword, newPassword: passwordForm.newPassword })
    if (res.code === 200) {
      ElMessage.success('密码修改成功，请重新登录')
      passwordForm.oldPassword = ''
      passwordForm.newPassword = ''
      passwordForm.confirmPassword = ''
      userStore.logout()
      // redirect handled by router guard
    } else {
      ElMessage.error(res.message)
    }
  } finally {
    changingPassword.value = false
  }
}

async function handleDeleteAddress(id: string) {
  const res = await userStore.deleteAddress(id)
  if (res.code === 200) ElMessage.success('删除成功')
  else ElMessage.error(res.message)
}

onMounted(async () => {
  await loadProvinces()
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
