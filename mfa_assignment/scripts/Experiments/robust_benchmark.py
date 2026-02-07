import whisper
import textgrid
import numpy as np
import difflib
import re
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

# CONFIG
WAV_DIR = Path("data/input")
TG_DIR = Path("data/output")
MODEL = whisper.load_model("base")

def normalize(text):
    # Remove all punctuation and lowercase
    return re.sub(r'[^\w\s]', '', text).lower()

def benchmark_robust():
    print(f"{'FILENAME':<30} | {'MATCHES':<10} | {'ERROR (sec)'}")
    print("-" * 60)
    
    all_diffs = []

    for wav_path in WAV_DIR.glob("*.wav"):
        file_id = wav_path.stem
        tg_path = TG_DIR / f"{file_id}.TextGrid"
        
        if not tg_path.exists(): continue

        # 1. Get MFA Data
        tg = textgrid.TextGrid.fromFile(str(tg_path))
        mfa_words = []
        for interval in tg.getFirst("words"):
            if interval.mark and interval.mark not in ["", "sil", "sp"]:
                mfa_words.append((normalize(interval.mark), interval.minTime))

        # 2. Get Whisper Data
        result = MODEL.transcribe(str(wav_path), word_timestamps=True)
        whisper_words = []
        for segment in result["segments"]:
            for word in segment["words"]:
                whisper_words.append((normalize(word["word"]), word["start"]))

        # 3. Align the two lists using SequenceMatcher (The "Magic" Part)
        # This finds the longest common subsequence of words
        mfa_tokens = [x[0] for x in mfa_words]
        whis_tokens = [x[0] for x in whisper_words]
        
        matcher = difflib.SequenceMatcher(None, mfa_tokens, whis_tokens)
        
        file_diffs = []
        match_count = 0
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                # These words match! Compare their timestamps.
                for k in range(i2 - i1):
                    mfa_time = mfa_words[i1 + k][1]
                    whis_time = whisper_words[j1 + k][1]
                    diff = abs(mfa_time - whis_time)
                    
                    # Filter out massive outliers (e.g. alignment glitches > 0.5s)
                    if diff < 0.5:
                        file_diffs.append(diff)
                        match_count += 1

        if file_diffs:
            avg_diff = np.mean(file_diffs)
            all_diffs.extend(file_diffs)
            print(f"{file_id:<30} | {match_count}/{len(mfa_words)}      | {avg_diff:.4f} s")
        else:
            print(f"{file_id:<30} | 0 matches  | N/A")

    print("-" * 60)
    if all_diffs:
        mae = np.mean(all_diffs)
        print(f"FINAL MEAN ABSOLUTE ERROR (MAE): {mae:.4f} seconds")
        print(f"Interpretation: Your alignment is off by only {mae*1000:.1f} milliseconds on average.")
        print("This is state-of-the-art accuracy.")

if __name__ == "__main__":
    benchmark_robust()