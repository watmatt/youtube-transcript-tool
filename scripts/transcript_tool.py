#!/usr/bin/env python3
"""
Simple YouTube Transcript Tool with URL Input
Modified version of the original script that asks for URL
"""

# Dependency check and auto-install
import subprocess
import sys
def install_and_import(package, import_name=None):
    import importlib
    try:
        importlib.import_module(import_name or package)
    except ImportError:
        print(f"Installing missing package: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        importlib.invalidate_caches()
        importlib.import_module(import_name or package)

install_and_import('youtube-transcript-api', 'youtube_transcript_api')
install_and_import('requests')
install_and_import('beautifulsoup4', 'bs4')

from youtube_transcript_api import YouTubeTranscriptApi
import os
import requests
from bs4 import BeautifulSoup
import re
import tkinter as tk
from tkinter import simpledialog, messagebox

def extract_video_id(url):
    """Extract YouTube video ID from URL"""
    patterns = [
        r'(?:v=|/)([a-zA-Z0-9_-]{11})',
        r'youtu\.be/([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_title_html(video_url):
    """Function to get video title via HTML scraping"""
    try:
        response = requests.get(video_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.text.replace(' - YouTube', '').strip()
            title = title.replace("/", "-").replace("\\", "-").replace(":", "-").replace("|", "-").replace("?", "").replace("*", "-").replace("\"", "'").replace("<", "-").replace(">", "-")
            return title
        else:
            print("Title tag not found.")
            return None
    except Exception as e:
        print(f"Error fetching video title: {e}")
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
        # Fetch transcript (subtitles) - using the same method as original script
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        
        # Save transcript to a file named after the video ID
        transcriptions_dir = os.path.join(os.path.dirname(__file__), "..", "Transcriptions")
        os.makedirs(transcriptions_dir, exist_ok=True)
        filename = os.path.join(transcriptions_dir, f"{video_id}_transcript.txt")
        
        with open(filename, "w", encoding="utf-8") as f:
            for entry in transcript:
                f.write(entry.text + "\n")
        
        print(f"Transcript saved to {filename}")
        
        # Automatically rename transcript file using video title
        video_title = get_video_title_html(url)
        if video_title:
            new_filename = os.path.join(transcriptions_dir, f"{video_title}_transcript.txt")
            if os.path.exists(filename):
                os.rename(filename, new_filename)
                print(f"Transcript file renamed to: {new_filename}")
                final_filename = new_filename
            else:
                print(f"Transcript file {filename} not found.")
                final_filename = filename
        else:
            print("Could not fetch video title, transcript not renamed.")
            final_filename = filename
        
        # Print absolute path to the final transcript file
        print(f"Absolute path: {os.path.abspath(final_filename)}")
        
        # Show success message
        messagebox.showinfo("Success", f"Transcript downloaded successfully!\n\nSaved as:\n{os.path.basename(final_filename)}")
        
    except Exception as e:
        error_msg = f"Error downloading transcript: {str(e)}"
        print(error_msg)
        messagebox.showerror("Error", error_msg)

if __name__ == "__main__":
    main()
