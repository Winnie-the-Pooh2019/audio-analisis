from difflib import SequenceMatcher
import argparse
import os
import threading
import tempfile
import dotenv
import os
import requests
from gradio_client import Client, handle_file


BASE_URL    = "http://localhost:8000"  # faster-whisper-server base URL
MODEL_NAME  = "Systran/faster-whisper-base"      # server model, e.g., 'small', 'base', etc.

client = Client(BASE_URL)


def transcribe_file(path):
    """Send WAV file to faster-whisper-server API and print the result."""
    print(f"Transcribing {path!r} via faster-whisper-server...")
    try:
        result = client.predict(
            file_path=handle_file(path),
            model=MODEL_NAME,
            task='transcribe',
            temperature=0,
            stream=False,
            api_name='/predict'
        )

        print("\n--- Transcript ---")
        print(result)
        print("------------------\n")

        return result
    except requests.RequestException as e:
        print(f"Error during transcription: {e}")


def compute_similarity(text1: str, text2: str) -> float:
    matcher = SequenceMatcher(None, text1, text2)
    return matcher.ratio() * 100


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe two audio files and compute text similarity."
    )
    parser.add_argument(
        "audio1", help="Path to first audio file (e.g., song1.mp3)"
    )
    parser.add_argument(
        "audio2", help="Path to second audio file (e.g., song2.mp3)"
    )
    parser.add_argument(
        "--model", default="base", choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size to use for transcription"
    )
    args = parser.parse_args()

    if not os.path.isfile(args.audio1) or not os.path.isfile(args.audio2):
        print("Error: One or both audio file paths are invalid.")
        return

    print("Transcribing first audio...")
    text1 = transcribe_file(args.audio1)
    print(f"First transcription:\n{text1}\n")

    print("Transcribing second audio...")
    text2 = transcribe_file(args.audio2)
    print(f"Second transcription:\n{text2}\n")

    similarity = compute_similarity(text1, text2)
    print(f"Text similarity: {similarity:.2f}%")


if __name__ == "__main__":
    main()
