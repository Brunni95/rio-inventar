<script setup>
import { computed } from 'vue';

const props = defineProps({
  page: { type: Number, required: true },
  pageSize: { type: Number, required: true },
  total: { type: Number, required: true },
  pageSizes: { type: Array, default: () => [10, 25, 50] },
});

const emit = defineEmits(['update:page', 'update:pageSize']);

const totalPages = computed(() => Math.max(1, Math.ceil(props.total / props.pageSize)));

const go = (p) => {
  const tp = totalPages.value;
  const next = Math.min(Math.max(1, p), tp);
  if (next !== props.page) emit('update:page', next);
};

const setSize = (size) => {
  if (size !== props.pageSize) {
    emit('update:pageSize', Number(size));
    emit('update:page', 1);
  }
};
</script>

<template>
  <div class="pagination" v-if="total > pageSize">
    <button type="button" :disabled="page===1" @click="go(1)">« Erste</button>
    <button type="button" :disabled="page===1" @click="go(page-1)">‹ Zurück</button>
    <span>Seite {{ page }} / {{ totalPages }} ({{ total }} Einträge)</span>
    <button type="button" :disabled="page===totalPages" @click="go(page+1)">Weiter ›</button>
    <button type="button" :disabled="page===totalPages" @click="go(totalPages)">Letzte »</button>
    <label class="page-size">
      Pro Seite:
      <select :value="pageSize" @change="setSize($event.target.value)">
        <option v-for="s in pageSizes" :key="s" :value="s">{{ s }}</option>
      </select>
    </label>
  </div>
  <div v-else class="pagination-placeholder" />
  
</template>

<style scoped>
.pagination {
  display: flex; align-items: center; gap: 0.5rem; margin-top: 0.75rem;
}
.pagination button {
  background: var(--btn-bg); color: var(--text-strong); border: 1px solid var(--color-border);
  border-radius: 6px; padding: 0.4rem 0.6rem;
}
.pagination button:disabled { opacity: 0.5; cursor: not-allowed; }
.pagination .page-size select {
  background: var(--btn-bg); color: var(--text-strong); border: 1px solid var(--color-border);
  border-radius: 6px; padding: 0.2rem 0.4rem;
}
</style>


