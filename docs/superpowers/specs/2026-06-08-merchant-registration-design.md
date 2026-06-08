# 商家注册功能设计

日期：2026-06-08
状态：已确认

## 背景

当前商家注册流程缺失。普通用户注册 `POST /user/api/register/` 只能创建 `role="user"` 的账号，商家角色账号只能通过 Django admin 手动创建。需要补充完整的商家自注册能力。

## 设计决策

- **方案 A**：注册时只需 username + password + phone，与普通用户注册字段一致。注册后得到 `role="merchant"` 账号，登录后去 `/application` 补充商家详细信息。
- 注册时同步创建最小化 `Merchant` 记录（phone 填充，status=pending），确保注册后可以立即登录（`MerchantLoginView` 会检查 Merchant 记录是否存在）。

## 后端改动

### 1. MerchantRegisterSerializer — `back-end/apps/merchant/serializers.py`

```
字段：
  username — 3-150 字符，唯一性校验
  password — 6-128 字符
  phone   — 11 位手机号，正则校验 ^1[3-9]\d{9}$

复用 to_internal_value 的 keys_to_snake 转换
```

### 2. MerchantRegisterView — `back-end/apps/merchant/views.py`

```
POST /merchant/api/register
authentication_classes = []
permission_classes = []

逻辑：
  1. 校验序列化器
  2. User.objects.create_user(username, password, phone, role="merchant")
  3. Merchant.objects.create(user=user, phone=phone, status="pending")
  4. 返回 success("注册成功")
```

### 3. 路由 — `back-end/apps/merchant/urls_merchant.py`

```
path("register", MerchantRegisterView.as_view(), name="merchant-register")
```

## 前端改动

### 4. Register.vue — `front-end/src/views/merchant/Register.vue`

```
表单：用户名、手机号、密码、确认密码
样式：深蓝背景 + 白色卡片，与 Login.vue 一致
成功后跳转 /login
底部有"已有账号？去登录"链接
```

### 5. 路由 — `front-end/src/router/merchant.ts`

```
/register → MerchantRegister，meta: { noAuth: true }
```

### 6. API — `front-end/src/api/merchant/auth.ts`

```
merchantRegister(data) → POST /register
```

### 7. Store — `front-end/src/stores/merchant/auth.ts`

```
register() action
```

### 8. Login.vue 补充

```
底部加"还没有账号？立即注册"链接
```

## 文件清单

| 操作 | 文件路径 |
|------|---------|
| 修改 | `back-end/apps/merchant/serializers.py` |
| 修改 | `back-end/apps/merchant/views.py` |
| 修改 | `back-end/apps/merchant/urls_merchant.py` |
| 新增 | `front-end/src/views/merchant/Register.vue` |
| 修改 | `front-end/src/router/merchant.ts` |
| 修改 | `front-end/src/api/merchant/auth.ts` |
| 修改 | `front-end/src/stores/merchant/auth.ts` |
| 修改 | `front-end/src/views/merchant/Login.vue` |

## 不变更

- 不影响现有普通用户注册
- 不影响商家登录逻辑
- 不影响入驻申请（/application）流程
- 不涉及数据库迁移（Merchant 模型无需修改）
