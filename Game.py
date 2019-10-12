import logging
from enum import Enum

class teams(Enum):
    T1 =1
    T2= 2

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
        self._goalEvents = []
        self._status = gameStatus.WAITINGPlayers

    def startSet(self):
        logging.info("Start set")

    def reset(self):
        logging.info("Game reset")

    def submit(self):
        logging.info("uploading to google")

    def registerPlayer(self,playerName,color,position):
        Player(playerName, color, position)
        if Player(playerName,color,position) in self._players:
                logging.error('Player Already registered')
                return False

        if self._status != gameStatus.WAITINGPlayers:
            logging.error('Trying to register a 5th player')

        logging.info(playerName + ' joined the game')
        self._players.append(Player(playerName,color,position))
        if len(self._players) == 4:
            logging.info('Game starting')
            for player in self._players:
                if player._color == colors.BLUE:
                        player._team = teams.T1
                elif player._color== colors.RED:
                        player._team = teams.T2
            self._status = gameStatus.STARTED

    def rollback(self):
        logging.info('Rollback')

    def score(self,player):
        if self._status != gameStatus.STARTED:
            logging.warning('Trying to score before game start')

        logging.info('Gooalll from '+ str(player)+', adding goal event, then computing score')
        self._goalEvents.append(player)
        self.ComputeScore()

        return

    def ComputeScore(self):
        self._currentSet = 1
        self._score = {self._currentSet:{teams.T1:0 , teams.T2:0}}
        self._manches= {teams.T1 : 0 ,teams.T2:0}
        for player in self._players:
                player._position = player._initialPosition
                player.color = player._initialColor
        lastEvent = ""

        nbEvents = len(self._goalEvents)
        for i,scorer in enumerate( self._goalEvents):
            self._score[self._currentSet][scorer._team] += 1
            logging.info(' encore un but')
            logging.info(self._currentSet)
            logging.info(self._score[self._currentSet][scorer._team])
            logging.info(self._score[self._currentSet][scorer._team] == 10)
            if (self._score[self._currentSet][scorer._team] == 10) :
                logging.debug('Set won by ' + str(scorer._color) + str(scorer._team))
                lastEvent = 'Set won by ' + str(scorer._color) + str(scorer._team)
                self._manches[scorer._team]+= 1

                for team in teams:
                        if self._manches[team] == 2:
                            logging.debug('Game won by ' + str(scorer._team))
                            lastEvent = 'Game won by ' + str(scorer._team)
                            self._status = gameStatus.OVER
                            return

                logging.debug('Starting a new set')
                self.swapTeamsSide()
                self._currentSet = self._currentSet +1
                self._score[self._currentSet]= {teams.T1 : 0 ,teams.T2: 0}
            else:
                if self._score[self._currentSet][scorer._team]%2 == 0:
                    self.swapFrontBack(scorer._team)
        logging.info("new score :"+str(self._score))
        logging.info(str(self._players[0])+" "+ str(self._players[2]))
        return lastEvent

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

    def __str__(self):
        return (str(self._players)+str(self._score))
