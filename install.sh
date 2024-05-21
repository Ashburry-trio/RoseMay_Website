#!/bin/bash
# Moves the files from the current directory
# to the home directory where they will be usefull
# First type: chmod +x ./install.sh
# To run: ./install.sh
`
chmod +x ./copyfiles.sh
mv * -t ~/ -f
rm -f -r *
cd ..
rm -f -r ./RoseMay_Website
cd ~/

