# Import libraries
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import sys
import psutil
import time
import webbrowser

# Initialize speech recognizer & engine
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)  # Set Female Voice if available

# Function to make Alexa speak
def engine_talk(text):
    print(f"Alexa: {text}")
    engine.say(text)
    engine.runAndWait()

# Function to recognize user commands
def user_commands():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice).lower()
            if 'alexa' in command:
                return command.replace('alexa', '').strip()
    except (sr.UnknownValueError, sr.RequestError):
        engine_talk("I couldn't understand. Please repeat.")
    return ""

# Function to open websites
def open_website(command):
    sites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "github": "https://www.github.com",
        "stackoverflow": "https://www.stackoverflow.com",
        "facebook": "https://www.facebook.com"
    }
    for site, url in sites.items():
        if site in command:
            engine_talk(f"Opening {site}")
            webbrowser.open(url)
            return True
    return False

# Function to get system info
def get_system_info():
    battery = psutil.sensors_battery()
    return f"Battery is at {battery.percent}% and {'charging' if battery.power_plugged else 'not charging'}."

# Function to set a reminder
def set_reminder(task, delay):
    engine_talk(f"Reminder set for {task} in {delay} seconds.")
    time.sleep(delay)
    engine_talk(f"Reminder: {task}")

# Function to send a WhatsApp message
def send_whatsapp_message(message):
    phone_number = "+1234567890"  # Replace with actual number
    engine_talk(f"Sending WhatsApp message: {message}")
    pywhatkit.sendwhatmsg_instantly(phone_number, message)
   

# Main function to run Alexa
def run_alexa():
    command = user_commands()
    
    if not command:
        return
    
    if 'play' in command:
        song = command.replace('play', '').strip()
        engine_talk(f"Playing {song}")
        pywhatkit.playonyt(song)
    
    elif 'time' in command:
        engine_talk(f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}")
    
    elif 'who is' in command or 'what is' in command:
        info = wikipedia.summary(command.replace('who is', '').replace('what is', ''), 1)
        print(info)
        engine_talk(info)
    
    elif 'joke' in command:
        engine_talk(pyjokes.get_joke())
    
    elif 'open' in command and not open_website(command):
        engine_talk("I can't open that website.")
    
    elif 'whatsapp' in command:
        engine_talk("What should I send?")
        message = user_commands()
        send_whatsapp_message(message)
    
    elif 'reminder' in command:
        engine_talk("What should I remind you about?")
        task = user_commands()
        engine_talk("In how many seconds?")
        try:
            set_reminder(task, int(user_commands()))
        except ValueError:
            engine_talk("Invalid time. Please try again.")
    
    elif 'battery' in command or 'system' in command:
        engine_talk(get_system_info())
    
    elif 'stop' in command or 'exit' in command:
        engine_talk("Goodbye!")
        sys.exit()
    
    else:
        engine_talk("Sorry, I couldn't understand that.")

# Keep listening
while True:
    run_alexa()
