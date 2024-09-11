
import pyttsx3 
import speech_recognition as sr 
import datetime
import wikipedia 
import webbrowser
from googlesearch import search
import smtplib
import requests
from bs4 import BeautifulSoup

engine = pyttsx3.init()
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am Jarvis. Please tell me how may I help you")       

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

def google_search(query):
    for j in search(query, num=1, stop=1, pause=2):
        r = requests.get(j)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Attempt to find the headline, usually in an <h1> tag
        headline = soup.find('h1')
        if headline:
            text = headline.get_text()
        else:
            # Fallback to using the meta description if no <h1> tag is found
            meta_description = soup.find('meta', attrs={'name': 'description'})
            text = meta_description['content'] if meta_description and meta_description.get('content') else "Headline not found."
        
        print(text)
        speak(text)
       

if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'tell me ' in query:
            query = query.replace("tell me", "")
            google_search(query)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'send email to aditya' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "adityamanapure22@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry aditya. I am not able to send this email")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'switch off' in query:
            speak("stopping the program")
            exit()

        else:
            print("No query matched")