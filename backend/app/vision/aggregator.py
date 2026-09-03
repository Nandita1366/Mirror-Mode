class VisionAggregator:
    def __init__(self):
        self.eye_scores = []
        self.posture_scores = []

    def add_frame_scores(self, eye_score: float, posture_score: float):
        self.eye_scores.append(eye_score)
        self.posture_scores.append(posture_score)

    def get_averages(self) -> dict:
        avg_eye = sum(self.eye_scores) / len(self.eye_scores) if self.eye_scores else 0.0
        avg_posture = sum(self.posture_scores) / len(self.posture_scores) if self.posture_scores else 0.0
        return {
            "avg_eye_contact": round(avg_eye, 2),
            "avg_posture": round(avg_posture, 2)
        }

    def reset(self):
        self.eye_scores.clear()
        self.posture_scores.clear()