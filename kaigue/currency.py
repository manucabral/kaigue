import re
import sys

try:
    import requests
except ImportError:
    print('Please install requests before running this program.')
    sys.exit(1)

class Currency:
    """
        Kaigue's Currency module for handling currency flactuations.

        NOTE: This module only works with the Argentine Peso (ARS).
        TODO: Add support for other currencies.
    """

    CURRENCY = {
        'Dolar Oficial': 0,
        'Dolar Blue': 1,
        'Dolar Soja': 2,
        'Dolar Contado con Liqui': 3,
        'Dolar Bolsa': 4,
    }

    ENDPOINT = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'

    @property
    def data(self) -> dict:
        """
            Gets the current currency data.
            
            returns:
                A dict with the currency data.
        """
        try:
            return requests.get(self.ENDPOINT).json()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)


    def price(self, currency: str) -> tuple:
        """
            Gets the price of a currency.

            params:
                currency: The currency to get the price from.
            
            returns:
                A tuple with the currency price (buy, sell).
        """
        currency_id = self.get_currency(currency)
        if currency_id is None:
            return None
        data = self.data[currency_id]['casa']
        name = data['nombre']
        buy, sell = data['compra'].replace(',', '.'), data['venta'].replace(',', '.')
        if 'No Cotiza' in buy:
            return None
        return name, float(buy), float(sell)
    
    def get_currency(self, text: str) -> float:
        """
            Gets the currency id from a string.

            returns:
                The requested currency id.
        """
        if re.search(r'dolar oficial|oficial|dólar oficial', text):
            return 0
        elif re.search(r'dolar blue|blue|dólar blue', text):
            return 1
        elif re.search(r'dolar soja|soja|dólar soja', text):
            return 2
        elif re.search(r'dolar contado con liqui|contado con liqui|dólar contado con liqui', text):
            return 3
        elif re.search(r'dolar bolsa|bolsa|dólar bolsa', text):
            return 4
        else:
            return None
        