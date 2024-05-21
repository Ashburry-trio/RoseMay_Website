#!/bin/bash
# Moves the files from the current directory
# to the home directory where they will be usefull

mv * -t ~/ -f
rm -f -r *
cd ..
rm -f -r ./RoseMay_Website
cd ~/

