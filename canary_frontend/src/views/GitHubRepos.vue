<template>
    <div class="repos">
        <h1>Your Repositories:</h1>
        <ul>
            <li v-for="repo in repos" :key="repo.id">
                <i class="fas fa-code-branch"></i>{{ repo.name }}
                <button @click="selectRepo(repo)">Select Repo</button>
            </li>
        </ul>
    </div> 
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import axios from 'axios';

    const repos = ref([]);
    
    const fetchRepositories = async () => {
        try {
            const response = await axios.get(`http:127.0.0.1:8000/auth/api/github/repositories`);
            repos.value = response.data;
        } catch (error) {
            console.error("Error fetching repositories:", error);
        }
    };

    const selectRepo = async (repo) => {
        try {
            await axios.post('http://127.0.0.1:8000/auth/api/github/select-repo/', {
            repo_name: repo.name,
            repo_url: repo.html_url
            });
            //router.push({ name: 'RepoDetails', params: { repoName: repo.name }}); // Redirect to details page
        } catch (error) {
            console.error("Error selecting repository:", error);
        }
        };

onMounted(() => {
  fetchRepositories();
});
</script>


<style scoped>
    .repos {
    margin: 20px;
    padding: 20px;
    }
</style>