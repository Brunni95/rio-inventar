<script setup>
// Der <script setup> Block bleibt exakt gleich wie vorher.
import { ref, onMounted } from 'vue';
import api from '../api';
import { getAccount } from '../authService';

const account = ref(null);
const assets = ref([]);
const errorMessage = ref('');
const editingAsset = ref(null);
const locations = ref([]);
const manufacturers = ref([]);
const statuses = ref([]);
const assetTypes = ref([]);
const suppliers = ref([]);

const newAssetForm = ref({
  inventory_number: '', serial_number: '', model: '', assigned_to: '',
  department: '', os_version: '', installation_date: null, warranty_expiry: null,
  purchase_date: null, notes: '', ip_address: '', hostname: '', mac_address: '',
  asset_type_id: null, manufacturer_id: null, status_id: null, location_id: null,
  supplier_id: null,
});

const fetchAllData = async () => {
  try {
    const [ assetsRes, locationsRes, manufacturersRes, statusesRes, assetTypesRes, suppliersRes ] = await Promise.all([
      api.get('/api/v1/assets'),
      api.get('/api/v1/locations'),
      api.get('/api/v1/manufacturers'),
      api.get('/api/v1/statuses'),
      api.get('/api/v1/asset-types'),
      api.get('/api/v1/suppliers'),
    ]);
    assets.value = assetsRes.data;
    locations.value = locationsRes.data;
    manufacturers.value = manufacturersRes.data;
    statuses.value = statusesRes.data;
    assetTypes.value = assetTypesRes.data;
    suppliers.value = suppliersRes.data;
  } catch (error) {
    errorMessage.value = 'Daten konnten nicht geladen werden.';
    console.error(error);
  }
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
      await api.post('/api/v1/assets', payload);
    }
    resetForm();
    await fetchAllData();
  } catch (error) {
    alert(`Fehler beim Speichern: ${error.response?.data?.detail || error.message}`);
  }
};

const deleteAsset = async (assetId) => {
  if (!confirm('Bist du sicher, dass du dieses Asset löschen möchtest?')) return;
  try {
    await api.delete(`/api/v1/assets/${assetId}`);
    await fetchAllData();
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
  };
};

const resetForm = () => {
  editingAsset.value = null;
  newAssetForm.value = {
    inventory_number: '', serial_number: '', model: '', assigned_to: '',
    department: '', os_version: '', installation_date: null, warranty_expiry: null,
    purchase_date: null, notes: '', ip_address: '', hostname: '', mac_address: '',
    asset_type_id: null, manufacturer_id: null, status_id: null, location_id: null,
    supplier_id: null,
  };
};

onMounted(async () => {
  const currentAccount = getAccount();
  if (currentAccount) {
    account.value = currentAccount;
    await fetchAllData();
  }
});
</script>

<template>
  <div class="inventory-container">
    <section class="card">
      <h2>{{ editingAsset ? 'Asset bearbeiten' : 'Neues Asset hinzufügen' }}</h2>
      <form @submit.prevent="handleSubmit">
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
          <input v-model="newAssetForm.assigned_to" placeholder="Zugewiesen an" />
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
          <td>{{ asset.assigned_to }}</td>
          <td>{{ asset.status.name }}</td>
          <td class="actions">
            <button @click="startEdit(asset)" title="Bearbeiten">✏️</button>
            <button @click="deleteAsset(asset.id)" title="Löschen">🗑️</button>
          </td>
        </tr>
        </tbody>
      </table>
      <p v-else>Keine Assets im Inventar vorhanden.</p>
    </section>
  </div>
</template>

<style scoped>
/* Dieser Container nimmt die volle Breite seines Eltern-Elements (.content-area) ein */
.inventory-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.card {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.form-grid {
  display: grid;
  /* Responsive Grid: Passt sich der Bildschirmbreite an */
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

textarea {
  width: 100%;
  min-height: 80px;
  margin-bottom: 1rem;
  box-sizing: border-box;
}

.form-actions {
  display: flex;
  gap: 1rem;
}

input, select, textarea, button {
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

button {
  cursor: pointer;
  border: none;
  font-weight: bold;
  color: white;
}

form button[type="submit"] {
  background-color: #42b883;
}
form button.cancel {
  background-color: #888;
}

table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  border-bottom: 1px solid #ddd;
  padding: 12px 15px;
  text-align: left;
}
th {
  background-color: #f8f8f8;
  font-weight: 600;
}
.actions button {
  padding: 0.25rem 0.5rem;
  margin-right: 5px;
  background: none;
  border: 1px solid #ccc;
  color: #333;
}
</style>
