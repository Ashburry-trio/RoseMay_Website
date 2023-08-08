# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Flask project

# In your PythonAnywhere.com Dashboard navigate to WEB
# Under WEB scroll down under CODE and "WSGI configuration file:"
# This is this file for wwww.mslscript.com. The only change needed is the
# UserName in the 'project_home' str variable and the Typing which requires
#
# from __future__ import annotations
#
# Since this file is auto-generated I do not think there is anything needed to be changed, but as you can see
# I have my project_home hardcoded.
from __future__ import annotations
from os import path
import sys

# add your project directory to the sys.path

project_home: str = path.expanduser("~/www")
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from flask_app import app as application
