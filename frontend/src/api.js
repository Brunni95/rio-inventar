import axios from 'axios';
import { acquireToken, logout } from './authService';

// Axios client configured with backend base URL (without /api/v1)
const apiBaseUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
const apiClient = axios.create({
  baseURL: apiBaseUrl,
});

// Attach bearer token to every request
apiClient.interceptors.request.use(
  async (config) => {
    const token = await acquireToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    console.error('Fehler im Axios Request Interceptor:', error);
    return Promise.reject(error);
  }
);

// Logout on 401 (token expired/invalid)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error?.response?.status === 401) {
      // Token abgelaufen/ungültig → Benutzer abmelden
      try { logout(); } catch (_) {}
    }
    return Promise.reject(error);
  }
);

// Exportiere die konfigurierte apiClient-Instanz, damit sie in anderen
// Teilen der Anwendung (z.B. in InventoryView.vue) importiert und verwendet werden kann.
export default apiClient;
