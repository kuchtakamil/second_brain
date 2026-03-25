# ok, the last version works great. Is there any easy way to get the transcripts f

**Data:** 25 lis 2025, 00:25:55 CET

---

**User:**

ok, the last version works great. Is there any easy way to get the transcripts from these shorts?

---

**Gemini:**

Yes, the easiest and most standard way to get transcripts (including for Shorts) is using the **`youtube-transcript-api`** library. It works perfectly with the video IDs we extracted using `yt-dlp`.

Shorts often rely on **auto-generated captions**, and this library can fetch those seamlessly.

### Prerequisites

You need to install the transcript API library alongside `yt-dlp`:

```
pip install youtube-transcript-api yt-dlp
```

### The Complete Code

This script combines the robust `yt-dlp` listing method with the transcript fetcher. It includes a helper to format the transcript into a clean block of text.

```
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from typing import List, Dict, Any

def get_channel_shorts(channel_url: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Retrieves Shorts metadata using yt-dlp.
    """
    target_url = f"{channel_url.rstrip('/')}/shorts"
    
    ydl_opts = {
        'quiet': True,
        'extract_flat': 'in_playlist', 
        'force_generic_extractor': False,
        'ignoreerrors': True,
        'sleep_interval': 1,
        'no_warnings': True,
        'playlist_end': limit, # Optimization: Only fetch the first 'limit' items
    }

    results = []
    print(f"1. Fetching list of Shorts from: {target_url}")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(target_url, download=False)
            
            if 'entries' in info_dict:
                for video in info_dict['entries']:
                    if video:
                        results.append({
                            'id': video.get('id'),
                            'title': video.get('title'),
                            'url': video.get('url'),
                            'duration': video.get('duration'),
                        })
    except Exception as e:
        print(f"Error fetching list: {e}")

    return results

def append_transcripts(shorts_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Iterates over the list of shorts and fetches transcripts for each.
    Modifies the dictionary in-place to add a 'transcript' key.
    """
    formatter = TextFormatter()
    
    print(f"2. Downloading transcripts for {len(shorts_list)} videos...")

    for i, short in enumerate(shorts_list):
        video_id = short['id']
        try:
            # fetch_transcript returns a list of dicts (text, start, duration)
            # We prioritize English ('en'), but you can add others like ['en', 'de']
            transcript_raw = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            
            # Convert the list of time-synced lines into a single readable string
            text_formatted = formatter.format_transcript(transcript_raw)
            
            # Clean up newlines if you want a single paragraph
            short['transcript'] = text_formatted.replace("\n", " ")
            print(f"   [OK] Transcript found for: {short['title'][:30]}...")
            
        except Exception as e:
            # Common errors: TranscriptsDisabled, NoTranscriptFound
            short['transcript'] = None
            print(f"   [X]  No transcript for: {short['title'][:30]}... ({type(e).__name__})")
            
    return shorts_list

# --- Main Execution ---
if __name__ == "__main__":
    # Example: Marques Brownlee (MKBHD) Shorts
    CHANNEL_URL = "https://www.youtube.com/@mkbhd"
    
    # 1. Get the list (Limit to 5 for this demo)
    shorts_data = get_channel_shorts(CHANNEL_URL, limit=5)
    
    # 2. Get the text
    shorts_with_text = append_transcripts(shorts_data)
    
    # 3. Print Results
    print("\n" + "="*50)
    for i, item in enumerate(shorts_with_text):
        status = "Available" if item['transcript'] else "Unavailable"
        print(f"\n{i+1}. {item['title']} (Transcript: {status})")
        if item['transcript']:
            # Print the first 200 characters of the transcript as a preview
            preview = item['transcript'][:200] + "..."
            print(f"   Preview: {preview}")
            print(f"   Link: https://youtu.be/{item['id']}")
```

### Key Details

- **`languages=['en']`**: I set this to prioritize English. If the Short is in another language, or if you want to support auto-translated fallbacks, you can modify this list or use `list_transcripts(video_id)` for more granular control.
- **`TextFormatter`**: This utility removes the timestamps (`start`: 0.5s) and gives you just the raw text, which is usually what you want for analysis or reading.
- **Error Handling**: Not all Shorts have captions. The `try/except` block ensures the script continues running even if one video fails (returning `None` for that specific transcript).

... [How to get the transcript of a YouTube video](https://www.youtube.com/watch?v=Z6nkEZyS9nA) ...

This video by the creator of the `youtube-transcript-api` explains the internal logic of fetching captions if you need to debug specific language issues.