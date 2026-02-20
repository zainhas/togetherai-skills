#!/usr/bin/env python3
"""
Together AI Speech-to-Text — Transcribe, Translate, Diarize (v2 SDK)

Transcription, translation to English, and speaker diarization.

Usage:
    python stt_transcribe.py audio.mp3

Requires:
    pip install together
    export TOGETHER_API_KEY=your_key
"""

import sys
from together import Together

client = Together()


def transcribe(audio_path: str, language: str = "en"):
    """Basic transcription."""
    with open(audio_path, "rb") as f:
        response = client.audio.transcriptions.create(
            file=f,
            model="openai/whisper-large-v3",
            language=language,
        )
    print(f"Transcription: {response.text}")
    return response.text


def transcribe_with_timestamps(audio_path: str):
    """Transcription with word-level timestamps."""
    with open(audio_path, "rb") as f:
        response = client.audio.transcriptions.create(
            file=f,
            model="openai/whisper-large-v3",
            response_format="verbose_json",
            timestamp_granularities="word",
        )
    for word in response.words:
        print(f"  [{word.start:.2f}s - {word.end:.2f}s] {word.word}")
    return response


def transcribe_with_diarization(audio_path: str, min_speakers: int = 1, max_speakers: int = 5):
    """Transcription with speaker identification."""
    with open(audio_path, "rb") as f:
        response = client.audio.transcriptions.create(
            file=f,
            model="openai/whisper-large-v3",
            response_format="verbose_json",
            diarize="true",
            min_speakers=min_speakers,
            max_speakers=max_speakers,
        )
    for segment in response.speaker_segments:
        print(f"  [{segment.speaker_id}] ({segment.start:.1f}s-{segment.end:.1f}s): {segment.text}")
    return response


def translate_to_english(audio_path: str):
    """Translate foreign-language audio to English text."""
    with open(audio_path, "rb") as f:
        response = client.audio.translations.create(
            file=f,
            model="openai/whisper-large-v3",
        )
    print(f"English translation: {response.text}")
    return response.text


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python stt_transcribe.py <audio_file> [--diarize] [--timestamps] [--translate]")
        sys.exit(1)

    audio_file = sys.argv[1]
    flags = sys.argv[2:]

    if "--translate" in flags:
        translate_to_english(audio_file)
    elif "--diarize" in flags:
        transcribe_with_diarization(audio_file)
    elif "--timestamps" in flags:
        transcribe_with_timestamps(audio_file)
    else:
        transcribe(audio_file)
