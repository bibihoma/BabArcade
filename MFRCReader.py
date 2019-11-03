import RPI.GPIO as GPIO
try:
    from mfrc522 import SimpleMFRC52
except ImportError:
    pass

import threading
import logging

class MFRCReader():
    def __init__(self):
        self.__loop = True
        self.__threading = threading.Thread(target=self.__read)
        self._startTime = time.time()
        self._RFIDTxt = None
        logging.info('MFRC detection started')
        self.__threading.start()

    def __read(self):
        reader = SimpleMFRC522()
        while self.__loop:
            id, text = reader.read()
            logging.info("NFC read: "+id+ " - "+text)
            self._RFIDTxt = text
        logging.info("Stopping listening on MFRC522")
        return

    def kill(self):
        logging.debug("well, if I knew how to do that, I would kill the thread")
        self.__loop = False