# unfortunately I got 1. Fetching list of Shorts from: https://www.youtube.com/@Jo

**Data:** 25 lis 2025, 00:31:01 CET

---

**User:**

unfortunately I got
1. Fetching list of Shorts from: https://www.youtube.com/@JonPengEnglish/shorts
2. Downloading transcripts for 675 videos...
   [X]  No transcript for: Restaurant English: Can I get ... (YouTubeRequestFailed)
   [X]  No transcript for: Useful Visa Interview English ... (YouTubeRequestFailed)
   [X]  No transcript for: Restaurant English: What does ... (YouTubeRequestFailed)
   [X]  No transcript for: Weekly Extra English Lessons a... (TranscriptsDisabled)
   [X]  No transcript for: Restaurant English: How to Ord... (YouTubeRequestFailed)

---

**Gemini:**

The error `YouTubeRequestFailed` typically indicates that **YouTube has soft-banned your IP address** temporarily because you sent too many requests too quickly (675 videos is a lot!). The `youtube-transcript-api` uses the web frontend, which has strict bot detection.

To fix this, we need to move the transcript downloading logic to **`yt-dlp`** as well. `yt-dlp` is much better at handling anti-bot measures, supports cookies, and can download subtitles directly.

Here is the complete, robust solution.

### Key Changes

1. **Pure `yt-dlp`:** We now use `yt-dlp` for *both* finding videos and downloading subtitles (bypassing the blocked library).
2. **VTT Cleaning:** I included a custom function to clean the messy `.vtt` subtitle format into readable text.
3. **Rate Limiting:** Added `time.sleep()` to prevent getting banned again.

### The Code

```
import yt_dlp
import time
import random
import os
import re
from typing import List, Dict, Any

def get_channel_shorts(channel_url: str) -> List[Dict[str, Any]]:
    """
    Fetches the list of Shorts using yt-dlp (fast metadata extraction).
    """
    target_url = f"{channel_url.rstrip('/')}/shorts"
    
    ydl_opts = {
        'quiet': True,
        'extract_flat': 'in_playlist', 
        'ignoreerrors': True,
        'no_warnings': True,
        # Optimization: Only get the first 50 to test (remove 'playlist_end' to get all)
        # 'playlist_end': 50, 
    }

    results = []
    print(f"--- 1. Fetching Shorts list from {target_url} ---")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(target_url, download=False)
        if 'entries' in info:
            for video in info['entries']:
                if video:
                    results.append({
                        'id': video['id'],
                        'title': video.get('title', 'Unknown Title'),
                        'url': video.get('url'),
                    })
    return results

def clean_vtt_text(vtt_content: str) -> str:
    """
    Parses raw VTT subtitle content into a clean string.
    Removes timestamps, duplicate lines, and HTML-like tags.
    """
    lines = []
    seen_lines = set()
    
    # Regex to strip tags like <c.colorE5E5E5> or <00:00:00.000>
    tag_pattern = re.compile(r'<[^>]+>')
    
    for line in vtt_content.splitlines():
        line = line.strip()
        
        # Skip empty lines, 'WEBVTT' headers, and timestamp lines (00:00 --> 00:00)
        if not line or line == 'WEBVTT' or '-->' in line:
            continue
            
        # Remove internal tags
        clean_line = tag_pattern.sub('', line)
        
        # YouTube auto-subs often duplicate lines; we deduplicate adjacent lines
        # and also use a set to avoid exact sentence repetitions in short succession
        if clean_line and clean_line not in seen_lines:
            lines.append(clean_line)
            seen_lines.add(clean_line)
            
            # Reset seen_lines periodically to allow same words later in video? 
            # For Shorts, global uniqueness is usually fine and cleaner.

    return " ".join(lines)

def download_transcript_ytdlp(video_id: str) -> str:
    """
    Uses yt-dlp to download the auto-generated subtitle file, reads it, and cleans it.
    Returns None if no subtitles are found.
    """
    # Temporary filename template
    temp_filename = f"temp_subs_{video_id}"
    
    ydl_opts = {
        'quiet': True,
        'skip_download': True,      # Don't download the video
        'writeautomaticsub': True,  # Download auto-generated subs
        'subtitleslangs': ['en'],   # English only
        'outtmpl': temp_filename,   # Output filename
        'no_warnings': True,
    }

    transcript_text = None

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
            
        # yt-dlp saves as filename.en.vtt
        expected_file = f"{temp_filename}.en.vtt"
        
        if os.path.exists(expected_file):
            with open(expected_file, 'r', encoding='utf-8') as f:
                raw_vtt = f.read()
                transcript_text = clean_vtt_text(raw_vtt)
            
            # Cleanup temp file
            os.remove(expected_file)
            
    except Exception:
        pass  # Fail silently for this video

    return transcript_text

# --- Main Execution ---
if __name__ == "__main__":
    CHANNEL = "https://www.youtube.com/@JonPengEnglish"
    
    # 1. Get the list
    shorts = get_channel_shorts(CHANNEL)
    print(f"Found {len(shorts)} shorts. Processing transcripts...")

    # 2. Process with Rate Limiting
    valid_transcripts = 0
    
    for i, short in enumerate(shorts):
        print(f"[{i+1}/{len(shorts)}] Processing: {short['title'][:40]}...", end=" ", flush=True)
        
        text = download_transcript_ytdlp(short['id'])
        
        if text:
            print(f"[OK] ({len(text)} chars)")
            short['transcript'] = text
            valid_transcripts += 1
            
            # Save or process immediately here if needed
            # with open("output.txt", "a") as f: f.write(f"{short['title']}\n{text}\n\n")
        else:
            print(f"[NO SUBS]")
            short['transcript'] = None

        # IMPORTANT: Sleep to avoid 429/RequestFailed errors
        # Random sleep between 2 and 5 seconds makes you look less like a bot
        time.sleep(random.uniform(2, 5))

    print(f"\nDone! Extracted {valid_transcripts} transcripts.")
```

### Why this works better

1. **Request Handling:** `yt-dlp` rotates its headers and mimics a real browser client more effectively than `youtube-transcript-api`.
2. **Robustness:** Even if one video fails, the script continues. The `time.sleep` is critical when processing 600+ items.
3. **Cookies (Optional):** If you *still* get errors, you can easily add authentication by adding one line to `ydl_opts`:

   ```
   # Use cookies from your Chrome browser (make sure Chrome is closed or allows reading)
   'cookiesfrombrowser': ('chrome',),
   ```

... [Using yt-dlp to download youtube transcript](https://www.youtube.com/watch?v=RDxuTwhi8LA) ...

This video demonstrates the `yt-dlp` workflow for text extraction, which is the exact method utilized in the code above to bypass the API restrictions you encountered.