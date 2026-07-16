"""Manim Voiceover adapter for Microsoft Edge's online speech service."""

from __future__ import annotations

from pathlib import Path

import edge_tts
from manim_voiceover.helper import remove_bookmarks
from manim_voiceover.services.base import SpeechService


class EdgeTTSService(SpeechService):
    """Generate cached narration with a selected Microsoft Edge voice."""

    def __init__(
        self,
        voice: str = "en-GB-RyanNeural",
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.pitch = pitch

    def generate_from_text(
        self,
        text: str,
        cache_dir: str | None = None,
        path: str | None = None,
        **kwargs,
    ) -> dict:
        """Synthesize one narration segment and return Manim's cache metadata."""

        output_dir = Path(cache_dir) if cache_dir is not None else Path(self.cache_dir)
        input_text = remove_bookmarks(text)
        input_data = {
            "input_text": input_text,
            "service": "edge-tts",
            "voice": self.voice,
            "rate": self.rate,
            "volume": self.volume,
            "pitch": self.pitch,
        }

        cached_result = self.get_cached_result(input_data, output_dir)
        if cached_result is not None:
            return cached_result

        audio_path = path or f"{self.get_audio_basename(input_data)}.mp3"
        communicator = edge_tts.Communicate(
            input_text,
            self.voice,
            rate=self.rate,
            volume=self.volume,
            pitch=self.pitch,
        )
        communicator.save_sync(str(output_dir / audio_path))

        return {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_path,
        }
