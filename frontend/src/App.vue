<script setup>
import { ref } from 'vue';
import { PublicClientApplication } from '@azure/msal-browser';
import { msalConfig, loginRequest, tokenRequest } from './authConfig';
import axios from 'axios';

const account = ref(null);
const apiResponse = ref(null);
const msalInstance = new PublicClientApplication(msalConfig);

// Nur Initialisierung
msalInstance.initialize().then(() => {
  const accounts = msalInstance.getAllAccounts();
  if (accounts.length > 0) {
    account.value = accounts[0];
  }
});

const handleLogin = async () => {
  try {
    const response = await msalInstance.loginPopup(loginRequest);
    account.value = response.account;
  } catch (err) {
    console.error("Login failed:", err);
  }
};

const handleLogout = () => {
  msalInstance.logoutPopup();
  account.value = null;
};

// Explizite Funktion nur für den API-Test
const testApiCall = async () => {
  apiResponse.value = 'Trying to get token...';
  console.log("Requesting token with scopes:", tokenRequest.scopes);

  const currentAccount = msalInstance.getAllAccounts()[0];
  if (!currentAccount) {
    apiResponse.value = "No account found. Please log in.";
    return;
  }

  try {
    const tokenResponse = await msalInstance.acquireTokenSilent({
      ...tokenRequest,
      account: currentAccount
    });

    console.log("Successfully acquired token:", tokenResponse);
    apiResponse.value = 'Token acquired. Calling API...';

    const headers = { Authorization: `Bearer ${tokenResponse.accessToken}` };
    const response = await axios.get('http://localhost:8000/api/v1/items', { headers });

    console.log("API Response:", response.data);
    apiResponse.value = response.data;

  } catch (err) {
    console.error("API call failed:", err);
    apiResponse.value = `Error: ${err.message}`;
  }
};
</script>

<template>
  <header>
    <h1>RIO-Inventar (Minimaler Test)</h1>
    <div v-if="account">
      <span>Willkommen, {{ account.name }}!</span>
      <button @click="handleLogout">Logout</button>
    </div>
    <div v-else>
      <button @click="handleLogin">Login</button>
    </div>
  </header>

  <main>
    <div v-if="account">
      <button @click="testApiCall">Test API Call</button>
      <h3>API Response:</h3>
      <pre>{{ apiResponse }}</pre>
    </div>
    <div v-else>
      <p>Bitte melde dich an, um den Test zu starten.</p>
    </div>
  </main>
</template>

<style scoped>
pre { background-color: #f5f5f5; padding: 1rem; border: 1px solid #ccc; }
button { margin: 0.5rem; }
</style>
