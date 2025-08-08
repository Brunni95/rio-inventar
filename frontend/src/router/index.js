import { createRouter, createWebHistory } from 'vue-router';
import DashboardView from '../views/DashboardView.vue';
import InventoryView from '../views/InventoryView.vue';
import MasterDataView from '../views/MasterDataView.vue';
import { getAccount, login } from '../authService';

const routes = [
  { path: '/', name: 'Dashboard', component: DashboardView, meta: { requiresAuth: true } },
  { path: '/inventory', name: 'Inventory', component: InventoryView, meta: { requiresAuth: true } },
  {
    path: '/master-data',
    name: 'MasterData',
    component: MasterDataView,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Globaler Route Guard für Authentifizierung
router.beforeEach(async (to) => {
  const requiresAuth = to.matched.some(r => r.meta?.requiresAuth !== false);
  if (!requiresAuth) return true;
  if (getAccount()) return true;
  try {
    await login();
  } catch (e) {
    // Popup abgebrochen o.ä.
  }
  // Prüfe erneut
  return !!getAccount();
});

export default router;
