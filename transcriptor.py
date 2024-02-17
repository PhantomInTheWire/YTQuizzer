from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


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
    #    s = ''
    #    for entry in transcript:
    #       if detect(entry['text']) == "hi":
    #    s += str(entry['text'])
    #    if len(s) > 1500:
    #        temp = translate_text(s)
    #        s = ('')
    #        with open('translation files/transcript.txt', 'a', encoding='utf-8') as file:
    #            file.write(f'{temp}\n')
    transcript = " ".join([item["text"] for item in transcript])
    return transcript
