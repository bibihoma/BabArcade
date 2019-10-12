from gpiozero.pins.mock import MockFactory
from gpiozero import Device, Button, LED
from time import sleep
import signal

import logging
from Game import *
# Set the default pin factory to a mock factory
logging.basicConfig(level=logging.DEBUG,format='%(funcName)s:%(lineno)d:%(message)s')
Device.pin_factory = MockFactory()

# Construct a couple of devices attached to mock pins 16 and 17, and link the
# devices
led = LED(17)
btn = Button(16)
btns[colors.BLUE][pos.BACK]=Button(10)
btns[colors.BLUE][pos.FRONT]=Button(11)
btns[colors.RED][pos.BACK]=Button(12)
btns[colors.RED][pos.FRONT]=Button(13)

led.source = btn
logging.info('Lets go')


# Here the button isn't "pushed" so the LED's value should be False
logging.debug(led.value)

# Get a reference to mock pin 16 (used by the button)
btn_pin = Device.pin_factory.pin(16)
mockBtn[colors.BLUE][pos.BACK]=Device.pin_factory.pin(10)
mockBtn[colors.BLUE][pos.FRONT]=Device.pin_factory.pin(11)
mockBtn[colors.RED][pos.BACK]=Device.pin_factory.pin(12)
mockBtn[colors.RED][pos.FRONT]=Device.pin_factory.pin(13)


# Drive the pin low (this is what would happen electrically when the button is
# pushed)
btn_pin.drive_low()
sleep(0.1) # give source some time to re-read the button state
logging.debug(led.value)
btn_pin.drive_high()
sleep(0.1)
logging.debug(led.value)
logging.debug(btn.value)
btn_pin.drive_low()
logging.debug(btn.value)

game = Game()
# Simulate RFID
game.registerPlayer("Jerem",colors.RED,pos.FRONT)
game.registerPlayer("Etienne",colors.RED,pos.BACK)
game.registerPlayer("Colin",colors.BLUE,pos.FRONT)
game.registerPlayer("Thomas",colors.BLUE,pos.BACK)

signal.pause()