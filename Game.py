from enum import Enum
class colors (Enum):
    BLUE= 1
    RED= 2

class pos (Enum):
    FRONT= 1
    BACK = 2
    AUTOGOAL = 3
    NEUTRAL = 4

class gameStatus(Enum):
    WAITINGPlayers=1
    STARTED = 2
    OVER = 3

class player:
    def __init__(self,playername,color, position):
            self._playername = playername
            self._color = color
            self._position = position

class game:
    def __init__(self):
        self._players = []
        self._score = []
        self._goalEvents = []
        self._status = gameStatus.STARTED

    def startSet(self):
        logging.info("Start set")

    def reset(self):
        logging.info("Game reset")

    def submit(self):
        logging.info("uploading to google")

    def registerPlayer(self,playerName,color,position):
        if self._status != gameStatus.WAITINGPlayers:
            logging.error('Trying to register a 5th player')
        logging.info(playerName + ' joined the game')
        self._players.append(Player(playerName,color,position))
        if len(self._players) == 4:
            logging.info('Game starting')
            self._status = gameStatus.STARTED

    def rollback(self):
        logging.info('Rollback')

    def score(self,player):
        if self._status != gameStatus.STARTED:
            logging.warning('Trying to score before game start')
        logging.info('Gooalll')
        self._goalEvents.append(player)

    def ComputeScore(self):
        currentSet = 1
        self._score[currentSet][colors.BLUE] = 0
        self._score[currentSet][colors.RED] = 0
        self._manches[colors.BLUE] = 0
        self._manches[colors.RED] = 0
        lastEvent = ""

        for scorer in self._goalEvents:
            if scorer._color == colors.RED:
                self._score[currentSet][colors.RED] += 1
            if scorer._color == colors.BLUE:
                self._score[currentSet][colors.BLUE] += 1
                lastEvent = ' encore un but'
            if self._score[currentSet][colors.BLUE] == 10 or self._score[currentSet][colors.RED] == 10 :
                logging.debug('Set won by ' + scorer._color)
                lastEvent = 'Set won by ' + scorer._color
                self._manches[scorer._color]+= 1

                for color in colors:
                        if self._manches[color] == 2:
                            logging.debug('Game won by ' + scorer._color)
                            lastEvent = 'Game won by ' + scorer._color
                            self._status = gameStatus.OVER

                else:
                    logging.debug('Starting a new set')
                    currentSet += 1
                    self._score[currentSet][colors.BLUE] = 0
                    self._score[currentSet][colors.RED] = 0

        return lastEvent

    def autogoal(self,color):
        logging.info('Autogoal')

    def swapPlayerPosition(self,color):
        logging.info('Swapping players position')

    def __str__(self):
        return (str(self._players)+str(self._score))
