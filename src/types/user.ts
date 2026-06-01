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
  name: string
  phone: string
  province: string
  city: string
  district: string
  detail: string
  isDefault: boolean
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
