// Mock data for development and demonstration
export const generateMockProgressData = (userId) => {
  const today = new Date();
  const lastWeek = new Date(today);
  lastWeek.setDate(lastWeek.getDate() - 7);

  // Generate daily activity for last 7 days
  const dailyActivity = [];
  for (let i = 6; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);

    dailyActivity.push({
      date: date.toISOString().split('T')[0],
      aptitude: Math.floor(Math.random() * 20) + 5,
      coding: Math.floor(Math.random() * 15) + 3,
      interviews: Math.floor(Math.random() * 3),
      score: Math.floor(Math.random() * 30) + 40
    });
  }

  // Generate skill distribution
  const skills = ['Quantitative', 'Logical', 'Verbal', 'Programming', 'DSA', 'System Design'];
  const skillData = skills.map(skill => ({
    name: skill,
    score: Math.floor(Math.random() * 50) + 30,
    questions: Math.floor(Math.random() * 50) + 10
  }));

  return {
    user_id: userId,
    overall_score: 65,
    daily_streak: 7,
    total_time_spent: 1280,
    aptitude: {
      tests_taken: 12,
      average_score: 72,
      best_score: 88,
      total_questions_attempted: 240,
      accuracy: 78,
      weak_areas: ['Probability', 'Time & Work'],
      strong_areas: ['Percentages', 'Ratios']
    },
    coding: {
      problems_attempted: 45,
      average_success_rate: 65,
      total_tests_passed: 128,
      total_tests_attempted: 195,
      languages: {
        'Python': 25,
        'Java': 12,
        'JavaScript': 8
      },
      difficulty_distribution: {
        'Easy': 20,
        'Medium': 18,
        'Hard': 7
      }
    },
    recent_activity: [
      { type: 'aptitude_test', score: 85, date: '2025-12-24', duration: '30 min' },
      { type: 'coding_problem', problem: 'Two Sum', success: true, date: '2025-12-23' },
      { type: 'mock_interview', score: 7.5, date: '2025-12-22', feedback: 'Good communication skills' },
      { type: 'aptitude_test', score: 72, date: '2025-12-21', duration: '25 min' },
      { type: 'coding_problem', problem: 'Reverse Linked List', success: true, date: '2025-12-20' }
    ],
    weekly_activity: dailyActivity,
    skill_distribution: skillData,
    achievements: [
      { id: 1, name: 'First Steps', description: 'Complete 10 questions', unlocked: true, icon: '' },
      { id: 2, name: 'Code Warrior', description: 'Solve 5 coding problems', unlocked: true, icon: '' },
      { id: 3, name: 'Aptitude Ace', description: 'Score 80+ in aptitude test', unlocked: false, icon: '' },
      { id: 4, name: '7-Day Streak', description: 'Practice for 7 consecutive days', unlocked: true, icon: '' }
    ],
    upcoming_goals: [
      { id: 1, goal: 'Complete 20 aptitude questions', progress: 15, total: 20 },
      { id: 2, goal: 'Solve 3 medium coding problems', progress: 1, total: 3 },
      { id: 3, goal: 'Take 1 mock interview', progress: 0, total: 1 }
    ],
    recommendations: [
      'Practice probability questions - your accuracy is 45%',
      'Try solving "Binary Search" problems - matches your skill level',
      'Schedule a mock interview for next week'
    ]
  };
};

export const getEmptyProgressData = (userId) => {
  return {
    user_id: userId,
    overall_score: 0,
    aptitude: { tests_taken: 0, average_score: 0, best_score: 0, total_questions_attempted: 0 },
    coding: { problems_attempted: 0, average_success_rate: 0, total_tests_passed: 0, total_tests_attempted: 0 },
    recent_activity: [],
    summary: {
      total_activities: 0,
      improvement_tips: [
        'Start practicing aptitude tests to improve your quantitative skills',
        'Try solving coding problems to enhance your programming skills',
        'Take a mock interview to practice communication skills'
      ]
    }
  };
};