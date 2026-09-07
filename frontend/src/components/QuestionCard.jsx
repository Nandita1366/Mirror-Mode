function QuestionCard({ question, questionNumber, totalQuestions, onStart, onSkip }) {
  return (
    <div>
      <p style={{ fontSize: 13, color: 'var(--text-secondary)', margin: '0 0 4px' }}>
        Session with yourself
      </p>
      <h1
        style={{
          fontFamily: 'var(--font-display)',
          fontWeight: 400,
          fontSize: 26,
          color: 'var(--text-primary)',
          margin: '0 0 22px',
          lineHeight: 1.3,
        }}
      >
        You're doing better than you think.
      </h1>

      <div
        style={{
          background: 'var(--bg-card)',
          borderRadius: 'var(--radius-card)',
          padding: '16px 18px',
          marginBottom: 20,
        }}
      >
        <p style={{ fontSize: 13, color: 'var(--text-secondary)', margin: '0 0 8px' }}>
          Question {questionNumber} of {totalQuestions}
        </p>
        <p style={{ fontSize: 15, color: 'var(--text-primary)', margin: 0, lineHeight: 1.6 }}>
          {question}
        </p>
      </div>

      <div style={{ display: 'flex', gap: 10 }}>
        <button
          onClick={onStart}
          style={{
            flex: 1,
            background: 'var(--accent)',
            color: 'var(--bg-page)',
            border: 'none',
            borderRadius: 'var(--radius-control)',
            padding: 11,
            fontSize: 14,
            cursor: 'pointer',
          }}
        >
          Start answering
        </button>
        <button
          onClick={onSkip}
          style={{
            background: 'transparent',
            border: '1.5px solid var(--border)',
            color: 'var(--text-secondary)',
            borderRadius: 'var(--radius-control)',
            padding: '11px 16px',
            fontSize: 14,
            cursor: 'pointer',
          }}
        >
          Skip
        </button>
      </div>
    </div>
  )
}

export default QuestionCard