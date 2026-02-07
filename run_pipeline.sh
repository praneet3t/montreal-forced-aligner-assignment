#!/bin/bash

# ==============================================================================
# MFA Forced Alignment Pipeline
# ==============================================================================
# This script automates the full forced alignment workflow:
# 1. Data Organization (WAV + Transcripts)
# 2. Dictionary Setup
# 3. G2P (Grapheme-to-Phoneme) for Out-of-Vocabulary words
# 4. Dictionary Merging
# 5. Forced Alignment (MFA)
# 6. Post-processing (Metrics & Visualization)
# ==============================================================================

# Stop on error
set -e

echo "--- Step 1: Organizing Data ---"
python.exe scripts/prep_data.py

echo "--- Step 2: Fetching Standard Dictionary ---"
python.exe scripts/setup_dict.py

echo "--- Step 3: Handling OOV (Out of Vocabulary) Words ---"
# Generate pronunciations for words missing from the standard dictionary
# We use --clean to ensure fresh run across sessions
cmd.exe /c "conda run -n aligner mfa g2p data/input english_us_arpa data/oov.dict --clean"

echo "--- Step 4: Merging Dictionaries ---"
# Combine standard dict + generated OOV dict for full coverage
cat english_us_arpa.dict data/oov.dict > data/combined.dict
echo "Created custom dictionary at data/combined.dict"

echo "--- Step 5: Running Alignment ---"
# Align using the combined dictionary
cmd.exe /c "conda run -n aligner mfa align data/input data/combined.dict english_us_arpa data/output --clean --verbose"

echo "--- Step 6: Post-Alignment Analytics ---"
# Calculate validity scores based on phoneme durations
python.exe scripts/eval_metrics.py

echo "--- Step 7: Generating Verification Visualization ---"
# Produce a Praat-style spectrogram + TextGrid overlay
python.exe scripts/praat_viz.py

echo ""
echo "=============================================================================="
echo "PROCESS COMPLETE"
echo "=============================================================================="
echo "Outputs:"
echo " - TextGrids:      data/output/*.TextGrid"
echo " - Log:            data/output/alignment_analysis.csv"
echo " - Visualization:  praat_verification.png"
echo "=============================================================================="