#!/bin/bash

# Grant execute permission with: chmod +x copyfiles.sh
# Execute with: ./copyfiles.sh
# to copy symbolic links to another web-app directory.

mkdir ~/www_proxy
mkdir ~/www_proxy/website
ln -s ~/www/website/* -t ~/www_proxy/website

