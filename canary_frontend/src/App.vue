<template>
  <div id="app">
    <div v-if="isAuthenticated">
      <LandingPage />
      <div v-if="isGitHubLinked">
        <GitHubRepos /> <!-- Show only if GitHub account is linked -->
      </div>

    </div>
    <div v-else>
      <HomeView />
    </div>
    <router-view />
  </div>
</template>

<script>
import { ref } from 'vue';
import HomeView from './views/HomeView.vue'; 
import LandingPage from './views/LandingPage.vue';
import GitHubRepos from './views/GitHubRepos.vue';

export default {
  components: {
    HomeView, 
    LandingPage,
    GitHubRepos
  },
  setup() {
    const isAuthenticated = ref(false);
    const isGitHubLinked = ref(false);  // Declare isGitHubLinked only once

    const token = localStorage.getItem('google_token');
    if (token) {
      isAuthenticated.value = true;
      console.log('Is Authenticated:', isAuthenticated.value);
    }

    const githubToken = localStorage.getItem('github_token'); // Check for GitHub token
    if (githubToken) {
      isGitHubLinked.value = true;
      console.log('GitHub Is Linked:', isGitHubLinked.value);
    }
    
    return {
      isAuthenticated,
      isGitHubLinked
    };
  },
};  
</script>


<style>
 
</style>
