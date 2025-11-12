import axios from 'axios';
import { API_BASE_URL } from '../config';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
