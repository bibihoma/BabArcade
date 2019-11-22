#	from gpiozero.pins.mock import MockFactory
from gpiozero import Device, Button, LED
from gpiozero.pins.rpigpio import RPiGPIOFactory
factory = RPiGPIOFactory()
from LedBlinker import LEDplus
import argparse
from time import sleep
import signal
import logging
from Game import *
game = Game()
from Dj import Dj
 

logging.basicConfig(level=logging.DEBUG,format='%(funcName)s:%(lineno)d:%(message)s')

Dj("Init")

BlueBackPin = 16 # "BOARD36"
BlueFrontPin = 26 # "BOARD37"
RedBackPin = 20 #"BOARD38"
RedFrontPin = 21# "BOARD40" #21
AllLedsPin =  5 # "BOARD29"

from MFRCReader import  MFRCReader
mfrcReader = MFRCReader()


logging.info('Set mocks')
mockBtn = {}

def setMockButton():
    # Set the default pin factory to a mock factory
    if mock:
        Device.pin_factory = MockFactory()
        mockBtn[colors.BLUE,pos.BACK]=Device.pin_factory.pin(BlueBackPin)
        mockBtn[colors.BLUE,pos.FRONT]=Device.pin_factory.pin(BlueFrontPin)
        mockBtn[colors.RED,pos.BACK]=Device.pin_factory.pin(RedBackPin)
        mockBtn[colors.RED,pos.FRONT]=Device.pin_factory.pin(RedFrontPin)



# devices
buttonBounceTime = 0.005
AllButtonsLEDs = LEDplus(AllLedsPin)
AllButtonsLEDs._blinkPeriod = 4
AllButtonsLEDs.blink()

btns = {}
btns[colors.BLUE,pos.BACK]=Button(BlueBackPin, hold_time=2, bounce_time=buttonBounceTime,pin_factory=factory)
btns[colors.BLUE,pos.FRONT]=Button(BlueFrontPin, hold_time=2, bounce_time=buttonBounceTime,pin_factory=factory)
btns[colors.RED,pos.BACK]=Button(RedBackPin, hold_time=2, bounce_time=buttonBounceTime,pin_factory=factory)
btns[colors.RED,pos.FRONT]=Button(RedFrontPin, hold_time=2, bounce_time=buttonBounceTime,pin_factory=factory)

discardNextReleases = False

logging.info("Binding buttons")

for color, position in btns:
        def onpress(color=color,position=position):
            logging.info("Button pressed " + str(color) +" "+  str(position))
            for  otherBtnColor, otherBtnPosition in btns:
               if  otherBtnColor != color  and otherBtnPosition != position and  btns[otherBtnColor,otherBtnPosition].is_pressed:
                   discardNextReleases = False
                   if  otherBtnColor != color:
                       game.rollback()
                   else:
                       game.joker(color)
              
        btns[color,position].when_pressed = onpress


        def onrelease(color=color,position=position):
            logging.info("Button released " + str(color) +" "+  str(position))
            if discardNextReleases:
                nbBtnsPressed = 0
                for color,position in btns:
                    if btns[color,position].is_pressed:
                        nbBtnsPressed = nbBtnsPressed +1
                if nbBtnsPressed > 1:
                    logging.info("let's discard this release, and continue to discard")
                else:
                    logging.info("this was the last btn release to discard")
                    discardNextReleases = False
                return

            if game._status==gameStatus.STARTED:
                partnerPosition = pos.BACK
                if position == pos.BACK:
                    partnerPosition= pos.FRONT
                if btns[color,partnerPosition].is_pressed:
                    game.joker(color)
                else:
                    game.score(game.getPlayerFromColorPosition(color,position))
            if game._status==gameStatus.WAITINGPlayers:
                if mfrcReader._RFIDTxtQueue:
                    game.registerPlayer(mfrcReader._RFIDTxtQueue,color,position)
                    mfrcReader._RFIDTxtQueue = None
                else:
                    logging.warning("need to tap NBA ring prior to tapping button")
                    Dj("Error")
                if game._status == gameStatus.STARTED:
                    AllButtonsLEDs.on()
                    mfrcReader.kill()
                else:
                    logging.debug(game._players)
                    logging.debug(len(game._players))
                    AllButtonsLEDs._blinkPeriod = 4- len(game._players)
            if game._status==gameStatus.OVER:
                logging.info("About to launch a rocket and submit score to googlesheet")
                sleep(5)
                game.submit()

        btns[color,position].when_released = onrelease
        def onheld(color=color,position=position):
            logging.info("Button held " + str(color) +" "+  str(position))
        btns[color,position].when_held = onheld

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

#logging.info("Emulate button with keyboards")
#from pynput.keyboard import Key, Listener

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
        logging.debug("Mock is off, lets wait sequence of events: card read then button pressed")

    while True:
        sleep(10)
        logging.debug("main programm still alive")
        pass   
    # Collect events until released
    with Listener(
            on_release=on_release) as listener:
        listener.join()

    logging.info("End of simulation is over")
    #sleep(40000)
