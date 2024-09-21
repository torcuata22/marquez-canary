<template>
    <div class="landing-page">
        <h1>Welcome!</h1>
        <p>Please click the button below to connect the app to your GitHub account.</p>
        <button @click="linkWithGitHub">Link GitHub Account</button>
    </div>
</template>


<script setup>
const linkWithGithub = () => {
const githubClientId = process.env.VUE_APP_GITHUB_CLIENT_ID;
const redirectUri = 'http://localhost:8000/auth/github/';
const url = `https://github.com/login/oauth/authorize?client_id=${githubClientId}&redirect_uri=${redirectUri}`;
window.location.href = url;
};
</script>

<style>

<style>