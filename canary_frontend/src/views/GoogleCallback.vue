<template>
  <div>
    <h1>Logging In...</h1>
    <p v-if="loading">Please wait...</p>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router'; // Import useRouter
import axios from 'axios';

const router = useRouter(); // Initialize the router
const loading = ref(true); // Track loading state
const error = ref(''); // Track error messages

onMounted(async () => {
  const hash = window.location.hash;
  if (hash) {
    const params = new URLSearchParams(hash.substring(1));
    const idToken = params.get('id_token');
    console.log("ID Token:", idToken);
    
    if (idToken) {
      try {
        const url = `http://127.0.0.1:8000/auth/google/`;
        const res = await axios.post(url, {
          id_token: idToken,
        });

        console.log("Login successful:", res.data);

        axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.token}`;

        // Redirect to the landing page after successful login
        router.push('/landing');
      } catch (errorResponse) {
        error.value = "Login failed. Please try again.";
        console.error("Error response from server:", errorResponse.response ? errorResponse.response.data : errorResponse);
      } finally {
        loading.value = false; // Set loading to false after processing
      }
    } else {
      error.value = "No ID token found.";
      loading.value = false;
    }
  } else {
    error.value = "No hash found in the URL.";
    loading.value = false;
  }
});
</script>
