import whisper
import textgrid
from pathlib import Path

# CONFIG
WAV_DIR = Path("data/input")
TG_DIR = Path("data/output")
MODEL = whisper.load_model("base")

def normalize(w):
    return w.strip(".,?!\"").lower()

def debug_first_file():
    # Pick the first wav file
    wav_files = list(WAV_DIR.glob("*.wav"))
    if not wav_files: return

    target_wav = wav_files[0]
    target_tg = TG_DIR / f"{target_wav.stem}.TextGrid"

    print(f"DEBUGGING FILE: {target_wav.name}")
    print("-" * 50)

    # 1. Get MFA Words
    tg = textgrid.TextGrid.fromFile(str(target_tg))
    mfa_words = [normalize(i.mark) for i in tg.getFirst("words") if i.mark and i.mark not in ["", "sil", "sp"]]

    # 2. Get Whisper Words
    result = MODEL.transcribe(str(target_wav))
    whisper_text = normalize(result["text"])

    print("--- MFA (Ground Truth) ---")
    print(mfa_words)
    print("\n--- WHISPER (AI Guess) ---")
    print(whisper_text.split()) # Splitting by space to roughly match list format

if __name__ == "__main__":
    debug_first_file()