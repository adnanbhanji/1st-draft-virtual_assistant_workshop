import speech_recognition as sr
import pyttsx3
import webbrowser

listener = sr.Recognizer()
engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)



def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    command = ''
    print('hi')
    try:
        print('hitry')
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration = 1)
            print('listening...')
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except Exception as e:
        print(e)
    return command


def run_alexa():
    command = take_command()
    print('cheching command' + command)
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