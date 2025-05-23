import requests
import geocoder
import pyowm
from datetime import datetime
import webbrowser
import pyttsx3 as p
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import wikipedia

class Assistant:
    def __init__(self):
        self.engine = p.init()
        self.engine.setProperty('rate', 180)
        self.engine.setProperty('voice', self.engine.getProperty('voices')[1].id)
        self.recognizer = sr.Recognizer()
        self.wiki_summary_length = 2  # Number of sentences to fetch from Wikipedia summary

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def get_user_location(self):
        try:
            g = geocoder.ip('me')
            if g:
                return g.city, g.country
        except Exception as e:
            print(f"An error occurred while fetching location: {e}")
        return None, None

    def get_weather(self, city):
        owm = pyowm.OWM('908b041480b3c32e74fe27fea221157c')
        mgr = owm.weather_manager()
        try:
            observation = mgr.weather_at_place(city)
            weather = observation.weather
            return weather
        except Exception as e:
            print(f"An error occurred while fetching weather: {e}")
            return None

    def get_current_time(self):
        now = datetime.now()
        return now.strftime("%I:%M %p")

    def open_website(self, url):
        webbrowser.open(url)

    def search_on_google(self, query):
        search_url = "https://www.google.com/search?q=" + query
        webbrowser.open(search_url)

    def search_on_youtube(self, query):
        search_url = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(search_url)

    def fetch_latest_news(self, query):
        try:
            api_key = '688b468522764a12813672d6582e6f35'
            url = f'https://newsapi.org/v2/everything?q={query}&apiKey={api_key}'
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
                return "Sorry, couldn't fetch the latest news."
        except Exception as e:
            print(f"An error occurred while fetching news: {e}")
            return "Sorry, couldn't fetch the latest news."

    def handle_query(self, text):
        if "no nothing else needed" in text:
            print("Goodbye! Have a great day!")
            self.speak("Goodbye! Have a great day!")
            return True
        elif any(keyword in text for keyword in ["what about you", "how are you"]):
            print("I am also having a good day, sir.")
            self.speak("I am also having a good day, sir.")
        elif "calculator" in text:
            self.speak("Sure, please provide the expression you want to calculate.")
            print("Sure, please provide the expression you want to calculate.")
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = self.recognizer.listen(source)
                try:
                    expression = self.recognizer.recognize_google(audio)
                    print(expression)
                    result = eval(expression)
                    print(result)
                    self.speak("The result is {}".format(result))
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except Exception as e:
                    print(f"Error in calculation: {e}")
                    self.speak("Sorry, I couldn't calculate that.")
        elif "news" in text:
            query = text.replace("news", "").strip()
            self.speak(f"Fetching latest news on {query}")
            news = self.fetch_latest_news(query)
            print(news)
            self.speak(news)
        elif "open YouTube" in text:
            self.speak("Opening YouTube")
            self.open_website("https://www.youtube.com")
        elif "play the video" in text:
            query = text.replace("play the video", "").strip()
            self.speak(f"Searching for {query} on YouTube")
            self.search_on_youtube(query)
        elif "open" in text:
            query = text.replace("open", "").strip()
            self.speak(f"Opening {query}")
            self.open_website(query)
        else:
            print("Searching Wikipedia...")
            try:
                search_result = wikipedia.summary(text, sentences=self.wiki_summary_length)
                print(search_result)
                self.speak(search_result)
            except wikipedia.DisambiguationError as e:
                print(f"Ambiguous term: {e}")
                self.speak("Sorry, I found multiple results. Please be more specific.")
            except wikipedia.PageError as e:
                print(f"Page not found: {e}")
                self.speak("Sorry, I couldn't find any information on that topic.")
            except Exception as e:
                print(f"Error: {e}")
                self.speak("Sorry, I couldn't fetch information on that topic.")

    def main_loop(self):
        city, _ = self.get_user_location()
        weather = self.get_weather(city)
        current_time = self.get_current_time()

        if weather:
            print("Hello! Currently, it's " + weather.status + " at your location. The temperature is {:.2f}°C.".format(weather.temperature('celsius')['temp']))
            print("The current time is {}.".format(current_time))

            self.speak("Hello! Currently, it's " + weather.status + " at your location. The temperature is {:.2f}°C.".format(weather.temperature('celsius')['temp']))
            self.speak("The current time is {}.".format(current_time))
        else:
            print("Hello! I couldn't fetch the weather information at the moment.")
            print("The current time is {}.".format(current_time))
            self.speak("Hello! I couldn't fetch the weather information at the moment.")
            self.speak("The current time is {}.".format(current_time))

        print("Hello , I am LIONEL. How can I assist you today?")
        self.speak("Hello , I am LIONEL. How can I assist you today?")

        while True:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = self.recognizer.listen(source)
                try:
                    text = self.recognizer.recognize_google(audio)
                    print(text)
                    if self.handle_query(text):
                        break
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print("Error fetching results from Google Speech Recognition service; {}".format(e))

assistant = Assistant()
assistant.main_loop()
