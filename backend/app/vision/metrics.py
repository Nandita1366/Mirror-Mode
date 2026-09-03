import math

def eye_contact_score(face_landmarks) -> float:
    """
    Rough proxy: checks how centered the iris is within the eye region.
    Returns a 0-100 score. Higher = better eye contact (looking at camera).
    """
    if not face_landmarks:
        return 0.0

    landmarks = face_landmarks.landmark

    # MediaPipe Face Mesh iris landmarks (requires refine_landmarks=True)
    left_iris = landmarks[468]
    left_eye_left = landmarks[33]
    left_eye_right = landmarks[133]

    eye_width = abs(left_eye_right.x - left_eye_left.x)
    if eye_width == 0:
        return 0.0

    iris_offset = abs(left_iris.x - (left_eye_left.x + left_eye_right.x) / 2)
    centeredness = max(0.0, 1 - (iris_offset / (eye_width / 2)))

    return round(centeredness * 100, 2)


def posture_score(pose_landmarks) -> float:
    """
    Rough proxy: checks shoulder levelness and head-to-shoulder alignment.
    Returns a 0-100 score. Higher = better posture.
    """
    if not pose_landmarks:
        return 0.0

    landmarks = pose_landmarks.landmark

    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]
    nose = landmarks[0]

    shoulder_tilt = abs(left_shoulder.y - right_shoulder.y)
    shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
    head_offset = abs(nose.x - shoulder_center_x)

    tilt_penalty = min(shoulder_tilt * 200, 50)
    offset_penalty = min(head_offset * 200, 50)

    score = 100 - tilt_penalty - offset_penalty
    return round(max(0.0, score), 2)