import { useEffect, useRef } from 'react'

function WebcamFeed({ videoRef }) {
  useEffect(() => {
    let stream

    const startCamera = async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true })
        if (videoRef.current) {
          videoRef.current.srcObject = stream
        }
      } catch (err) {
        console.error('Camera access denied or failed:', err)
      }
    }

    startCamera()

    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop())
      }
    }
  }, [videoRef])

  return (
    <video
      ref={videoRef}
      autoPlay
      playsInline
      muted
      style={{
        width: '100%',
        borderRadius: 'var(--radius-card)',
        background: '#000',
      }}
    />
  )
}

export default WebcamFeed