#!/usr/bin/env python3
"""Command-line YouTube Transcript Tool (always timestamped).

Output format:
    [HH:MM:SS] text

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

try:  # Prefer package-relative import
    from . import transcript_common as tcommon  # type: ignore
except Exception:  # pragma: no cover
    try:  # Fallback to absolute import when running as a loose script
        import transcript_common as tcommon  # type: ignore
    except Exception:
        tcommon = None  # type: ignore

if tcommon:
    tcommon.ensure_deps()
else:  # Fallback inline installer (edge case)
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
        response = requests.get(video_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.text.replace(' - YouTube', '').strip()
            title = re.sub(r'[<>:"/\\|?*]', '-', title)
            title = re.sub(r'-+', '-', title)
            return title[:100]
    except Exception:
        return None
    return None

def main():
    print("=== YouTube Transcript Tool (CLI - Timestamped) ===\n")
    
    # Ask for URL via command line
    url = input("Enter YouTube URL: ").strip()
    
    if not url:
        print("No URL provided. Exiting.")
        return
    
    # Validate URL
    if not ('youtube.com' in url or 'youtu.be' in url):
        print("Error: Please enter a valid YouTube URL")
        return
    
    # Extract video ID
    video_id = extract_video_id(url)
    if not video_id:
        print("Error: Could not extract video ID from URL")
        return
    
    print(f"\nProcessing video ID: {video_id}")
    print(f"URL: {url}")
    print("\nDownloading transcript...")
    
    try:
        # Fetch transcript (subtitles)
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)

        # Save transcript to a file named after the video ID
        transcriptions_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Transcriptions"))
        os.makedirs(transcriptions_dir, exist_ok=True)
        filename = os.path.join(transcriptions_dir, f"{video_id}_transcript.txt")

        with open(filename, "w", encoding="utf-8") as f:
            if tcommon:
                lines: List[str] = tcommon.build_timestamped_lines(transcript)  # type: ignore
            else:
                # Fallback inline timestamp builder
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
            for line in lines:
                f.write(line + "\n")
        
        print(f"✓ Transcript saved to {filename}")

        # Automatically rename transcript file using video title
        print("Fetching video title...")
        video_title = get_video_title_html(url)
        if video_title:
            target = os.path.join(transcriptions_dir, f"{video_title}_transcript.txt")
            if tcommon:
                target = tcommon.unique_path(target)  # ensure no collision
            try:
                if os.path.exists(filename):
                    os.rename(filename, target)
                    print(f"✓ Transcript file renamed to: {os.path.basename(target)}")
                    final_filename = target
                else:
                    print(f"Warning: Transcript file {filename} not found.")
                    final_filename = filename
            except OSError as e:
                print(f"Rename collision/permission issue ({e}); keeping original filename.")
                final_filename = filename
        else:
            print("Warning: Could not fetch video title, transcript not renamed.")
            final_filename = filename

        # Print absolute path to the final transcript file
        print(f"\n✓ SUCCESS! Transcript saved at:")
        print(f"  {os.path.abspath(final_filename)}")
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        print("\nPossible issues:")
        print("- Video has no captions/subtitles available")
        print("- Video is private or restricted")
        print("- Network connection issue")
        print("- Invalid video URL")

if __name__ == "__main__":
    main()
