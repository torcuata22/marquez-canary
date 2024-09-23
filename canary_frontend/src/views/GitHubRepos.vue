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
import { ref, onMounted } from 'vue';
import axios from 'axios';

const repos = ref([]); // Holds the repositories

const fetchRepositories = async () => {
  const token = localStorage.getItem('github_token'); // Fetch token from localStorage
  console.log("Github Token:", token);
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

// Fetch repositories on component mount
onMounted(() => {
  fetchRepositories();
  handleGitHubCallback();
});

// Function to handle the GitHub callback
const handleGitHubCallback = async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get('code');

  if (code) {
    try {
      const response = await axios.get(`/auth/github/callback/?code=${code}`);
      console.log(response.data); // Log the response data

      if (response.data.message) {
        // If the linking was successful, fetch repositories again
        fetchRepositories();
      } else {
        console.error('Failed to link GitHub account:', response.data.error);
      }
    } catch (error) {
      console.error("Error handling GitHub callback:", error);
    }
  }
};

const linkGitHub = () => {
  // Redirect user to GitHub login
  window.location.href = 'https://github.com/login/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&scope=user:email';
};

const selectRepo = async (repo) => {
  try {
    await axios.post('http://127.0.0.1:8000/auth/api/github/select-repo/', {
      repo_name: repo.name,
      repo_url: repo.html_url
    });
    // You can add navigation to the repo details page here if required
    console.log(`Repo ${repo.name} selected`);
  } catch (error) {
    console.error("Error selecting repository:", error);
  }
};
</script>

<style scoped>
/* Add any styles here */
</style>
