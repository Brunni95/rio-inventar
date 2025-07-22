<script setup>
import { ref, onMounted, watch } from 'vue';
import api from '../api';
import { getAccount } from '../authService';

// --- Refs für die Daten ---
const assets = ref([]);
const errorMessage = ref('');
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

const searchQuery = ref('');
let debounceTimer = null;

const newAssetForm = ref({
  inventory_number: '', serial_number: '', model: '', purchase_price: null,
  department: '', os_version: '', installation_date: null, warranty_expiry: null,
  purchase_date: null, notes: '', ip_address: '', hostname: '', mac_address: '',
  asset_type_id: null, manufacturer_id: null, status_id: null, location_id: null,
  supplier_id: null, user_id: null,
});

watch(searchQuery, () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    fetchAssets();
  }, 300);
});

const fetchAssets = async () => {
  try {
    const params = new URLSearchParams();
    if (searchQuery.value) {
      params.append('search', searchQuery.value);
    }
    const response = await api.get(`/api/v1/assets/?${params.toString()}`);
    assets.value = response.data;
  } catch (error) {
    errorMessage.value = 'Asset-Daten konnten nicht geladen werden.';
    console.error(error);
  }
};

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
  window.scrollTo({ top: 0, behavior: 'smooth' });
  editingAsset.value = asset;
  newAssetForm.value = {
    ...asset,
    asset_type_id: asset.asset_type.id,
    manufacturer_id: asset.manufacturer.id,
    status_id: asset.status.id,
    location_id: asset.location.id,
    supplier_id: asset.supplier?.id,
    user_id: asset.user?.id,
  };
};

const resetForm = () => {
  editingAsset.value = null;
  newAssetForm.value = {
    inventory_number: '', serial_number: '', model: '', purchase_price: null,
    department: '', os_version: '', installation_date: null, warranty_expiry: null,
    purchase_date: null, notes: '', ip_address: '', hostname: '', mac_address: '',
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
      <h2>{{ editingAsset ? 'Asset bearbeiten' : 'Neues Asset hinzufügen' }}</h2>
      <form @submit.prevent="handleSubmit">
        <!-- Das Formular bleibt unverändert -->
        <div class="form-grid">
          <input v-model="newAssetForm.inventory_number" placeholder="Inventarnummer *" required />
          <select v-model="newAssetForm.asset_type_id" required>
            <option :value="null" disabled>Geräte-Typ wählen... *</option>
            <option v-for="type in assetTypes" :key="type.id" :value="type.id">{{ type.name }}</option>
          </select>
          <select v-model="newAssetForm.manufacturer_id" required>
            <option :value="null" disabled>Hersteller wählen... *</option>
            <option v-for="man in manufacturers" :key="man.id" :value="man.id">{{ man.name }}</option>
          </select>
          <input v-model="newAssetForm.model" placeholder="Modell" />
          <input v-model="newAssetForm.serial_number" placeholder="Seriennummer" />
          <select v-model="newAssetForm.status_id" required>
            <option :value="null" disabled>Status wählen... *</option>
            <option v-for="stat in statuses" :key="stat.id" :value="stat.id">{{ stat.name }}</option>
          </select>
          <select v-model="newAssetForm.location_id" required>
            <option :value="null" disabled>Standort wählen... *</option>
            <option v-for="loc in locations" :key="loc.id" :value="loc.id">{{ loc.name }}</option>
          </select>
          <select v-model="newAssetForm.user_id">
            <option :value="null">-- Keinem Benutzer zugewiesen --</option>
            <option v-for="user in users" :key="user.id" :value="user.id">{{ user.display_name }}</option>
          </select>
          <input v-model.number="newAssetForm.purchase_price" type="number" step="0.01" placeholder="Kaufpreis" />
          <label>Kaufdatum: <input v-model="newAssetForm.purchase_date" type="date" /></label>
          <label>Garantie bis: <input v-model="newAssetForm.warranty_expiry" type="date" /></label>
          <input v-model="newAssetForm.hostname" placeholder="Hostname" />
          <input v-model="newAssetForm.ip_address" placeholder="IP-Adresse" />
        </div>
        <textarea v-model="newAssetForm.notes" placeholder="Notizen..."></textarea>
        <div class="form-actions">
          <button type="submit">{{ editingAsset ? 'Änderungen speichern' : 'Asset erstellen' }}</button>
          <button v-if="editingAsset" @click="resetForm" type="button" class="cancel">Abbrechen</button>
        </div>
      </form>
    </section>

    <section class="card">
      <h2>Inventarliste</h2>
      <div class="toolbar">
        <input v-model="searchQuery" placeholder="Suchen nach Inventar-Nr, Modell, Benutzer, Standort..." />
      </div>
      <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
      <table v-else-if="assets.length > 0">
        <thead>
        <tr>
          <th>Inventar-Nr.</th>
          <th>Typ</th>
          <th>Modell</th>
          <th>Standort</th>
          <th>Benutzer</th>
          <th>Status</th>
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
          </td>
        </tr>
        </tbody>
      </table>
      <p v-else>Keine Assets gefunden.</p>
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
/* Der meiste Style bleibt unverändert */
.inventory-container { display: flex; flex-direction: column; gap: 2rem; }
.card { background-color: white; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 1rem; }
textarea { width: 100%; min-height: 80px; margin-bottom: 1rem; }
.form-actions { display: flex; gap: 1rem; }
input, select, textarea, button { padding: 0.75rem; border: 1px solid #ccc; border-radius: 4px; }
button { cursor: pointer; border: none; font-weight: bold; color: white; }
form button[type="submit"] { background-color: #42b883; }
form button.cancel { background-color: #888; }
table { width: 100%; border-collapse: collapse; }
th, td { border-bottom: 1px solid #ddd; padding: 12px 15px; text-align: left; }
th { background-color: #f8f8f8; font-weight: 600; }
.actions button { padding: 0.25rem 0.5rem; margin-right: 5px; background: none; border: 1px solid #ccc; color: #333; }
.toolbar { margin-bottom: 1.5rem; }
.toolbar input { width: 100%; padding: 0.75rem; border: 1px solid #ccc; border-radius: 4px; }

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
