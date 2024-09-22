import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LandingPage from '../views/LandingPage.vue';
import GitHubRepos from '../views/GitHubRepos.vue'; 
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
    path: '/githubrepos',
    name: 'GitHubRepos',
    component: GitHubRepos,
  },
  {
    path: '/auth/github',
    name: 'GitHubCallback',
    component: GitHubCallback, 
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
