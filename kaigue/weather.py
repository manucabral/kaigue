import sys
import json

try:
    import requests
except ImportError:
    print('Please install requests before running this program.')
    sys.exit(1)

class Weather:
    """
        Kaigue's Weather module for handling weather requests.

        parameters:
            lang: The language to set. (default: 'es')
    """

    def __init__(self, lang: str):
        self.lang = lang.split('-')[0]
    
    @property
    def location(self) -> str:
        """
            Gets the user location.
            
            returns:
                The user location.
        """
        try:
            return requests.get('https://ipinfo.io/loc').text
        except requests.exceptions.RequestException as e:
            raise SystemExit(e) from e
    
    @property
    def city(self) -> str:
        """
            Gets the user city.

            returns:
                The user city.
        """
        try:
            return requests.get('https://ipinfo.io/city').text
        except requests.exceptions.RequestException as e:
            raise SystemExit(e) from e
    
    @property
    def data(self) -> dict:
        """
            Gets the weather data.

            returns:
                A dict with the weather data.
        """
        try:
            return json.loads(requests.get(f'https://wttr.in/?lang={self.lang}&format=j1').text)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e) from e

    @property
    def current_condition(self) -> dict:
        """
            Gets the current condition.

            returns:
                The current condition.
        """
        return self.data['current_condition'][0]

    @property
    def now(self) -> tuple:
        """
            Gets the current temperature and description.

            returns:
                The current temperature and description.
        """
        field = 'lang_es' if self.lang == 'es' else 'weatherDesc'
        desc = self.current_condition.get(field)[0].get('value')
        return self.current_condition['temp_C'], desc
