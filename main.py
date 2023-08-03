import openai
from apikey import api_data
import pyttsx3
import speech_recognition as sr
import webbrowser
import tkinter as tk
from PIL import Image, ImageTki

openai.api_key = api_data

completion = openai.Completion()


def Reply(question):
    prompt = f'Nimesha: {question}\nHinata:'
    response = completion.create(
        prompt=prompt, engine="text-davinci-002", stop=['Nimesha'], max_tokens=50)
    answer = response.choices[0].text.strip()
    return answer


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Adjust speaking rate and volume for a smoother experience
engine.setProperty('rate', 160)  # Adjust the rate as per your preference
engine.setProperty('volume', 0.8)  # Adjust the volume as per your preference


def speak(text):
    engine.say(text)
    engine.runAndWait()


speak("Hi, I'm Hinata, your personal voice assistant!")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    print("Recognizing.....")
    try:
        query = r.recognize_google(audio, language='en-in')
        print("Nimesha Said: {} \n".format(query))
        return query
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Could you please repeat?")
        return takeCommand()


def takeYouTubeQuery():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening for YouTube search....')
        r.pause_threshold = 1
        audio = r.listen(source)

    print("Recognizing YouTube search query.....")
    try:
        query = r.recognize_google(audio, language='en-in')
        print("User Said: {} \n".format(query))
        return query
    except sr.UnknownValueError:
        print("Sorry, I didn't catch the YouTube search query. Please try again.")
        return takeYouTubeQuery()


def on_button_click():
    query = takeCommand().lower()
    ans = Reply(query)
    print(ans)
    speak(ans)

    if 'open youtube' in query:
        speak("Sure, opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    if 'play' in query and 'song' in query:
        speak("Sure, what song would you like to search for on YouTube?")
        song_query = takeYouTubeQuery()
        speak(f"Searching for the song '{song_query}' on YouTube.")
        url = f"https://www.youtube.com/results?search_query={song_query}"
        webbrowser.open(url)

    if 'open google' in query:
        speak("Sure, opening Google.")
        webbrowser.open("https://www.google.com")

    if 'bye' in query:
        speak("Goodbye!")
        root.quit()


root = tk.Tk()
root.title("Hinata - Voice Assistant")
root.geometry("400x400")
root.configure(bg="black")  # Set black background

# Load microphone image
mic_image_path = "mic.png"
mic_image = Image.open(mic_image_path)
mic_image = mic_image.resize((50, 50), Image.ANTIALIAS)
mic_icon = ImageTk.PhotoImage(mic_image)

button = tk.Button(
    root,
    image=mic_icon,
    command=on_button_click,
    bd=0,  # Remove button border
    bg="black",  # Set button background to match the window background
    relief="flat",
)
button.place(relx=0.5, rely=0.5, anchor="center")

root.mainloop()
