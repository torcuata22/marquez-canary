<template>
  <div class="repos">
    <h1>Your Repositories:</h1>
    <div class="container">
    <ul class="table table-striped" v-if="repos.length">
      <li v-for="repo in repos" :key="repo.id">
        <p class=""><i class="fas fa-code-branch"></i> {{ repo.name }}</p>
        <button class="btn btn-primary" @click="selectRepo(repo)">Select Repo</button>
      </li>
    </ul>
    <p v-else>No repositories found or not linked to GitHub.</p>
    <button v-if="!repos.length && !isLinked" @click="linkGitHub">Link GitHub Account</button>
  </div>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const repos = ref([]);
const router = useRouter();

const fetchRepositories = async () => {
  const tokenValue = localStorage.getItem('githubToken');
  if (tokenValue) {
    try {
      const response = await axios.get('https://api.github.com/user/repos', {
        headers: {
          Authorization: `token ${tokenValue}`
        }, 
        params: {
          per_page: 40,
          page:1
        }
      });

      const reposData = response.data;
      const totalPages = response.headers.link && response.headers.link.match(/rel="last"/)
        ? parseInt(response.headers.link.match(/&page=(\d+)/)[1])
        : 1;

      for (let page = 2; page <= totalPages; page++) {
        const nextPageResponse = await axios.get('https://api.github.com/user/repos', {
          headers: {
            Authorization: `token ${tokenValue}`
          },
          params: {
            per_page: 100,
            page
          }
        });
        reposData.push(...nextPageResponse.data);
      }

      repos.value = reposData;
    } catch (error) {
      console.error("Error fetching repositories:", error);
    }
  } else {
    console.error("No token found.");
  }
};

const selectRepo = (repo) => {
  console.log("Selecting repo:", repo);
  axios.post('/api/select-repo/', { repo_name: repo.name, repo_url: repo.html_url })
    .then(response => {
      router.push({
        name: 'SingleGitHubRepo',
        params: {
          repoName: repo.name,
          repoUrl: repo.html_url
        }
      });
      console.log(response.data);
    })
    .catch(error => {
      console.error(error);
    });
};

onMounted(() => {
  fetchRepositories();
});
</script>

<style scoped>

</style>