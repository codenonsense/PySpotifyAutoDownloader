import subprocess

# List of required libraries
required_libraries = ['spotipy', 'pandas', 'yt_dlp']

# Install libraries if not already installed
for library in required_libraries:
    try:
        __import__(library)
    except ImportError:
        subprocess.check_call(['pip', 'install', library])


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import pandas as pd
import yt_dlp
from docx import Document
import re

# Set up credentials
client_id = '862429e9caba4b5aa711f5b79215e55a'
client_secret = '6bbc75104da64733ac5bb67b04ab86a3'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def extract_playlist_id(url):
    pattern = r'playlist/([a-zA-Z0-9]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        raise ValueError('Invalid Spotify playlist URL')

# Get Spotify playlist URL from user input
playlist_url = input('Enter the Spotify playlist URL: ')

# Extract playlist ID
playlist_id = extract_playlist_id(playlist_url)

# Construct Spotify URI
spotify_uri = f'spotify:playlist:{playlist_id}'

# Print the Spotify URI
print(f'Spotify URI: {spotify_uri}')

results = sp.playlist_tracks(spotify_uri)

csv_file_path = 'playlist_songs.csv'

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Song Name'])  # Write header row

    for track in results['items']:
        song_name = track['track']['name']
        csv_writer.writerow([song_name])

print(f'Song names have been saved to {csv_file_path}.')

df = pd.read_csv('playlist_songs.csv')

for i, song_name in enumerate(df['Song Name']):
    with yt_dlp.YoutubeDL({}) as ydl:
        info = ydl.extract_info(f"ytsearch:{song_name}", download=True)
        if 'entries' in info:
            video = info['entries'][0]
            song_info = {
                'Song Name': song_name,
                'Artist/Channel Name': video['uploader'],
                'YouTube Link': video['webpage_url'],
                'Title': video['title']
            }
            

            # Print the information
            print(f"Song {i+1}:")
            for key, value in song_info.items():
                print(f"{key}: {value}")
            print("-----------------------------------")
            
                