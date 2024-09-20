import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LandingPage from '../components/LandingPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView, 
  },
  {
    path: '/landing',
    name: 'LandingPage',
    component: LandingPage,
  }
];


const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
