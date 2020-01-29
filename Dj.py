from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import glob
import logging
import random
from gtts import gTTS
pygame.mixer.init()


class Dj():
    def __init__(self,event,playerName="",announce=None, replay = False):
        if replay == True:
            return ;
        logging.info(event)
        file =''
        if event=="Announce":
            filePattern= 'sounds/announces/'+announce+'*'

            matchingFilesList = glob.glob(filePattern)
            if len(matchingFilesList) == 0:
                logging.info("initiating google translation for "+ announce)
                tts = gTTS(text = announce, lang = 'en')
                file ='sounds/announces/'+announce+'.mp3'
                tts.save(file)
                logging.info("google translation successful")
            else:
                file = random.choice(matchingFilesList)
        else:
            logging.debug(playerName)
            search = 'sounds/'+playerName+'/'+event+'*'
            matchingFilesList = glob.glob(search)
            if len(matchingFilesList)> 0:
                file = random.choice(matchingFilesList)
            else:
                search = 'sounds/'+event+'*'
                matchingFilesList = glob.glob(search)
                file = random.choice(matchingFilesList)
        logging.debug("About to play file:"+ file)
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()


