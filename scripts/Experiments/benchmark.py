import whisper
import textgrid
import numpy as np
from pathlib import Path
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# CONFIG
WAV_DIR = Path("data/input")
TG_DIR = Path("data/output")
MODEL_SIZE = "base"  # 'tiny', 'base', 'small', 'medium', 'large'

def normalize_word(w):
    # simple cleaner: remove punctuation and lower case
    return w.strip(".,?!\"").lower()

def benchmark_alignment():
    print(f"Loading Whisper model ('{MODEL_SIZE}')...")
    model = whisper.load_model(MODEL_SIZE)
    
    print(f"\n{'FILENAME':<25} | {'MATCHED WORDS':<15} | {'AVG DEVIATION (sec)':<20}")
    print("-" * 65)
    
    all_deviations = []
    
    # Iterate over files
    for wav_path in WAV_DIR.glob("*.wav"):
        file_id = wav_path.stem
        tg_path = TG_DIR / f"{file_id}.TextGrid"
        
        if not tg_path.exists():
            continue
            
        # 1. Get MFA Timestamps
        tg = textgrid.TextGrid.fromFile(str(tg_path))
        mfa_words = []
        for interval in tg.getFirst("words"):
            if interval.mark and interval.mark not in ["", "sil", "sp"]:
                mfa_words.append({
                    "word": normalize_word(interval.mark),
                    "start": interval.minTime
                })
        
        # 2. Get Whisper Timestamps
        # resulting in a list of segments, we need word-level
        result = model.transcribe(str(wav_path), word_timestamps=True)
        whisper_words = []
        for segment in result["segments"]:
            for word in segment["words"]:
                whisper_words.append({
                    "word": normalize_word(word["word"]),
                    "start": word["start"]
                })
                
        # 3. Compare (Fuzzy Matching by time and text)
        deviations = []
        matches = 0
        
        # Simple matching strategy: Look for the same word within a 0.5s window
        for m_w in mfa_words:
            best_match_diff = float('inf')
            
            for w_w in whisper_words:
                # If words are same (or close)
                if m_w["word"] == w_w["word"]:
                    diff = abs(m_w["start"] - w_w["start"])
                    if diff < 0.5: # Only count if it's within 500ms (to avoid matching wrong instance of 'the')
                        if diff < best_match_diff:
                            best_match_diff = diff
            
            if best_match_diff != float('inf'):
                deviations.append(best_match_diff)
                matches += 1
        
        if deviations:
            avg_dev = np.mean(deviations)
            all_deviations.extend(deviations)
            print(f"{file_id:<25} | {matches}/{len(mfa_words)} words     | {avg_dev:.4f} s")
        else:
            print(f"{file_id:<25} | 0 matches       | N/A")

    print("-" * 65)
    if all_deviations:
        print(f"OVERALL MEAN ABSOLUTE ERROR (MAE): {np.mean(all_deviations):.4f} seconds")
        print("Interpretation: Lower is better. < 0.1s indicates high agreement with SOTA models.")
    else:
        print("No matches found. Check if transcripts differ significantly.")

if __name__ == "__main__":
    benchmark_alignment()