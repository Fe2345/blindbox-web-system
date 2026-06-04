import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import axios from 'axios'
import App from './App.vue'
import router from './router'
import { setupMock } from './mock'
import './styles/global.css'

// 在 setupMock() 替换 axios.defaults.adapter 之前保存原始 adapter，
// 供 request.ts 使用，确保用户 API 请求直接走真实 XHR，不经过 mock 链路。
;(window as any).__axiosOriginalAdapter = axios.defaults.adapter

if (import.meta.env.VITE_USE_MOCK === 'true') {
  setupMock()
}

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus, { locale: zhCn })

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.mount('#app')
