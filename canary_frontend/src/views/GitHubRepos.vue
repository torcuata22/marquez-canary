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
});

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

</style>
