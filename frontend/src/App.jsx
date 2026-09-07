import { useState, useRef } from 'react'
import QuestionCard from './components/QuestionCard'
import WebcamFeed from './components/WebcamFeed'
import { startSession, getNextQuestion, getReport } from './lib/api'
import { useInterviewSocket } from './hooks/useInterviewSocket'
import { useAudioRecorder } from './hooks/useAudioRecorder'

function App() {
  const [sessionId, setSessionId] = useState(null)
  const [question, setQuestion] = useState('')
  const [phase, setPhase] = useState('idle') // idle | ready | answering | evaluated | report
  const [role] = useState('Backend Developer')
  const [questionNumber, setQuestionNumber] = useState(1)
  const TOTAL_QUESTIONS = 5
  const videoRef = useRef(null)
  const streamRef = useRef(null)
  const [report, setReport] = useState(null)

  const {
    connect, disconnect, sendAudioChunk, requestEvaluation,
    transcript, evaluation, connected
  } = useInterviewSocket(sessionId)

  const { start: startRecording, stop: stopRecording } = useAudioRecorder(sendAudioChunk)

  const handleBegin = async () => {
    const res = await startSession(role)
    setSessionId(res.session_id)
    setQuestion(res.question)
    setPhase('ready')
  }

  const handleStartAnswering = () => {
    connect()
    setPhase('answering')

    setTimeout(() => {
      if (videoRef.current?.srcObject) {
        streamRef.current = videoRef.current.srcObject
        startRecording(streamRef.current)
      }
    }, 500) // small delay to ensure socket is open
  }

  const handleFinishAnswering = () => {
    stopRecording()
    setTimeout(async () => {
      requestEvaluation(question, transcript)
      setPhase('evaluated')
    }, 500)
  }

  const handleNextQuestion = async () => {
  if (questionNumber >= TOTAL_QUESTIONS) {
    const res = await getReport(sessionId)
    setReport(res)
    setPhase('report')
    return
  }
  const res = await getNextQuestion(role)
  setQuestion(res.question)
  setQuestionNumber((n) => n + 1)
  setPhase('ready')
}

  return (
    <div style={{ maxWidth: 520, margin: '60px auto', padding: '0 20px' }}>
      {phase === 'idle' && (
        <button
          onClick={handleBegin}
          style={{
            background: 'var(--accent)', color: 'var(--bg-page)', border: 'none',
            borderRadius: 'var(--radius-control)', padding: '12px 20px', fontSize: 15, cursor: 'pointer',
          }}
        >
          Begin practice session
        </button>
      )}

      {phase === 'ready' && (
        <QuestionCard
          question={question}
          questionNumber={questionNumber}
          totalQuestions={TOTAL_QUESTIONS}
          onStart={handleStartAnswering}
          onSkip={() => {}}
        />
      )}

      {phase === 'answering' && (
        <div>
          <WebcamFeed videoRef={videoRef} />
          <p style={{ margin: '16px 0', color: 'var(--text-secondary)', fontSize: 13 }}>
            {connected ? 'Recording... speak your answer' : 'Connecting...'}
          </p>
          <p style={{ fontSize: 14, color: 'var(--text-primary)' }}>{transcript}</p>
          <button
            onClick={handleFinishAnswering}
            style={{
              background: 'var(--accent)', color: 'var(--bg-page)', border: 'none',
              borderRadius: 'var(--radius-control)', padding: 11, fontSize: 14, cursor: 'pointer', width: '100%',
            }}
          >
            Finish answering
          </button>
        </div>
      )}

      {phase === 'evaluated' && evaluation && (
        <div>
          <h2 style={{ fontFamily: 'var(--font-display)', fontWeight: 400 }}>Feedback</h2>
          <p><strong>Content:</strong> {evaluation.content_score}/10</p>
          <p><strong>Structure:</strong> {evaluation.structure_score}/10</p>
          <p><strong>Strength:</strong> {evaluation.strength}</p>
          <p><strong>Improvement:</strong> {evaluation.improvement}</p>
          <button
            onClick={handleNextQuestion}
            style={{
              background: 'var(--accent)', color: 'var(--bg-page)', border: 'none',
              borderRadius: 'var(--radius-control)', padding: 11, fontSize: 14, cursor: 'pointer', width: '100%', marginTop: 16,
            }}
          >
            {questionNumber >= TOTAL_QUESTIONS ? 'See final report' : 'Next question'}
          </button>
        </div>
      )}

      {phase === 'report' && report && (
  <div>
    <p style={{ fontSize: 13, color: 'var(--text-secondary)', margin: '0 0 4px' }}>
      Session complete
    </p>
    <h1
      style={{
        fontFamily: 'var(--font-display)', fontWeight: 400, fontSize: 26,
        color: 'var(--text-primary)', margin: '0 0 22px', lineHeight: 1.3,
      }}
    >
      Here's how you did.
    </h1>

    <div
      style={{
        background: 'var(--bg-card)', borderRadius: 'var(--radius-card)',
        padding: '16px 18px', marginBottom: 20,
      }}
    >
      <p style={{ fontSize: 13, color: 'var(--text-secondary)', margin: '0 0 8px' }}>
        {report.total_questions} questions answered · avg content score {report.average_content_score}/10
      </p>
      <p style={{ fontSize: 15, color: 'var(--text-primary)', margin: 0, lineHeight: 1.6, whiteSpace: 'pre-wrap' }}>
        {report.report}
      </p>
    </div>

    <button
      onClick={() => {
        setPhase('idle')
        setQuestionNumber(1)
        setReport(null)
      }}
      style={{
        background: 'var(--accent)', color: 'var(--bg-page)', border: 'none',
        borderRadius: 'var(--radius-control)', padding: 11, fontSize: 14, cursor: 'pointer', width: '100%',
      }}
    >
      Practice again
    </button>
  </div>
)}
    </div>
  )
}

export default App