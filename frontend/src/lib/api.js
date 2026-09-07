import axios from 'axios'

const API_BASE = 'http://127.0.0.1:8000'

export const startSession = async (role) => {
  const res = await axios.post(`${API_BASE}/session/start`, { role })
  return res.data
}

export const getNextQuestion = async (role) => {
  const res = await axios.post(`${API_BASE}/session/next-question`, { role })
  return res.data
}

export const submitAnswer = async (sessionId, question, transcript) => {
  const res = await axios.post(`${API_BASE}/session/answer`, {
    session_id: sessionId,
    question,
    transcript,
  })
  return res.data
}

export const getReport = async (sessionId) => {
  const res = await axios.get(`${API_BASE}/session/${sessionId}/report`)
  return res.data
}

export const getWebSocketUrl = (sessionId) =>
  `ws://127.0.0.1:8000/ws/interview/${sessionId}`