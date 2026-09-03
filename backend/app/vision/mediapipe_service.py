import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
mp_pose = mp.solutions.pose

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True  # needed for iris landmarks (468+)
)
pose = mp_pose.Pose(static_image_mode=False)

def process_frame(frame):
    face_results = face_mesh.process(frame)
    pose_results = pose.process(frame)

    face_landmarks = face_results.multi_face_landmarks[0] if face_results.multi_face_landmarks else None
    pose_landmarks = pose_results.pose_landmarks if pose_results.pose_landmarks else None

    return face_landmarks, pose_landmarks