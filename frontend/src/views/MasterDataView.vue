<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';

// Refs für die Listen der Stammdaten
const locations = ref([]);
const manufacturers = ref([]);
const statuses = ref([]);
const assetTypes = ref([]);
const suppliers = ref([]);

// Refs für die Eingabefelder der neuen Einträge
const newLocation = ref({ name: '', description: '' });
const newManufacturer = ref({ name: '' });
const newStatus = ref({ name: '' });
const newAssetType = ref({ name: '' });
const newSupplier = ref({ name: '', contact_person: '' });

// Funktion, um alle Stammdaten-Listen zu laden (unverändert)
const fetchAllMasterData = async () => {
  try {
    const [locationsRes, manufacturersRes, statusesRes, assetTypesRes, suppliersRes] = await Promise.all([
      api.get('/api/v1/locations/'),
      api.get('/api/v1/manufacturers/'),
      api.get('/api/v1/statuses/'),
      api.get('/api/v1/asset-types/'),
      api.get('/api/v1/suppliers/'),
    ]);
    locations.value = locationsRes.data;
    manufacturers.value = manufacturersRes.data;
    statuses.value = statusesRes.data;
    assetTypes.value = assetTypesRes.data;
    suppliers.value = suppliersRes.data;
  } catch (error) {
    console.error("Fehler beim Laden der Stammdaten:", error);
    alert("Die Stammdaten konnten nicht geladen werden.");
  }
};

// --- NEU: Eigene, einfache Funktion für jede Karte ---

const addLocation = async () => {
  if (!newLocation.value.name.trim()) return alert("Der Name darf nicht leer sein.");
  try {
    await api.post('/api/v1/locations/', newLocation.value);
    newLocation.value = { name: '', description: '' }; // Formular zurücksetzen
    await fetchAllMasterData();
  } catch (e) { alert(`Fehler: ${e.response?.data?.detail || e.message}`); }
};

const addManufacturer = async () => {
  if (!newManufacturer.value.name.trim()) return alert("Der Name darf nicht leer sein.");
  try {
    await api.post('/api/v1/manufacturers/', newManufacturer.value);
    newManufacturer.value = { name: '' };
    await fetchAllMasterData();
  } catch (e) { alert(`Fehler: ${e.response?.data?.detail || e.message}`); }
};

const addStatus = async () => {
  if (!newStatus.value.name.trim()) return alert("Der Name darf nicht leer sein.");
  try {
    await api.post('/api/v1/statuses/', newStatus.value);
    newStatus.value = { name: '' };
    await fetchAllMasterData();
  } catch (e) { alert(`Fehler: ${e.response?.data?.detail || e.message}`); }
};

const addAssetType = async () => {
  if (!newAssetType.value.name.trim()) return alert("Der Name darf nicht leer sein.");
  try {
    await api.post('/api/v1/asset-types/', newAssetType.value);
    newAssetType.value = { name: '' };
    await fetchAllMasterData();
  } catch (e) { alert(`Fehler: ${e.response?.data?.detail || e.message}`); }
};

const addSupplier = async () => {
  if (!newSupplier.value.name.trim()) return alert("Der Name darf nicht leer sein.");
  try {
    await api.post('/api/v1/suppliers/', newSupplier.value);
    newSupplier.value = { name: '', contact_person: '' };
    await fetchAllMasterData();
  } catch (e) { alert(`Fehler: ${e.response?.data?.detail || e.message}`); }
};

onMounted(fetchAllMasterData);
</script>

<template>
  <div class="master-data-container">
    <h1>Stammdaten-Verwaltung</h1>
    <div class="grid">
      <!-- Sektion für Standorte -->
      <div class="card">
        <h2>Standorte</h2>
        <!-- KORREKTUR: Ruft die spezifische Funktion auf -->
        <form @submit.prevent="addLocation">
          <input v-model="newLocation.name" placeholder="Neuer Standort Name" />
          <input v-model="newLocation.description" placeholder="Beschreibung" />
          <button type="submit">Hinzufügen</button>
        </form>
        <ul>
          <li v-for="item in locations" :key="item.id">{{ item.name }}</li>
        </ul>
      </div>

      <!-- Sektion für Hersteller -->
      <div class="card">
        <h2>Hersteller</h2>
        <form @submit.prevent="addManufacturer">
          <input v-model="newManufacturer.name" placeholder="Neuer Hersteller" />
          <button type="submit">Hinzufügen</button>
        </form>
        <ul>
          <li v-for="item in manufacturers" :key="item.id">{{ item.name }}</li>
        </ul>
      </div>

      <!-- Sektion für Status -->
      <div class="card">
        <h2>Status</h2>
        <form @submit.prevent="addStatus">
          <input v-model="newStatus.name" placeholder="Neuer Status" />
          <button type="submit">Hinzufügen</button>
        </form>
        <ul>
          <li v-for="item in statuses" :key="item.id">{{ item.name }}</li>
        </ul>
      </div>

      <!-- Sektion für Geräte-Typen -->
      <div class="card">
        <h2>Geräte-Typen</h2>
        <form @submit.prevent="addAssetType">
          <input v-model="newAssetType.name" placeholder="Neuer Geräte-Typ" />
          <button type="submit">Hinzufügen</button>
        </form>
        <ul>
          <li v-for="item in assetTypes" :key="item.id">{{ item.name }}</li>
        </ul>
      </div>

      <!-- Sektion für Lieferanten -->
      <div class="card">
        <h2>Lieferanten</h2>
        <form @submit.prevent="addSupplier">
          <input v-model="newSupplier.name" placeholder="Neuer Lieferant" />
          <input v-model="newSupplier.contact_person" placeholder="Ansprechperson" />
          <button type="submit">Hinzufügen</button>
        </form>
        <ul>
          <li v-for="item in suppliers" :key="item.id">{{ item.name }} <span v-if="item.contact_person">({{ item.contact_person }})</span></li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.master-data-container {
  width: 100%;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}
.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  background-color: #f9f9f9;
}
.card h2 {
  margin-top: 0;
  border-bottom: 2px solid #eee;
  padding-bottom: 0.5rem;
}
form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
input {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  padding: 0.5rem;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
ul {
  list-style-type: none;
  padding: 0;
  max-height: 200px;
  overflow-y: auto;
}
li {
  background-color: white;
  padding: 0.5rem;
  border: 1px solid #eee;
  margin-bottom: 5px;
  border-radius: 4px;
}
</style>
