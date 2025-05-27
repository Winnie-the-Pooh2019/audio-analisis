import whisper
from difflib import SequenceMatcher
import argparse
import os


def transcribe_audio(path: str, model_size: str = "base") -> str:
    """
    Transcribes an audio file using Whisper.

    Args:
        path (str): Path to the audio file.
        model_size (str): Size of the Whisper model to load (tiny, base, small, medium, large).

    Returns:
        str: The transcribed text.
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(path)
    return result.get("text", "").strip()


def compute_similarity(text1: str, text2: str) -> float:
    """
    Computes similarity percentage between two texts using SequenceMatcher.

    Args:
        text1 (str): First text string.
        text2 (str): Second text string.

    Returns:
        float: Similarity ratio in percentage.
    """
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
    text1 = transcribe_audio(args.audio1, args.model)
    print(f"First transcription:\n{text1}\n")

    print("Transcribing second audio...")
    text2 = transcribe_audio(args.audio2, args.model)
    print(f"Second transcription:\n{text2}\n")

    similarity = compute_similarity(text1, text2)
    print(f"Text similarity: {similarity:.2f}%")


if __name__ == "__main__":
    main()
