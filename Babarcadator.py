from gpiozero.pins.mock import MockFactory
from gpiozero import Device, Button, LED
from time import sleep
import logging
import Game
# Set the default pin factory to a mock factory
logging.basicConfig(level=logging.DEBUG,format='%(funcName)s:%(lineno)d:%(message)s')
Device.pin_factory = MockFactory()

# Construct a couple of devices attached to mock pins 16 and 17, and link the
# devices
led = LED(17)
btn = Button(16)
led.source = btn
logging.info('Lets go')


# Here the button isn't "pushed" so the LED's value should be False
logging.debug(led.value)

# Get a reference to mock pin 16 (used by the button)
btn_pin = Device.pin_factory.pin(16)

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


