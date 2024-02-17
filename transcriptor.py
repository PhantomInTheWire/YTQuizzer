from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from langdetect import detect
from googletrans import Translator


def translate_text(text):
    translator = Translator()  # Specify source language as Hindi
    out = translator.translate(text, dest='en')  # Use the translator object
    return out.text  # Return only the translated text


def get_id(url):
    # Parse the URL
    parsed_url = urlparse(url)
    # Extract the query parameters
    query_params = parse_qs(parsed_url.query)
    # Extract the video ID from the query parameters
    video_id = query_params["v"][0]
    return video_id


def get_transcript(url):
    v_id = get_id(url)
    transcript = YouTubeTranscriptApi.get_transcript(v_id, languages=["hi", "en"])
    s = ''
    a = ''
    for entry in transcript:
        if detect(entry['text']) == "hi":
            s += str(entry['text'])
            if len(s) > 1500:
                a += translate_text(s)
                s = ''
    return a


get_transcript("https://www.youtube.com/watch?v=I5srDu75h_M&list=PLfqMhTWNBTe3LtFWcvwpqTkUSlB32kJop&index=3")
