import { ref } from 'vue';
import api from '../api';

export function useApiList(endpoint, { defaultSortBy = 'id', defaultSortDir = 'desc', defaultPageSize = 10 } = {}) {
  const items = ref([]);
  const total = ref(0);
  const error = ref('');
  const search = ref('');
  const sortBy = ref(defaultSortBy);
  const sortDir = ref(defaultSortDir);
  const page = ref(1);
  const pageSize = ref(defaultPageSize);

  async function fetchList() {
    try {
      const params = new URLSearchParams();
      if (search.value) params.append('search', search.value);
      params.append('order_by', sortBy.value);
      params.append('order_dir', sortDir.value);
      params.append('skip', String((page.value - 1) * pageSize.value));
      params.append('limit', String(pageSize.value));
      const res = await api.get(`${endpoint}?${params.toString()}`);
      items.value = res.data.items;
      total.value = res.data.total;
    } catch (e) {
      error.value = 'Daten konnten nicht geladen werden';
      // eslint-disable-next-line no-console
      console.error(e);
    }
  }

  return { items, total, error, search, sortBy, sortDir, page, pageSize, fetchList };
}


