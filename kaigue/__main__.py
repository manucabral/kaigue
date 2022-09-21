import os
import re
import sys
import datetime

from kaigue.currency import Currency
from kaigue.weather import Weather
from kaigue.web import Web

try:
    import pyttsx3
    import speech_recognition
except ImportError as e:
    print(f'Please install {e.name} before running this program.')
    sys.exit(1)

class Kaigue:
    """
        Kaigue's Assistant core

        Optional parameters:
            volume (str): The volume to set.
            rate (str): The rate to set.
            voice_id (str): The voice id to set.
            lang (str): The language to set.
            username (str): The user name to set.
            verbose (bool): If the assistant should log to the console.
    """

    # no used yet
    path = os.path.dirname(os.path.abspath(__file__))[0:-8]
    running = False

    def __init__(self, **kwargs):
        self.microphone = speech_recognition.Microphone()
        self.recognizer = speech_recognition.Recognizer()
        self.engine = pyttsx3.init()
        self.lang = kwargs.get('lang', 'es-ES')
        self.rate = kwargs.get('rate', 150)
        self.volume = kwargs.get('volume', 0.9)
        self.voice_id = kwargs.get('voice_id', 0)
        self.username = kwargs.get('username', 'Unknown')
        self.verbose = kwargs.get('verbose', False)
        self.weather = Weather(self.lang)
        self.web = Web(self.lang)
        self.currency = Currency()

    def log(self, text: str) -> None:
        """
            Logs a text to the console.

            arameters:
                text (str): The text to log.
            returns:
                None
        """
        print(f'[{self.hour}] {text}')

    def get_engine_propertie(self, propertie: str) -> str:
        """
            Gets a pyttsx3 engine propertie.

            Parameters:
                propertie (str): The propertie to get.
            returns:
                The value of the propertie.
        """
        return self.engine.getProperty(propertie)

    def set_engine_propertie(self, propertie: str, value: str) -> None:
        """
            Sets a pyttsx3 engine propertie.

            Parameters:
                propertie (str): The propertie to set.
                value (str): The value to set.
            returns:
                None
        """
        if propertie == 'voice':
            voices = self.engine.getProperty('voices')
            value = voices[value].id
        self.engine.setProperty(propertie, value)
    def say(self, text: str) -> None:
        """
            Makes the assistant say something.

            Parameters:
                text (str): The text to say.
            returns:
                None
        """
        self.engine.say(text)
        self.engine.runAndWait()

    @property
    def has_internet(self) -> bool:
        """
            Checks if the user has internet connection.

            returns:
                True if the user has internet connection, False otherwise.
        """
        return os.system('ping -n 1 www.google.com > null') == 0
        
    @property
    def hour(self) -> str:
        """
            Gets the current hour.

            returns:
                The current hour.
        """
        return datetime.datetime.now().strftime('%H:%M:%S')
    
    @property
    def date(self) -> str:
        """
            Gets the current date.

            returns:
                The current date.
        """
        return datetime.datetime.now().strftime('%d/%m/%Y')


    def greet(self, from_user: bool = False) -> None:
        """
            Greets the user.
        """
        hour = int(self.hour.split(':')[0])
        text = ''
        if hour >= 6 and hour < 12:
            text = 'Buenos días'
        elif hour >= 12 and hour < 20:
            text = 'Buenas tardes'
        elif hour >= 20 or hour < 6:
            text = 'Buenas noches'
        self.say(f'¡Hola {self.username}!' if from_user else f'{text} {self.username}')

    def listen(self) -> speech_recognition.AudioData:
        """
            Listen from the user microphone.
            
            returns:
                The audio data.
        """
        with self.microphone as source:
            if self.verbose:
                self.log('Listening ..')
            #self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        return audio
    
    def recognize(self, audio: speech_recognition.AudioData) -> str:
        """
            Recognizes the audio data.

            Parameters:
                audio (speech_recognition.AudioData): The audio data to recognize.
            returns:
                The recognized text.
        """
        try:
            return self.recognizer.recognize_google(audio, language=self.lang)
        except speech_recognition.UnknownValueError:
            return ''
        
        
    def wait_for_command(self) -> str:
        """
            Waits for the user to say a command.

            returns:
                The command said by the user.
        """
        audio = self.listen()
        text = self.recognize(audio)
        return text.lower()

    def handle_command(self, command: str) -> None:
        """
            Handles the command said by the user.

            Parameters:
                command (str): The command to handle.
            returns:
                None
        """

        if re.search(r'adiós|chau|chao|nos vemos|desconéctate', command):
            self.stop()
        
        elif re.search(r'hola|buenos días', command):
            self.greet(from_user=True)
        
        elif re.search(r'hora|qué hora es', command):
            self.say(f'Son las {self.hour}')
        
        elif re.search(r'temperatura|qué temperatura hace|cómo está el tiempo|tiempo', command):
            self.temperature()
        
        elif re.search(r'ir a|navegar|ir a la página|ir a la web|ir a la página web', command):
            self.open_website()
        
        elif re.search(r'buscar|buscar en internet|búscame algo|precio|buscar precio', command):
            self.search()
    
        elif re.search(r'dolarhoy|dolar|cuánto está el dolar|dólar', command):
            self.currency_price()

        elif re.search(r'muchas gracias|gracias', command):
            self.say('De nada')

        else:
            self.say('No te entendí')
    
    def temperature(self) -> None:
        """
            Gets the temperature.
        """
        if not self.has_internet:
            self.say('No tienes conexión a internet')
            return
        
        temp, desc = self.weather.now
        self.say(f'Hace {temp} grados y está {desc}')

    def open_website(self) -> None:
        """
            Opens a website in the default browser.
        """
        if not self.has_internet:
            self.say('No tienes conexión a internet')
            return
        
        self.say('¿Qué página quieres abrir?')
        command = self.wait_for_command()
        if not command:
            self.say('No te entendí')
            return
        
        url = self.web.get_url(command)
        self.say(f'Abriendo {url.split(".")[1]}')
        self.web.open(url)

    def search(self) -> None:
        """
            Searches a text (for now only supports google).
        """
        if not self.has_internet:
            self.say('No tienes conexión a internet')
            return

        self.say('¿En dónde quieres buscar?')
        command = self.wait_for_command()
        engine =  self.web.get_search_engine(command)
        if not engine:
            self.say('No te entendí o no sé buscar en ese sitio. Perdón.')
            return
        
        self.say('¿Qué quieres buscar?')
        text = self.wait_for_command()
        if not text:
            self.say('No te entendí')
            return
        
        self.say(f'Buscando {text} en {engine}')
        self.web.search(text, engine)

    def currency_price(self) -> None:
        """
            Gets the price of a currency.
        """
        if not self.has_internet:
            self.say('No tienes conexión a internet')
            return
        
        self.say('Decime cuál dólar querés saber')
        text = self.wait_for_command()
        if not text:
            self.say('No te entendí')
            return
        data = self.currency.price(text)
        if not data:
            self.say('No está cotizando o no conozco ese tipo de dólar')
            return
        name, buy, sell = data
        self.say(f'El {name} está a {buy} para comprar y {sell} para vender')

    def setting_up(self) -> None:
        """
            Sets up the assistant.
        """
        if self.verbose:
            self.log('Setting up the assistant')
        self.set_engine_propertie('volume', self.volume)
        self.set_engine_propertie('rate', self.rate)
        self.set_engine_propertie('voice', self.voice_id)
        
    def stop(self):
        """
            Stops the assistant.
        """
        self.say('Desconectandome, hasta luego.')
        self.running = False

    def run(self):
        """
            Runs the assistant until it's stopped.
        """
        self.setting_up()
        self.greet()
        self.running = True

        if not self.has_internet:
            self.say('No tienes conexión a internet. No podré hacer muchas cosas.')
        try:
            while self.running:
                command = self.wait_for_command()
                if command:
                    if self.verbose:
                        self.log(f'Recognized: {command}')
                    self.handle_command(command)
        except KeyboardInterrupt:
            self.stop() 
        