from gpiozero.pins.mock import MockFactory
from gpiozero import Device, Button, LED

from LedBlinker import LEDplus
import argparse
from time import sleep
import signal
mock = True
import logging
from Game import *
game = Game()

try:
    from MFRCReader import  MFRCReader
    mfrcReader = MFRCReader()
except ImportError:
    pass


logging.basicConfig(level=logging.DEBUG,format='%(funcName)s:%(lineno)d:%(message)s')

logging.info('Set mocks')
mockBtn = {}
rollBackButtonMock = None
jokerButtonMock = None
submitButtonMock = None
def setMockButton():
    # Set the default pin factory to a mock factory
    if mock:
        Device.pin_factory = MockFactory()
        mockBtn[colors.BLUE,pos.BACK]=Device.pin_factory.pin(10)
        mockBtn[colors.BLUE,pos.FRONT]=Device.pin_factory.pin(11)
        mockBtn[colors.RED,pos.BACK]=Device.pin_factory.pin(12)
        mockBtn[colors.RED,pos.FRONT]=Device.pin_factory.pin(13)
        rollBackButtonMock = Device.pin_factory.pin(7)
        jokerButtonMock = Device.pin_factory.pin(5)
        submitButtonMock = Device.pin_factory.pin(3)


# devices
AllButtonsLEDs = LEDplus(18)
AllButtonsLEDs._blinkPeriod = 4
AllButtonsLEDs.blink()

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
            if game._status==gameStatus.STARTED:
                game.score(game.getPlayerFromColorPosition(color,position))
            if game._status==gameStatus.WAITINGPlayers:
                if mfrcReader._RFIDTxt:
                    game.registerPlayer(mfrcReader._RFIDTxt,color,position)
                    mfrcReader._RFIDTxt = None
                else:
                    logging.warning("need to tap NBA ring prior to tapping button")
                if game._status == gameStatus.STARTED:
                    AllButtonsLEDs.on()
                    mfrcReader.kill()
                else:
                    AllButtonsLEDs._blinkPeriod(4-len(game._players))

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

logging.info("Starting player registration")
game.registerPlayer("Jerem", colors.RED, pos.FRONT)
game.registerPlayer("Etienne", colors.RED, pos.BACK)
game.registerPlayer("Colin", colors.BLUE, pos.FRONT)

if mock==True:
    game.registerPlayer("Thomas",colors.BLUE,pos.BACK)





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

logging.info("Emulate button with keyboards")
from pynput.keyboard import Key, Listener

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arcadify Foosball')
    parser.add_argument('--MockRPi', action='store_true')
    args = parser.parse_args()
    logging.debug("There")
    logging.debug(args)
    if args.MockRPi:
        mock = True
        logging.debug('Mocking')
        setMockButton()
    else:
        mock = False




    # Collect events until released
    logging.debug("here")
    with Listener(
            on_release=on_release) as listener:
        listener.join()

    logging.info("End of simulation is over")
    #sleep(40000)