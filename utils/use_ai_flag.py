# utils/use_ai_flag.py
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--no-ai", action="store_true")
args, _ = parser.parse_known_args()

USE_AI = not args.no_ai
