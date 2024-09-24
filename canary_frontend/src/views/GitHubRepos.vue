<template>
  <div class="repos">
    <h1>Your Repositories:</h1>
    <ul v-if="repos.length">
      <li v-for="repo in repos" :key="repo.id">
        <i class="fas fa-code-branch"></i> {{ repo.name }}
        <button @click="selectRepo(repo)">Select Repo</button>
      </li>
    </ul>
    <p v-else>No repositories found or not linked to GitHub.</p>
    <button @click="linkGitHub">Link GitHub Account</button>
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue';
import axios from 'axios';

const emit = defineEmits(['githubLinked']); // Emit event to parent
const repos = ref([]); // Holds the repositories

const fetchRepositories = async () => {
  const token = localStorage.getItem('github_token'); // Fetch token from localStorage
  console.log("GitHub Token:", token);
  if (token) {
    try {
      const response = await axios.get('https://api.github.com/user/repos', {
        headers: {
          Authorization: `token ${token}`
        }
      });
      repos.value = response.data; // Set the response data (repos) to the `repos` ref
    } catch (error) {
      console.error("Error fetching repositories:", error);
    }
  } else {
    console.error("No token found.");
  }
};

// Function to handle the GitHub callback (retrieves code and fetches token)
const handleGitHubCallback = async () => {
  console.log('Handling GitHub callback...');
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get('code'); // Extract the code from URL

  if (code) {
    try {
      const response = await axios.get(`/auth/github/callback/?code=${code}`);
      console.log('Response from GitHub callback:', response.data); // Log the response data (token)

      if (response.data.access_token) {
        const token = response.data.access_token;

        // Store the token in localStorage
        localStorage.setItem('github_token', token);
        console.log('GitHub access token saved to localStorage');

        // Emit an event to notify App.vue that GitHub is linked
        emit('githubLinked', true);
        
        // Fetch repositories using the new token
        fetchRepositories();

      } else {
        console.warning('No code URL found');
        console.error('Failed to retrieve access token:', response.data.error);
      }
    } catch (error) {
      console.error("Error handling GitHub callback:", error);
    }
  } else {
    console.warn('No code found in URL for GitHub callback.');
  }
};

// Link GitHub
const linkGitHub = () => {
  const clientId = 'YOUR_CLIENT_ID'; // Replace with your GitHub OAuth client ID
  const redirectUri = encodeURIComponent('YOUR_REDIRECT_URI'); // Replace with your redirect URI
  window.location.href = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=user:email`;
};

// Fetch repositories and handle GitHub callback on component mount
onMounted(() => {
  console.log("GitHubRepos component is mounted");
  handleGitHubCallback(); // Handle the callback and extract token
  fetchRepositories(); // Fetch repos if token is already in localStorage
  
});
</script>



<style scoped>
/* Add any styles here */
</style>
