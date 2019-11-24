from Dj import Dj

import logging
from enum import Enum
from googleWrapper2 import uploadResults
import json
import random

class Event(dict):
    def __str__(self):
        copy = self
        if "scorer" in copy:
            copy["scorer"]= copy["scorer"]._playername
        return json.dumps(copy)

class teams(Enum):
    T1 =1
    T2= 2

def getOtherTeam(team):
    if  team == teams.T1:
        return teams.T2
    else:
        return teams.T1

class colors (Enum):
    BLUE= 1
    RED= 2

class pos (Enum):
    FRONT= 1
    BACK = 2
    GOALFROMDEFENSE = 3
    NEUTRAL = 4

class gameStatus(Enum):
    WAITINGPlayers=1
    STARTED = 2
    OVER = 3

class Player:
    def __init__(self,playername,color, position):
            self._playername = playername
            self._color = color
            self._position = position
            self._team = "unassigned"
            self._initialPosition = position
            self._initialColor = color

    def __str__(self):
        return (self._playername + " " + str( self._team) + " " + str(self._color) +" " + str(self._position) )

class Game:
    def __init__(self):
        self._players = []
        self._score = []
        self._events = []
        self._status = gameStatus.WAITINGPlayers
        self._winners = []
        self._loosers = []

    def startSet(self):
        logging.info("Start set")

    def reset(self):
        logging.info("Game reset")

    def submit(self):
        logging.info("uploading to google")
        Dj("Submit")
        flattenedEvents =[]
        for event in self._events:
            flattenedEvents.append(str(event))
        uploadResults(self._winners[0],self._winners[1],self._loosers[0],self._loosers[1],flattenedEvents)
        logging.info("Game result uploaded successfully")

    def registerPlayer(self,playerName,color,position):
        for player in self._players:
            logging.debug(player._playername+"-compareted to-"+playerName)
            if player._playername == playerName:
                logging.error('Player Already registered')
                Dj("Error")
                return False

        if self._status != gameStatus.WAITINGPlayers:
            logging.error('Trying to register a 5th player')
            Dj("Error")
            return False

        for registeredPlayer in self._players:
            if registeredPlayer._color == color and registeredPlayer._position == position:
                logging.debug([registeredPlayer._color, color , registeredPlayer._position, position])
                logging.error('This slot is already registered by another player')
                Dj("Error")
                return False

        playerJoinAnnounces = [ playerName+" joinded the game.", playerName+" is in.", "Welcome "+ playerName + ".", "Go " + playerName+ " Go"]
        announce = random.choice(playerJoinAnnounces)
        logging.info(playerName + ' joined the game')
        self._players.append(Player(playerName,color,position))
        Dj("Announce","speaker", announce = announce)
        if len(self._players) == 4:
            logging.info('Game starting')
            for player in self._players:
                if player._color == colors.BLUE:
                        player._team = teams.T1
                elif player._color== colors.RED:
                        player._team = teams.T2
            self.initializeGameAfterPlayerSelection()
            Dj('GameStart')

    def initializeGameAfterPlayerSelection(self):
        self._status = gameStatus.STARTED
        self._winners = []
        self._loosers = []
        self._currentSet = 1
        self._score = {self._currentSet:{teams.T1:0 , teams.T2:0}}
        self._manches= {teams.T1 : 0 ,teams.T2:0}
        for player in self._players:
                player._position = player._initialPosition
                player.color = player._initialColor

    def getTeamOfColor(self,color):
        if  self._players[0]._color == color:
            return  self._players[0]._team
        else:
            return getOtherTeam(self._players[0]._team)

    def rollback(self):
        logging.info('Rollback')
        if len(self._events) > 0:
            Dj("Announce",playerName = "Speaker",announce="Video assistant referee decision... Last action cancelled.")
            self._events.pop()
            self.initializeGameAfterPlayerSelection()
            for event in self._events:
                self.processEvent(event,replay=True)
            return
        else:
            logging.warning("Trying to rollback although there are no actions yet")
            Dj("Error")


    def score(self,player):
        if self._status != gameStatus.STARTED:
            logging.error('Trying to score before game start, or after it ended')
            return

        logging.info('Gooalll from '+ str(player)+', adding goal event, then processing event')
        self._events.append(Event({"type":'G',"scorer":player,"def":"TBD"}))
        self.processEvent(self._events[-1])
        return

    def joker(self,color):
        logging.info("Joker, front and back player swap on "+str(color))
        Dj("Switch","speaker")
        frontPlayer =""
        backPlayer =""
        for player in  self._players:
            if player._color == color:
                if player._position== pos.FRONT:
                    frontPlayer = player._playername
                if player._position== pos.BACK:
                    backPlayer  = player._playername

        announce = "Joker.  " + frontPlayer + " goes to front and " + backPlayer + "goes to back."
        Dj('Announce',playerName='speaker',announce=announce)
        self._events.append(Event({"type":'Joker',"color":color}))
        self.processEvent(self._events[-1])

    def processEvent(self,event,replay = False):
        if event["type"] == 'G':
            scorer = event["scorer"]
            self._score[self._currentSet][scorer._team] += 1
            if (self._score[self._currentSet][scorer._team] == 10) :
                logging.debug('Set won by ' + str(scorer._color) + str(scorer._team))
                lastEvent = 'Set won by ' + str(scorer._color) + str(scorer._team)
                self._manches[scorer._team]+= 1
                if self._manches[scorer._team] == 2:
                    logging.debug('Game won by ' + str(scorer._team))
                    lastEvent = 'Game won by ' + str(scorer._team)
                    self._status = gameStatus.OVER
                    self._winners = []
                    self._loosers = []
                    for player in self._players:
                        if player._team == scorer._team:
                            self._winners.append(player._playername)
                        else:
                            self._loosers.append(player._playername)
                    Dj("Victory",scorer._playername, replay=replay)

                    return
                else:
                    logging.debug('Starting a new set')
                    self.swapTeamsSide()
                    self._currentSet = self._currentSet +1
                    self._score[self._currentSet]= {teams.T1 : 0 ,teams.T2: 0}
                    Dj("Set",scorer._playername, replay = replay)
            else:
                if self._score[self._currentSet][scorer._team]%2 == 0:
                    self.swapFrontBack(scorer._team)
                    Dj('Switch', scorer._playername, replay= replay)
                else:
                    logging.debug('no switch, just a goal')
                    Dj('Goal',scorer._playername, replay = replay)

            logging.info("new score :"+str(self._score))
            logging.info(str(self._players[0])+" "+ str(self._players[2]))
        elif event["type"]=="Joker":
            logging.info("Joker used by " + str(event["color"]))
            self.swapFrontBack(self.getTeamOfColor(event["color"]))

    def autogoal(self,color):
        logging.info('Autogoal')

    def swapFrontBack(self,team):
        for player in self._players:
            if player._team == team:
                if player._position == pos.FRONT:
                    player._position = pos.BACK
                elif player._position ==pos.BACK:
                    player._position = pos.FRONT

                #logging.info('position after player position swap '+ str(player))

    def swapTeamsSide(self):
        logging.info('Swapping teams colors')
        for player in self._players:
            #logging.info("before swap " + str( player))
            if player._color == colors.RED:
                    player._color = colors.BLUE
            elif player._color == colors.BLUE:
                    player._color=colors.RED
            logging.info("after swap " + str( player))

    def getPlayerFromColorPosition(self,color,pos):
        for player in self._players:
            if player._position == pos and player._color==color:
                return player
        logging.error("no player found at position")

    def announceStatus(self):
        announce ='    Red ' + str(self._score[self._currentSet][self.getTeamOfColor(colors.RED )] )+"." 
        announce+= " Blue " + str(self._score[self._currentSet][self.getTeamOfColor(colors.BLUE )] )+"." 
        frontPlayers = []
        for player in self._players:
            if player._position == pos.FRONT:
                frontPlayers.append(player._playername )
        announce += " and ".join( frontPlayers) + ' attack.'
        Dj("Announce" , playerName="speaker",announce=announce)
	

    def __str__(self):
        return (str(self._players)+str(self._score))
