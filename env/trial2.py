import speech_recognition as sr
import pyttsx3
import webbrowser
import sounddevice as sd
import numpy as np

listener = sr.Recognizer()
engine = pyttsx3.init()

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    command = ''
    # print('hi')
    try:
        # print('hitry')
        with sd.InputStream(samplerate=16000, blocksize=2048):
            print('listening...')
            duration = 4  # seconds
            fs=44100
            myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
            sd.default.samplerate = fs
            sd.default.channels = 1
            sd.wait()

            command = listener.recognize_google(myrecording.tobytes())
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except Exception as e:
        print(e)
    return command

def run_alexa():
    command = take_command()
    print('checking command ' + command)
    if 'blackboard' in command:
        talk('I am opening blackboard')
        webbrowser.open('https://blackboard.ie.edu/')
    if ('mail' or 'gmail' or 'inbox') in command:
        talk('I am opening mail')
        webbrowser.open('https://mail.google.com/mail/u/0/#inbox')
    if 'notion' in command:
        talk('I am opening notion')
        webbrowser.open('https://www.notion.so/')
    # else:
    #     talk('Please say the command again.')

while True:
    run_alexa()
