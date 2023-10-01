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
    print('hi')
    try:
        print('hitry')
        with sd.InputStream(callback=print_sound_level):
            print('listening...')
            with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source, duration=1)
                voice = listener.listen(source, timeout=5, phrase_time_limit=5)
                command = listener.recognize_google(voice)
                command = command.lower()
                if 'alexa' in command:
                    command = command.replace('alexa', '')
                    print(command)
    except Exception as e:
        print(e)
    return command


def print_sound_level(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    print("|" * int(volume_norm))


def run_alexa():
    command = take_command()
    print('checking command' + command)
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
