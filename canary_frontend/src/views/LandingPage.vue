<template>
  <div class="container p-5">
    <div class="card mx-auto mt-5 shadow-lg p-3 mb-5 bg-body-tertiary rounded" style="width: 18rem;">
      <div class="card-body text-center">
        <img src="../assets/github.png" class="card-img-top" alt="Logo">
        <h5 class="card-title mt-5">Link to Your Github Account</h5>
        <button @click="signInWithGitHub" class="btn btn-lg btn-block btn-primary mt-5">
          <i class="fab fa-github"></i> Link to GitHub
        </button>
      </div>
    </div>
  </div>
</template>



<script>
import { getAuth, GithubAuthProvider, signInWithPopup } from "firebase/auth";


export default {
  name: 'LandingPage',
  methods:{
    async signInWithGitHub() {
  const auth = getAuth(); // Instance initialized in main.js
  const provider = new GithubAuthProvider();
  
  try {
    const result = await signInWithPopup(auth, provider);
    console.log('RESULT', result);

    // Extract the credential from the result
    const credential = GithubAuthProvider.credentialFromResult(result);
    
    // Get the access token
    const token = credential.accessToken;

    // Save the token to localStorage
    if (token) {
      localStorage.setItem('githubToken', token); // Save token for later use
      console.log('GitHub Access Token:', token);
    } else {
      console.error('No credential found. Unable to retrieve GitHub token.');
    }

    // Redirect to the success page
    this.$router.push('/githubrepos');
  } catch (error) {
    console.error('Error during GitHub sign-in:', error);
  }
}

  }
}
  
</script>




<style scoped>

  body {
    background-color: #f8f8f8;
  }
  .btn-github {
    background-color: #333;
    color: white;
    font-size: 16px;
    padding: 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  .btn-github i {
    margin-right: 10px;
  }
</style>