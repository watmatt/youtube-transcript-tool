"""Common helpers for YouTube transcript tools.

Keeps logic for:
 - Video ID extraction
 - Title fetch & sanitization
 - Transcript line building (plain / timestamped)
 - Timestamp formatting

All functions are defensive and side-effect free (except network call in title fetch).
This module also exposes a helper to ensure runtime dependencies are present.
"""
from __future__ import annotations

from typing import Iterable, List, Union, Any
import re
import requests
from bs4 import BeautifulSoup
import subprocess
import sys

# Type hint compatible shape (dict or attr object)
TranscriptEntry = Union[dict, Any]

_VIDEO_ID_PATTERNS = [
    r'(?:v=|/)([a-zA-Z0-9_-]{11})',
    r'youtu\.be/([a-zA-Z0-9_-]{11})',
]

def extract_video_id(url: str) -> str | None:
    for pattern in _VIDEO_ID_PATTERNS:
        m = re.search(pattern, url)
        if m:
            return m.group(1)
    return None

_SANITIZE_RE = re.compile(r'[<>:"/\\|?*]')
_DASH_COLLAPSE_RE = re.compile(r'-+')

def sanitize_title(title: str) -> str:
    t = _SANITIZE_RE.sub('-', title).strip()
    t = _DASH_COLLAPSE_RE.sub('-', t)
    return t[:100]

def fetch_video_title(url: str, timeout: int = 10) -> str | None:
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        title_tag = soup.find('title')
        if not title_tag:
            return None
        raw = title_tag.text.replace(' - YouTube', '').strip()
        return sanitize_title(raw)
    except Exception:
        return None

def _entry_text(entry: TranscriptEntry) -> str:
    if isinstance(entry, dict):
        return entry.get('text', '') or ''
    return getattr(entry, 'text', '') or ''

def _entry_start(entry: TranscriptEntry) -> float:
    if isinstance(entry, dict):
        return float(entry.get('start', 0.0) or 0.0)
    return float(getattr(entry, 'start', 0.0) or 0.0)

def format_timestamp(seconds: float) -> str:
    total = int(seconds)
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    return f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"00:{m:02d}:{s:02d}"

def build_plain_lines(transcript: Iterable[TranscriptEntry]) -> List[str]:
    lines: List[str] = []
    for entry in transcript:
        txt = _entry_text(entry).strip()
        if not txt:
            continue
        lines.append(txt)
    return lines

def build_timestamped_lines(transcript: Iterable[TranscriptEntry]) -> List[str]:
    lines: List[str] = []
    for entry in transcript:
        txt = _entry_text(entry).strip()
        if not txt:
            continue
        ts = format_timestamp(_entry_start(entry))
        lines.append(f"[{ts}] {txt}")
    return lines


def unique_path(path: str) -> str:
    """Return a filesystem path that doesn't exist by appending _2, _3, ... if needed."""
    import os
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    counter = 2
    candidate = f"{base}_{counter}{ext}"
    while os.path.exists(candidate):
        counter += 1
        candidate = f"{base}_{counter}{ext}"
    return candidate


def ensure_deps():
    """Install required third-party libraries if missing (idempotent)."""
    import importlib
    pkgs = [
        ("youtube-transcript-api", "youtube_transcript_api"),
        ("requests", None),
        ("beautifulsoup4", "bs4"),
    ]
    for pkg, import_name in pkgs:
        name = import_name or pkg
        try:
            importlib.import_module(name)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
            importlib.invalidate_caches()
