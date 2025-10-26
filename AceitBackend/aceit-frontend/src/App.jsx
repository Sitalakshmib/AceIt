import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [topics, setTopics] = useState([])
  const [questions, setQuestions] = useState([])
  const [selectedTopic, setSelectedTopic] = useState('')
  const [userId, setUserId] = useState('user123')
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [selectedOption, setSelectedOption] = useState(null)
  const [answers, setAnswers] = useState({})
  const [showResult, setShowResult] = useState(false)
  const [correctAnswers, setCorrectAnswers] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Fetch available topics on component mount
  useEffect(() => {
    fetchTopics()
  }, [])

  const fetchTopics = async () => {
    try {
      setLoading(true)
      const response = await fetch(`${import.meta.env.VITE_API_URL}/aptitude/topics`)
      const data = await response.json()
      setTopics(data.topics)
      if (data.topics.length > 0) {
        setSelectedTopic(data.topics[0])
      }
      setError('')
    } catch (err) {
      setError('Failed to fetch topics: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const fetchQuestions = async () => {
    try {
      setLoading(true)
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/aptitude/questions?user_id=${userId}&topic=${selectedTopic}&count=5`
      )
      const data = await response.json()
      setQuestions(data)
      setCurrentQuestionIndex(0)
      setSelectedOption(null)
      setAnswers({})
      setShowResult(false)
      setCorrectAnswers(0)
      setError('')
    } catch (err) {
      setError('Failed to fetch questions: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleOptionSelect = (optionIndex) => {
    setSelectedOption(optionIndex)
  }

  const handleNextQuestion = () => {
    // Save the answer
    const currentQuestion = questions[currentQuestionIndex]
    const newAnswers = {
      ...answers,
      [currentQuestion.id]: selectedOption
    }
    setAnswers(newAnswers)

    // Move to next question or show results
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
      setSelectedOption(null)
    } else {
      // Submit answers and show results
      submitAnswers(newAnswers)
    }
  }

  const submitAnswers = async (answersToSubmit) => {
    try {
      setLoading(true)
      const response = await fetch(`${import.meta.env.VITE_API_URL}/aptitude/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          answers: answersToSubmit,
          topic: selectedTopic
        })
      })
      
      const data = await response.json()
      setCorrectAnswers(data.correct)
      setShowResult(true)
      setError('')
    } catch (err) {
      setError('Failed to submit answers: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleRestart = () => {
    fetchQuestions()
  }

  const currentQuestion = questions[currentQuestionIndex]

  return (
    <div className="app">
      <header className="app-header">
        <h1>AceIT - Adaptive Aptitude Learning</h1>
        <p>Personalized aptitude preparation that adapts to your skill level</p>
      </header>

      <main className="app-main">
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {!questions.length && !showResult && (
          <div className="setup-section">
            <div className="user-setup">
              <label htmlFor="userId">User ID:</label>
              <input
                type="text"
                id="userId"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                placeholder="Enter your user ID"
              />
            </div>

            <div className="topic-selector">
              <label htmlFor="topic">Select Topic:</label>
              <select
                id="topic"
                value={selectedTopic}
                onChange={(e) => setSelectedTopic(e.target.value)}
              >
                {topics.map((topic) => (
                  <option key={topic} value={topic}>
                    {topic.replace('_', ' ').toUpperCase()}
                  </option>
                ))}
              </select>
            </div>

            <button 
              onClick={fetchQuestions} 
              disabled={loading || !selectedTopic}
              className="start-button"
            >
              {loading ? 'Loading...' : 'Start Practice'}
            </button>
          </div>
        )}

        {questions.length > 0 && !showResult && currentQuestion && (
          <div className="question-section">
            <div className="question-header">
              <span className="question-count">
                Question {currentQuestionIndex + 1} of {questions.length}
              </span>
              <span className="question-topic">
                Topic: {selectedTopic.replace('_', ' ').toUpperCase()}
              </span>
              <span className="question-difficulty">
                Difficulty: {currentQuestion.difficulty}
              </span>
            </div>

            <div className="question-content">
              <h2>{currentQuestion.question}</h2>
              
              <div className="options">
                {currentQuestion.options.map((option, index) => (
                  <button
                    key={index}
                    className={`option-button ${
                      selectedOption === index ? 'selected' : ''
                    }`}
                    onClick={() => handleOptionSelect(index)}
                  >
                    <span className="option-label">
                      {String.fromCharCode(65 + index)}.
                    </span>
                    <span className="option-text">{option}</span>
                  </button>
                ))}
              </div>
            </div>

            <div className="question-actions">
              <button
                onClick={handleNextQuestion}
                disabled={selectedOption === null}
                className="next-button"
              >
                {currentQuestionIndex < questions.length - 1 ? 'Next Question' : 'Submit Answers'}
              </button>
            </div>
          </div>
        )}

        {showResult && (
          <div className="results-section">
            <h2>Practice Results</h2>
            <div className="results-summary">
              <p>
                You answered <strong>{correctAnswers}</strong> out of{' '}
                <strong>{questions.length}</strong> questions correctly.
              </p>
              <p className="percentage">
                Score: {Math.round((correctAnswers / questions.length) * 100)}%
              </p>
            </div>
            
            <div className="detailed-results">
              <h3>Question Review</h3>
              {questions.map((question, index) => {
                const userAnswer = answers[question.id]
                const isCorrect = userAnswer === question.correct
                return (
                  <div 
                    key={question.id} 
                    className={`question-review ${isCorrect ? 'correct' : 'incorrect'}`}
                  >
                    <p className="question-text">
                      <strong>Q{index + 1}:</strong> {question.question}
                    </p>
                    <p className="user-answer">
                      <strong>Your answer:</strong>{' '}
                      {userAnswer !== undefined ? (
                        <>
                          {String.fromCharCode(65 + userAnswer)}. {question.options[userAnswer]}
                          {isCorrect ? ' ✅' : ' ❌'}
                        </>
                      ) : (
                        'Not answered'
                      )}
                    </p>
                    {!isCorrect && (
                      <p className="correct-answer">
                        <strong>Correct answer:</strong>{' '}
                        {String.fromCharCode(65 + question.correct)}. {question.options[question.correct]}
                      </p>
                    )}
                    {question.explanation && (
                      <p className="explanation">
                        <strong>Explanation:</strong> {question.explanation}
                      </p>
                    )}
                  </div>
                )
              })}
            </div>

            <button onClick={handleRestart} className="restart-button">
              Practice Again
            </button>
          </div>
        )}

        {loading && (
          <div className="loading">
            Loading...
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>AceIT - Adaptive Learning Platform</p>
      </footer>
    </div>
  )
}

export default App