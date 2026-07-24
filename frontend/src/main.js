import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import App from './App.vue'
import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('./views/ProjectList.vue') },
  { path: '/project/:id', component: () => import('./views/ProjectEdit.vue') },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.mount('#app')
