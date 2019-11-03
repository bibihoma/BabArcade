from gpiozero import LED, Device
from gpiozero.pins.mock import MockFactory
Device.pin_factory = MockFactory()
import time
import threading
import logging

class LEDplus():
    def __init__(self,pinnumber):
        self.led = LED(pinnumber)
        self.__loop = True
        self.__threading = threading.Thread(target=self.__blink)
        self._startTime = time.time()
        self._blinkPeriod=1


    def on(self,):
        self.__loop = False
        self.maybejoin()
        self.led.on()
        logging.debug("All goal buttons switched on")

    def off(self, ):
        self.__loop = False
        self.maybejoin()
        self.led.off()

    def maybejoin(self,):
        if self.__threading.isAlive():
            self.__threading.join()

    def blink(self):
        self.__threading = threading.Thread(target=self.__blink)
        self.__threading.start()

    def __blink(self):
        self.__loop = True
        while self.__loop:
            self.led.toggle()
            time.sleep(self._blinkPeriod/2)
            time.time()-self._startTime
            logging.info("Blink-"+str(self.__threading.ident)+' '+ str(time.localtime().tm_sec))
        self.led.off()
