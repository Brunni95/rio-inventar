// frontend/src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import { initializeMsal } from './authService';

import './assets/main.css'

// Initialisiere MSAL und starte danach die Vue App
initializeMsal().then(() => {
  createApp(App).mount('#app');
});
