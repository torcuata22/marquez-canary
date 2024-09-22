<template>
  <div class="container p-5">
    <div class="card mx-auto mt-5 shadow-lg p-3 mb-5 bg-body-tertiary rounded" style="width: 18rem;">
      <div class="card-body text-center">
        <img src="../assets/google.png" class="card-img-top" alt="Logo">
        <h5 class="card-title mt-5">Login Here</h5>
          <button @click="loginWithGoogle" class="btn btn-lg btn-block btn-primary mt-5 flex justify-center">
          <i class="fab fa-google flex justify-center"></i> Login with Google
      </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import axios from 'axios';

const loginWithGoogle = () => {
  const clientId = process.env.VUE_APP_GOOGLE_CLIENT_ID;
  const redirectUri = 'http://127.0.0.1:8080/callback/';
  const scope = 'email profile';
  const nonce = btoa(Math.random().toString()); 
  
  const url = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=id_token&scope=${scope}&nonce=${nonce}`;
  window.location.href = url;
};

// Use onMounted to handle loading after the component mounts
onMounted(() => {
  const hash = window.location.hash;
  if (hash) {
    const params = new URLSearchParams(hash.substring(1));
    const idToken = params.get('id_token');

    if (idToken) {
      localStorage.setItem('idToken', idToken);
      sendTokenToBackend(idToken);
    }
  }
});

const sendTokenToBackend = async (idToken) => {
  try {
    const url = `http://127.0.0.1:8000/auth/google/`;
    const res = await axios.post(url, { id_token: idToken });
    localStorage.setItem('google_token', res.data.token);
    console.log('Login successful', res.data)
    window.location.href = '/landing'; 

  } catch (error) {
    console.error("Error during login:", error);
  }
};
</script>

<style scoped>


.card-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.btn {
  width: 100%; 
}

</style>