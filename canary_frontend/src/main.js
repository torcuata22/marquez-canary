import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { initializeApp } from "firebase/app";


const firebaseConfig = {
  apiKey: "AIzaSyDeOqPoTh2c5aNVHaPEgmA7VLDNLBaOK7U",
  authDomain: "canary-take-home-cd144.firebaseapp.com",
  projectId: "canary-take-home-cd144",
  storageBucket: "canary-take-home-cd144.appspot.com",
  messagingSenderId: "796706068386",
  appId: "1:796706068386:web:bd485476897544fcd7c4fb"
};

// Initialize Firebase
initializeApp(firebaseConfig);

//const app = createApp(App)
//app.use(router)

createApp(App).use(store).use(router).mount('#app');


// Import the functions you need from the SDKs you need

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration

