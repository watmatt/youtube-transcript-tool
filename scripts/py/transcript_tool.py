#!/usr/bin/env python3
"""GUI YouTube Transcript Tool (always timestamped).

Final filename pattern after title resolution:
    <video_title>_transcript.txt
Falls back to:
    <video_id>_transcript.txt
"""

import sys

from youtube_transcript_api import YouTubeTranscriptApi
import os
import requests
from bs4 import BeautifulSoup
import re
from typing import List

try:
    from . import transcript_common as tcommon  # type: ignore
except Exception:
    try:
        import transcript_common as tcommon  # type: ignore
    except Exception:
        tcommon = None  # type: ignore

if tcommon:
    tcommon.ensure_deps()
else:  # Minimal fallback installer
    import subprocess
    def _install(p, imp=None):
        import importlib
        try:
            importlib.import_module(imp or p)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", p])
    _install('youtube-transcript-api', 'youtube_transcript_api')
    _install('requests')
    _install('beautifulsoup4', 'bs4')
import tkinter as tk
from tkinter import simpledialog, messagebox

def extract_video_id(url):
    if tcommon:
        return tcommon.extract_video_id(url)
    patterns = [r'(?:v=|/)([a-zA-Z0-9_-]{11})', r'youtu\.be/([a-zA-Z0-9_-]{11})']
    for pattern in patterns:
        m = re.search(pattern, url)
        if m:
            return m.group(1)
    return None

def get_video_title_html(video_url):
    if tcommon:
        return tcommon.fetch_video_title(video_url)
    try:
        response = requests.get(video_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.text.replace(' - YouTube', '').strip()
            title = title.replace("/", "-").replace("\\", "-").replace(":", "-").replace("|", "-").replace("?", "").replace("*", "-").replace("\"", "'").replace("<", "-").replace(">", "-")
            return title
    except Exception:
        return None
    return None

def main():
    # Create root window but hide it
    root = tk.Tk()
    root.withdraw()
    
    # Ask for URL
    url = simpledialog.askstring(
        "YouTube Transcript Tool",
        "Enter YouTube URL:",
        initialvalue=""
    )
    
    if not url:
        print("No URL provided. Exiting.")
        return
    
    # Validate URL
    if not ('youtube.com' in url or 'youtu.be' in url):
        messagebox.showerror("Error", "Please enter a valid YouTube URL")
        return
    
    # Extract video ID
    video_id = extract_video_id(url)
    if not video_id:
        messagebox.showerror("Error", "Could not extract video ID from URL")
        return
    
    print(f"Processing video ID: {video_id}")
    print(f"URL: {url}")
    
    try:
        # Fetch transcript
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)

        transcriptions_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Transcriptions"))
        os.makedirs(transcriptions_dir, exist_ok=True)
        suffix = "_transcript.txt"
        filename = os.path.join(transcriptions_dir, f"{video_id}{suffix}")

        if tcommon:
            lines: List[str] = tcommon.build_timestamped_lines(transcript)  # type: ignore
        else:
            # Fallback timestamp builder
            def _ts(sec: float) -> str:
                sec = int(sec)
                h = sec // 3600
                m = (sec % 3600) // 60
                s = sec % 60
                return f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"00:{m:02d}:{s:02d}"
            lines = []
            for entry in transcript:
                txt = getattr(entry, 'text', '') if not isinstance(entry, dict) else entry.get('text', '')
                if not txt:
                    continue
                start = getattr(entry, 'start', 0.0) if not isinstance(entry, dict) else entry.get('start', 0.0)
                lines.append(f"[{_ts(start)}] {txt}")

        with open(filename, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")

        print(f"Transcript saved to {filename}")

        video_title = get_video_title_html(url)
        if video_title:
            target = os.path.join(transcriptions_dir, f"{video_title}{suffix}")
            if tcommon:
                target = tcommon.unique_path(target)
            try:
                if os.path.exists(filename):
                    os.rename(filename, target)
                    print(f"Transcript file renamed to: {target}")
                    final_filename = target
                else:
                    final_filename = filename
            except OSError as e:
                print(f"Rename failed ({e}); keeping original filename.")
                final_filename = filename
        else:
            final_filename = filename

        print(f"Absolute path: {os.path.abspath(final_filename)}")
        messagebox.showinfo("Success", f"Transcript downloaded successfully!\n\nSaved as:\n{os.path.basename(final_filename)}")

    except Exception as e:
        error_msg = f"Error downloading transcript: {str(e)}"
        print(error_msg)
        messagebox.showerror("Error", error_msg)

if __name__ == "__main__":
    main()
