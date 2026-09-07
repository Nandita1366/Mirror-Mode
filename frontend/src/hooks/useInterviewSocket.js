import { useRef, useState, useCallback } from 'react'
import { getWebSocketUrl } from '../lib/api'

export function useInterviewSocket(sessionId) {
  const socketRef = useRef(null)
  const [transcript, setTranscript] = useState('')
  const [evaluation, setEvaluation] = useState(null)
  const [connected, setConnected] = useState(false)

  const connect = useCallback(() => {
    const ws = new WebSocket(getWebSocketUrl(sessionId))
    ws.binaryType = 'arraybuffer'

    ws.onopen = () => setConnected(true)
    ws.onclose = () => setConnected(false)

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'transcript') {
        setTranscript((prev) => prev + ' ' + data.text)
      } else if (data.type === 'evaluation') {
        setEvaluation(data)
      }
    }

    socketRef.current = ws
  }, [sessionId])

  const sendAudioChunk = useCallback((blob) => {
    blob.arrayBuffer().then((buffer) => {
      if (socketRef.current?.readyState === WebSocket.OPEN) {
        socketRef.current.send(buffer)
      }
    })
  }, [])

  const sendVideoFrame = useCallback((blob) => {
    blob.arrayBuffer().then((buffer) => {
      if (socketRef.current?.readyState === WebSocket.OPEN) {
        socketRef.current.send(buffer)
      }
    })
  }, [])

  const requestEvaluation = useCallback((question, fullTranscript) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ type: 'evaluate', question, transcript: fullTranscript }))
    }
  }, [])

  const disconnect = useCallback(() => {
    socketRef.current?.close()
  }, [])

  return { connect, disconnect, sendAudioChunk, sendVideoFrame, requestEvaluation, transcript, evaluation, connected }
}