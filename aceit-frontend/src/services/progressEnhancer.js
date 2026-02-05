// Progress Data Enhancer - Combines real backend data with mock visualizations
export const enhanceProgressData = (realData) => {
  if (!realData) return generateEmptyEnhancedData();

  const today = new Date();
  const userId = realData.user_id || 'unknown';

  // Generate mock visualizations based on real data
  const weeklyActivity = generateWeeklyActivityFromRealData(realData);
  const skillDistribution = generateSkillDistributionFromRealData(realData);
  const achievements = generateAchievementsFromRealData(realData);
  const recommendations = generateRecommendationsFromRealData(realData);
  const goals = generateGoalsFromRealData(realData);

  return {
    // REAL DATA (from backend)
    user_id: userId,
    overall_score: realData.overall_score || 0,
    daily_streak: calculateDailyStreak(realData.recent_activity || []),
    total_time_spent: calculateTotalTimeSpent(realData.recent_activity || []),

    // Real module data
    aptitude: {
      tests_taken: realData.aptitude?.tests_taken || 0,
      average_score: realData.aptitude?.average_score || 0,
      best_score: realData.aptitude?.best_score || 0,
      total_questions_attempted: realData.aptitude?.total_questions_attempted || 0,
      accuracy: realData.aptitude?.average_score || 0,
      weak_areas: identifyWeakAreas(realData, 'aptitude'),
      strong_areas: identifyStrongAreas(realData, 'aptitude')
    },

    coding: {
      problems_attempted: realData.coding?.problems_attempted || 0,
      average_success_rate: realData.coding?.average_success_rate || 0,
      total_tests_passed: realData.coding?.total_tests_passed || 0,
      total_tests_attempted: realData.coding?.total_tests_attempted || 0,
      languages: analyzeLanguages(realData.recent_activity || []),
      difficulty_distribution: analyzeDifficulty(realData.recent_activity || [])
    },

    // Enhanced data (mock + real)
    recent_activity: formatRecentActivity(realData.recent_activity || []),
    weekly_activity: weeklyActivity,
    skill_distribution: skillDistribution,
    achievements: achievements,
    upcoming_goals: goals,
    recommendations: recommendations,

    // Metadata
    summary: {
      total_activities: realData.summary?.total_activities ||
        (realData.aptitude?.tests_taken || 0) +
        (realData.coding?.problems_attempted || 0),
      improvement_tips: realData.summary?.improvement_tips || recommendations
    }
  };
};

// Helper functions
const generateWeeklyActivityFromRealData = (realData) => {
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  const today = new Date();

  return days.map((day, index) => {
    const date = new Date(today);
    date.setDate(date.getDate() - (6 - index));
    const dateStr = date.toISOString().split('T')[0];

    // Check if we have real activity for this day
    const dayActivity = (realData.recent_activity || []).filter(activity =>
      activity.timestamp && activity.timestamp.includes(dateStr)
    );

    if (dayActivity.length > 0) {
      const aptitudeCount = dayActivity.filter(a => a.module === 'aptitude').length;
      const codingCount = dayActivity.filter(a => a.module === 'coding').length;
      const interviewCount = dayActivity.filter(a => a.module && a.module.includes('interview')).length;

      return {
        day,
        date: dateStr,
        aptitude: aptitudeCount * 2, // Scale for visualization
        coding: codingCount * 2,
        interviews: interviewCount,
        score: calculateDailyScore(dayActivity)
      };
    }

    // Fallback to mock data
    return {
      day,
      date: dateStr,
      aptitude: Math.floor(Math.random() * 5) + (realData.aptitude?.tests_taken > 0 ? 1 : 0),
      coding: Math.floor(Math.random() * 4) + (realData.coding?.problems_attempted > 0 ? 1 : 0),
      interviews: Math.floor(Math.random() * 2),
      score: Math.floor(Math.random() * 20) + 40
    };
  });
};

const generateSkillDistributionFromRealData = (realData) => {
  const baseSkills = [
    { name: 'Quantitative', baseScore: realData.aptitude?.average_score || 0 },
    { name: 'Logical', baseScore: realData.aptitude?.average_score ? realData.aptitude.average_score - 10 : 0 },
    { name: 'Verbal', baseScore: realData.aptitude?.average_score ? realData.aptitude.average_score - 5 : 0 },
    { name: 'Programming', baseScore: realData.coding?.average_success_rate || 0 },
    { name: 'Problem Solving', baseScore: realData.coding?.average_success_rate ? realData.coding.average_success_rate - 5 : 0 },
    { name: 'System Design', baseScore: 0 }
  ];

  return baseSkills.map(skill => ({
    name: skill.name,
    score: Math.max(10, Math.min(100, skill.baseScore + Math.floor(Math.random() * 20))),
    questions: Math.floor(Math.random() * 30) +
      (skill.name === 'Programming' ? (realData.coding?.problems_attempted || 0) * 2 : 0) +
      (['Quantitative', 'Logical', 'Verbal'].includes(skill.name) ? (realData.aptitude?.total_questions_attempted || 0) / 3 : 0)
  }));
};

const generateAchievementsFromRealData = (realData) => {
  const achievements = [];

  // First Steps - Complete any question
  if ((realData.aptitude?.tests_taken || 0) + (realData.coding?.problems_attempted || 0) > 0) {
    achievements.push({
      id: 1,
      name: 'Quant Master',
      description: 'Complete 50 Quantitative questions',
      unlocked: true,
      icon: ''
    });
  }

  // Code Warrior - Solve coding problems
  if ((realData.coding?.problems_attempted || 0) >= 5) {
    achievements.push({
      id: 2,
      name: 'Code Warrior',
      description: 'Solve 5 coding problems',
      unlocked: true,
      icon: ''
    });
  }

  // Aptitude Ace - Score 80+ in aptitude
  if ((realData.aptitude?.average_score || 0) >= 80) {
    achievements.push({
      id: 3,
      name: 'Aptitude Ace',
      description: 'Score 80+ in aptitude test',
      unlocked: true,
      icon: ''
    });
  } else {
    achievements.push({
      id: 3,
      name: 'Aptitude Ace',
      description: 'Score 80+ in aptitude test',
      unlocked: false,
      icon: ''
    });
  }

  // Consistency - Based on recent activity
  const recentDays = new Set((realData.recent_activity || []).map(a =>
    a.timestamp ? a.timestamp.split('T')[0] : ''
  )).size;

  if (recentDays >= 7) {
    achievements.push({
      id: 4,
      name: 'Practice Streak',
      description: 'Practice for 7 consecutive days',
      unlocked: true,
      icon: ''
    });
  } else if (recentDays >= 3) {
    achievements.push({
      id: 4,
      name: `${recentDays}-Day Streak`,
      description: `Practice for ${recentDays} days`,
      unlocked: true,
      icon: '🔥'
    });
  }

  return achievements;
};

const generateRecommendationsFromRealData = (realData) => {
  const recommendations = [];

  // Based on aptitude performance
  if ((realData.aptitude?.tests_taken || 0) === 0) {
    recommendations.push('Start practicing aptitude tests to improve your quantitative skills');
  } else if ((realData.aptitude?.average_score || 0) < 60) {
    recommendations.push(`Practice more aptitude questions - current score: ${realData.aptitude.average_score}%`);
  }

  // Based on coding performance
  if ((realData.coding?.problems_attempted || 0) === 0) {
    recommendations.push('Try solving coding problems to enhance your programming skills');
  } else if ((realData.coding?.average_success_rate || 0) < 50) {
    recommendations.push(`Focus on understanding test cases - success rate: ${realData.coding.average_success_rate}%`);
  }

  // Based on interview activity
  const hasInterviews = (realData.recent_activity || []).some(a =>
    a.module && a.module.includes('interview')
  );
  if (!hasInterviews) {
    recommendations.push('Take a mock interview to practice communication skills');
  }

  // Add generic recommendations if we don't have enough
  if (recommendations.length < 3) {
    const generic = [
      'Review data structures and algorithms',
      'Practice time management during tests',
      'Work on problem-solving approaches',
      'Improve communication skills for interviews'
    ];
    while (recommendations.length < 3) {
      const randomRec = generic[Math.floor(Math.random() * generic.length)];
      if (!recommendations.includes(randomRec)) {
        recommendations.push(randomRec);
      }
    }
  }

  return recommendations;
};

const generateGoalsFromRealData = (realData) => {
  const goals = [];

  // Aptitude goal
  const aptitudeAttempted = realData.aptitude?.total_questions_attempted || 0;
  goals.push({
    id: 1,
    goal: 'Complete 50 aptitude questions',
    progress: Math.min(aptitudeAttempted, 50),
    total: 50
  });

  // Coding goal
  const codingAttempted = realData.coding?.problems_attempted || 0;
  goals.push({
    id: 2,
    goal: 'Solve 10 coding problems',
    progress: Math.min(codingAttempted, 10),
    total: 10
  });

  // Interview goal
  const interviewCount = (realData.recent_activity || []).filter(a =>
    a.module && a.module.includes('interview')
  ).length;
  goals.push({
    id: 3,
    goal: 'Take 3 mock interviews',
    progress: Math.min(interviewCount, 3),
    total: 3
  });

  return goals;
};

// Utility functions
const calculateDailyStreak = (activities) => {
  if (activities.length === 0) return 0;

  const dates = activities
    .map(a => a.timestamp ? new Date(a.timestamp).toDateString() : '')
    .filter(date => date);

  const uniqueDates = [...new Set(dates)];
  return Math.min(uniqueDates.length, 7); // Max 7-day streak for demo
};

const calculateTotalTimeSpent = (activities) => {
  // Mock calculation - in a real app, you'd track actual time
  return (activities.length * 15 * 60); // 15 minutes per activity
};

const identifyWeakAreas = (realData, module) => {
  // Mock implementation - in real app, analyze question topics
  return module === 'aptitude' ? ['Probability', 'Time & Work'] : ['Dynamic Programming', 'Graphs'];
};

const identifyStrongAreas = (realData, module) => {
  // Mock implementation
  return module === 'aptitude' ? ['Percentages', 'Ratios'] : ['Arrays', 'Strings'];
};

const analyzeLanguages = (activities) => {
  // Mock analysis
  return {
    'Python': 25,
    'Java': 12,
    'JavaScript': 8
  };
};

const analyzeDifficulty = (activities) => {
  // Mock analysis
  return {
    'Easy': 20,
    'Medium': 18,
    'Hard': 7
  };
};

const formatRecentActivity = (activities) => {
  return activities.slice(0, 5).map(activity => {
    let type = '';
    let title = '';

    if (activity.module === 'aptitude') {
      type = 'aptitude_test';
      title = 'Aptitude Test';
    } else if (activity.module === 'coding') {
      type = 'coding_problem';
      title = activity.problem_title || 'Coding Problem';
    } else if (activity.module && activity.module.includes('interview')) {
      type = 'mock_interview';
      title = 'Mock Interview';
    }

    return {
      type,
      title,
      score: activity.percentage || activity.score || 0,
      date: activity.timestamp ? new Date(activity.timestamp).toLocaleDateString() : new Date().toLocaleDateString(),
      details: `${activity.percentage || activity.score || 0}% score`
    };
  });
};

const calculateDailyScore = (dayActivities) => {
  if (dayActivities.length === 0) return 50;

  const totalScore = dayActivities.reduce((sum, activity) =>
    sum + (activity.percentage || activity.score || 0), 0
  );
  return Math.min(100, Math.floor(totalScore / dayActivities.length));
};

const generateEmptyEnhancedData = () => {
  return {
    user_id: 'unknown',
    overall_score: 0,
    daily_streak: 0,
    total_time_spent: 0,
    aptitude: {
      tests_taken: 0,
      average_score: 0,
      best_score: 0,
      total_questions_attempted: 0,
      accuracy: 0,
      weak_areas: [],
      strong_areas: []
    },
    coding: {
      problems_attempted: 0,
      average_success_rate: 0,
      total_tests_passed: 0,
      total_tests_attempted: 0,
      languages: {},
      difficulty_distribution: {}
    },
    recent_activity: [],
    weekly_activity: [],
    skill_distribution: [],
    achievements: [],
    upcoming_goals: [],
    recommendations: [],
    summary: {
      total_activities: 0,
      improvement_tips: []
    }
  };
};

export default enhanceProgressData;