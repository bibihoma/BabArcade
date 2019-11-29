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
BlueFrontPin = 13
RedBackPin = 20 #"BOARD38"
RedFrontPin = 21 # "BOARD40" #21
AllLedsPin =  4

from MFRCReader import  MFRCReader
mfrcReader = MFRCReader()

AllButtonsLEDs._blinkPeriod = 4- len(game._players)

# devices
buttonBounceTime = None
AllButtonsLEDs = LEDplus(AllLedsPin)
AllButtonsLEDs._blinkPeriod = 4
AllButtonsLEDs.blink()

btns = {}
btns[colors.BLUE,pos.BACK]=Button(BlueBackPin, hold_time=2, bounce_time=buttonBounceTime,pin_factory=factory)
btns[colors.BLUE,pos.FRONT]=Button(BlueFrontPin, hold_time=2, bounce_time=buttonBounceTime,pin_factory=factory)
btns[colors.RED,pos.BACK]=Button(RedBackPin, hold_time=2, bounce_time=buttonBounceTime,pin_factory=factory)
btns[colors.RED,pos.FRONT]=Button(RedFrontPin, hold_time=2, bounce_time=buttonBounceTime,pin_factory=factory)

game._discardNextReleases = False

logging.info("Binding buttons")

for color, position in btns:
        def onpress(color=color,position=position):
            logging.info("Button pressed " + str(color) +" "+  str(position))
            for  otherBtnColor, otherBtnPosition in btns:
              
               if  (otherBtnColor != color  or  otherBtnPosition != position) and  btns[otherBtnColor,otherBtnPosition].is_pressed:
                   logging.debug("Discarding button releases from now on")
                   game._discardNextReleases = True
                   if  otherBtnColor != color and  otherBtnPosition== position:
                       game.rollback()
                       return
                   if  otherBtnColor != color and otherBtnPosition != position:
                       game.announceStatus()
                       return
                   if otherBtnColor == color:
                       game.joker(color)
                       return
              
            logging.debug("only this button is pressed")
              
        btns[color,position].when_pressed = onpress


        def onrelease(color=color,position=position):
            logging.info("Button released " + str(color) +" "+  str(position))
            if game._discardNextReleases:
                logging.debug("button releases are currently discarded")
                nbBtnsPressed = 0
                for color,position in btns:
                    logging.debug(btns[color,position])
                    if btns[color,position].is_active:
                        nbBtnsPressed = nbBtnsPressed +1
                logging.debug("nb btns pressed: " + str(nbBtnsPressed))
                if nbBtnsPressed > 0:
                    logging.info("let's discard this release, and continue to discard")
                else:
                    logging.info("this was the last btn release to discard")
                    game._discardNextReleases = False
                return

            if game._status==gameStatus.STARTED:
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
            game._discardNextReleases = True
            game.announceStatus()
        btns[color,position].when_held = onheld

logging.info("Bindind buttons complete")




def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False
    if key == Key.shift_l:
        btns[colors.RED,pos.BACK].onrelease(colors.RED,pos.BACK)
    if key == Key.ctrl_l:
        btns[colors.RED,pos.FRONT].onrelease(colors.RED,pos.FRONT)
    if key == Key.ctrl_r:
        btns[colors.BLUE,pos.BACK].onrelease(colors.BLUE,pos.BACK)
    if key == Key.shift_r:
        btns[colors.BLUE,pos.FRONT].onrelease(colors.BLUE,pos.FRONT)
    if key == Key.left:
        logging.info("Simulating a rollback button release")

    if key == Key.up:
        logging.info("Simulating a joker button release")

    if key == Key.down:
        logging.info("Simulating Submit score release")


#logging.info("Emulate button with keyboards")
#from pynput.keyboard import Key, Listener

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arcadify Foosball')
    parser.add_argument('--MockRPi', action='store_true')
    args = parser.parse_args()
    logging.debug("There")
    logging.debug(args)
    if args.MockRPi:
        logging.info("Emulating Plaer registration")
        game.registerPlayer("Jerem",  colors.RED, pos.FRONT)
        game.registerPlayer("Etienne",colors.RED, pos.BACK)
        game.registerPlayer("Colin",  colors.BLUE,pos.FRONT)
        game.registerPlayer("Thomas", colors.BLUE,pos.BACK)
    else:
        logging.info("Starting player registration")

    # Collect events until released
    with Listener(
            on_release=on_release) as listener:
        listener.join()

    logging.info("End of simulation is over")
    #sleep(40000)
