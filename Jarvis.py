
import speech_recognition as sr   
import webbrowser                   
import pyttsx3                      
import musicLibrary                  
import requests                        

from gtts import gTTS                   
import pygame                              
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()                                    
newsapi = "YOURAPIKEY"

def speak_old(text):
    engine.say(text)      
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)           
    tts.save('temp.mp3') 
    pygame.mixer.init()    

    pygame.mixer.music.load('temp.mp3')    
    pygame.mixer.music.play()              
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)          
    
    pygame.mixer.music.unload()       
    os.remove("temp.mp3")              


def processCommand(c):                  
    if "open google" in c.lower():                    
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):                  
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
           
            data = r.json()
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

    

if __name__ == "__main__":
    speak("Hello My name is Jarvis. How can i help u ?")
    while True:
        r = sr.Recognizer()             
        print("recognizing...")
        try:
            with sr.Microphone() as source:   
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)      
            word = r.recognize_google(audio)                                     .
            if(word.lower() == "jarvis"):
                speak("Yes")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:                                                         
            print("Error; {0}".format(e))
