import pyttsx3

engine = pyttsx3.init()
engine.save_to_file("Hello, this is a test of the whisper transcription pipeline.", "test_audio.wav")
engine.runAndWait()
print("test_audio.wav created")