<template>
  <button @click="loginWithGoogle">Login with Google</button>
</template>

<script setup>
const loginWithGoogle = () => {
  const clientId = process.env.VUE_APP_GOOGLE_CLIENT_ID
  const redirectUri = 'http://localhost:8080/callback/'
  const scope = 'email profile';
  const nonce = btoa(Math.random().toString()); 
  
  const url = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=id_token&scope=${scope}&nonce=${nonce}`;
  window.location.href = url;
};

// Add logic to capture the token after redirect
window.addEventListener('load', async () => {
  const hash = window.location.hash;
  if (hash) {
    const params = new URLSearchParams(hash.substring(1));
    const idToken = params.get('id_token');
    console.log("ID Token:", idToken);
    if (idToken) {
      try {
        const res = await fetch('http://localhost:8000/auth/google/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ id_token: idToken }), // Send token to backend
        });

        if (!res.ok) {
          const errorDetails = await res.json();
          console.error("Error response from server:", errorDetails);
        } else {
          const data = await res.json();
          console.log("Login successful:", data);
        }
      } catch (error) {
        console.error("Error during login:", error);
      }
    }
  }
});
</script>
