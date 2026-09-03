import mediapipe as mp
import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
ret, frame = cap.read()
print("Webcam OK" if ret else "Webcam FAILED")
cap.release()