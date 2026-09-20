import sounddevice as sd
import whisper

SAMPLE_RATE = 16000
DURATION = 5


def listen():
    print("\nSpeak your question...")
    
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    audio = audio.flatten()

    print("Transcribing...")

    model = whisper.load_model("base")

    result = model.transcribe(
        audio,
        fp16=False,
        language="en"
    )

    return result["text"].strip()