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

    def __str__(self):
        return (self._playername + " " + self._team + " " + self._color +" " + self._position )

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
        logging.info('Gooalll, adding goal event, then computing score')
        self._goalEvents.append(player)
        self.ComputeScore()

        return

    def ComputeScore(self):
        self._currentSet = 1
        self._score[self._currentSet][teams.T1] = 0
        self._score[self._currentSet][teams.T2] = 0
        self._manches[teams.T1] = 0
        self._manches[teams.T2] = 0
        lastEvent = ""

        for scorer in self._goalEvents:
            self._score[self._currentSet][scorer._team] += 1
            lastEvent = ' encore un but'

            if self._score[self._currentSet][teams.T1] == 10 or self._score[self._currentSet][teams.T2] == 10 :
                logging.debug('Set won by ' + scorer._color + scorer._team)
                lastEvent = 'Set won by ' + scorer._color + scorer._team
                self._manches[scorer._team]+= 1

                for team in teams:
                        if len(self._manches[team]) == 2:
                            logging.debug('Game won by ' + scorer._color)
                            lastEvent = 'Game won by ' + scorer._color
                            self._status = gameStatus.OVER
                            return


                else:
                    logging.debug('Starting a new set')
                    self.swapTeamsColors()
                    self._currentSet += 1
                    self._score[self._currentSet][teams.T1] = 0
                    self._score[self._currentSet][teams.T2] = 0
            else:
                if self._score[self._currentSet][scorer._team]%2 == 0:
                    self.swapPlayersPosition(scorer._team)

        return lastEvent

    def autogoal(self,color):
        logging.info('Autogoal')

    def swapPlayersPosition(self,team):
        logging.info('Swapping players position')
        for player in self._players:
            if player._team == team:
                if player._position == pos.FRONT:
                    player._position = pos.BACK
                elif player._position ==pos.BACK:
                    player._position = pos.FRONT
                logging.info('position after player position swap '+ player)

    def swapTeamsColors(self):
        logging.info('Swapping teams colors')
        for player in self._players:
            if player._color == colors.RED:
                    player._color = colors.BLUE
            if player._color == colors.BLUE:
                    player._color=colors.RED
            logging.info("after swap " + player)


    def __str__(self):
        return (str(self._players)+str(self._score))
