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
python3 Babarcadator.py

cd /
