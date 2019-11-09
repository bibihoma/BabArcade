#	from gpiozero.pins.mock import MockFactory
from gpiozero import Device, Button, LED

#from LedBlinker import LEDplus
import argparse
from time import sleep
import signal
import logging

button =Button("BOARD32")

while True:
    sleep(0.5)
    if button.is_pressed:
        print("Button is pressed")
        print(button)
    else:
        print("Button is not pressed")
        print(button)