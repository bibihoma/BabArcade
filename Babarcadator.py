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
btns[colors.BLUE,pos.BACK]=Button(10, hold_time=2)
btns[colors.BLUE,pos.FRONT]=Button(11, hold_time=2)
btns[colors.RED,pos.BACK]=Button(12, hold_time=2)
btns[colors.RED,pos.FRONT]=Button(13, hold_time=2)

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




btn_pin2 = Device.pin_factory.pin(2)
def hello():
    logging.info("HELLO")

logging.info("Binding buttons")
for color, position in btns:
    def onpress(color=color,position=position):
        logging.info("Button pressed " + str(color) +" "+  str(position))
    btns[color,position].when_pressed = onpress
    def onrelease(color=color,position=position):
        logging.info("Button released " + str(color) +" "+  str(position))
        game.score(game.getPlayerFromColorPosition(color,position))
    btns[color,position].when_released = onrelease
    def onheld(color=color,position=position):
        logging.info("Button held " + str(color) +" "+  str(position))
    btns[color,position].when_held = onheld
logging.info("Bindind buttons complete")


# Simulate RFID
game.registerPlayer("Jerem",colors.RED,pos.FRONT)
game.registerPlayer("Etienne",colors.RED,pos.BACK)
game.registerPlayer("Colin",colors.BLUE,pos.FRONT)
game.registerPlayer("Thomas",colors.BLUE,pos.BACK)


#for i in range(0,10):
#    mockBtn[colors.BLUE,pos.BACK].drive_low()
#    mockBtn[colors.BLUE,pos.BACK].drive_high()

from pynput.keyboard import Key, Listener

def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False
    if key == Key.shift_l:
        mockBtn[colors.RED, pos.BACK].drive_low()
        mockBtn[colors.RED, pos.BACK].drive_high()
    if key == Key.ctrl_l:
        mockBtn[colors.RED,pos.FRONT].drive_low()
        mockBtn[colors.RED,pos.FRONT].drive_high()
    if key == Key.ctrl_r:
        mockBtn[colors.BLUE, pos.BACK].drive_low()
        mockBtn[colors.BLUE, pos.BACK].drive_high()
    if key == Key.shift_r:
        mockBtn[colors.BLUE,pos.FRONT].drive_low()
        mockBtn[colors.BLUE,pos.FRONT].drive_high()

# Collect events until released
with Listener(
        on_release=on_release) as listener:
    listener.join()

logging.info("End of simulation is over")
#sleep(40000)