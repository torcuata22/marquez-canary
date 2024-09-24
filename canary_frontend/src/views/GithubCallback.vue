<template>
  <div>
    <h1>Processing GitHub Callback...</h1>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const code = ref('');

onMounted(async () => {
  console.log("GitHubCallback component is mounted");
  console.log("Current URL:", window.location.href);

  // Extract the code from the URL
  code.value = new URLSearchParams(window.location.search).get('code');

  if (code.value) {
    console.log("Code Received:", code.value);
    try {
      // Send the code to the backend to get the access token
      const backendUrl = `http://127.0.0.1:8000/auth/github/callback/?code=${code.value}`;
      const response = await axios.get(backendUrl);

      console.log("Backend Response:", response.data); 

      if (response.data && response.data.token) { 
        console.log("Storing token:", response.data.token);
        localStorage.setItem('github_token', response.data.token); // Store token in localStorage
        console.log("Token after storage:", localStorage.getItem('github_token'));

        // Navigate to GitHubRepos view
        router.push({ name: 'GitHubRepos' });
      } else {
        console.error('Failed to link GitHub account:', response.data.error || 'No token in response');
      }
    } catch (error) {
      console.error("Error linking GitHub account:", error);
    }
  } else {
    console.error("No code found in the URL.");
  }
});
</script>
