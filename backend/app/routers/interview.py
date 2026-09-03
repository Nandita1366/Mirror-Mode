from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket_manager import manager
from app.audio.audio_buffer import save_audio_chunk
from app.audio.whisper_service import transcribe_audio
from app.llm.evaluator import evaluate_answer
from app.vision.mediapipe_service import process_frame
from app.vision.metrics import eye_contact_score, posture_score
from app.vision.aggregator import VisionAggregator
import os
import json
import numpy as np
import cv2

router = APIRouter()

# Track one aggregator per session
session_aggregators = {}

@router.websocket("/ws/interview/{session_id}")
async def interview_websocket(websocket: WebSocket, session_id: str):
    await manager.connect(session_id, websocket)
    session_aggregators[session_id] = VisionAggregator()

    try:
        while True:
            data = await websocket.receive()

            if "bytes" in data:
                raw_bytes = data["bytes"]

                # Try decoding as an image frame first (JPEG from frontend canvas)
                np_arr = np.frombuffer(raw_bytes, np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                if frame is not None:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    face_landmarks, pose_landmarks = process_frame(frame_rgb)
                    eye = eye_contact_score(face_landmarks)
                    posture = posture_score(pose_landmarks)
                    session_aggregators[session_id].add_frame_scores(eye, posture)
                else:
                    # Otherwise treat as audio chunk
                    audio_path = save_audio_chunk(raw_bytes)
                    transcript = transcribe_audio(audio_path)
                    os.remove(audio_path)
                    await manager.send_json(session_id, {
                        "type": "transcript",
                        "text": transcript
                    })

            elif "text" in data:
                msg = json.loads(data["text"])

                if msg.get("type") == "evaluate":
                    result = evaluate_answer(msg["question"], msg["transcript"])
                    vision_avg = session_aggregators[session_id].get_averages()
                    session_aggregators[session_id].reset()

                    await manager.send_json(session_id, {
                        "type": "evaluation",
                        **result,
                        **vision_avg
                    })

    except WebSocketDisconnect:
        manager.disconnect(session_id)
        session_aggregators.pop(session_id, None)