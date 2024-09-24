<template>
  <div class="container p-5">
    <div class="card mx-auto mt-5 shadow-lg p-3 mb-5 bg-body-tertiary rounded" style="width: 18rem;">
      <div class="card-body text-center">
        <img src="../assets/github.png" class="card-img-top" alt="Logo">
        <h5 class="card-title mt-5">Link to Your Github Account</h5>
        <button @click="linkWithGithub" class="btn btn-lg btn-block btn-primary mt-5">
          <i class="fab fa-github"></i> Link to GitHub
        </button>
      </div>
    </div>
  </div>
</template>


<script setup>
import axios from 'axios';

const linkWithGithub = async () => {
  console.log('Linking with GitHub...');
  
  try {
    const response = await axios.get('http://127.0.0.1:8000/auth/github/');
    // Assuming the backend returns the GitHub authorization URL:
    const githubAuthUrl = response.data.url;
    console.log("Redirecting to:", githubAuthUrl);
    window.location.href = githubAuthUrl;
  } catch (error) {
    console.error("Error while linking with GitHub:", error);
  }
};

// No need for onMounted() unless you want to initialize something on load
</script>

<style scoped>

  body {
    background-color: #f8f8f8;
  }
  .btn-github {
    background-color: #333;
    color: white;
    font-size: 16px;
    padding: 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  .btn-github i {
    margin-right: 10px;
  }
</style>