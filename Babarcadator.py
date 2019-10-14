from gpiozero.pins.mock import MockFactory
from gpiozero import Device, Button, LED
from time import sleep
import signal

import logging
from Game import *
game = Game()

logging.basicConfig(level=logging.DEBUG,format='%(funcName)s:%(lineno)d:%(message)s')

logging.info('Set mocks')
# Set the default pin factory to a mock factory
Device.pin_factory = MockFactory()
mockBtn={}
mockBtn[colors.BLUE,pos.BACK]=Device.pin_factory.pin(10)
mockBtn[colors.BLUE,pos.FRONT]=Device.pin_factory.pin(11)
mockBtn[colors.RED,pos.BACK]=Device.pin_factory.pin(12)
mockBtn[colors.RED,pos.FRONT]=Device.pin_factory.pin(13)
rollBackButtonMock = Device.pin_factory.pin(7)
jokerButtonMock = Device.pin_factory.pin(5)
submitButtonMock = Device.pin_factory.pin(3)

# devices
btns = {}
btns[colors.BLUE,pos.BACK]=Button(10, hold_time=2)
btns[colors.BLUE,pos.FRONT]=Button(11, hold_time=2)
btns[colors.RED,pos.BACK]=Button(12, hold_time=2)
btns[colors.RED,pos.FRONT]=Button(13, hold_time=2)
rollBackButton = Button(7)
jokerButton = Button(5)
SubmitButton = Button(3)

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

def rollBackButtonRelease():
    logging.info("Rollback button released")
    game.rollback()
rollBackButton.when_released = rollBackButtonRelease

def jokerButtonRelease():
    logging.info("joker button released")
    game.joker()
jokerButton.when_released = jokerButtonRelease

def submitButtonRelease():
    logging.info("submit button released")
    logging.info(game._status)
    if game._status != gameStatus.OVER:
        logging.warning("Trying to submit to google a game that is not over")
        return
    game.submit()
SubmitButton.when_released = submitButtonRelease

logging.info("Bindind buttons complete")


logging.info(" Simulate RFID registration")
game.registerPlayer("Jerem",colors.RED,pos.FRONT)
game.registerPlayer("Etienne",colors.RED,pos.BACK)
game.registerPlayer("Colin",colors.BLUE,pos.FRONT)
game.registerPlayer("Thomas",colors.BLUE,pos.BACK)



logging.info("Emulate button with keyboards")
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

    if key == Key.left:
        logging.info("Simulating a rollback button release")
        rollBackButtonMock.drive_low()
        rollBackButtonMock.drive_high()

    if key == Key.up:
        logging.info("Simulating a joker button release")
        jokerButtonMock.drive_low()
        jokerButtonMock.drive_high()

    if key == Key.down:
        logging.info("Simulating Submit score release")
        submitButtonMock.drive_low()
        submitButtonMock.drive_high()



# Collect events until released
with Listener(
        on_release=on_release) as listener:
    listener.join()

logging.info("End of simulation is over")
#sleep(40000)