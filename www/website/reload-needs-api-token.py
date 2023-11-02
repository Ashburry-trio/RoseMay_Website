# Rename this file to reload.py
# And add the API Token below from the Accounts page on PythonAnywhere.com. Use www.bing.com/chat if you need help finding the API tokens
# or email liveuser@pythonanwhere.com and ask for the directions to the API tokens.

import requests

username = "ashburry"
api_token = "API Token"
domain_name = "www.mslscript.com"
response = ['']
def reload():
    del response[0]
    response.append(requests.post(
        f'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain_name}/reload/',
        headers={'Authorization': f'Token {api_token}'}
    ))
    if response[0].status_code == 200:
        print('Web app reloaded successfully.')
    else:
        print(f'Unexpected status code {response[0].status_code}: {response[0].content}')