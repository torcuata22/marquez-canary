<template>
  <div id="app">
    <div v-if="isAuthenticated">
      <LandingPage />
      <div v-if="isGitHubLinked">
        <GitHubRepos @githubLinked="setGitHubLinked" /> <!-- Show only if GitHub account is linked -->
      </div>
    </div>
    <div v-else>
      <HomeView />
    
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { onMounted } from 'vue'; 
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
    const isGitHubLinked = ref(false);

    const token = localStorage.getItem('google_token');
    if (token) {
      isAuthenticated.value = true;
    }

    const githubToken = localStorage.getItem('token'); // Check for GitHub token
    if (githubToken) {
      isGitHubLinked.value = true;
      console.log("GitHub Token:", githubToken);
    }

    // update isGitHubLinked
    const setGitHubLinked = (linked) => {
      isGitHubLinked.value = linked;
    };

    // Log values when component is mounted
    onMounted(() => {
      console.log('Is Authenticated:', isAuthenticated.value);
      console.log('GitHub Token:', githubToken);
      console.log('GitHub Is Linked:', isGitHubLinked.value);
    });

    return {
      isAuthenticated,
      isGitHubLinked,
      setGitHubLinked
    };
  },
};
</script>



<style>
 
</style>
