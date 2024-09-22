<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'; // Import the router
import axios from 'axios';

const code = ref('');
const router = useRouter(); // Initialize the router

onMounted(() => {
  code.value = new URLSearchParams(window.location.search).get('code');
  console.log("Received code:", code.value);

  if (code.value) {
    const tokenUrl = `https://github.com/login/oauth/access_token`; 

    axios.post(tokenUrl, {
      client_id: process.env.VUE_APP_GITHUB_CLIENT_ID,
      client_secret: process.env.VUE_APP_GITHUB_CLIENT_SECRET,
      code: code.value,
      redirect_uri: 'http://127.0.0.1:8080/auth/github/callback',
    }, {
      headers: {
        Accept: 'application/json' 
      }
    })
    .then(response => {
      console.log('Access token response:', response.data); 
      const accessToken = response.data.access_token; // Access token from response

      if (accessToken) {
        localStorage.setItem('github_token', accessToken);
        console.log("Access token stored, redirecting to /githubrepos...");
        router.push('/githubrepos');
      } else {
        console.error("No access token found in response.");
      }
    })
    .catch(error => console.error('Error getting access token:', error));
  } else {
    console.error("No code found in the URL.");
  }
});
</script>

