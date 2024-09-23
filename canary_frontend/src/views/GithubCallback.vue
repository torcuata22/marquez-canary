<script setup>
import { ref, onMounted } from 'vue';
//import { useRouter } from 'vue-router'; // Import the router
//import axios from 'axios';
console.log("GitHub callback URL:", window.location.href);
console.log("GithubCallback component is rendered");
const code = ref('');


onMounted(() => {
    code.value = new URLSearchParams(window.location.search).get('code');
    if (code.value) {
        console.log("Code Received:", code.value);
        const backendUrl = `http://127.0.0.1:8000/auth/github/callback?code=${code.value}`;
         window.location.href = backendUrl; // Redirect to the backend
    } else {
        console.error("No code found in the URL.");
    }
});

        

</script>

