import textgrid
from pathlib import Path
import numpy as np

# CONFIG
TG_DIR = Path("data/output")
MIN_PHONE_DURATION = 0.03  # 30ms (Below this is suspiciously fast)
MAX_PHONE_DURATION = 1.0   # 1 second (Above this is suspiciously long for a single phone)

def evaluate_quality():
    tg_files = list(TG_DIR.glob("*.TextGrid"))
    if not tg_files:
        print("No TextGrids found.")
        return

    total_phones = 0
    bad_phones = 0
    file_scores = []

    print(f"{'FILENAME':<20} | {'VALIDITY':<10} | {'ISSUES'}")
    print("-" * 50)

    for tg_path in tg_files:
        tg = textgrid.TextGrid.fromFile(str(tg_path))
        phones_tier = tg.getFirst("phones")
        
        file_total = 0
        file_bad = 0
        
        for interval in phones_tier:
            # Skip silence or empty markers
            if interval.mark in ["", "sil", "sp"]: 
                continue
                
            duration = interval.maxTime - interval.minTime
            file_total += 1
            
            # CHECK: Is the phone duration physically possible?
            if duration < MIN_PHONE_DURATION or duration > MAX_PHONE_DURATION:
                file_bad += 1
                bad_phones += 1
        
        if file_total == 0:
            score = 0
        else:
            score = ((file_total - file_bad) / file_total) * 100
            
        file_scores.append(score)
        print(f"{tg_path.stem:<20} | {score:5.1f}%     | {file_bad} outliers")

    # Final Summary
    avg_score = np.mean(file_scores) if file_scores else 0
    print("\n" + "="*50)
    print(f"FINAL ALIGNMENT VALIDITY SCORE: {avg_score:.2f}%")
    print("="*50)
    print("(Score based on % of phonemes with physically realistic durations)")

if __name__ == "__main__":
    evaluate_quality()