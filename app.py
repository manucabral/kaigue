"""
    Kaigue - A Virtual Assistant for Windows
    Application entry point.
"""

import yaml
from kaigue import Kaigue

def get_user_config() -> dict:
    """
        Gets the user config.

        returns:
            A dict with the user config.
    """
    try:
        with open('config.yml', 'r', encoding='utf-8') as file:
            return yaml.load(file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        return {}

if __name__ == '__main__':
    config = get_user_config()
    kai = Kaigue(**config)
    kai.run()
