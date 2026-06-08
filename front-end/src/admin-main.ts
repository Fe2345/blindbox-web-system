import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import AdminApp from './AdminApp.vue'
import router from './router/admin'
import { setupMock } from './mock'
import './styles/admin.css'

if (import.meta.env.VITE_USE_MOCK === 'true') {
  setupMock()
}

const app = createApp(AdminApp)

app.use(createPinia())
app.use(router)
app.use(ElementPlus, { locale: zhCn })

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.mount('#app')
