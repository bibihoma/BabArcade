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
led1 = LED(17)
btn1 = Button(16)
btns = {}
btns[colors.BLUE,pos.BACK]=Button(10)
btns[colors.BLUE,pos.FRONT]=Button(11)
btns[colors.RED,pos.BACK]=Button(12)
btns[colors.RED,pos.FRONT]=Button(13)

led1.source = btn1
logging.info('Lets go')


# Here the button isn't "pushed" so the LED's value should be False
logging.debug(led1.value)

game = Game()

def blueBackBtnRelease():
    logging.info("Button released")
    player = game.getPlayerFromColorPosition(colors.BLUE,pos.BACK)
    game.score(player)

def blueBackBtnPress():
    logging.info("Button pressed")


# Get a reference to mock pin 16 (used by the button)
btn_pin = Device.pin_factory.pin(16)
mockBtn={}
mockBtn[colors.BLUE,pos.BACK]=Device.pin_factory.pin(10)
mockBtn[colors.BLUE,pos.FRONT]=Device.pin_factory.pin(11)
mockBtn[colors.RED,pos.BACK]=Device.pin_factory.pin(12)
mockBtn[colors.RED,pos.FRONT]=Device.pin_factory.pin(13)

mockBtn[colors.BLUE,pos.BACK].when_released = blueBackBtnRelease
btn_pin.when_pressed = blueBackBtnPress



# Simulate RFID
game.registerPlayer("Jerem",colors.RED,pos.FRONT)
game.registerPlayer("Etienne",colors.RED,pos.BACK)
game.registerPlayer("Colin",colors.BLUE,pos.FRONT)
game.registerPlayer("Thomas",colors.BLUE,pos.BACK)

btn_pin2 = Device.pin_factory.pin(2)
def hello():
    print("Hello")

button = Button(2)
button.when_pressed = hello
sleep(0.1)
btn_pin2.drive_low()


btn_pin.drive_low()
sleep(0.1)
btn_pin.drive_high()
sleep(0.1)
btn_pin.drive_low()
sleep(2)
#sleep(40000)