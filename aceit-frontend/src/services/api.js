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
  try {
    const userStr = localStorage.getItem('aceit_user');
    if (!userStr) {
      console.warn('[API] No user found in localStorage, using guest_user');
      return 'guest_user';
    }
    const user = JSON.parse(userStr);
    const userId = user?.id || user?.user_id || 'guest_user';
    console.log('[API] Current user ID:', userId);
    return userId;
  } catch (error) {
    console.error('[API] Error getting user ID:', error);
    return 'guest_user';
  }
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
      user_id: userId,
      answers
    });
  },
  getCategories: () => api.get('/aptitude/categories'),
  getDetailedResults: (data) => api.post('/aptitude/detailed-results', data),

  // New adaptive practice endpoints
  getNextQuestion: (category, topic = null, reset = false) => {
    const userId = getCurrentUserId();
    const params = new URLSearchParams({ user_id: userId, category });
    if (topic) params.append('topic', topic);
    if (reset) params.append('reset', 'true');
    return api.get(`/aptitude/practice/next-question?${params.toString()}`);
  },
  submitPracticeAnswer: (questionId, userAnswer, timeSpent, shuffledOptions = null) => {
    const userId = getCurrentUserId();
    return api.post('/aptitude/practice/submit-answer', {
      user_id: userId,
      question_id: questionId,
      user_answer: userAnswer,
      time_spent: timeSpent,
      shuffled_options: shuffledOptions
    });
  },
  getUserProficiency: () => {
    const userId = getCurrentUserId();
    return api.get(`/aptitude/proficiency/${userId}`);
  }
};

// Mock Test APIs
export const mockTestAPI = {
  generateTest: (testType, category = null, topic = null) => {
    return api.post('/mock-tests/generate', {
      test_type: testType,
      category,
      topic
    });
  },
  getTest: (testId) => api.get(`/mock-tests/${testId}`),
  startTest: (testId) => {
    const userId = getCurrentUserId();
    return api.post(`/mock-tests/${testId}/start`, { user_id: userId });
  },
  submitAnswer: (testId, attemptId, questionId, userAnswer, timeSpent, answerText = null) => {
    return api.post(`/mock-tests/${testId}/submit-answer`, {
      attempt_id: attemptId,
      question_id: questionId,
      user_answer: userAnswer,
      answer_text: answerText,
      time_spent: timeSpent
    });
  },
  completeTest: (testId, attemptId) => {
    return api.post(`/mock-tests/${testId}/complete`, { attempt_id: attemptId });
  },
  getResults: (testId, attemptId) => {
    return api.get(`/mock-tests/${testId}/results/${attemptId}`);
  },
  getUserAttempts: () => {
    const userId = getCurrentUserId();
    return api.get(`/mock-tests/user/${userId}/attempts`);
  }
};

// Analytics APIs
export const analyticsAPI = {
  getDashboard: () => {
    const userId = getCurrentUserId();
    return api.get(`/analytics/dashboard/${userId}`);
  },
  getProgressHistory: (days = 30) => {
    const userId = getCurrentUserId();
    return api.get(`/analytics/progress/${userId}`, { params: { days } });
  },
  getTopicAnalytics: (topic) => {
    const userId = getCurrentUserId();
    return api.get(`/analytics/topic/${userId}/${topic}`);
  },
  getDailyProgress: (days = 7) => {
    const userId = getCurrentUserId();
    return api.get(`/analytics/daily-progress?user_id=${userId}&days=${days}&_t=${Date.now()}`);
  },
  getMockReport: () => {
    const userId = getCurrentUserId();
    return api.get(`/analytics/mock-report?user_id=${userId}&_t=${Date.now()}`);
  },
  getAICoach: () => {
    const userId = getCurrentUserId();
    return api.get(`/analytics/ai-coach?user_id=${userId}&_t=${Date.now()}`);
  },
  getOverallSummary: () => {
    const userId = getCurrentUserId();
    return api.get(`/analytics/overall-summary?user_id=${userId}&_t=${Date.now()}`);
  },
  getUnifiedAnalytics: () => {
    const userId = getCurrentUserId();
    return api.get(`/analytics/unified/${userId}`);
  },
  startCoach: () => {
    const userId = getCurrentUserId();
    const formData = new FormData();
    formData.append('user_id', userId);
    return api.post('/analytics/coach/start', formData);
  },
  sendCoachMessage: (sessionId, textMessage = null, audioBlob = null) => {
    const formData = new FormData();
    formData.append('session_id', sessionId);
    if (textMessage) formData.append('text_message', textMessage);
    if (audioBlob) formData.append('audio_file', audioBlob, 'coach_audio.webm');
    return api.post('/analytics/coach/answer', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  generateCoachAudio: (text) => {
    const formData = new FormData();
    formData.append('text', text);
    return api.post('/analytics/coach/audio', formData);
  }
};

export const codingAPI = {
  getProblems: () => api.get('/coding/problems'),
  getProblemDetails: (problemId) => api.get(`/coding/problems/${problemId}`),
  submitCode: (problemId, code, language = 'python', action = 'run') => {
    const userId = getCurrentUserId();
    return api.post('/coding/submit', {
      problemId,
      code,
      language,
      user_id: userId,
      action  // 'run' or 'submit'
    });
  },
  getSolvedProblems: () => {
    const userId = getCurrentUserId();
    return api.get('/coding/user-progress', {
      params: { user_id: userId }
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

  // Resume Creator endpoints
  generateContent: (data) => api.post('/resume/generate-content', data),

  download: (userData, generatedContent, templateType, styleOptions) => {
    return api.post('/resume/download-resume', {
      user_data: userData,
      generated_content: generatedContent,
      template_type: templateType,
      style_options: styleOptions
    }, {
      responseType: 'blob'
    });
  }
};

export const progressAPI = {
  getUserProgress: (userId) => api.get(`/progress/${userId}`),
};

export default api;