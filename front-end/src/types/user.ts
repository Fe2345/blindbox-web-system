export interface UserInfo {
  id: string
  username: string
  phone: string
  avatar: string
  points: number
  status: 'active' | 'frozen'
  createdAt: string
}

export interface LoginForm {
  username: string
  password: string
}

export interface RegisterForm {
  username: string
  phone: string
  password: string
  confirmPassword: string
}

export interface Address {
  id: string
  receiver_name: string
  receiver_phone: string
  province: { code: string; name: string; level: number }
  city: { code: string; name: string; level: number }
  district: { code: string; name: string; level: number }
  street: string
  detail: string
  is_default: boolean
}

export interface AdminUser {
  id: string
  username: string
  phone: string
  email: string
  status: 'active' | 'frozen'
  points: number
  assetCount: number
  orderCount: number
  createdAt: string
}
