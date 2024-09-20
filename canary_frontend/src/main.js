import { createApp } from 'vue'
import App from './App.vue'
//import router from './router'
//import store from './store'
import vue3GoogleLogin from 'vue3-google-login'

const app = createApp(App)

app.use(vue3GoogleLogin, {
    clientId: '479613814071-8vr213m5pftojeumbm4q3gl163skqn33.apps.googleusercontent.com'
// clientId: process.env.GOOGLE_CLIENT_ID

})

app.mount('#app')

// GOOGLE_CLIENT_ID='479613814071-8vr213m5pftojeumbm4q3gl163skqn33.apps.googleusercontent.com'
// GOOGLE_CLIENT_SECRET='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'