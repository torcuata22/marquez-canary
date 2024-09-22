import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LandingPage from '../views/LandingPage.vue';
import Repos from '../views/Repos.vue'; 
import CallbackView from '../views/Callback.vue';
import GitHubCallback from '../views/GitHubCallback.vue';

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
  },
  {
    path: '/repos',
    name: 'Repos',
    component: Repos,
  },
  {
    path: '/auth/github',
    name: 'GitHubCallback',
    component: GitHubCallback, // Add the GitHub OAuth callback view
  },
  {
    path: '/callback', // Add the callback route
    name: 'Callback',
    component: CallbackView, // Use a new view to handle the token
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
