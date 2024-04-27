# Rename this file to reload.py
# And add the API Token below from the Accounts page on PythonAnywhere.com.

import requests
from os.path import isfile, isdir, expanduser, join
from os import mkdir, rename, listdir, remove
import requests

upath = '/home/Ashburry/www/website/templates/users/'

def user_path(dir) -> None | str:
    while '\\' in dir:
        dir = dir.replace('\\','')
    while '/' in dir:
        dir = dir.replace('/','')
    return expanduser(join('~','www','website','templates','users',dir))
    return None

def make_user_dir(dir: str) -> None:
    dir = dir.lower() # dir = user.lower()
    upath = user_path(dir)
    if isdir(upath):
        return None
    try:
        mkdir(upath)
    except OSError:
        pass
    return None

def erase_user_page(user: str) -> None:
    user = user.lower()
    upath = join(user_path(user),'index.html')
    try:
        remove(upath)
    except OSError:
        pass
    return None

def api_upload_default_files(user: str) -> None:
    user = user.lower()
    path = '/home/Ashburry/www/website/templates/default_user'
    files = listdir(path)

    for page in files:
        upload_page(user, '/home/Ashburry/www/website/templates/users/'+user+'/'+page)
    return None

# new_index = join(user_path(user), 'new-index.html')
def upload_page(user: str, page: str) -> None:
    global upath
    user = user.lower()
    with open('{upath}{username}/index.html'.format(username=user,upath=upath),'a') as fp:
        fp.write("<p>Creating index.html: "+page+"</p>")

    fp = open(page, 'rb')
    url = 'https://www.pythonanywhere.com/api/v0/user/Ashburry/files{upath}{username}/index.html'.format(username=user,upath=upath)
    headers = {'Authorization': 'Token 4045d366ab128f97daa8b542a7af7f40e1d385b1'}
    files = {'content': fp}
    response = requests.post(url, headers=headers, files=files)
    fp.close()

    if response.status_code == 201:
        with open('{upath}{username}/index.html'.format(username=user,upath=upath),'a') as fp:
            fp.write("<p>File uploaded successfully.</p>")
    else:
        with open('{upath}{username}/index.html'.format(username=user,upath=upath),'a') as fp:
            fp.write("<p>Upload Failed!</p>{code}".format(code='None'))

    return None