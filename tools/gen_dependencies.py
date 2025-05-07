if __name__ == "__main__":


    with open("../requirements.txt", encoding='utf-8') as f:
        lines = [f'"{line.strip()}"' for line in f if line.strip() and not line.startswith("#")]
    print("[dependencies = [\n  " + ",\n  ".join(lines) + "\n]]")
