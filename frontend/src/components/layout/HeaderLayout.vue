<script setup>
import { ref, onMounted } from 'vue';
import { login, logout, getAccount } from '../../authService';

const account = ref(null);
const dark = ref(false);

const handleLogin = async () => {
  const acc = await login();
  if (acc) account.value = acc;
};
const handleLogout = () => {
  logout();
  account.value = null;
};

const toggleDark = () => {
  dark.value = !dark.value;
  const root = document.documentElement;
  if (dark.value) root.classList.add('dark'); else root.classList.remove('dark');
  try { localStorage.setItem('theme:dark', String(dark.value)); } catch (_) {}
};

onMounted(() => {
  const acc = getAccount();
  if (acc) account.value = acc;
  // initial state from localStorage or classList
  try { dark.value = document.documentElement.classList.contains('dark') || localStorage.getItem('theme:dark') === 'true'; } catch (_) {}
});
</script>

<template>
  <div class="app-shell">
    <header class="header">
      <div class="container header-row">
        <div class="brand">
          <router-link to="/" class="logo">🚀 RIO Inventar</router-link>
        </div>
        <nav class="nav">
          <router-link to="/" exact-active-class="active">Dashboard</router-link>
          <router-link to="/inventory" exact-active-class="active">Inventar</router-link>
          <router-link to="/master-data" exact-active-class="active">Stammdaten</router-link>
        </nav>
        <div class="actions">
          <button class="btn ghost" @click="toggleDark" title="Dark Mode">🌓</button>
          <div v-if="account" class="user">
            <span class="name">{{ account.name }}</span>
            <button class="btn" @click="handleLogout">Logout</button>
          </div>
          <div v-else>
            <button class="btn primary" @click="handleLogin">Login</button>
          </div>
        </div>
      </div>
    </header>
    <main class="container content">
      <slot />
    </main>
  </div>
  
</template>

<style scoped>
.app-shell { min-height: 100vh; background: var(--color-background); }
.header {
  position: sticky; top: 0; z-index: 10;
  backdrop-filter: blur(8px);
  background: var(--header-bg);
  border-bottom: 1px solid var(--border-color);
}
.header-row { display: flex; align-items: center; justify-content: space-between; height: 64px; }
.logo { text-decoration: none; color: var(--text-strong); font-weight: 800; letter-spacing: 0.2px; }
.nav { display: flex; gap: 1rem; }
.nav a { color: var(--text-muted); text-decoration: none; padding: 0.5rem 0.25rem; border-bottom: 2px solid transparent; }
.nav a:hover { color: var(--accent-strong); }
.nav a.active { color: var(--accent-strong); border-bottom-color: var(--accent); }
.actions { display: flex; align-items: center; gap: 0.75rem; }
.user { display: flex; align-items: center; gap: 0.5rem; }
.name { color: var(--text-muted); }
.btn { border: 1px solid var(--border-color); background: var(--btn-bg); color: var(--text-strong); padding: 0.45rem 0.75rem; border-radius: 8px; cursor: pointer; }
.btn:hover { border-color: var(--accent); }
.btn.primary { background: var(--accent); border-color: var(--accent); color: #0b3325; font-weight: 700; }
.btn.ghost { background: transparent; }
.content { padding-top: 1.25rem; padding-bottom: 2rem; }
</style>


