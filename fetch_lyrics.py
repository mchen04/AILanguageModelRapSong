import re
import lyricsgenius
import spotipy
from langdetect import detect, LangDetectException
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm
import requests
import time

def read_api_keys_from_file(filename):
    """Load API keys from a file."""
    with open(filename, 'r') as f:
        lines = f.readlines()
        keys = {}
        for line in lines:
            key, value = line.strip().split(' = ')
            keys[key] = value
    return keys

def initialize_spotipy_client(keys):
    """Configure and return Spotipy client."""
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=keys['SPOTIFY_CLIENT_ID'], client_secret=keys['SPOTIFY_CLIENT_SECRET']))

def retrieve_songs_from_spotify(sp_client, artist_name):
    """Get songs of a given artist from Spotify."""
    results = sp_client.search(q=f'artist:{artist_name}', type='artist')
    artist_id = results['artists']['items'][0]['id']
    albums = sp_client.artist_albums(artist_id, album_type='album,single', limit=50)
    all_songs = [track['name'] for album in albums['items'] for track in sp_client.album_tracks(album['id'])['items']]
    return all_songs

def fetch_lyrics_from_genius(song_title, artist_name, genius_key, max_retries=3, delay=5):
    retries = 0
    genius = lyricsgenius.Genius(genius_key, verbose=False, timeout=10)  # Setting timeout to 10 seconds
    while retries < max_retries:
        try:
            song = genius.search_song(song_title, artist_name)
            return song.lyrics if song else None
        except requests.exceptions.Timeout:
            retries += 1
            time.sleep(delay)  # Wait for a few seconds before retrying
    return None  # Return None if all retries failed


def clean_lyrics(lyrics, artist_name):
    """Clean the lyrics based on specified filters."""
    filters = [
        r'(?i)^See\s' + re.escape(artist_name) + r'.*',
        r'^You might also like.*',
        r'^\[.*\]',
        r'.*[\U00010000-\U0010ffff].*',
        r'^\d+\..*',
        r'^\d+/\d+.*',
        r'^\d+\.\d+K$',
        r'^[A-Za-z\s&\*\$’]+(?:\s-\s|\s&\s|\s–\s).*',
        r'^.*\s\((feat\.|ft\.|with).*',
        r'^.*" feat\..*',
        r'^.*"\s.*',
        r'^•\s.*:\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d+.*',
        r'^-\s.*\s\(\d+,\d+,\d+\)',
        r'^.*\s-\s.*feat\..*',
        r'^.*\s-\s.*&\s.*',
        r'^.*\s/\s.*\s-\s.*',
        r'^.*\s-\s[A-Za-z\s&\*\$’]+.*'
        r'^Contributors',
        r'^Translations',
        r'(?i)^See\s+\w+\s+LiveGet tickets as low as \$\d+',
        r'(?i)^You might also likeYou might also like',
        r'^\d+ ContributorsTranslations.* Lyrics'
        r'^.*\s(?:-\s|&\s|–\s).*'
        r'^\d+\s(contributors|translators)$'
    ]

    see_artist_live_pattern = r'(?i)^See\s' + re.escape(artist_name) + r'\sLive'
    get_tickets_pattern = r'(?i)Get tickets as low as \$\d+'
    you_might_also_like_pattern = r'(?i)You might also like'

    lyrics = re.sub(see_artist_live_pattern, '', lyrics)
    lyrics = re.sub(get_tickets_pattern, '', lyrics)
    lyrics = re.sub(you_might_also_like_pattern, '', lyrics)

    lines = lyrics.split('\n')
    lines = [line for line in lines if not any(re.match(pattern, line) for pattern in filters)]
    
    # Clean out patterns like "7embed" from the lines without deleting the entire line
    embed_pattern = r'\d+Embed'
    lines = [re.sub(embed_pattern, '', line) for line in lines]

    embed_pattern_word_only = r'\bembed\b'
    lines = [re.sub(embed_pattern_word_only, '', line, flags=re.IGNORECASE) for line in lines]

    lines = [line for line in lines if line and not line.startswith('[') and not line.endswith(']')]


    # 1. Delete lines that are over 25 words
    lines = [line for line in lines if len(line.split()) <= 25]

    # 2. Delete lines that start with anything that isn't a (, number, or character
    lines = [line for line in lines if re.match(r'^[a-zA-Z0-9(]', line)]

    # 3. Delete any line that ends with a decimal number of any kind
    lines = [line for line in lines if not re.search(r'\.\d+$', line)]

    # 4. If a line ends with a number and the line before or after it ends with a decimal number, delete the line
    to_remove = set()
    for i, line in enumerate(lines):
        if re.search(r'\d+$', line):  # if line ends with a number
            if i > 0 and re.search(r'\.\d+$', lines[i-1]):  # check the line before
                to_remove.add(i)
            if i < len(lines) - 1 and re.search(r'\.\d+$', lines[i+1]):  # check the line after
                to_remove.add(i)
    lines = [line for i, line in enumerate(lines) if i not in to_remove]

    cleaned_lyrics = '\n'.join(lines)

    try:
        if detect(cleaned_lyrics) == 'en':
            return cleaned_lyrics
        else:
            #print(f"Lyrics not primarily in English for song by {artist_name}.")
            return None
    except LangDetectException:
        #print(f"Error detecting language for song by {artist_name}. It's possible the lyrics don't have enough recognizable features.")
        return None

def fetch_and_store_lyrics(sp_client, genius_key, artist_name):
    songs = retrieve_songs_from_spotify(sp_client, artist_name)
    total_songs = len(songs)

    with open('lyrics.txt', 'a', encoding='utf-8') as f:
        for song_title in tqdm(songs, desc=f"Processing {artist_name}", total=total_songs, position=0, leave=True):
            exclusion_terms = {
                "remix", "stripped", "interlude", "sped up", "slow down", "sped-up",
                "slow-down", "version", "live", "live-session", "live session", "acoustic",
                "unplugged", "demo", "edit", "re-recorded", "reprise", "instrumental",
                "dub", "mashup", "orchestral", "a cappella", "karaoke", "take", "cut",
                "loop", "segue", "re-edit", "re-mix"
            }
            if any(term in song_title.lower() for term in exclusion_terms):
                #print(f"Skipping {song_title} due to exclusion terms.")
                continue

            lyrics = fetch_lyrics_from_genius(song_title, artist_name, genius_key)
            if lyrics:
                lyrics = clean_lyrics(lyrics, artist_name)
                if not lyrics:
                    continue
                
                f.write(lyrics + '\n')
            #else:
                #print(f"Lyrics not found for {song_title} by {artist_name}")

if __name__ == "__main__":
    artists = input("Enter the names of the artists you want to check (separated by commas): ")
    artist_list = [artist.strip() for artist in artists.split(",")]

    api_keys = read_api_keys_from_file('keys.txt')
    sp_client = initialize_spotipy_client(api_keys)

    for artist_name in artist_list:
        fetch_and_store_lyrics(sp_client, api_keys['GENIUS_API_KEY'], artist_name)
