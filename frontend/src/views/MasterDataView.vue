<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';
import { getAccount } from '../authService';

// Der Haupt-State für alle Stammdaten, bleibt unverändert
const masterData = ref({
  locations: [],
  manufacturers: [],
  statuses: [],
  suppliers: [],
  'asset-types': [],
});

// State für die Formular-Eingaben, bleibt unverändert
const newItems = ref({
  locations: { name: '' },
  manufacturers: { name: '' },
  statuses: { name: '' },
  suppliers: { name: '' },
  'asset-types': { name: '' },
});

const errorMessage = ref('');

// Konfigurationsobjekt, um Wiederholungen zu vermeiden. Bleibt gleich.
const dataTypes = {
  locations: { title: 'Standorte', endpoint: '/api/v1/locations/' },
  manufacturers: { title: 'Hersteller', endpoint: '/api/v1/manufacturers/' },
  statuses: { title: 'Status-Typen', endpoint: '/api/v1/statuses/' },
  suppliers: { title: 'Lieferanten', endpoint: '/api/v1/suppliers/' },
  'asset-types': { title: 'Geräte-Typen', endpoint: '/api/v1/asset-types/' },
};

// Funktion zum Laden aller Daten, bleibt unverändert.
const fetchAllMasterData = async () => {
  try {
    const requests = Object.entries(dataTypes).map(([key, config]) =>
      api.get(config.endpoint).then(response => ({ key, data: response.data }))
    );
    const results = await Promise.all(requests);
    results.forEach(({ key, data }) => {
      masterData.value[key] = data;
    });
  } catch (error) {
    errorMessage.value = 'Stammdaten konnten nicht geladen werden.';
    console.error(error);
  }
};

// Funktion zum Hinzufügen neuer Einträge, bleibt unverändert.
const handleAddItem = async (type) => {
  try {
    const config = dataTypes[type];
    const newItem = newItems.value[type];
    if (!newItem.name.trim()) return;

    const response = await api.post(config.endpoint, { name: newItem.name });
    masterData.value[type].push(response.data);
    newItem.name = ''; // Formular zurücksetzen
  } catch (error) {
    alert(`Fehler beim Hinzufügen von '${dataTypes[type].title}': ${error.response?.data?.detail || error.message}`);
  }
};

// ==========================================================
// NEU: Funktion zum Löschen von Einträgen
// ==========================================================
const handleDeleteItem = async (type, id) => {
  // Sicherheitsabfrage, um versehentliches Löschen zu verhindern
  if (!confirm('Bist du sicher, dass du diesen Eintrag löschen möchtest? Diese Aktion kann nicht rückgängig gemacht werden.')) {
    return;
  }

  try {
    const config = dataTypes[type];
    // Der API-Aufruf an den neuen DELETE-Endpunkt
    await api.delete(`${config.endpoint}${id}`);

    // Bei Erfolg: Entferne das Element aus der lokalen Liste für ein sofortiges UI-Update
    const index = masterData.value[type].findIndex(item => item.id === id);
    if (index !== -1) {
      masterData.value[type].splice(index, 1);
    }
  } catch (error) {
    // Hier fangen wir die Fehler vom Backend ab
    if (error.response && error.response.status === 409) {
      // Speziell für den "Conflict"-Fehler (wenn der Eintrag noch verwendet wird)
      alert(`Löschen fehlgeschlagen: ${error.response.data.detail}`);
    } else {
      // Allgemeiner Fehler
      alert(`Ein Fehler ist aufgetreten. Der Eintrag konnte nicht gelöscht werden.`);
    }
    console.error(`Fehler beim Löschen von '${type}' mit ID ${id}:`, error);
  }
};

// onMounted bleibt unverändert
onMounted(() => {
  if (getAccount()) {
    fetchAllMasterData();
  }
});
</script>

<template>
  <div class="master-data-container">
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <!-- Die Grid-Struktur bleibt unverändert -->
    <div class="grid">
      <div v-for="(config, type) in dataTypes" :key="type" class="card">
<h3>{{ config.title }}</h3>

        <!-- Das Formular zum Hinzufügen bleibt unverändert -->
        <form @submit.prevent="handleAddItem(type)" class="add-form">
          <input v-model="newItems[type].name" :placeholder="`Neuen ${config.title.slice(0, -1)} hinzufügen...`" required />
<button type="submit" class="btn-primary">+</button>
        </form>

        <!-- Die Liste wird um den Löschen-Button erweitert -->
        <ul class="item-list">
          <li v-for="item in masterData[type]" :key="item.id">
            <span>{{ item.name }}</span>
            <!-- ========================================================== -->
            <!-- NEU: Der Button zum Löschen -->
            <!-- ========================================================== -->
            <button @click="handleDeleteItem(type, item.id)" class="delete-btn" title="Löschen">
              🗑️
            </button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.master-data-container {
  max-width: 1200px;
  margin: 0 auto;
}

.grid {
  display: grid;
  /* Passt die Anzahl der Spalten an die Bildschirmbreite an */
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.card {
  background-color: var(--card-bg);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  border: 1px solid var(--color-border);
}

.card h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.75rem;
  color: var(--text-strong);
}

.add-form {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.add-form input {
  flex-grow: 1;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.add-form button {
  flex-shrink: 0;
  width: 44px;
  border: none;
  background-color: #42b883;
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.add-form button:hover {
  background-color: #369469;
}

.item-list {
  list-style: none;
  padding: 0;
  margin: 0;
  overflow-y: auto; /* Falls die Liste sehr lang wird */
}

.item-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0.5rem;
  border-bottom: 1px solid var(--color-border);
}

.item-list li:last-child {
  border-bottom: none;
}

/* ========================================================== */
/* NEU: Style für den Löschen-Button */
/* ========================================================== */
.delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  padding: 0.5rem;
  border-radius: 50%;
  line-height: 1;
  width: 32px;
  height: 32px;
  transition: background-color 0.2s, color 0.2s;
}

.delete-btn:hover {
  background-color: #fce8e6; /* Leichter roter Hintergrund */
  color: #d93025; /* Rote Farbe für das Icon */
}

.error-message {
  color: #d93025;
  background-color: #fce8e6;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
}
</style>
