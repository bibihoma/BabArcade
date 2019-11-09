#	from gpiozero.pins.mock import MockFactory
from gpiozero import Device, Button, LED

from LedBlinker import LEDplus
import argparse
from time import sleep
import signal
import logging
from Game import *
game = Game()

logging.basicConfig(level=logging.DEBUG,format='%(funcName)s:%(lineno)d:%(message)s')

#b32 = Button("BOARD32")
#logging.debug(b32)
#sleep(2)
#logging.debug(b32)
#sleep(3)


#try:
from MFRCReader import  MFRCReader
mfrcReader = MFRCReader()
#except ImportError:
#    logging.warning("Could not import MFRCReader")
#    logging.warning(str(ImportError))
#    print(ImportError)


logging.info('Set mocks')
mockBtn = {}
rollBackButtonMock = None
jokerButtonMock = None
submitButtonMock = None
def setMockButton():
    # Set the default pin factory to a mock factory
    if mock:
        Device.pin_factory = MockFactory()
        mockBtn[colors.BLUE,pos.BACK]=Device.pin_factory.pin(36)
        mockBtn[colors.BLUE,pos.FRONT]=Device.pin_factory.pin(37)
        mockBtn[colors.RED,pos.BACK]=Device.pin_factory.pin(38)
        mockBtn[colors.RED,pos.FRONT]=Device.pin_factory.pin(40)
        rollBackButtonMock = Device.pin_factory.pin(35)
        jokerButtonMock = Device.pin_factory.pin(5)
        submitButtonMock = Device.pin_factory.pin(3)


# devices
AllButtonsLEDs = LEDplus("BOARD29")
AllButtonsLEDs._blinkPeriod = 4
AllButtonsLEDs.blink()

btns = {}
btns[colors.BLUE,pos.BACK]=Button("BOARD36", hold_time=2)
btns[colors.BLUE,pos.FRONT]=Button("BOARD37", hold_time=2)
btns[colors.RED,pos.BACK]=Button("BOARD38", hold_time=2)
btns[colors.RED,pos.FRONT]=Button("BOARD40", hold_time=2)
rollBackButton = Button("BOARD35")
logging.debug(rollBackButton)
jokerButton = Button("BOARD33")
SubmitButton = Button("BOARD31")



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
                if mfrcReader._RFIDTxtQueue:
                    game.registerPlayer(mfrcReader._RFIDTxtQueue,color,position)
                    mfrcReader._RFIDTxtQueue = None
                else:
                    logging.warning("need to tap NBA ring prior to tapping button")
                if game._status == gameStatus.STARTED:
                    AllButtonsLEDs.on()
                    mfrcReader.kill()
                else:
                    logging.debug(game._players)
                    logging.debug(len(game._players))
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


    logging.info("Starting player registration")
    game.registerPlayer("Jerem", colors.RED, pos.FRONT)
    game.registerPlayer("Etienne", colors.RED, pos.BACK)
    game.registerPlayer("Colin", colors.BLUE, pos.FRONT)

    if mock==True:
        logging.debug("Autoregistering player4 as game is mocked")
        game.registerPlayer("Thomas",colors.BLUE,pos.BACK)
    else:
        logging.debug("Mock is off, lets wait the combination of 2 events: card read then button pressed")

    #while True:
    #    logging.debug(rollBackButton)
    #    logging.debug(rollBackButton.is_pressed)
    #    sleep(1)



    # Collect events until released
    with Listener(
            on_release=on_release) as listener:
        listener.join()

    logging.info("End of simulation is over")
    #sleep(40000)