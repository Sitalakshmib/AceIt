import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';
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
  getQuestions: (params = {}) => api.get('/aptitude/questions', { params }),
  submitAnswers: (answers) => api.post('/aptitude/submit', { answers }),
  getTopics: () => api.get('/aptitude/topics'),
  getDetailedResults: (data) => api.post('/aptitude/detailed-results', data),
};

export const codingAPI = {
  getProblems: () => api.get('/coding/problems'),
  submitCode: (problemId, code) => api.post('/coding/submit', { problemId, code }),
};

export const resumeAPI = {
  analyze: (formData) => api.post('/resume/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  getJobRoles: () => api.get('/resume/job-roles'),
};

export const progressAPI = {
  getUserProgress: (userId) => api.get(`/progress/${userId}`),
};

export default api;