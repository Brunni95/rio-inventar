<script setup>
import { ref } from 'vue';
import { logout } from '../../authService';

const isSidebarOpen = ref(true);

const handleLogout = () => {
  try { logout(); } catch (_) {}
};
</script>

<template>
  <div class="layout-root" :class="{ 'sidebar-collapsed': !isSidebarOpen }">
    <aside class="sidebar">
      <div class="brand">
        <button class="burger" @click="isSidebarOpen = !isSidebarOpen" title="Toggle menu">☰</button>
        <span class="logo">🚀</span>
        <span class="title">RIO Inventar</span>
      </div>
      <nav class="menu">
        <router-link to="/" class="menu-item" exact-active-class="active">Dashboard</router-link>
        <router-link to="/inventory" class="menu-item" exact-active-class="active">Inventar</router-link>
        <router-link to="/master-data" class="menu-item" exact-active-class="active">Stammdaten</router-link>
      </nav>
      <div class="sidebar-footer">
        <button class="logout" @click="handleLogout">Logout</button>
      </div>
    </aside>
    <div class="content">
      <header class="topbar">
        <div class="topbar-left">
          <slot name="toolbar-left" />
        </div>
        <div class="topbar-right">
          <slot name="toolbar-right" />
        </div>
      </header>
      <main class="main container">
        <slot />
      </main>
    </div>
  </div>
</template>

<style scoped>
.layout-root {
  display: grid;
  grid-template-columns: 260px 1fr;
  min-height: 100vh;
}
.layout-root.sidebar-collapsed {
  grid-template-columns: 80px 1fr;
}
.sidebar {
  background: #0f172a;
  color: #cbd5e1;
  display: flex;
  flex-direction: column;
  padding: 0.75rem 0.75rem 1rem;
}
.brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.25rem 1rem;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
.burger {
  background: transparent;
  color: #cbd5e1;
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 6px;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
}
.logo { font-size: 1.25rem; }
.title { font-weight: 700; letter-spacing: 0.2px; }
.menu { display: flex; flex-direction: column; padding-top: 0.5rem; }
.menu-item {
  color: #cbd5e1;
  text-decoration: none;
  padding: 0.6rem 0.65rem;
  border-radius: 6px;
  margin: 0.1rem 0;
}
.menu-item:hover { background: rgba(255,255,255,0.06); }
.menu-item.active { background: #1e293b; color: #e2e8f0; }
.sidebar-footer { margin-top: auto; }
.logout {
  width: 100%;
  background: #334155;
  color: #e2e8f0;
  border: none;
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
}
.logout:hover { background: #475569; }
.content { display: flex; flex-direction: column; }
.topbar {
  position: sticky; top: 0; z-index: 5;
  backdrop-filter: blur(8px);
  background: rgba(255,255,255,0.8);
  border-bottom: 1px solid #e5e7eb;
  height: 56px;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 1rem;
}
.main { padding-top: 1.25rem; padding-bottom: 2rem; }
</style>


