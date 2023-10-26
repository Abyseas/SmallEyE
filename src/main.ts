import { createApp } from 'vue'
import router from './utils/router'
import ElementPlus from 'element-plus'
import IconHome from '~icons/custom/home'
import IconFire from '~icons/custom/fire'
import IconUser from '~icons/custom/user'
import IconSparkle from '~icons/custom/sparkle'
import 'element-plus/dist/index.css'
import './style.css'
import 'swiper/css/bundle'
import App from './App.vue'

const app = createApp(App)
app.use(router)
app.use(ElementPlus)

app.component('IconHome', IconHome)
app.component('IconFire', IconFire)
app.component('IconUser', IconUser)
app.component('IconSparkle', IconSparkle)

app.mount('#app')
