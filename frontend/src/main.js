import { createApp } from 'vue'
import App from './App.vue'
import { initializeMsal } from './authService'
import router from './router' // NEU: Importiere den Router

import './assets/main.css'

initializeMsal().then(() => {
  const app = createApp(App);
  app.use(router); // NEU: Sage der App, sie soll den Router benutzen
  app.mount('#app');
});
