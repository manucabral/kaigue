import re
import os

class Web:
    """
        Kaigue's Web module for handling web requests and searches.

        parameters:
            lang: The language to set. (default: 'es')
    """

    SEARCH_ENGINE = {
        'google': 'https://google.com/search?q={text}',
        'youtube': 'https://youtube.com/results?search_query={text}',
        'facebook': 'https://facebook.com/search/top/?q={text}',
        'instagram': 'https://instagram.com/explore/tags/{text}',
        'twitter': 'https://twitter.com/search?q={text}',
        'mercadolibre': 'https://listado.mercadolibre.com.ar/{text}',
    }

    def __init__(self, lang: str) -> None:
        self.lang = lang

    def open(self, url: str) -> None:
        """
            Opens a website.

            parameters:
                url: The website url.
            
            returns:
                None
        """
        if not url:
            return
        os.system(f'start {url}')
    
    def get_search_engine(self, text: str) -> str:
        """
            Gets the search engine.

            parameters:
                text: The text to get the search engine.

            returns:
                The search engine.
        """
        if re.search(r'google|google.com', text):
            return 'google'
        elif re.search(r'youtube|youtube.com', text):
            return 'youtube'
        elif re.search(r'facebook|facebook.com', text):
            return 'facebook'
        elif re.search(r'instagram|instagram.com', text):
            return 'instagram'
        elif re.search(r'twitter|twitter.com', text):
            return 'twitter'
        elif re.search(r'mercadolibre|mercadolibre.com', text):
            return 'mercadolibre'
        else:
            return None

    def get_url(self, text: str) -> str:
        """
            Gets the website url.

            parameters:
                text: The text to get the url.

            returns:
                The website url.
        """
        if re.search(r'google|google.com', text):
            return 'www.google.com'
        elif re.search(r'youtube|youtube.com', text):
            return 'www.youtube.com'
        elif re.search(r'facebook|facebook.com', text):
            return 'www.facebook.com'
        elif re.search(r'instagram|instagram.com', text):
            return 'www.instagram.com'
        elif re.search(r'twitter|twitter.com', text):
            return 'www.twitter.com'
        elif re.search(r'github|github.com', text):
            return 'www.github.com'
        else:
            return None
    
        
    
    def search(self, text: str, engine: str) -> None:
        """
            Searches in the web.

            parameters:
                text: The text to search.
                engine: The search engine.

            returns:
                None
        """
        if not text:
            return
        if not engine:
            engine = 'google'
        url = self.SEARCH_ENGINE[engine].format(text=text)
        self.open(url)