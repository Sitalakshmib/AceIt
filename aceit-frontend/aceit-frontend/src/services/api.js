import axios from 'axios';

// Use the proxy path for API requests
const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('aceit_access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Real APIs
export const authAPI = {
  login: async (email, password) => {
    const res = await api.post('/auth/login', { email, password });
    const { access_token } = res.data;
    if (access_token) localStorage.setItem('aceit_access_token', access_token);
    return res;
  },
  register: async (userData) => {
    const res = await api.post('/auth/register', userData);
    return res;
  }
};

export const aptitudeAPI = {
  getQuestions: () => api.get('/aptitude/questions'),
  submitAnswers: (answers) => api.post('/aptitude/submit', { answers }),
};

export const codingAPI = {
  getProblems: () => api.get('/coding/problems'),
  submitCode: (problemId, code) => api.post('/coding/submit', { problemId, code }),
};

export default api;