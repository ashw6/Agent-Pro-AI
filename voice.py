from faster_whisper import WhisperModel
import tempfile

model = WhisperModel("base")

def speech_to_text(audio):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(audio.read())
        path = f.name

    segments, _ = model.transcribe(path)
    return " ".join([s.text for s in segments])