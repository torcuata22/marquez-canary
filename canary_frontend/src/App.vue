<template>
  <div id="app">
    <div v-if="isAuthenticated">
      <LandingPage />
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

export default {
  components: {
    HomeView, 
    LandingPage
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
