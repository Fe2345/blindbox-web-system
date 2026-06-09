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
  receiverName: string
  receiverPhone: string
  province: { code: string; name: string; level: number }
  city: { code: string; name: string; level: number }
  district: { code: string; name: string; level: number }
  street: string
  detail: string
  isDefault: boolean
}

export interface AdminUser {
  id: string
  username: string
  phone: string
  role: string
  isActive: boolean
  avatar: string
  dateJoined: string
  lastLogin: string | null
}
