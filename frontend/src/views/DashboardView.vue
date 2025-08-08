<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';

const isLoading = ref(true);
const error = ref('');
const stats = ref({
  totalAssets: 0,
  inUse: 0,
  inStock: 0,
  inRepair: 0,
  byType: [],
});

const fetchStats = async () => {
  try {
    // Minimaler Ansatz: wir laden Assets und aggregieren clientseitig
    const res = await api.get('/api/v1/assets/?limit=1000');
    const items = res.data || [];
    stats.value.totalAssets = items.length;
    stats.value.inUse = items.filter((a) => a.status?.name?.toLowerCase().includes('betrieb')).length;
    stats.value.inStock = items.filter((a) => a.status?.name?.toLowerCase().includes('lager')).length;
    stats.value.inRepair = items.filter((a) => a.status?.name?.toLowerCase().includes('repar')).length;
    const map = new Map();
    for (const a of items) {
      const key = a.asset_type?.name || 'Unbekannt';
      map.set(key, (map.get(key) || 0) + 1);
    }
    stats.value.byType = Array.from(map.entries()).map(([name, count]) => ({ name, count }));
  } catch (e) {
    error.value = 'Dashboard-Daten konnten nicht geladen werden.';
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchStats);
</script>

<template>
  <div>
    <h2>Dashboard</h2>
    <div v-if="isLoading">Lade...</div>
    <div v-else>
      <div class="cards">
        <div class="kpi-card">
          <div class="kpi-value">{{ stats.totalAssets }}</div>
          <div class="kpi-label">Gesamt-Assets</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-value">{{ stats.inUse }}</div>
          <div class="kpi-label">Im Betrieb</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-value">{{ stats.inStock }}</div>
          <div class="kpi-label">An Lager</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-value">{{ stats.inRepair }}</div>
          <div class="kpi-label">In Reparatur</div>
        </div>
      </div>

      <div class="widgets">
        <div class="widget">
          <h3>Geräte nach Typ</h3>
          <ul class="type-list">
            <li v-for="item in stats.byType" :key="item.name">
              <span>{{ item.name }}</span>
              <span class="badge">{{ item.count }}</span>
            </li>
          </ul>
        </div>

        <div class="widget">
          <h3>Schnellaktionen</h3>
          <div class="actions">
            <router-link to="/inventory" class="btn primary">Neues Asset</router-link>
            <router-link to="/master-data" class="btn">Stammdaten pflegen</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
h2 { margin: 0 0 1rem; }
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}
.kpi-card {
  background: var(--card-bg);
  border: 1px solid var(--color-border);
  border-radius: 10px;
  padding: 1rem 1.25rem;
  box-shadow: 0 2px 6px rgba(0,0,0,0.04);
}
.kpi-value { font-size: 2rem; font-weight: 800; color: var(--text-strong); }
.kpi-label { color: var(--text-muted); }
.widgets {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1rem;
  margin-top: 1rem;
}
.widget {
  background: var(--card-bg);
  border: 1px solid var(--color-border);
  border-radius: 10px;
  padding: 1rem 1.25rem;
}
.type-list { list-style: none; margin: 0; padding: 0; }
.type-list li {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.6rem 0; border-bottom: 1px solid #f3f4f6;
}
.type-list li:last-child { border-bottom: none; }
.badge {
  background: var(--accent-weak); color: var(--accent-strong); font-weight: 700;
  border-radius: 999px; padding: 0.15rem 0.5rem; font-size: 0.85rem;
}
.actions { display: flex; gap: 0.5rem; }
.btn {
  display: inline-block; text-decoration: none; color: var(--text-strong); background: var(--btn-bg);
  padding: 0.6rem 0.9rem; border-radius: 8px; border: 1px solid var(--color-border);
}
.btn.primary { background: var(--accent); color: #063523; border-color: var(--accent); }
</style>


