import webbrowser # open blackboard etc
import geocoder # get location
import requests # make API GET Requests
import speech_recognition as sr # Recognize audio
from gtts import gTTS # Google Text to Speech
# from playsound import playsound # Need it with gtts
# pip install pyaudio
import tempfile
from tempfile import TemporaryFile
from pygame import mixer
import streamlit as st
import pandas as pd
import numpy as np
from quickstart import main

top_news_url = ('https://newsapi.org/v2/top-headlines?country=gb&apiKey=4956d442731e4f4a9c6b8ab201436a83')

# def Text_to_speech(message):
#     print(message)
#     speech = gTTS(text = message, lang='en')
#     speech.save('voice.mp3')
#     playsound('voice.mp3')

def Text_to_speech(message):
    print(message)
    speech = gTTS(text = message, lang='en')
    mixer.init()
    sf = TemporaryFile()
    speech.write_to_fp(sf)
    sf.seek(0)
    mixer.music.load(sf)
    mixer.music.play()
    #speech.save('voice.mp3')
    #playsound('voice.mp3')

listener = sr.Recognizer()
def take_command():
    command = ''
    try:
        with sr.Microphone() as source:
            print('listening...')
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)
            command = listener.recognize_google(voice)
            # command = command.lower().replace('alexa', '')
            # print("Command: " + command)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print("Command: " + command)
            
    except Exception as e:
        print(e)
    return command


def run_alexa():
    while True:
        command = take_command()

        if 'blackboard' in command:
            Text_to_speech('I am opening blackboard')
            webbrowser.open('https://blackboard.ie.edu/')

        elif 'mail' in command or 'gmail' in command or 'inbox' in command:
            Text_to_speech('I am opening mail..')
            webbrowser.open('https://mail.google.com/mail/u/0/#inbox')

        elif 'notion' in command:
            Text_to_speech('I am opening notion')
            webbrowser.open('https://www.notion.so/')

        elif 'joke' in command:
            Text_to_speech('I am finding a joke..')
            response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
            
            if response.status_code == 200:
                joke = response.json()["joke"]
                print(joke)
                Text_to_speech(joke)
            else:
                print("Failed to retrieve joke. Status code:", response.status_code)

        elif 'weather' in command:
            Text_to_speech('I am getting the weather..')
            g = geocoder.ip('me')
            response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={g.latlng[0]}&lon={g.latlng[1]}&appid=6a135bc7b549672e2c7ad106580fc8aa&units=metric"
    , headers={"Accept": "application/json"})
            if response.status_code == 200:
                weather = response.json()

                print(f"In {weather['name']} it is currently and {weather['weather'][0]['main']} and {weather['main']['temp']} °C")
                Text_to_speech(f"In {weather['name']} it is currently and {weather['weather'][0]['main']} and {weather['main']['temp']} °C")
            else:
                print("Failed to retrieve weather. Status code:", response.status_code)
        
        elif 'news about' in command:
            search_query = command.split("news about")[1]
            response = requests.get(F'https://newsapi.org/v2/top-headlines?q={search_query}&apiKey=4956d442731e4f4a9c6b8ab201436a83', headers={"Accept": "application/json"})
            if response.status_code == 200:
                articles = response.json()['articles']
                count = 0
                for article in articles:
                    Text_to_speech(article['title'])
                    print(article['title'])
                    if count == 2:
                        break
                    count = count + 1
            else:
                print("Failed to retrieve news. Status code:", response.status_code)

        elif 'news' in command:
            print('I am getting the top stories..')
            response = requests.get(top_news_url, headers={"Accept": "application/json"})
            if response.status_code == 200:
                articles = response.json()['articles']
                for article in articles:
                    Text_to_speech(article['title'])
                    print(article['title'])
            else:
                print("Failed to retrieve news. Status code:", response.status_code)

        elif 'plot of' in command:
            search_query = command.split("plot of")[1]
            response = requests.get(f'https://www.omdbapi.com/?t={search_query}&plot=full&apiKey=9e1b88d0', headers={"Accept": "application/json"})
            if response.status_code == 200:
                plot = response.json()['Plot']
                Text_to_speech(plot)
            else:
                print("Failed to retrieve plot. Status code:", response.status_code)
        
        elif 'class' in command or 'classes' in command:
            classes = main()
            if classes is None: 
                Text_to_speech("No Classes Today or Tomorrow")
            else:
                output = ""
                for event in classes:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    # print(start, event['summary'])
                    output += f"You have {event['summary']} at {start} "
                Text_to_speech(output)

        elif 'terminate' in command:
            print('Terminating the program...')
            break
    # else:
    #     talk('Please say the command again.')


run_alexa()

# st.title('Uber pickups in NYC')