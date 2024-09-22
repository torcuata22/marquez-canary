<template>
  <div>
    <h2>GitHub OAuth Callback</h2>
    <p v-if="errorMessage">{{ errorMessage }}</p>
    <p v-else>Processing your GitHub authentication...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const errorMessage = ref('');
const isLoading = ref(true);
const router = useRouter();

onMounted(async () => {
  const code = new URLSearchParams(window.location.search).get('code');

  if (code) {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/auth/github/callback/?code=${code}`);
      console.log('Response from backend:', response.data);
      localStorage.setItem('github_linked', 'true');

      // Redirect to GitHubRepos after successful linking
      router.push('/githubrepos');
    } catch (error) {
      console.error('Error linking GitHub account:', error);
      errorMessage.value = 'Failed to link GitHub account. Please try again.';
    }
  } else {
    errorMessage.value = 'No authorization code provided.';
  }

  isLoading.value = false;
});
</script>

<style scoped>
/* Add styles as needed */
</style>
