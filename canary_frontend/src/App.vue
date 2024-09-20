<template>
  <div id="app">
    <google-login @success="onLoginSuccess" @fail="onLoginFail" />
  </div>
</template>

<script>
export default {
  methods: {
    onLoginSuccess(response) {
      console.log('Google login successful:', response);
      // You can send the response to your Django backend here via Axios
    },
    onLoginFail(error) {
      console.log('Google login failed:', error);
    }
  }
}
</script>