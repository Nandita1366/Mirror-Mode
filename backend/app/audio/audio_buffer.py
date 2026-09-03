import os
import uuid

TEMP_DIR = "temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)

def save_audio_chunk(audio_bytes: bytes) -> str:
    filename = f"{TEMP_DIR}/{uuid.uuid4()}.webm"
    with open(filename, "wb") as f:
        f.write(audio_bytes)
    return filename