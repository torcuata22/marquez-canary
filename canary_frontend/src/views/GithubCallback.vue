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

onMounted(async () => {
  const queryParams = new URLSearchParams(window.location.search);
  const token = queryParams.get('token');

  if (token) {
    console.log('GitHub Token found:', token);
    

   
    const url = 'http://127.0.0.1:8000/auth/github/callback/';
    await axios.post(url, {
          githubToken: token,
        });
        localStorage.setItem('githubToken', token); // Store the token
    // Redirect or navigate to the desired route
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    router.push('/githubrepos'); // Redirect after storing
  } else {
    error.value = 'No token found in URL.';
    loading.value = false;
    console.error('Error handling GitHub callback: No token found');
  }
});
</script>


