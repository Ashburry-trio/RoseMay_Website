import requests
from configparser import ConfigParser
from os import path
from os.path import expanduser

# Reading the API key from the config file
config = ConfigParser()
config.read(expanduser(path.join('~','www','app','ipreg.ini')))
api_key = config['ipreg']['api_key']

def get_ip_info(ip_address, api_key = api_key) -> str | bool:
    url = f'https://api.ipregistry.co/{ip_address}?key={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return None

