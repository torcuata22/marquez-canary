<template>
  <div>
    <h2>GitHub OAuth Callback</h2>
    <p>Processing your GitHub authentication...</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';

onMounted(() => {
  // Fetch code from URL query params
  const code = new URLSearchParams(window.location.search).get('code');
  console.log('GitHub authorization code:', code);

  // Add logic to exchange the code for an access token with the backend (like I did with Google)
});
</script>

<style scoped>

</style>
