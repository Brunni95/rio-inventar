// Datei: frontend/src/api.js

import axios from 'axios';
import { acquireToken, logout } from './authService';

// Erstelle eine neue axios-Instanz.
// WICHTIG: Die baseURL sollte NUR die Adresse deines Backends sein, OHNE /api/v1.
// Der Port (hier :8000) muss mit dem Port übereinstimmen, den dein Backend in docker-compose.yml verwendet.
const apiBaseUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
const apiClient = axios.create({
  baseURL: apiBaseUrl,
});

// Ein "Interceptor" ist eine Funktion, die bei jeder Anfrage ausgeführt wird,
// bevor sie tatsächlich an das Backend gesendet wird.
apiClient.interceptors.request.use(
  async (config) => {
    // Hole den Authentifizierungs-Token für den aktuellen Benutzer.
    const token = await acquireToken();

    // Wenn ein Token vorhanden ist, füge ihn zum "Authorization"-Header hinzu.
    // Das Backend verwendet diesen Header, um den Benutzer zu authentifizieren.
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Gib die modifizierte Konfiguration zurück, damit die Anfrage gesendet werden kann.
    return config;
  },
  (error) => {
    // Falls beim Erstellen der Anfrage ein Fehler auftritt.
    console.error('Fehler im Axios Request Interceptor:', error);
    return Promise.reject(error);
  }
);

// Antwort-Interceptor: Bei 401 ggf. ausloggen
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
