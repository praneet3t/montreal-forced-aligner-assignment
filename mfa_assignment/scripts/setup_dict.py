import os
import shutil
from pathlib import Path

def setup_dictionary():
    # Define paths
    home = Path(os.path.expanduser("~"))
    mfa_local_path = home / "Documents/MFA/pretrained_models/dictionary/english_us_arpa.dict"
    target_path = Path("english_us_arpa.dict")

    print(f"Looking for dictionary at: {mfa_local_path}")

    # 1. Try local copy
    if mfa_local_path.exists():
        print(f"Found local dictionary. Copying to {target_path}...")
        shutil.copy(mfa_local_path, target_path)
        return

    # 2. If not found, that's unexpected given previous checks
    print("Error: Could not find dictionary locally.")
    print("Please ensure you have run: conda run -n aligner mfa model download dictionary english_us_arpa")
    exit(1)

if __name__ == "__main__":
    setup_dictionary()
