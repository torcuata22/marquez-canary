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
      <router-view /> <!--just in case I add something else -->
  </div>
</template>

<script>
import { ref } from 'vue';
import HomeView from './views/HomeView.vue'; 
// eslint-disable-next-line no-unused-vars
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
  const token = localStorage.getItem('google_token');
  if (token) {
    isAuthenticated.value = true;
  }
  return {
    isAuthenticated
  };
},  
};
</script>

<style>
 /*global styles go here*/
</style>
