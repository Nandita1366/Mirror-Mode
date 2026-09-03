import cv2
from app.vision.mediapipe_service import process_frame
from app.vision.metrics import eye_contact_score, posture_score

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

print("Capturing 30 frames... look at your webcam.")
for i in range(30):
    ret, frame = cap.read()
    if not ret:
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_landmarks, pose_landmarks = process_frame(frame_rgb)

    eye = eye_contact_score(face_landmarks)
    posture = posture_score(pose_landmarks)

    print(f"Frame {i}: eye_contact={eye}, posture={posture}")

cap.release()