import axios from 'axios';

// In production, API is on same domain with /api prefix
// In development, use localhost
const API_URL = import.meta.env.PROD ? '/api' : 'http://localhost:8000/api';

const API = axios.create({
  baseURL: API_URL,
  withCredentials: true,
});

// Add token to requests
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default API;