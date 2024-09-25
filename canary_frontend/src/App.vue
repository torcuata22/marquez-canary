<template>
  <div id="app">
    <LandingPage v-if="isAuthenticated" />
    <GitHubRepos v-if="isAuthenticated && isGitHubLinked" @githubLinked="setGitHubLinked" />
    <HomeView v-if="!isAuthenticated" />
  </div>
</template>


<script>
import { ref } from 'vue';
import HomeView from './views/HomeView.vue';
import LandingPage from './views/LandingPage.vue';
import GitHubRepos from './views/GitHubRepos.vue';

export default {
  components: { HomeView, LandingPage, GitHubRepos },
  setup() {
    const isAuthenticated = ref(!!localStorage.getItem('google_token'));
    const isGitHubLinked = ref(!!localStorage.getItem('githubToken'));

    const setGitHubLinked = (linked) => {
      isGitHubLinked.value = linked;
    };

    return { isAuthenticated, isGitHubLinked, setGitHubLinked };
  },
};
</script>



<style>
 
</style>
