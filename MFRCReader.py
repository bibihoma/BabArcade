#!/usr/bin/env python
import RPi.GPIO as GPIO
import logging

try:
    from mfrc522 import SimpleMFRC522
except ImportError:
    logging.error("Could not import SimpleMRFC52")

import threading
import logging

class MFRCReader():
    def __init__(self):
        self.__loop = True
        self.__threading = threading.Thread(target=self.__read)
        self._RFIDTxt = None
        logging.info('MFRC detection started')
        self.__threading.start()

    def __read(self):
        
        while self.__loop:
            try:
                reader = SimpleMFRC522()
                id, text = reader.read()
                logging.info("NFC read: "+str(id)+ " - "+text)
                self._RFIDTxt = text
            except exception:
                    print( exception)
            
        logging.info("Stopping listening on MFRC522")
        return

    def kill(self):
        logging.debug("well, if I knew how to do that, I would kill the thread")
        self.__loop = False