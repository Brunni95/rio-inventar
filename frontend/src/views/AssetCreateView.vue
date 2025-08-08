<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

const locations = ref([]);
const manufacturers = ref([]);
const statuses = ref([]);
const assetTypes = ref([]);
const suppliers = ref([]);
const users = ref([]);

const newAssetForm = ref({
  inventory_number: '', serial_number: '', model: '', purchase_price: null,
  department: '', os_version: '', installation_date: null, warranty_expiry: null,
  purchase_date: null, notes: '', ip_address: '', hostname: '', mac_address: '',
  room: '', asset_type_id: null, manufacturer_id: null, status_id: null, location_id: null,
  supplier_id: null, user_id: null,
});

async function fetchDropdownData() {
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
}

async function handleSubmit() {
  const payload = { ...newAssetForm.value };
  for (const key of ['installation_date', 'warranty_expiry', 'purchase_date']) {
    if (!payload[key]) payload[key] = null;
  }
  if (route.name === 'AssetEdit' && route.params.id) {
    await api.put(`/api/v1/assets/${route.params.id}`, payload);
  } else {
    await api.post('/api/v1/assets/', payload);
  }
  router.push('/inventory');
}

onMounted(async () => {
  await fetchDropdownData();
  // If editing, preload asset data
  if (route.name === 'AssetEdit' && route.params.id) {
    const res = await api.get(`/api/v1/assets/${route.params.id}`);
    const asset = res.data;
    newAssetForm.value = {
      ...asset,
      asset_type_id: asset.asset_type?.id ?? null,
      manufacturer_id: asset.manufacturer?.id ?? null,
      status_id: asset.status?.id ?? null,
      location_id: asset.location?.id ?? null,
      supplier_id: asset.supplier?.id ?? null,
      user_id: asset.user?.id ?? null,
      room: asset.room || '',
    };
  }
});
</script>

<template>
  <div class="inventory-container">
    <section class="card">
      <div class="header">
        <h2>{{ route.name === 'AssetEdit' ? 'Asset bearbeiten' : 'Neues Asset hinzufügen' }}</h2>
        <button class="btn" @click="router.push('/inventory')">Zurück zur Liste</button>
      </div>
      <!-- Reuse same structured form layout as in InventoryView -->
      <form @submit.prevent="handleSubmit">
        <div class="form-sections">
          <div class="form-section">
            <h3 class="section-title">Identifikation</h3>
            <div class="grid-2">
              <div class="form-control">
                <label for="inventory_number">Inventarnummer <span class="req">*</span></label>
                <input id="inventory_number" v-model="newAssetForm.inventory_number" required placeholder="z. B. IT-LAP-001" />
                <small class="hint">Eindeutige Kennung</small>
              </div>
              <div class="form-control">
                <label for="asset_type_id">Geräte-Typ <span class="req">*</span></label>
                <select id="asset_type_id" v-model="newAssetForm.asset_type_id" required>
                  <option :value="null" disabled>Bitte wählen…</option>
                  <option v-for="type in assetTypes" :key="type.id" :value="type.id">{{ type.name }}</option>
                </select>
              </div>
              <div class="form-control">
                <label for="manufacturer_id">Hersteller <span class="req">*</span></label>
                <select id="manufacturer_id" v-model="newAssetForm.manufacturer_id" required>
                  <option :value="null" disabled>Bitte wählen…</option>
                  <option v-for="man in manufacturers" :key="man.id" :value="man.id">{{ man.name }}</option>
                </select>
              </div>
              <div class="form-control">
                <label for="model">Modell</label>
                <input id="model" v-model="newAssetForm.model" placeholder="z. B. Latitude 7440" />
              </div>
              <div class="form-control">
                <label for="serial_number">Seriennummer</label>
                <input id="serial_number" v-model="newAssetForm.serial_number" placeholder="Seriennummer" />
              </div>
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-title">Zuweisung & Standort</h3>
            <div class="grid-2">
              <div class="form-control">
                <label for="status_id">Status <span class="req">*</span></label>
                <select id="status_id" v-model="newAssetForm.status_id" required>
                  <option :value="null" disabled>Bitte wählen…</option>
                  <option v-for="stat in statuses" :key="stat.id" :value="stat.id">{{ stat.name }}</option>
                </select>
              </div>
              <div class="form-control">
                <label for="location_id">Standort <span class="req">*</span></label>
                <select id="location_id" v-model="newAssetForm.location_id" required>
                  <option :value="null" disabled>Bitte wählen…</option>
                  <option v-for="loc in locations" :key="loc.id" :value="loc.id">{{ loc.name }}</option>
                </select>
              </div>
              <div class="form-control">
                <label for="user_id">Benutzer</label>
                <select id="user_id" v-model="newAssetForm.user_id">
                  <option :value="null">-- Keinem Benutzer zugewiesen --</option>
                  <option v-for="user in users" :key="user.id" :value="user.id">{{ user.display_name }}</option>
                </select>
              </div>
              <div class="form-control">
                <label for="room">Raum</label>
                <input id="room" v-model="newAssetForm.room" placeholder="z. B. A101" />
              </div>
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-title">Kauf & Garantie</h3>
            <div class="grid-2">
              <div class="form-control">
                <label for="purchase_price">Kaufpreis</label>
                <input id="purchase_price" v-model.number="newAssetForm.purchase_price" type="number" step="0.01" placeholder="z. B. 2200.50" />
              </div>
              <div class="form-control">
                <label for="supplier_id">Lieferant</label>
                <select id="supplier_id" v-model="newAssetForm.supplier_id">
                  <option :value="null">-- Kein Lieferant --</option>
                  <option v-for="sup in suppliers" :key="sup.id" :value="sup.id">{{ sup.name }}</option>
                </select>
              </div>
              <div class="form-control">
                <label for="purchase_date">Kaufdatum</label>
                <input id="purchase_date" v-model="newAssetForm.purchase_date" type="date" />
              </div>
              <div class="form-control">
                <label for="warranty_expiry">Garantie bis</label>
                <input id="warranty_expiry" v-model="newAssetForm.warranty_expiry" type="date" />
              </div>
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-title">Netzwerk</h3>
            <div class="grid-2">
              <div class="form-control">
                <label for="hostname">Hostname</label>
                <input id="hostname" v-model="newAssetForm.hostname" placeholder="Hostname" />
              </div>
              <div class="form-control">
                <label for="ip_address">IP-Adresse</label>
                <input id="ip_address" v-model="newAssetForm.ip_address" placeholder="z. B. 10.0.0.5" />
              </div>
              <div class="form-control">
                <label for="mac_address">MAC-Adresse</label>
                <input id="mac_address" v-model="newAssetForm.mac_address" placeholder="AA:BB:CC:DD:EE:FF" />
              </div>
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-title">Notizen</h3>
            <div class="form-control">
              <label for="notes" class="sr-only">Notizen</label>
              <textarea id="notes" v-model="newAssetForm.notes" placeholder="Relevante Hinweise, Zubehör, Besonderheiten…"></textarea>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-primary">Asset erstellen</button>
          <button @click="router.push('/inventory')" type="button" class="btn ghost">Abbrechen</button>
        </div>
      </form>
    </section>
  </div>
</template>

<style scoped>
.inventory-container { display: flex; flex-direction: column; gap: 2rem; }
.card { background-color: var(--card-bg); border-radius: 8px; padding: 1.5rem; box-shadow: none; border: 1px solid var(--color-border); }
.header { display:flex; justify-content: space-between; align-items:center; margin-bottom: 0.5rem; }
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
</style>


