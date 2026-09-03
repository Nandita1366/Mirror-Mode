from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_audio(file_path: str) -> str:
    segments, info = model.transcribe(file_path)
    return " ".join(seg.text for seg in segments)