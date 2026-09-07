import { useRef, useCallback } from 'react'

export function useAudioRecorder(onChunk) {
  const mediaRecorderRef = useRef(null)

  const start = useCallback((stream) => {
    const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm' })
    recorder.ondataavailable = (e) => {
      if (e.data.size > 0) onChunk(e.data)
    }
    recorder.start(3000) // send a chunk every 3 seconds
    mediaRecorderRef.current = recorder
  }, [onChunk])

  const stop = useCallback(() => {
    mediaRecorderRef.current?.stop()
  }, [])

  return { start, stop }
}