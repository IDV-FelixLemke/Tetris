import random
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

from tile import *

class Game(QObject):
    signalGameEnded = pyqtSignal()
    signalNewScore = pyqtSignal(int)
    def __init__(self, board, app):
        super(Game, self).__init__()
        self.AI = None
        self.board = board
        
        self.score = 0
        
        self.signalGameEnded.connect(app.gameEnded)
        self.signalNewScore.connect(app.newScore)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.setSingleShot(True)
        
        self.moveDir = None
        self.rotate = False
        
    def setAI(self, ai):
        self.AI = ai

    def startGame(self, delay = 100):
        self.timer.start(delay)
        
    def tick(self):
        if not self.board.tile:
            self.spawnRandomTile()
            #if self.board.checkCollision(self.board.tile, Pos(0,0)) == True:
                #self.signalGameEnded.emit()
                #return 
            if self.AI:
                self.AI.planMove(self.board, self.board.tile)
        if self.AI and self.AI.bestRoute:
            (self.moveDir, self.rotate) = self.AI.bestRoute.getNextMove()
            self.moveDir.y = 0 # step are save as 1,1 or -1,1, but moveDir should not include y-direction
        if self.moveDir:
            if self.board.checkCollision(self.board.tile, self.moveDir) == False:
                self.board.tile.moveBy(self.moveDir)
        self.moveDir = None
        if self.rotate:
            moveDir = self.moveDir
            if not moveDir:
                moveDir = Pos(0,0)
            if self.board.checkCollision(self.board.tile, moveDir, True) == False:
                self.board.tile.rotateClockwise()
        self.rotate = False
        if self.board.checkCollision(self.board.tile, Pos(0,1)) == True:
            if self.board.fixTile() != 0:
                self.signalGameEnded.emit()
                return
            numberOfClears = self.board.clearRows()
            if numberOfClears != 0:
                self.increaseScore(numberOfClears)
        else:
            self.board.tile.moveBy(Pos(0,1))
        self.timer.start()

    def increaseScore(self, count):
        if count == 1:
            self.score += 40
        elif count == 2:
            self.score += 100
        elif count == 3:
            self.score += 300
        elif count == 4:
            self.score += 1200
        self.signalNewScore.emit(self.score)

    def spawnRandomTile(self):
        currentTile = None
        startX = int(self.board.w / 2)
        tilenr = random.randrange(0,7);
        if tilenr == 0:
            currentTile = Tile_I(startX,-4)
        elif tilenr == 1:   
            currentTile = Tile_J(startX,-3)
        elif tilenr == 2:
            currentTile = Tile_L(startX,-3)
        elif tilenr == 3:
            currentTile = Tile_O(startX,-2)
        elif tilenr == 4:
            currentTile = Tile_S(startX,-2)
        elif tilenr == 5:
            currentTile = Tile_T(startX,-2)
        elif tilenr == 6:
            currentTile = Tile_Z(startX,-2)
        self.board.addTile(currentTile)
