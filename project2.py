from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import requests
import time
import randfacts
from googlesearch import search
from googletrans import Translator
from langdetect import detect
import geocoder
import pyowm
from datetime import datetime
import sys
import googlemaps
import webbrowser
import psutil
import cv2

class Infow:
    def _init_(self):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.translator = Translator()
        # self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # self.emotion_model = cv2.dnn.readNetFromTensorflow('emotion_model.pb')
        # self.emotions = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

    def get_info(self, query):
        self.query = query
        self.driver.get(url="https://www.wikipedia.org")
        search_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "searchInput")))
        search_input.send_keys(self.query)
        search_input.send_keys(Keys.RETURN)

    def search_and_play_video(self, query):
        try:
            self.driver.get("https://www.youtube.com")
            search_input = self.wait.until(EC.presence_of_element_located((By.NAME, "search_query")))
            search_input.send_keys(query)
            search_input.send_keys(Keys.RETURN)
            self.wait.until(EC.presence_of_element_located((By.ID, "video-title")))
            video_link = self.wait.until(EC.element_to_be_clickable((By.ID, "video-title")))
            video_link.click()
        except TimeoutException:
            print("Timeout occurred while trying to play the video.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def open_website(self, url):
        webbrowser.open(url)


    def google_search(self, query):
        try:
            if not self.is_internet_available():
                print("No internet connection. Please check your network settings.")
                return

            search_results = search(query, num_results=1)
            for result in search_results:
                speak(f"Here is what I found on Google:")
                print(result)
        except requests.RequestException as e:
            print(f"An error occurred during the Google search: {e}")
            print("Please try again later.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please try again later.")


    def is_internet_available(self):
        try:
            requests.get("https://www.google.com", timeout=5)
            return True
        except requests.RequestException:
            return False
        
    def open_whatsapp(self):
        webbrowser.open("https://web.whatsapp.com")


    def detect_faces(self, image_path):
        try:
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            return faces
        except Exception as e:
            print(f"An error occurred during face detection: {e}")
            return []

class translations:
    def _init_(self):
        self.translator = Translator()

    def translate_text(self, text, target_language):
        try:
            source_language = detect(text)
            translation = self.translator.translate(text, src=source_language, dest=target_language)
            return translation.text
        except Exception as e:
            print(f"An error occurred during translation: {e}")
            return None
        
class wp:
    def open_whatsapp(self):
        self.driver.get('https://web.whatsapp.com/')
        input("Press Enter after scanning QR code and logging in...")

    def send_whatsapp_message(self, contact_name, message):
        search_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.send_keys(contact_name)
        time.sleep(2)  # Wait for contacts to load
        search_box.send_keys(Keys.RETURN)
        message_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="1"]')
        message_box.send_keys(message)
        message_box.send_keys(Keys.RETURN)

    def read_last_message(self, contact_name):
        search_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.send_keys(contact_name)
        time.sleep(2)  # Wait for contacts to load
        search_box.send_keys(Keys.RETURN)
        time.sleep(1)  # Wait for messages to load
        messages = self.driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]')
        last_message = messages[-1].text if messages else None
        return last_message

class OpenStreetMap:
    def search_location(self, location):
        try:
            map_url = f"https://www.openstreetmap.org/search?query={location}"
            webbrowser.open(map_url)
            print(f"Opening OpenStreetMap for {location}")
            while True:
                time.sleep(1)
                if not any("chromedriver" in proc.name() for proc in psutil.process_iter()):
                    print("Web browser closed.")
                    break
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

class news:
    def _init_(self):
        self.api_key = '688b468522764a12813672d6582e6f35'

    def get_latest_news(self):
        try:
            url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={self.api_key}'
            response = requests.get(url)
            data = response.json()
            if data['status'] == 'ok':
                articles = data['articles'][:5]
                latest_news = "Here are the latest headlines:\n"
                for article in articles:
                    title = article['title']
                    source = article['source']['name']
                    latest_news += f"- {title}, from ({source})\n"
                return latest_news
            else:
                return "Sorry, I couldn't fetch the latest news at the moment."
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Sorry, I couldn't fetch the latest news at the moment."

class joke:
    def tell_joke(self):
        try:
            url = 'https://official-joke-api.appspot.com/random_joke'
            response = requests.get(url)
            joke_data = response.json()
            joke = f"{joke_data['setup']} {joke_data['punchline']}"
            return joke
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Sorry, I couldn't fetch a joke at the moment."
        
class calculate:
    def calculate_expression(self, expression):
        try:
            expression = expression.replace("times", "*")
            expression = expression.replace("x", "*")
            result = eval(expression)
            return f"The result of {expression} is {result}"
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Sorry, I couldn't calculate the expression"


import pyttsx3 as p
import speech_recognition as sr

engine=p.init()
rate=engine.getProperty('rate')
engine.setProperty('rate',180)
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"An error occurred while speaking: {e}")

r=sr.Recognizer()

def get_user_location():
    try:
        g = geocoder.ip('me')
        if g:
            return g.city, g.country
        else:
            return None, None
    except Exception as e:
        print(f"An error occurred while fetching location: {e}")
        return None, None

def get_weather(city):
    try:
        owm = pyowm.OWM('908b041480b3c32e74fe27fea221157c')
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(city)
        weather = observation.weather
        return weather
    except TimeoutError:
        print("Timeout error occurred while fetching weather data.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    return current_time

city, country = get_user_location()
weather = get_weather(city)
current_time = get_current_time()

sys.stdout.buffer.write("Hello! Currently, it's {} at your location. The temperature is {:.2f}°C.\n".format(weather.status, weather.temperature('celsius')['temp']).encode('utf-8'))
sys.stdout.buffer.write("The current time is {}.\n".format(current_time).encode('utf-8'))

speak("Hello! Currently, it's {} at your location. The temperature is {:.2f}°C.".format(weather.status, weather.temperature('celsius')['temp']))
speak("The current time is {}.".format(current_time))

print("Hello Sir, I am your voice assistant. How are you?")
speak("Hello Sir, I am your voice assistant. How are you?")

while True:
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, 1.2)
        print("listening...")
        try:
            audio = r.listen(source, timeout=5)
            text2 = r.recognize_google(audio)
            print(text2)
        except sr.UnknownValueError:
            speak("Sorry could not understand your command...can you please repeat?")
            print("Sorry could not understand your command...can you please repeat?")
            continue
        except sr.RequestError:
            speak("Sorry, unable to access the Google API. Please check your internet connection.")
            print("Sorry, unable to access the Google API. Please check your internet connection.")
            continue

    if "no nothing else needed" in text2:
            print("Goodbye Sir and have a great day!")
            speak("Goodbye Sir and have a great day!")
            break

    if "how are you" in text2 or ("what" in text2 and "about" in text2 and "you" in text2):
        speak("I am also having a good day sir")
        print("I am also having a good day sir")
    speak("What can I do for you?")
    print("What can I do for you?")

    with sr.Microphone() as source:
        r.energy_threshold=10000
        r.adjust_for_ambient_noise(source,1.2)
        print("listening...")
        try:
            audio = r.listen(source, timeout=5)
            text2 = r.recognize_google(audio)
            print(text2)
        except sr.UnknownValueError:
            speak("Sorry could not understand your command...can you please repeat?")
            print("Sorry could not understand your command...can you please repeat?")
            continue
        except sr.RequestError:
            speak("Sorry, unable to access the Google API. Please check your internet connection.")
            print("Sorry, unable to access the Google API. Please check your internet connection.")
            continue

    if "sing me a song" in text2:
        speak("I am not that good in singing but I will try...")
        print("I am not that good in singing but I will try...")

        speak("""Jingle bells, jingle bells
              jingle all the way
              Santa Claus is coming around
              riding on his slay hey""")
        print("""Jingle bells, jingle bells
              jingle all the way
              Santa Claus is coming around
              riding on his slay hey""")
        
        speak("Did you like it?")
        print("Did you like it?")
        with sr.Microphone() as source:
            r.energy_threshold=10000
            r.adjust_for_ambient_noise(source,1.2)
            print("listening...")
            try:
                audio = r.listen(source, timeout=5)
                comp = r.recognize_google(audio)
                print(comp)
            except sr.UnknownValueError:
                speak("Sorry could not understand your command...can you please repeat?")
                print("Sorry could not understand your command...can you please repeat?")
                continue
            except sr.RequestError:
                speak("Sorry, unable to access the Google API. Please check your internet connection.")
                print("Sorry, unable to access the Google API. Please check your internet connection.")
                continue
        if "very good" in comp or "Awesome" in comp or "Fine" in comp:
            speak("Aww...Thank you!")
            print("Aww...Thank you!")
        elif "not good" in comp or "Meh" in comp or "You can do better" in comp:
            speak("Sorry...I will do better next time!")
            print("Sorry...I will do better next time!")


    if "information" in text2:
        speak("Which topic do you need information on?")
        print("Which topic do you need information on?")

        with sr.Microphone() as source:
            r.energy_threshold=10000
            r.adjust_for_ambient_noise(source,1.2)
            print("listening...")
            try:
                audio = r.listen(source, timeout=5)
                info = r.recognize_google(audio)
                print(info)
            except sr.UnknownValueError:
                speak("Sorry could not understand your command...can you please repeat?")
                print("Sorry could not understand your command...can you please repeat?")
                continue
            except sr.RequestError:
                speak("Sorry, unable to access the Google API. Please check your internet connection.")
                print("Sorry, unable to access the Google API. Please check your internet connection.")
                continue
        print("searching {} in wikipedia".format(info))
        speak("searching {} in wikipedia".format(info))
        assist = Infow()
        assist.get_info(info)
        while assist.driver.current_url:
            try:
                pass
            except WebDriverException as e:
                print(f"WebDriverException occurred: {e}")
                break


    if "question" in text2:
        speak("What question do you want to ask?")

        with sr.Microphone() as source:
            r.energy_threshold=10000
            r.adjust_for_ambient_noise(source,1.2)
            print("listening...")
            try:
                audio = r.listen(source, timeout=5)
                qus = r.recognize_google(audio)
                print(qus)
            except sr.UnknownValueError:
                speak("Sorry could not understand your command...can you please repeat?")
                print("Sorry could not understand your command...can you please repeat?")
                continue
            except sr.RequestError:
                speak("Sorry, unable to access the Google API. Please check your internet connection.")
                print("Sorry, unable to access the Google API. Please check your internet connection.")
                continue
        
        print("Searching in google...")
        speak("Searching in google...")
        assist=Infow()
        assist.google_search(qus)

    if "open WhatsApp" in text2:
        assist = Infow()
        assist.open_whatsapp()
        print("Opening WhatsApp...")
        speak("Opening WhatsApp...")
        while assist.driver.current_url:
            try:
                pass
            except WebDriverException as e:
                print(f"WebDriverException occurred: {e}")
                break

    
    elif "translate" in text2:
        print("What do you want to translate?")
        speak("What do you want to translate?")
        with sr.Microphone() as source:
            r.energy_threshold=10000
            r.adjust_for_ambient_noise(source,1.2)
            print("listening...")
            try:
                audio = r.listen(source, timeout=5)
                txt = r.recognize_google(audio)
                print(txt)
            except sr.UnknownValueError:
                speak("Sorry could not understand your command...can you please repeat?")
                print("Sorry could not understand your command...can you please repeat?")
                continue
            except sr.RequestError:
                speak("Sorry, unable to access the Google API. Please check your internet connection.")
                print("Sorry, unable to access the Google API. Please check your internet connection.")
                continue

        print("What do you want to translate it to?")
        speak("What do you want to translate it to?")
        with sr.Microphone() as source:
            r.energy_threshold=10000
            r.adjust_for_ambient_noise(source,1.2)
            print("listening...")
            try:
                audio = r.listen(source, timeout=5)
                lang = r.recognize_google(audio)
                print(lang)
            except sr.UnknownValueError:
                speak("Sorry could not understand your command...can you please repeat?")
                print("Sorry could not understand your command...can you please repeat?")
                continue
            except sr.RequestError:
                speak("Sorry, unable to access the Google API. Please check your internet connection.")
                print("Sorry, unable to access the Google API. Please check your internet connection.")
                continue
        
        print("Translating...")
        speak("Translating...")
        assist = translations()
        translation = assist.translate_text(txt, lang)
        sys.stdout.buffer.write(translation.encode('utf-8'))
        speak(translation)
    
    elif "detect faces" in text2:
        assist = Infow()
        faces = assist.detect_faces("image.jpg")
        print(faces)

    if "search YouTube" in text2:
        print("Please specify the video you want to search for.")
        speak("Please specify the video you want to search for.")
        with sr.Microphone() as source:
            r.energy_threshold=10000
            r.adjust_for_ambient_noise(source,1.2)
            print("listening...")
            try:
                audio = r.listen(source, timeout=5)
                query = r.recognize_google(audio)
                print(query)
            except sr.UnknownValueError:
                speak("Sorry could not understand your command...can you please repeat?")
                print("Sorry could not understand your command...can you please repeat?")
                continue
            except sr.RequestError:
                speak("Sorry, unable to access the Google API. Please check your internet connection.")
                print("Sorry, unable to access the Google API. Please check your internet connection.")
                continue
        
        print("Searching for {} on YouTube".format(query))
        speak("Searching for {} on YouTube".format(query))
        assist = Infow()
        assist.search_and_play_video(query)
        while assist.driver.current_url:
            try:
                pass
            except WebDriverException as e:
                print(f"WebDriverException occurred: {e}")
                break


    if "latest news" in text2:
        print("Searching for the latest news...")
        speak("Searching for the latest news...")
        assist=news()
        latest_news=assist.get_latest_news()
        print(latest_news)
        speak(latest_news)

    if "fact" in text2 or "facts" in text2:
        x=randfacts.get_fact()
        print(x)
        speak("Did you know that, "+x)

    if "joke" in text2:
        print("Sure Sir, get ready for some chuckles")
        speak("Sure Sir, get ready for some chuckles")
        j=joke()
        joke_data=j.tell_joke()
        print(joke_data)
        speak(joke_data)

    if "calculate" in text2:
        print("Sure, what expression do you want to calculate?")
        speak("Sure, what expression do you want to calculate?")
        with sr.Microphone() as source:
            r.energy_threshold=10000
            r.adjust_for_ambient_noise(source,1.2)
            print("listening...")
            try:
                audio = r.listen(source, timeout=5)
                exp = r.recognize_google(audio)
                print(exp)
            except sr.UnknownValueError:
                speak("Sorry could not understand your command...can you please repeat?")
                print("Sorry could not understand your command...can you please repeat?")
                continue
            except sr.RequestError:
                speak("Sorry, unable to access the Google API. Please check your internet connection.")
                print("Sorry, unable to access the Google API. Please check your internet connection.")
                continue

        print("Calculating {}".format(exp))
        speak("Calculating {}".format(exp))
        assist = calculate()
        res=assist.calculate_expression(exp)
        print(res)
        speak(res)

    if "location" in text2:
        print("Sure, what location do you want?")
        speak("Sure, what location do you want?")
        with sr.Microphone() as source:
            r.energy_threshold=10000
            r.adjust_for_ambient_noise(source,1.2)
            print("listening...")
            try:
                audio = r.listen(source, timeout=5)
                loc = r.recognize_google(audio)
                print(loc)
            except sr.UnknownValueError:
                speak("Sorry could not understand your command...can you please repeat?")
                print("Sorry could not understand your command...can you please repeat?")
                continue
            except sr.RequestError:
                speak("Sorry, unable to access the Google API. Please check your internet connection.")
                print("Sorry, unable to access the Google API. Please check your internet connection.")
                continue

        print("Finding location of {}".format(loc))
        speak("Finding location of {}".format(loc))
        assist = OpenStreetMap()
        assist.search_location(loc)

    print("Is there anything else I can assist you with?")
    speak("Is there anything else I can assist you with?")