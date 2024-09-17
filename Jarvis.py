
import speech_recognition as sr   # Used to convert spoken language into text.
import webbrowser                   # Opens a web browser to a specified URL.
import pyttsx3                      # Provides text-to-speech functionality
import musicLibrary                    # this module we made to store some songs, so that we can directly say jarvis to open the song.
import requests                         # this is to make http request in order to access news through news api

from gtts import gTTS                   # Google Text-to-Speech, converts text to speech and saves it as an MP3 file.
import pygame                              # Handles multimedia functions, like playing audio.
import os

# Here we are using two-three "text to speech" function
# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()                                    # Initializes the text-to-speech engine.
newsapi = "d07dd927e940405abcd523835d025fd1"

def speak_old(text):
    engine.say(text)       # Converts text into speech using the pyttsx3 engine.
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)            # Converts the text into speech and saves it as an MP3 file named temp.mp3.
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()    # Initializes the Pygame mixer module for audio playback.

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')    # Loads the MP3 file to be played.

    # Play the MP3 file
    pygame.mixer.music.play()               #  Plays the loaded MP3 file.

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)          # Checks if the music is still playing. If yes, the program waits (tick(10) keeps the program running).
    
    pygame.mixer.music.unload()        #  Stops and unloads the current music file.
    os.remove("temp.mp3")               # Deletes the temporary MP3 file to clean up.


def processCommand(c):                  
    if "open google" in c.lower():                     # Opens the specified URL in the default web browser.
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):                    # this is for music
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

    

if __name__ == "__main__":
    speak("Hello My name is Jarvis. How can i help u ?")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()             #Creates a Recognizer object to convert speech to text.
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:   # Uses the microphone as the audio source.
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)      # Listens for speech with a 2-second timeout and 1-second phrase limit.
            word = r.recognize_google(audio)                                     # Converts the captured audio to text using Google’s speech recognition.
            if(word.lower() == "jarvis"):
                speak("Yes")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:                                                          # Catches and prints any errors that occur during the listening or processing of commands.
            print("Error; {0}".format(e))