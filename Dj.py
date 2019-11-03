from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import glob
import logging
import random
pygame.mixer.init()


class Dj():
    def __init__(self,event,playerName=""):
        file = 'sounds/"+event"+*'
        logging.debug(playerName)
        search = 'sounds/'+playerName+'/'+event+'*'
        matchingFilesList = glob.glob(search)
        if len(matchingFilesList)> 0:
            file = random.choice(matchingFilesList)
        else:
            search = 'sounds/'+event+'*'
            matchingFilesList = glob.glob(search)
            file = random.choice(matchingFilesList)
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()


