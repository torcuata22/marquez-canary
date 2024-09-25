import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LandingPage from '../views/LandingPage.vue';
import GitHubRepos from '../views/GitHubRepos.vue'; 
import GoogleCallback from '../views/GoogleCallback.vue';
import GitHubCallback from '../views/GithubCallback.vue';
import SingleGitHubRepo from '../views/SingelGitHubRepo.vue';


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
    path: '/auth/callback/github', 
    name: 'GitHubCallback',
    component: GitHubCallback,
  },
  {
    path: '/githubrepos',
    name: 'GitHubRepos',
    component: GitHubRepos,
  },
  {
    path: '/githubrepos/:repoName',
    name: 'SingleGitHubRepo',
    component: SingleGitHubRepo,
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
