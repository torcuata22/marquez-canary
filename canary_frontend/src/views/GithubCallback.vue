<script setup>
console.log('GitHubCallback component rendered');
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const handleGitHubCallback = async () => {
  const queryParams = new URLSearchParams(window.location.search);
  const token = queryParams.get('token');

  if (token) {
    localStorage.setItem('githubToken', token);
    console.log('Token saved to local storage:', localStorage.getItem('githubToken'));
    router.push('/githubrepos');
  } else {
    console.log('Error handling GitHub callback');
  }
};

onMounted(() => {
  handleGitHubCallback();
});
</script>