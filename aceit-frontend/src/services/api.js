import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
const api = axios.create({
  baseURL: API_BASE_URL,
});

export { API_BASE_URL };

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('aceit_access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Helper function to get current user ID
const getCurrentUserId = () => {
  const user = JSON.parse(localStorage.getItem('aceit_user'));
  return user?.id;
};

// Real APIs
export const authAPI = {
  login: async (email, password) => {
    const res = await api.post('/auth/login', { email, password });
    const { access_token, user } = res.data;
    if (access_token) {
      localStorage.setItem('aceit_access_token', access_token);
      localStorage.setItem('aceit_user', JSON.stringify(user));
    }
    return res;
  },
  register: async (userData) => {
    const res = await api.post('/auth/register', userData);
    return res;
  }
};

export const aptitudeAPI = {
  getQuestions: (params = {}) => api.get('/aptitude/questions', { params }),
  submitAnswers: (answers) => {
    const userId = getCurrentUserId();
    return api.post('/aptitude/submit', {
      user_id: userId,  // Add user_id here
      answers
    });
  },
  getCategories: () => api.get('/aptitude/categories'),
  getDetailedResults: (data) => api.post('/aptitude/detailed-results', data),
};

export const codingAPI = {
  getProblems: () => api.get('/coding/problems'),
  submitCode: (problemId, code, language = 'python') => {
    const userId = getCurrentUserId();
    return api.post('/coding/submit', {
      problemId,
      code,
      language,
      user_id: userId
    });
  },
};

export const resumeAPI = {
  analyze: (formData) => {
    const userId = getCurrentUserId();
    console.log('[API] resumeAPI.analyze called');
    console.log('[API] userId from localStorage:', userId);

    const formDataWithUserId = new FormData();
    formDataWithUserId.append('user_id', userId || 'guest_user');
    // Append all files and data from original formData
    for (const [key, value] of formData.entries()) {
      console.log('[API] Appending:', key, value);
      formDataWithUserId.append(key, value);
    }

    return api.post('/resume/analyze', formDataWithUserId, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  getJobRoles: () => api.get('/resume/job-roles'),
};

export const progressAPI = {
  getUserProgress: (userId) => api.get(`/progress/${userId}`),
};

export default api;