#!/bin/sh
# launcher.sh
#navigate then python
set -x
cd /home/pi/BabArcade 
echo "$USER"
date >> logs.txt
pyenv verions
python -V  
git pull  
/home/pi/.pyenv/versions/3.7.5/bin/python Babarcadator.py

cd /
