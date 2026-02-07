def check_dict(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) < 2:
                print(f"Line {i} is problematic: {repr(line)}")

if __name__ == "__main__":
    check_dict("data/combined.dict")
