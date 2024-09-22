<template>
  <div class="landing-page">
    <h1>Welcome!</h1>
    <p>Please click the button below to connect the app to your GitHub account.</p>
    <button @click="linkWithGithub">
    <i class="fab fa-github"></i> Link GitHub Account
    </button>
  </div>
</template>

<script setup>
const linkWithGithub = () => {
    const githubClientId = process.env.VUE_APP_GITHUB_CLIENT_ID;
    const redirectUri = 'http://localhost:8000/auth/github/'; // Django will handle this route
    const url = `https://github.com/login/oauth/authorize?client_id=${githubClientId}&redirect_uri=${redirectUri}`;
    window.location.href = url;
};
</script>

<style scoped>
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
