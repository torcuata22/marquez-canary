<template>
  <div>
    <h1>Logging in with GitHub...</h1>
    <p v-if="loading">Please wait...</p>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const loading = ref(true);
const error = ref('');

onMounted(() => {
  const queryParams = new URLSearchParams(window.location.search);
  const token = queryParams.get('token');

  if (token) {
    console.log('GitHub Token found:', token);
    localStorage.setItem('githubToken', token); // Store the token

    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

    // Redirect or navigate to the desired route
    router.push('/githubrepos'); // Redirect after storing
  } else {
    error.value = 'No token found in URL.';
    loading.value = false;
    console.error('Error handling GitHub callback: No token found');
  }
});
</script>


