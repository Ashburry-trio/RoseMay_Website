#!/bin/bash
# Moves the files from the current directory
# to the home directory where they will be usefull
# First type: chmod +x ./install.sh
# To run: source ./install.sh
mv * -t ~/ -f
cd ..
rm -f -r ./RoseMay_Website
cd ~/
python -m pip install --upgrade pip
python -m pip install --upgrade --upgrade-strategy eager -r requirements.txt
