import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/user/Login.vue'),
    meta: { noAuth: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/user/Register.vue'),
    meta: { noAuth: true },
  },
  {
    path: '/',
    component: () => import('@/layouts/UserLayout.vue'),
    children: [
      { path: '', name: 'Home', component: () => import('@/views/user/Home.vue') },
      { path: 'blindbox', name: 'BlindBoxList', component: () => import('@/views/user/BlindBoxList.vue') },
      { path: 'blindbox/:id', name: 'BlindBoxDetail', component: () => import('@/views/user/BlindBoxDetail.vue') },
      { path: 'draw-result', name: 'DrawResult', component: () => import('@/views/user/DrawResult.vue') },
      { path: 'assets', name: 'MyAssets', component: () => import('@/views/user/MyAssets.vue') },
      { path: 'assets/:id', name: 'AssetDetail', component: () => import('@/views/user/AssetDetail.vue') },
      { path: 'exchange', name: 'ExchangeCenter', component: () => import('@/views/user/ExchangeCenter.vue') },
      { path: 'exchange/publish', name: 'PublishExchange', component: () => import('@/views/user/PublishExchange.vue') },
      { path: 'exchange/handle', name: 'ExchangeHandle', component: () => import('@/views/user/ExchangeHandle.vue') },
      { path: 'orders', name: 'MyOrders', component: () => import('@/views/user/MyOrders.vue') },
      { path: 'points', name: 'PointsDetail', component: () => import('@/views/user/PointsDetail.vue') },
      { path: 'transactions', name: 'TransactionRecords', component: () => import('@/views/user/TransactionRecords.vue') },
      { path: 'profile', name: 'PersonalCenter', component: () => import('@/views/user/PersonalCenter.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
  if (!to.meta.noAuth && !isLoggedIn) {
    next('/login')
    return
  }
  if (!to.meta.noAuth && localStorage.getItem('user_role') !== 'user') {
    localStorage.removeItem('isLoggedIn')
    localStorage.removeItem('user_role')
    next('/login')
    return
  }
  next()
})

export default router
