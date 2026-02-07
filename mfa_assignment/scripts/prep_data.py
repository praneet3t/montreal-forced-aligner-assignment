import os
import shutil
from pathlib import Path

# Configuration
SOURCE_WAV = Path("wav")           # Expects 'wav' folder in root
SOURCE_TRANS = Path("transcripts") # Expects 'transcripts' folder in root
OUTPUT_DIR = Path("data/input")

def main():
    # Clean and recreate output directory
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    # Get list of audio files
    wav_files = list(SOURCE_WAV.glob("*.wav"))
    
    if not wav_files:
        print("Error: No .wav files found in 'wav/' folder.")
        return

    print(f"Found {len(wav_files)} audio files. Processing...")

    for wav_path in wav_files:
        filename = wav_path.stem
        
        # 1. Copy Audio
        shutil.copy(wav_path, OUTPUT_DIR / wav_path.name)
        
        # 2. Find and Copy Transcript (rename to .lab)
        # Checks for .txt first, then .lab
        txt_path = SOURCE_TRANS / f"{filename}.txt"
        lab_path = SOURCE_TRANS / f"{filename}.lab"
        
        target_lab = OUTPUT_DIR / f"{filename}.lab"

        if txt_path.exists():
            shutil.copy(txt_path, target_lab)
        elif lab_path.exists():
            shutil.copy(lab_path, target_lab)
        else:
            print(f"Warning: Missing transcript for {filename}")

    print(f"Data preparation complete. Files ready in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()