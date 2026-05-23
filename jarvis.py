import speech_recognition as aa
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import requests

# Initialize recognizer and text-to-speech engine
listener = aa.Recognizer()
machine = pyttsx3.init()

# Function for Jarvis to speak
def talk(text):
    machine.say(text)
    machine.runAndWait()

# Function to capture user voice input
def input_instruction():
    try:
        with aa.Microphone() as origin:
            print("Listening...")
            speech = listener.listen(origin)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
            if "jarvis" in instruction:
                instruction = instruction.replace('jarvis', '')
            return instruction
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to fetch weather information
def get_weather(city):
    api_key = "b1e88ecef346227f7c8be8ef073b01c7"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={'b1e88ecef346227f7c8be8ef073b01c7'}&units=metric"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            return f"The weather in {city} is {weather} with a temperature of {temp}°C."
        else:
            return f"Unable to fetch the weather information for {city}. Please try again."
    except Exception as e:
        return f"An error occurred: {e}"

# Main function to process commands
def play_Jarvis():
    instruction = input_instruction()
    if not instruction:
        talk("I didn't hear anything. Please try again.")
        return

    print(f"Instruction: {instruction}")

    if "play" in instruction:
        song = instruction.replace('play', "").strip()
        talk(f"Playing {song}")
        pywhatkit.playonyt(song)

    elif 'time' in instruction:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f'Current time is {time}')

    elif 'date' in instruction:
        date = datetime.datetime.now().strftime('%d/%m/%Y')
        talk(f"Today's date is {date}")

    elif 'how are you' in instruction:
        talk('I am fine, how about you?')

    elif 'what is your name' in instruction:
        talk('I am Jarvis, your personal assistant. What can I do for you?')

    elif 'who is' in instruction:
        human = instruction.replace('who is', "").strip()
        try:
            info = wikipedia.summary(human, sentences=1)
            print(info)
            talk(info)
        except wikipedia.exceptions.DisambiguationError:
            talk("There are multiple results. Please be more specific.")
        except wikipedia.exceptions.PageError:
            talk("I couldn't find anything on that topic.")

    elif 'weather' in instruction:
        talk("Which city do you want to know about?")
        city = input_instruction()
        if city:
            weather_info = get_weather(city)
            print(weather_info)
            talk(weather_info)
        else:
            talk("I didn't hear the city name. Please try again.")

    else:
        talk('I did not understand. Please repeat.')

# Start Jarvis
play_Jarvis()