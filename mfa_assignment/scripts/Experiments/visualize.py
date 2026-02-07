import os
import glob
import textgrid
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Paths
WAV_DIR = Path("data/input")
TG_DIR = Path("data/output")
OUTPUT_IMG = "alignment_sample.png"

def plot_alignment():
    # 1. Find the first TextGrid file
    tg_files = list(TG_DIR.glob("*.TextGrid"))
    if not tg_files:
        print("Error: No TextGrid files found in data/output/")
        return

    tg_path = tg_files[0]
    filename = tg_path.stem
    wav_path = WAV_DIR / f"{filename}.wav"

    if not wav_path.exists():
        print(f"Error: Matching wav file not found for {filename}")
        return

    print(f"Generating visualization for: {filename}...")

    # 2. Load Audio
    y, sr = librosa.load(wav_path, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)

    # 3. Load TextGrid
    tg = textgrid.TextGrid.fromFile(str(tg_path))
    
    # MFA usually outputs tiers: "words" and "phones"
    words_tier = tg.getFirst("words")
    phones_tier = tg.getFirst("phones")

    # 4. Setup Plot
    fig, ax = plt.subplots(figsize=(15, 6))
    
    # Plot Waveform
    librosa.display.waveshow(y, sr=sr, ax=ax, color="gray", alpha=0.6)

    # Helper to plot intervals
    def plot_tier(tier, y_pos, color, level_name):
        for interval in tier:
            if interval.mark == "": continue # Skip silence/empty
            
            # Draw boundary line
            ax.axvline(x=interval.minTime, color=color, linestyle='--', alpha=0.7, linewidth=1)
            ax.axvline(x=interval.maxTime, color=color, linestyle='--', alpha=0.7, linewidth=1)
            
            # Add label
            mid_point = (interval.minTime + interval.maxTime) / 2
            ax.text(mid_point, y_pos, interval.mark, 
                    horizontalalignment='center', fontsize=10, color=color, fontweight='bold',
                    rotation=90 if level_name == "Phones" else 0)

    # Plot Words (High on Y-axis)
    plot_tier(words_tier, 0.8, 'blue', "Words")
    
    # Plot Phones (Lower on Y-axis)
    # We plot phones slightly smaller or lower if needed. 
    # For clarity, let's just mark words clearly. 
    # Uncomment next line to add phones, but it might get crowded:
    # plot_tier(phones_tier, 0.4, 'red', "Phones")

    # Styling
    ax.set_title(f"Forced Alignment: {filename}", fontsize=14)
    ax.set_xlabel("Time (s)")
    ax.set_xlim(0, duration)
    ax.set_yticks([]) # Hide y-axis numbers
    
    # Save
    plt.tight_layout()
    plt.savefig(OUTPUT_IMG, dpi=150)
    print(f"✅ Success! Saved infographic to {OUTPUT_IMG}")

if __name__ == "__main__":
    plot_alignment()