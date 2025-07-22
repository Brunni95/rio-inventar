import { createRouter, createWebHistory } from 'vue-router';
import InventoryView from '../views/InventoryView.vue';
import MasterDataView from '../views/MasterDataView.vue';

const routes = [
  {
    path: '/',
    name: 'Inventory',
    component: InventoryView,
  },
  {
    path: '/master-data',
    name: 'MasterData',
    component: MasterDataView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
