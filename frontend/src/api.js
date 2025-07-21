// frontend/src/api.js
import axios from 'axios';
import { acquireToken } from './authService';

const api = axios.create({
  baseURL: 'http://localhost:8000'
});

api.interceptors.request.use(async (config) => {
  const token = await acquireToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
