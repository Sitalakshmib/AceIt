# Elite Adaptive Aptitude System - Quick Start Guide

## 🚀 Getting Started

### Prerequisites
- ✅ Gemini API key configured in `.env`
- ✅ Backend server running on port 8000
- ✅ Database migrated with elite columns

---

## 📝 Step-by-Step Setup

### 1. Database Migration

For **SQLite** (Development):
```bash
cd aceit_backend

# Option A: Delete and recreate (recommended for SQLite)
rm aceit_dev.db
python3 -c "from database_postgres import Base, engine; Base.metadata.create_all(engine)"

# Option B: Run migration script (may have issues with SQLite)
python3 scripts/migrate_elite_aptitude.py
```

For **PostgreSQL** (Production):
```bash
cd aceit_backend
python3 scripts/migrate_elite_aptitude.py
```

### 2. Test Question Generation

```bash
cd aceit_backend
python3 scripts/test_elite_question_generator.py
```

**Expected Output:**
```
✅ PASS - Taxonomy
✅ PASS - Quality Validation
✅ PASS - Single Question
✅ PASS - Multiple Categories
✅ PASS - Difficulty Progression
✅ PASS - Batch Generation

Overall: 6/6 tests passed (100.0%)
```

**Note:** If you see quota errors, wait a few minutes and try again, or the system will automatically use cached questions.

---

## 🎯 Using the Elite Endpoints

### Generate a Single Question

```bash
curl -X POST http://localhost:8000/aptitude/elite/generate-question \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_123",
    "category": "Quantitative",
    "sub_topic": "Probability"
  }'
```

**Response:**
```json
{
  "question_id": "uuid-here",
  "question": "In a bag containing 5 red, 4 blue, and 3 green balls...",
  "options": ["A", "B", "C", "D"],
  "difficulty_level": "Advanced",
  "primary_concepts": ["conditional_probability", "complement_rule"],
  "time_to_solve_sec": 120,
  "metadata": {
    "trap_explanation": "Option C is tempting...",
    "optimal_strategy": "Use complement approach...",
    "common_mistake": "Students often forget...",
    "concept_depth": "multi",
    "cognitive_load": "high",
    "trap_density": "medium"
  }
}
```

### Get User's Adaptive Profile

```bash
curl http://localhost:8000/aptitude/elite/adaptive-profile/test_user_123
```

**Response:**
```json
{
  "user_tier": "advanced",
  "overall_stats": {
    "total_attempted": 150,
    "total_correct": 112,
    "overall_accuracy": 74.67,
    "avg_time_ratio": 0.92
  },
  "strengths": ["Probability", "Number Systems"],
  "weaknesses": ["Seating Arrangements"],
  "error_patterns": {
    "conceptual": 15,
    "careless": 8,
    "overthinking": 12,
    "time_pressure": 5
  },
  "recommended_focus": {
    "category": "Logical",
    "sub_topic": "Seating Arrangements",
    "difficulty": "Intermediate",
    "reason": "Low accuracy detected. Focus on building fundamentals."
  }
}
```

### Start Practice Session

```bash
curl -X POST http://localhost:8000/aptitude/elite/practice-session \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_123",
    "category": "Quantitative",
    "sub_topic": "Probability",
    "question_count": 5
  }'
```

### Get Error Analysis

```bash
curl http://localhost:8000/aptitude/elite/error-analysis/test_user_123
```

---

## 📊 Available Categories & Subtopics

### Quantitative
- Number Systems
- Percentages & Ratios
- Averages & Alligation
- Time & Work
- Time Speed Distance
- Profit Loss Discount
- Simple Compound Interest
- Permutation Combination
- Probability
- Data Interpretation

### Logical
- Syllogisms
- Seating Arrangements
- Puzzles
- Blood Relations
- Coding Decoding
- Direction Sense
- Clocks Calendars
- Input Output

### Verbal
- Reading Comprehension
- Sentence Correction
- Para Jumbles
- Critical Reasoning
- Vocabulary in Context

### Data Sufficiency
- Quant Hybrid
- Logic Hybrid

---

## 🔧 Configuration

### Difficulty Levels
- **Beginner:** Single concept, 60-90 seconds
- **Intermediate:** Two concepts, 90-120 seconds
- **Advanced:** 2-3 concepts, 120-150 seconds
- **Elite:** 3+ concepts, 90-120 seconds (requires insight)

### User Tiers
- **Developing:** 0-40% accuracy
- **Competent:** 40-60% accuracy
- **Advanced:** 60-80% accuracy
- **Elite:** 80-100% accuracy

---

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY not found"
**Solution:** Add to `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

### Issue: "Quota exceeded"
**Solution:** 
- Wait a few minutes (free tier has rate limits)
- Use cached questions from database
- Upgrade to paid Gemini API tier

### Issue: "Database migration failed"
**Solution (SQLite):**
```bash
rm aceit_dev.db
python3 -c "from database_postgres import Base, engine; Base.metadata.create_all(engine)"
```

### Issue: "Invalid category/subtopic"
**Solution:** Check available options:
```bash
curl http://localhost:8000/aptitude/categories
```

---

## 📈 Performance Tips

### 1. Pre-generate Questions
Generate questions during off-peak hours:
```python
from services.elite_question_generator import EliteQuestionGenerator

generator = EliteQuestionGenerator()
questions = generator.generate_batch(
    category="Quantitative",
    sub_topic="Probability",
    difficulty_level="Advanced",
    count=50  # Generate 50 questions
)
```

### 2. Use Database Caching
Generated questions are automatically stored in the database and can be reused.

### 3. Batch API Calls
Use `/elite/practice-session` instead of multiple `/elite/generate-question` calls.

---

## 🎓 Example Usage Flow

### New User Journey

1. **User registers** → System creates profile with tier "developing"
2. **User starts practice** → System generates Beginner questions
3. **User answers correctly** → System tracks performance
4. **After 10 questions** → System analyzes:
   - Accuracy: 80%
   - Avg time: Fast
   - Error pattern: Low
5. **System upgrades** → User tier: "competent", Difficulty: "Intermediate"
6. **Continues practice** → Questions adapt in real-time
7. **After 50 questions** → User reaches "advanced" tier
8. **System recommends** → Focus areas based on weaknesses

---

## 📚 Integration with Frontend

### Sample React Component

```jsx
import { useState, useEffect } from 'react';
import axios from 'axios';

function ElitePractice({ userId }) {
  const [question, setQuestion] = useState(null);
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    // Fetch user profile
    axios.get(`/aptitude/elite/adaptive-profile/${userId}`)
      .then(res => setProfile(res.data));
  }, [userId]);

  const generateQuestion = async () => {
    const response = await axios.post('/aptitude/elite/generate-question', {
      user_id: userId,
      category: 'Quantitative',
      sub_topic: 'Probability'
    });
    setQuestion(response.data);
  };

  return (
    <div>
      <h2>Your Tier: {profile?.user_tier}</h2>
      <h3>Accuracy: {profile?.overall_stats.overall_accuracy}%</h3>
      
      <button onClick={generateQuestion}>Generate Question</button>
      
      {question && (
        <div>
          <p>{question.question}</p>
          {question.options.map((opt, i) => (
            <button key={i}>{opt}</button>
          ))}
          <p>Time: {question.time_to_solve_sec}s</p>
          <p>Difficulty: {question.difficulty_level}</p>
        </div>
      )}
    </div>
  );
}
```

---

## ✅ Verification Checklist

Before going live:

- [ ] Database migrated successfully
- [ ] Test script passes (at least 4/6 tests)
- [ ] Can generate questions for all categories
- [ ] Adaptive profile returns correct data
- [ ] Error analysis works
- [ ] Frontend integration tested
- [ ] API response times acceptable (<3s)
- [ ] Gemini API quota sufficient

---

## 🎉 You're Ready!

The Elite Adaptive Aptitude System is now fully operational. Start generating CAT/GMAT/GRE-level questions and watch your users' performance improve with intelligent adaptation!

**Next Steps:**
1. Run database migration
2. Test question generation
3. Integrate with frontend
4. Monitor user performance
5. Collect feedback for improvements

---

**Support:** Check [walkthrough.md](file:///Users/sitalakshmib/.gemini/antigravity/brain/2f396671-a081-49b7-a828-87f3cd8658df/walkthrough.md) for detailed documentation.
