# Forced Alignment Pipeline

This repository provides an automated pipeline for generating word and phoneme-level alignments from audio and transcripts using the Montreal Forced Aligner (MFA).

## Installation

### 1. Environment Setup
Create and activate a dedicated Conda environment:
```bash
conda create -n aligner python=3.10 -c conda-forge -y
conda activate aligner
```

### 2. Install Dependencies
Install MFA and the required Python analysis libraries:
```bash
conda install -c conda-forge montreal-forced-aligner -y
pip install -r requirements.txt
```

### 3. Download MFA Models
Download the necessary pretrained models for English:
```bash
mfa model download dictionary english_us_arpa
mfa model download acoustic english_us_arpa
mfa model download g2p english_us_arpa
```

## Dataset Preparation

1.  Place raw audio files in the `wav/` folder.
2.  Place corresponding text transcripts in the `transcripts/` folder.
3.  Ensure the filenames match (e.g., `sentence1.wav` and `sentence1.txt`).

## Running the Alignment

Execute the main pipeline script. This script handles data organization, OOV pronunciation generation, and the final alignment:

```bash
bash run_pipeline.sh
```

### Output Files
- **TextGrids**: Final alignment results are saved in `data/output/*.TextGrid`.
- **Visualization**: A visual confirmation image is generated at `praat_verification.png`.
- **Metrics**: A quality report is printed to the terminal console.

