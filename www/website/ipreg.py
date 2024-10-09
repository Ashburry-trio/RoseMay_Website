import requests
from configparser import ConfigParser
from os import path
from os.path import expanduser
from warnings import warn
# Reading the API key from the config file
config = ConfigParser()
config_file = expanduser(path.join('~','www','app','ipreg.ini'))
config.read(config_file)
api_key: str


def reset_cycle(myconfig = None):
    global config
    if myconfig:
        config.clear()
        for section in myconfig:
            config[section] = {}
            for option in myconfig[section]:
                config[section][option] = myconfig[section][option]
        del myconfig
    if not config.has_section('ipreg'):
        config['ipreg'] = {}
    try:
        api_key = config['ipreg']['api_key_1']
        if api_key == 'Get an account at www.ipregistry.co':
            raise KeyError
    except KeyError:
        config['ipreg']['api_key_1'] = 'Get an account at www.ipregistry.co'
        try:
            api_key = config['ipreg']['api_key_2']
            if api_key == 'Get an account at www.ipregistry.co':
                raise KeyError
        except KeyError:
            config['ipreg']['api_key_2'] = 'Get an account at www.ipregistry.co'
            try:
                api_key = config['ipreg']['api_key_3']
                if api_key == 'Get an account at www.ipregistry.co':
                    raise KeyError
            except KeyError:
                config['ipreg']['api_key_3'] = 'Get an account at www.ipregistry.co'
                api_key = None

    if not config.has_section('cycle'):
        config['cycle'] = {}
        config['cycle']['api_key_1'] = '0'
        config['cycle']['api_key_2'] = '0'
        config['cycle']['api_key_3'] = '0'
    with open(config_file, 'w') as fp:
        config.write(fp, space_around_delimiters = True)


def get_ip_info(ip_address: str) -> str | bool | None:
    global config
    global config_file

    config.read(config_file)
    first_key: int | str = config['cycle']['api_key_1']
    new_key: str = 'api_key_1'

    if first_key:
        if config['cycle']['api_key_2'] < first_key:
            new_key = 'api_key_2'
        else:
            if config['cycle']['api_key_3'] < first_key:
                new_key = 'api_key_3'
            else:
                new_key = 'api_key_1'

    if not config['ipreg'][new_key] or ' ' in config['ipreg'][new_key]:
        if new_key == 'api_key_1':
            new_key = 'api_key_2'
        if new_key == 'api_key_2':
            if not config['ipreg'][new_key] or ' ' in config['ipreg'][new_key]:
                new_key = 'api_key_3'
        if new_key == 'api_key_3':
            if not config['ipreg'][new_key] or ' ' in config['ipreg'][new_key]:
                new_key = 'api_key_1'

    if not config['ipreg'][new_key] or ' ' in config['ipreg'][new_key]:
        warn('No API Keys Available from https://www.ipregistry.co' \
        + f' Get from URL and put your key in {config_file}',UserWarning)
        return None

    api_key = config['ipreg'][new_key]
    url = f'https://api.ipregistry.co/{ip_address}?key={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException:
        return None

reset_cycle()
