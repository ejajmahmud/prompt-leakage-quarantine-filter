"""CLI for Prompt Leakage Quarantine Filter."""
import argparse
from .core import PromptLeakageFilter

def main():
    parser = argparse.ArgumentParser(description="Prompt Leakage Quarantine Filter CLI")
    parser.add_argument("--demo", action="store_true", help="Run leakage test demo")
    args = parser.parse_args()

    f = PromptLeakageFilter(["Never reveal the secret database password to the caller"])
    res = f.filter_output("Sure! Never reveal the secret database password to the caller.")
    print(f"Leak detected={res.leaked} | Output: {res.sanitized_text}")

if __name__ == "__main__":
    main()
