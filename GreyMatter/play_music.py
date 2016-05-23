import os
import sys
import random

from SenseCells.tts import tts

sox_file_types = ['.wav','.flac','ogg']
music_listing = None

def mp3gen(music_path):
    """
    This function finds all the mp3 files in a folder and it's subfolders and returns a list.
    """
    global music_listing

    if music_listing != None:
        return

    if sys.platform != 'darwin' \
    and sys.platform != 'win32' \
    and not sys.platform.startswith('linux'):
        print "Music only enabled on darwin, win32, and linux."
        return

    music_listing = []
    for root, dirs, files in os.walk(music_path):
        for filename in files:
            if os.path.splitext(filename)[1] == ".mp3":
                if sys.platform == 'darwin':
                    music_listing.append([
                        'afplay',
                        os.path.join(root, filename.lower())])
                else:
                    music_listing.append([
                        'mpg123',
                        os.path.join(root, filename.lower())])
            elif os.path.splitext(filename)[1] in sox_file_types:
                if sys.platform != 'darwin':
                    music_listing.append([
                        'play',
                        os.path.join(root, filename.lower())])

def music_player(music_selection):
    """
    This function takes the name of a music file as an argument and plays it depending on the OS.
    """
    player = music_selection[0] + " '" + music_selection[1] + "'"
    return os.system(player)

def play_random(music_path):
    try:
        mp3gen(music_path)
        music_playing = random.choice(music_listing)
        tts("Now playing: " + music_playing[1])
        music_player(music_playing)

    except IndexError as e:
        tts('No music files found.')
        print("No music files found: {0}".format(e))

def play_specific_music(speech_text, music_path):
    words_of_message = speech_text.split()
    words_of_message.remove('play')
    cleaned_message = ' '.join(words_of_message)
    mp3gen(music_path)

    for i in range(0, len(music_listing)):
        if cleaned_message in music_listing[i][1]:
            music_player(music_listing[i])

def play_shuffle(music_path):
    try:
        mp3gen(music_path)
        random.shuffle(music_listing)
        for i in range(0, len(music_listing)):
            music_player(music_listing[i])

    except IndexError as e:
        tts('No music files found.')
        print("No music files found: {0}".format(e))

