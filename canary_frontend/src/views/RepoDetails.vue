<template>
    <div class="repo-details">
        <h1>{{ repo.name }}</h1>
        <p>{{ repo.repo_url }}</p>
        <p>{{ repo.retrieved_at }}</p>
    </div>



</template>  

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const repo = ref({});
const route = useRoute();

const fetchRepoDetails = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/auth/api/github/repo/${route.params.repoName}/`);
    repo.value = response.data;
  } catch (error) {
    console.error("Error fetching repository details:", error);
  }
};

onMounted(() => {
  fetchRepoDetails();
});
</script>