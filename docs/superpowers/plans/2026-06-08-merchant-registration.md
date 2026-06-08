# Merchant Registration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add merchant self-registration API endpoint and frontend registration page so merchants can create their own accounts.

**Architecture:** Add `MerchantRegisterSerializer` + `MerchantRegisterView` on the backend (following existing merchant patterns), a new `Register.vue` page on the frontend (mirroring `Login.vue` styling), with route/API/store wiring and a link from the login page.

**Tech Stack:** Django REST Framework, Vue 3 + Element Plus + Pinia + TypeScript

---

### Task 1: Add MerchantRegisterSerializer

**Files:**
- Modify: `back-end/apps/merchant/serializers.py`

- [ ] **Step 1: Add serializer class**

Append to `back-end/apps/merchant/serializers.py`:

```python
class MerchantRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=150)
    password = serializers.CharField(min_length=6, max_length=128)
    phone = serializers.CharField(max_length=11)

    def to_internal_value(self, data):
        return super().to_internal_value(keys_to_snake(data))

    def validate_username(self, value):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def validate_phone(self, value):
        if not re.match(r"^1[3-9]\d{9}$", value):
            raise serializers.ValidationError("请输入有效的 11 位手机号")
        return value
```

- [ ] **Step 2: Verify no syntax errors**

Run: `cd back-end && python -c "from apps.merchant.serializers import MerchantRegisterSerializer; print('OK')"`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add back-end/apps/merchant/serializers.py
git commit -m "feat: add MerchantRegisterSerializer for merchant registration"
```

---

### Task 2: Add MerchantRegisterView

**Files:**
- Modify: `back-end/apps/merchant/views.py`

- [ ] **Step 1: Add view class**

Insert after the imports (line 18) and before `MerchantLoginView` (line 20). Add the serializer import first, then add the view:

Update the import line for serializers (line 12-17) to include `MerchantRegisterSerializer`:

```python
from apps.merchant.serializers import (
    MerchantSerializer, MerchantLoginSerializer, MerchantRegisterSerializer,
    ProductSerializer, ProductWriteSerializer, ProductUpdateSerializer,
    InventorySerializer, InventoryUpdateSerializer, InventoryRecordSerializer,
    ShipmentTaskSerializer, ShipmentConfirmSerializer,
)
```

Add the view before `MerchantLoginView`:

```python
class MerchantRegisterView(APIView):
    """商家注册 — POST /merchant/api/register"""

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        ser = MerchantRegisterSerializer(data=request.data)
        if not ser.is_valid():
            return error(ser.errors, status.HTTP_400_BAD_REQUEST)

        data = ser.validated_data
        user = User.objects.create_user(
            username=data["username"],
            password=data["password"],
            phone=data.get("phone", ""),
        )
        user.role = User.Role.MERCHANT
        user.save(update_fields=["role"])

        Merchant.objects.create(
            user=user,
            phone=data.get("phone", ""),
            status=Merchant.Status.PENDING,
        )
        return success(None, "注册成功")
```

Note: Need to add `User` import. The current views.py doesn't import User directly. Add `User` to the existing imports or use `get_user_model()`:

Add at line 1 area, or use `from django.contrib.auth import authenticate, get_user_model` and do `User = get_user_model()` at top.

Simpler: use the model import. After `from apps.merchant.models import ...` (line 11), add:

Actually `User` isn't imported. The cleanest way: add `from apps.accounts.models import User` after line 11.

- [ ] **Step 2: Verify view loads**

Run: `cd back-end && python -c "from apps.merchant.views import MerchantRegisterView; print('OK')"`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add back-end/apps/merchant/views.py
git commit -m "feat: add MerchantRegisterView for merchant registration"
```

---

### Task 3: Add register URL route

**Files:**
- Modify: `back-end/apps/merchant/urls_merchant.py`

- [ ] **Step 1: Add route**

Update imports to include `MerchantRegisterView`:

```python
from apps.merchant.views import (
    MerchantRegisterView,
    MerchantLoginView, MerchantInfoView,
    ...
)
```

Add route as first pattern in `urlpatterns`:

```python
urlpatterns = [
    # 注册
    path("register", MerchantRegisterView.as_view(), name="merchant-register"),
    # 认证
    path("login", MerchantLoginView.as_view(), name="merchant-login"),
    ...
]
```

- [ ] **Step 2: Verify URL resolves**

Run: `cd back-end && python manage.py check`
Expected: no errors

- [ ] **Step 3: Commit**

```bash
git add back-end/apps/merchant/urls_merchant.py
git commit -m "feat: add merchant register endpoint route"
```

---

### Task 4: Create Register.vue page

**Files:**
- Create: `front-end/src/views/merchant/Register.vue`

- [ ] **Step 1: Create registration page**

```vue
<template>
  <div class="login-page">
    <div class="login-card">
      <h2>商家注册</h2>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="0" size="large">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="phone">
          <el-input v-model="form.phone" placeholder="手机号" prefix-icon="Phone" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input v-model="form.confirmPassword" type="password" placeholder="确认密码" prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" style="width: 100%" @click="handleRegister">注册</el-button>
        </el-form-item>
      </el-form>
      <div class="login-tip">
        已有账号？<router-link to="/login">去登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { merchantRegister } from '@/api/merchant/auth'

const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  username: '',
  phone: '',
  password: '',
  confirmPassword: '',
})

const validateConfirmPassword = (_rule: any, value: string, callback: any) => {
  if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 150, message: '用户名长度 3-150 字符', trigger: 'blur' },
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 128, message: '密码长度 6-128 字符', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' },
  ],
}

async function handleRegister() {
  await formRef.value?.validate()
  loading.value = true
  try {
    const res: any = await merchantRegister({
      username: form.username,
      phone: form.phone,
      password: form.password,
    })
    if (res.code === 200) {
      ElMessage.success('注册成功，请登录')
      router.push('/login')
    } else {
      ElMessage.error(res.message)
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0d2137;
}
.login-card {
  background: #fff;
  border-radius: 12px;
  padding: 40px;
  width: 400px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}
.login-card h2 { text-align: center; margin-bottom: 30px; color: #303133; font-size: 22px; }
.login-tip { text-align: center; margin-top: 12px; color: #909399; font-size: 13px; }
.login-tip a { color: #409eff; text-decoration: none; }
</style>
```

- [ ] **Step 2: Verify file is syntactically valid (TypeScript compilation happens at build time)**

No separate command needed for .vue file validation; the build step will catch issues.

- [ ] **Step 3: Commit**

```bash
git add front-end/src/views/merchant/Register.vue
git commit -m "feat: add merchant registration page"
```

---

### Task 5: Add register route

**Files:**
- Modify: `front-end/src/router/merchant.ts`

- [ ] **Step 1: Add /register route**

Add before the `/login` route:

```typescript
  {
    path: '/register',
    name: 'MerchantRegister',
    component: () => import('@/views/merchant/Register.vue'),
    meta: { noAuth: true },
  },
```

- [ ] **Step 2: Commit**

```bash
git add front-end/src/router/merchant.ts
git commit -m "feat: add /register route for merchant registration"
```

---

### Task 6: Add merchantRegister API function

**Files:**
- Modify: `front-end/src/api/merchant/auth.ts`

- [ ] **Step 1: Add API function**

Append to the file:

```typescript
export function merchantRegister(data: { username: string; password: string; phone: string }) {
  return request.post('/register', data)
}
```

- [ ] **Step 2: Commit**

```bash
git add front-end/src/api/merchant/auth.ts
git commit -m "feat: add merchantRegister API function"
```

---

### Task 7: Add register link to Login.vue

**Files:**
- Modify: `front-end/src/views/merchant/Login.vue`

- [ ] **Step 1: Replace the test account tip with a register link**

Change line 16 from:
```html
      <div class="login-tip">测试账号：merchant / merchant123</div>
```
To:
```html
      <div class="login-tip">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </div>
```

- [ ] **Step 2: Verify the link styling**

The existing `.login-tip` style covers the text, but add link color. Append to the `<style scoped>` block:

```css
.login-tip a { color: #409eff; text-decoration: none; }
```

- [ ] **Step 3: Commit**

```bash
git add front-end/src/views/merchant/Login.vue
git commit -m "feat: add register link to merchant login page"
```

---

### Task 8: End-to-end verification

- [ ] **Step 1: Backend check**

Run: `cd back-end && python manage.py check`
Expected: `System check identified no issues (0 silenced).`

- [ ] **Step 2: Test backend registration endpoint**

Start backend dev server, then test with curl:

```bash
curl -s -X POST http://127.0.0.1:8000/merchant/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testmerchant","password":"test123456","phone":"13800138000"}' | python -m json.tool
```

Expected: `{"code": 200, "message": "注册成功", "data": null}`

- [ ] **Step 3: Verify user created in DB**

Run: `cd back-end && python manage.py shell -c "from apps.accounts.models import User; u = User.objects.get(username='testmerchant'); print(u.role, u.phone)"`
Expected: `merchant 13800138000`

- [ ] **Step 4: Verify Merchant record created**

Run: `cd back-end && python manage.py shell -c "from apps.merchant.models import Merchant; m = Merchant.objects.get(user__username='testmerchant'); print(m.phone, m.status)"`
Expected: `13800138000 pending`

- [ ] **Step 5: Test duplicate username rejection**

```bash
curl -s -X POST http://127.0.0.1:8000/merchant/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testmerchant","password":"test123456","phone":"13800138001"}' | python -m json.tool
```

Expected: error response about duplicate username

- [ ] **Step 6: Frontend type-check and build**

Run: `cd front-end && npx vue-tsc --noEmit 2>&1 | head -30`
Expected: no type errors (some existing unrelated errors may exist, check that Register.vue has no errors)

- [ ] **Step 7: Clean up test data**

```bash
cd back-end && python manage.py shell -c "
from apps.accounts.models import User
from apps.merchant.models import Merchant
User.objects.filter(username='testmerchant').delete()
Merchant.objects.filter(phone='13800138000').delete()
print('cleaned')
"
```
