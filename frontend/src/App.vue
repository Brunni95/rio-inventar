<script setup>
// Der Script-Teil bleibt unverändert
import { ref, onMounted } from 'vue';
import { login, logout, getAccount } from './authService';

const account = ref(null);

const handleLogin = async () => {
  const loggedInAccount = await login();
  if (loggedInAccount) {
    account.value = loggedInAccount;
  }
};

const handleLogout = () => {
  logout();
  account.value = null;
};

onMounted(() => {
  const currentAccount = getAccount();
  if (currentAccount) {
    account.value = currentAccount;
  }
});
</script>

<template>
  <div id="app-container">
    <!-- Der Header-Hintergrund ist immer volle Breite -->
    <header class="app-header">
      <!-- Der Inhalt des Headers ist im .container zentriert und begrenzt -->
      <div class="container header-content">
        <div class="logo-area">
          <h1>🚀 RIO-Inventar</h1>
        </div>
        <nav v-if="account" class="main-nav">
          <router-link to="/">Inventar</router-link>
          <router-link to="/master-data">Stammdaten</router-link>
        </nav>
        <div class="auth-panel">
          <div v-if="account">
            <span>Willkommen, {{ account.name }}!</span>
            <button @click="handleLogout">Logout</button>
          </div>
          <div v-else>
            <button @click="handleLogin">Login</button>
          </div>
        </div>
      </div>
    </header>

    <!-- Der Hauptinhalt ist ebenfalls im .container zentriert und begrenzt -->
    <main class="content-area container">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
/* Die Styles in App.vue werden jetzt viel einfacher und sauberer */

.app-header {
  background-color: white;
  border-bottom: 1px solid #ddd;
  height: 60px;
  flex-shrink: 0;
  position: sticky;
  top: 0;
  z-index: 10;
}

/* Wir nutzen Flexbox, um den Header-Inhalt zu arrangieren */
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.logo-area {
  flex-shrink: 0;
}

.main-nav {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  flex-grow: 1;
}

.main-nav a {
  text-decoration: none;
  color: #555;
  font-weight: 500;
  padding: 20px 0;
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease-in-out;
}

.main-nav a:hover {
  color: #42b883;
}

.main-nav a.router-link-exact-active {
  color: #42b883;
  border-bottom-color: #42b883;
}

.auth-panel {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Der .content-area-Container braucht jetzt nur noch vertikales Padding */
.content-area {
  flex-grow: 1;
  padding-top: 2rem;
  padding-bottom: 2rem;
}
</style>
