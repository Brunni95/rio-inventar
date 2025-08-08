<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';
import { getAccount } from '../authService';
import AssetQrButton from '../components/qr/AssetQrButton.vue';
import Pagination from '../components/Pagination.vue';
import { useApiList } from '../composables/useApiList';

// Central list state via composable (server-side pagination + sorting)
const { items: assets, total, error: errorMessage, search: searchQuery, sortBy, sortDir, page, pageSize, fetchList: fetchAssets } = useApiList('/api/v1/assets/');
const router = useRouter();
const editingAsset = ref(null);
const locations = ref([]);
const manufacturers = ref([]);
const statuses = ref([]);
const assetTypes = ref([]);
const suppliers = ref([]);
const users = ref([]);

// --- NEU: Refs für die Historien-Anzeige ---
const selectedAssetForHistory = ref(null);
const assetHistory = ref([]);
const isLoadingHistory = ref(false);

let debounceTimer = null;

const newAssetForm = ref({
  inventory_number: '', serial_number: '', model: '', purchase_price: null,
  department: '', os_version: '', installation_date: null, warranty_expiry: null,
  purchase_date: null, notes: '', ip_address: '', hostname: '', mac_address: '',
  room: '', asset_type_id: null, manufacturer_id: null, status_id: null, location_id: null,
  supplier_id: null, user_id: null,
});

watch(searchQuery, () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    page.value = 1;
    fetchAssets();
  }, 300);
});

const totalPages = () => Math.max(1, Math.ceil(total.value / pageSize.value));

const changeSort = (key) => {
  if (sortBy.value === key) {
    sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortBy.value = key;
    sortDir.value = 'asc';
  }
  page.value = 1;
  fetchAssets();
};

// Refetch when page or page size changes (Pagination component emits updates)
watch([page, pageSize], () => {
  fetchAssets();
});


const fetchDropdownData = async () => {
  try {
    const [ locationsRes, manufacturersRes, statusesRes, assetTypesRes, suppliersRes, usersRes ] = await Promise.all([
      api.get('/api/v1/locations/'),
      api.get('/api/v1/manufacturers/'),
      api.get('/api/v1/statuses/'),
      api.get('/api/v1/asset-types/'),
      api.get('/api/v1/suppliers/'),
      api.get('/api/v1/users/'),
    ]);
    locations.value = locationsRes.data;
    manufacturers.value = manufacturersRes.data;
    statuses.value = statusesRes.data;
    assetTypes.value = assetTypesRes.data;
    suppliers.value = suppliersRes.data;
    users.value = usersRes.data;
  } catch (error) {
    errorMessage.value = 'Stammdaten konnten nicht geladen werden.';
  }
};

// --- NEU: Funktion zum Anzeigen der Historie ---
const showHistory = async (asset) => {
  selectedAssetForHistory.value = asset;
  isLoadingHistory.value = true;
  try {
    const response = await api.get(`/api/v1/assets/${asset.id}/logs`);
    assetHistory.value = response.data;
  } catch (error) {
    console.error("Fehler beim Laden der Historie:", error);
    alert("Historie konnte nicht geladen werden.");
  } finally {
    isLoadingHistory.value = false;
  }
};

const closeHistoryModal = () => {
  selectedAssetForHistory.value = null;
  assetHistory.value = [];
};

const handleSubmit = async () => {
  try {
    const payload = { ...newAssetForm.value };
    for (const key of ['installation_date', 'warranty_expiry', 'purchase_date']) {
      if (!payload[key]) payload[key] = null;
    }
    if (editingAsset.value) {
      await api.put(`/api/v1/assets/${editingAsset.value.id}`, payload);
    } else {
      await api.post('/api/v1/assets/', payload);
    }
    resetForm();
    await fetchAssets();
  } catch (error) {
    alert(`Fehler beim Speichern: ${error.response?.data?.detail || error.message}`);
  }
};

const deleteAsset = async (assetId) => {
  if (!confirm('Bist du sicher, dass du dieses Asset löschen möchtest?')) return;
  try {
    await api.delete(`/api/v1/assets/${assetId}`);
    await fetchAssets();
  } catch (error) {
    alert('Asset konnte nicht gelöscht werden.');
  }
};

const startEdit = (asset) => {
  router.push({ name: 'AssetEdit', params: { id: asset.id } });
};

const resetForm = () => {
  editingAsset.value = null;
  newAssetForm.value = {
    inventory_number: '', serial_number: '', model: '', purchase_price: null,
    department: '', os_version: '', installation_date: null, warranty_expiry: null,
    purchase_date: null, notes: '', ip_address: '', hostname: '', mac_address: '', room: '',
    asset_type_id: null, manufacturer_id: null, status_id: null, location_id: null,
    supplier_id: null, user_id: null,
  };
};

onMounted(async () => {
  if (getAccount()) {
    await fetchDropdownData();
    await fetchAssets();
  }
});
</script>

<template>
  <div class="inventory-container">
    

    <section class="card">
      <h2>Inventarliste</h2>
      <div class="toolbar">
        <input v-model="searchQuery" placeholder="Suchen nach Inventar-Nr, Modell, Benutzer, Standort..." />
        <div class="toolbar-actions">
          <button class="btn-primary" @click="fetchAssets">Aktualisieren</button>
          <button @click="resetForm">Formular zurücksetzen</button>
        </div>
      </div>
      <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
      <table v-else-if="assets.length > 0">
        <thead>
        <tr>
          <th @click="changeSort('inventory_number')" style="cursor:pointer">Inventar-Nr.</th>
          <th @click="changeSort('asset_type.name')" style="cursor:pointer">Typ</th>
          <th @click="changeSort('manufacturer.name')" style="cursor:pointer">Modell</th>
          <th @click="changeSort('location.name')" style="cursor:pointer">Standort</th>
          <th @click="changeSort('user.display_name')" style="cursor:pointer">Benutzer</th>
          <th @click="changeSort('status.name')" style="cursor:pointer">Status</th>
          <th>Aktionen</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="asset in assets" :key="asset.id">
          <td>{{ asset.inventory_number }}</td>
          <td>{{ asset.asset_type.name }}</td>
          <td>{{ asset.manufacturer.name }} {{ asset.model }}</td>
          <td>{{ asset.location.name }}</td>
          <td>{{ asset.user?.display_name || '---' }}</td>
          <td>{{ asset.status.name }}</td>
          <td class="actions">
            <button @click="startEdit(asset)" title="Bearbeiten">✏️</button>
            <button @click="deleteAsset(asset.id)" title="Löschen">🗑️</button>
            <!-- NEU: Button für die Historie -->
            <button @click="showHistory(asset)" title="Historie anzeigen">📜</button>
            <AssetQrButton :asset-id="asset.id" :inventory-number="asset.inventory_number" />
          </td>
        </tr>
        </tbody>
      </table>
      <p v-else>Keine Assets gefunden.</p>
      <Pagination v-model:page="page" v-model:page-size="pageSize" :total="total" />
    </section>

    <!-- NEU: Das Modal-Fenster für die Historie -->
    <div v-if="selectedAssetForHistory" class="modal-overlay" @click.self="closeHistoryModal">
      <div class="modal-content">
        <h3>Historie für: {{ selectedAssetForHistory.inventory_number }}</h3>
        <button class="close-button" @click="closeHistoryModal">×</button>
        <div v-if="isLoadingHistory">Lade Verlauf...</div>
        <ul v-else-if="assetHistory.length > 0" class="history-list">
          <li v-for="log in assetHistory" :key="log.id">
            <span class="timestamp">{{ new Date(log.timestamp).toLocaleString() }}</span>
            <span class="user">{{ log.changed_by_user.display_name }}</span>
            <span class="action">{{ log.action }}</span>
            <span class="details" v-if="log.field_changed">
              Feld '{{ log.field_changed }}' geändert von '{{ log.old_value }}' zu '{{ log.new_value }}'
            </span>
            <span class="details" v-else>{{ log.notes }}</span>
          </li>
        </ul>
        <p v-else>Keine Historie für dieses Asset vorhanden.</p>
      </div>
    </div>

  </div>
</template>

<style scoped>
.inventory-container { display: flex; flex-direction: column; gap: 2rem; }
.card { background-color: var(--card-bg); border-radius: 8px; padding: 1.5rem; box-shadow: none; border: 1px solid var(--color-border); }
.form-sections { display: flex; flex-direction: column; gap: 1.25rem; }
.form-section { padding: 1rem; border: 1px solid var(--color-border); border-radius: 8px; background: var(--card-bg); }
.section-title { margin: 0 0 0.75rem 0; font-size: 0.95rem; color: var(--text-muted); font-weight: 600; }
.grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 0.9rem; }
.form-control { display: flex; flex-direction: column; gap: 0.35rem; }
.form-control label { font-size: 0.9rem; color: var(--text-strong); }
.form-control .hint { color: var(--text-muted); font-size: 0.8rem; }
.req { color: #ef4444; margin-left: 0.2rem; }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
input, select, textarea { padding: 0.7rem 0.75rem; background: var(--btn-bg); color: var(--text-strong); border: 1px solid var(--color-border); border-radius: 6px; }
textarea { width: 100%; min-height: 100px; }
.form-actions { display: flex; gap: 0.6rem; margin-top: 1rem; }
button { cursor: pointer; border: 1px solid var(--color-border); background: var(--btn-bg); color: var(--text-strong); border-radius: 6px; padding: 0.6rem 0.9rem; }
.btn-primary { background: var(--accent); border-color: var(--accent); color: white; }
.btn.ghost { background: transparent; }
table { width: 100%; border-collapse: collapse; }
th, td { border-bottom: 1px solid var(--color-border); padding: 12px 15px; text-align: left; color: var(--text-strong); }
th { background-color: var(--color-background-mute); font-weight: 600; color: var(--text-strong); }
.actions button { padding: 0.25rem 0.5rem; margin-right: 5px; background: none; border: 1px solid #ccc; color: #333; }
.toolbar { margin-bottom: 1.5rem; display: flex; gap: 0.75rem; align-items: center; }
.toolbar input { flex: 1; padding: 0.75rem; border: 1px solid #ccc; border-radius: 4px; }
.toolbar-actions { display: flex; gap: 0.5rem; }
.pagination { display: flex; align-items: center; gap: 0.5rem; margin-top: 0.75rem; }
.pagination button { background: var(--btn-bg); color: var(--text-strong); border: 1px solid var(--color-border); border-radius: 6px; padding: 0.4rem 0.6rem; }
.pagination button:disabled { opacity: 0.5; cursor: not-allowed; }
.pagination .page-size select { background: var(--btn-bg); color: var(--text-strong); border: 1px solid var(--color-border); border-radius: 6px; padding: 0.2rem 0.4rem; }

/* --- NEU: Styles für das Modal --- */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}
.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}
.close-button {
  position: absolute;
  top: 10px;
  right: 15px;
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #888;
}
.history-list {
  list-style: none;
  padding: 0;
}
.history-list li {
  display: grid;
  grid-template-columns: 160px 150px 150px 1fr;
  gap: 1rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid #eee;
  font-size: 0.9rem;
}
.history-list .timestamp { color: #666; }
.history-list .user { font-weight: bold; }
.history-list .action { color: #007bff; }
</style>
