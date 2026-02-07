import parselmouth
from parselmouth.praat import call
import textgrid
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# CONFIG
WAV_DIR = Path("data/input")
TG_DIR = Path("data/output")
OUTPUT_IMG = "praat_verification.png"

def draw_spectrogram(spectrogram, dynamic_range=70):
    X, Y = spectrogram.x_grid(), spectrogram.y_grid()
    sg_db = 10 * np.log10(spectrogram.values)
    plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap='afmhot')
    plt.ylim([spectrogram.ymin, spectrogram.ymax])
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")

def draw_textgrid(tg_obj, duration):
    # Setup tiers (Words and Phones)
    tiers = [tg_obj.getFirst("words"), tg_obj.getFirst("phones")]
    
    # Draw logic
    for i, tier in enumerate(tiers):
        y_min = i * 0.5
        y_max = (i + 1) * 0.5
        
        for interval in tier:
            # Draw boundary line
            plt.axvline(x=interval.minTime, color='blue', linewidth=1, alpha=0.7)
            
            # Draw text label centered
            mid = (interval.minTime + interval.maxTime) / 2
            if interval.mark and interval.mark not in ["", "sil", "sp"]:
                plt.text(mid, y_min + 0.25, interval.mark, 
                         horizontalalignment='center', fontsize=10, color='black')

        # Draw horizontal separator
        plt.axhline(y=y_max, color='black', linewidth=2)

def main():
    # 1. Grab the first file pair
    wav_files = list(WAV_DIR.glob("*.wav"))
    if not wav_files: return
    
    wav_path = str(wav_files[0])
    tg_path = str(TG_DIR / f"{wav_files[0].stem}.TextGrid")
    
    print(f"Generating Praat view for: {wav_files[0].name}...")

    # 2. Load using Parselmouth (The ACTUAL Praat Engine)
    snd = parselmouth.Sound(wav_path)
    tg = textgrid.TextGrid.fromFile(tg_path)
    
    # 3. Create Plot
    plt.figure(figsize=(12, 8))
    
    # Top: Spectrogram (The "Physical" Reality)
    plt.subplot(2, 1, 1)
    spectrogram = snd.to_spectrogram()
    draw_spectrogram(spectrogram)
    plt.title("Praat Spectrogram & Alignment (Automated)", fontsize=14)
    
    # Bottom: TextGrid (The "Model" Output)
    plt.subplot(2, 1, 2)
    plt.xlim([0, snd.duration])
    plt.ylim([0, 1]) # 2 tiers normalized
    draw_textgrid(tg, snd.duration)
    plt.yticks([0.25, 0.75], ["Words", "Phones"])
    
    # Save
    plt.tight_layout()
    plt.savefig(OUTPUT_IMG, dpi=150)
    print(f"Saved {OUTPUT_IMG}")

if __name__ == "__main__":
    main()