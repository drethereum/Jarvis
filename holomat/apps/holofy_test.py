import pygame
import sys
import time
import subprocess
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import find_dotenv, load_dotenv, set_key

# Load .env file
dotenv_path = find_dotenv()
if not dotenv_path:
    print("Error: .env file not found")
    exit(1)
load_dotenv(dotenv_path,override=True)

# Spotify API credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

scope = "user-read-playback-state,user-modify-playback-state,playlist-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=scope))

pygame.init()

screen_width, screen_height = 1440, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Holofy Music Player")

# Load font
font = pygame.font.Font(None, 36)
white =  (255, 255, 255)

# Load images
background_img = pygame.image.load('holomat/resources/spotify/banner.png')
play_button_img = pygame.image.load('holomat/resources/spotify/play.png')
pause_button_img = pygame.image.load('holomat/resources/spotify/pause.png')
prev_button_img = pygame.image.load('holomat/resources/spotify/previous.png')
skip_button_img = pygame.image.load('holomat/resources/spotify/skip.png')

# Scale images
background = pygame.transform.smoothscale(background_img, (screen_width, screen_height))

button_scale = 0.5
play_button_width, play_button_height = play_button_img.get_size()
play_button = pygame.transform.smoothscale(play_button_img, (int(play_button_width * button_scale), int(play_button_height * button_scale)))
pause_button_width, pause_button_height = pause_button_img.get_size()
pause_button = pygame.transform.smoothscale(pause_button_img, (int(pause_button_width * button_scale), int(pause_button_height * button_scale)))
prev_button_width, prev_button_height = prev_button_img.get_size()
prev_button = pygame.transform.smoothscale(prev_button_img, (int(prev_button_width * button_scale), int(prev_button_height * button_scale)))
skip_button_width, skip_button_height = skip_button_img.get_size()
skip_button = pygame.transform.smoothscale(skip_button_img, (int(skip_button_width * button_scale), int(skip_button_height * button_scale)))

# Position images
background_rect = background.get_rect(center=screen.get_rect().center)

play_button_rect = play_button.get_rect()
pause_button_rect = pause_button.get_rect()
prev_button_rect = prev_button.get_rect()
skip_button_rect = skip_button.get_rect()

total_button_width = (play_button_rect.width + pause_button_rect.width +
               prev_button_rect.width + skip_button_rect.width) + 30  # total spacing between buttons

button_pos_x = (screen_width - total_button_width) // 2
button_pos_y = (screen_height - 400) # number of pixels from the bottom of the screen

button_spacing = 10
prev_button_rect.topleft = (button_pos_x, button_pos_y)
play_button_rect.topleft = (prev_button_rect.topright[0] + button_spacing, button_pos_y)
pause_button_rect.topleft = (play_button_rect.topright[0] + button_spacing, button_pos_y)
skip_button_rect.topleft = (pause_button_rect.topright[0] + button_spacing, button_pos_y)

def get_active_device():
    devices = sp.devices()['devices']
    if not devices:
        print('No devices found. Defaulting...')
        return None

    for device in devices:
        if device['is_active']:
            print(device['id'])
            return device['id']
    
    return devices[0]['id'] # If no active device is found, return the first available device

def open_spotify_app():
    try:
        if sys.platform == "darwin":  # macOS
            subprocess.run(["open", "-a", "Spotify"])
        elif sys.platform == "win32":  # Windows
            os.system("start spotify") # specify path to Spotify.exe if necessary
        time.sleep(5)  # Give Spotify some time to open
        return True
    except Exception as e:
        print(f"Failed to open Spotify app: {e}")
        return False
    
def close_spotify_app():
    try:
        if sys.platform == "darwin":  # macOS
            subprocess.run(["pkill", "Spotify"])
        elif sys.platform == "win32":  # Windows
            os.system("taskkill /f /im Spotify.exe")
        time.sleep(1)  # Give some time to close the process
        return True
    except Exception as e:
        print(f"Failed to close Spotify app: {e}")
        return False

def play_song(song_uri):
    device_id = spotify_device_id
    if device_id:
        sp.start_playback(device_id=device_id, uris=[song_uri])

def pause_song():
    device_id = spotify_device_id
    if device_id:
        sp.pause_playback(device_id=device_id)

def prev_song():
    device_id = spotify_device_id
    if device_id:
        sp.previous_track(device_id=device_id)

def skip_song():
    device_id = spotify_device_id
    if device_id:
        sp.skip_track(device_id=device_id)

def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    return results['items']

open_spotify_app()
spotify_device_id = get_active_device()

# Spotify Track Selection
playlist_id = '2JRXnerNyzSs7W7eOpYvU3'
tracks = get_playlist_tracks(playlist_id)
track_index = 0

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print("Spotify Application Closed")
            close_spotify_app()
            print("Holofy Application Closed")
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                play_song(tracks[track_index]['track']['uri'])
            elif pause_button_rect.collidepoint(event.pos):
                pause_song()
            elif skip_button_rect.collidepoint(event.pos):
                track_index = (track_index + 1) % len(tracks)
                play_song(tracks[track_index]['track']['uri'])
            elif prev_button_rect.collidepoint(event.pos):
                track_index = (track_index - 1) % len(tracks)
                play_song(tracks[track_index]['track']['uri'])

        # Display the current track
        track_name = tracks[track_index]['track']['name']
        track_artist = tracks[track_index]['track']['artists'][0]['name']
        track_title = font.render(f"{track_name} by {track_artist}", True, white)

        track_title_rect = track_title.get_rect()
        track_title_rect.centerx = screen.get_rect().centerx
        track_title_rect.bottom = button_pos_y - 100

        screen.blit(background,background_rect)
        screen.blit(track_title, track_title_rect)
        screen.blit(play_button, play_button_rect)
        screen.blit(pause_button, pause_button_rect)
        screen.blit(prev_button, prev_button_rect)
        screen.blit(skip_button, skip_button_rect)

        pygame.display.flip()