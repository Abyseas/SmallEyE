import { createApp } from 'vue'
import router from './utils/router'
import ElementPlus from 'element-plus'
import IconHome from '~icons/custom/home'
import IconFire from '~icons/custom/fire'
import IconUser from '~icons/custom/user'
import IconSparkle from '~icons/custom/sparkle'
import IconTech from '~icons/custom/tech'
import IconFood from '~icons/custom/food'
import IconMovie from '~icons/custom/movie'
import IconGame from '~icons/custom/game'
import IconBook from '~icons/custom/book'
import IconNews from '~icons/custom/fire'
import IconMusic from '~icons/custom/music'
import IconFashion from '~icons/custom/fashion'
import IconLife from '~icons/custom/life'
import IconSport from '~icons/custom/sport'

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
app.component('IconTech', IconTech)
app.component('IconFood', IconFood)
app.component('IconMovie', IconMovie)
app.component('IconGame', IconGame)
app.component('IconBook', IconBook)
app.component('IconNews', IconNews)
app.component('IconMusic', IconMusic)
app.component('IconFashion', IconFashion)
app.component('IconLife', IconLife)
app.component('IconSport', IconSport)

app.mount('#app')
