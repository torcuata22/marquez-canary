import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LandingPage from '../views/LandingPage.vue';
import GitHubRepos from '../views/GitHubRepos.vue'; 
import GoogleCallback from '../views/GoogleCallback.vue';
import GithubCallback from '../views/GithubCallback.vue';


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
    path: '/auth/github/callback',
    name: 'GithubCallback',
    component: GithubCallback, 
  },
  {
    path: '/callback', 
    name: 'GoogleCallback',
    component: GoogleCallback, 
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
