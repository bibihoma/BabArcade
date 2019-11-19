#!/bin/sh
# launcher.sh
#navigate then python
set -x
cd /
cd home/pi/BabArcade
python -V
git pull
python Babarcadator.py
cd /
