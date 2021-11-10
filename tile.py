from PyQt5 import QtWidgets, QtGui, QtCore
from pixel import *

class Pos:
    def __init__(self, x,y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Tile:
    def __init__(self, posX, posY):
        self.pos = Pos(posX, posY)
        self.pixel = []
        self.rot = 0
        self.color = QtCore.Qt.white
        self.currentState = 0
        self.board = None
        self.leftTop = None
        self.rightBottom = None

    def __del__(self):
        for pix in self.pixel:
            if pix.graphicsPixel and self.board and self.board.graphicsBoard:
                if pix.graphicsPixel.scene():
                    self.board.graphicsBoard.removeItem(pix.graphicsPixel)
                del pix.graphicsPixel
    
    def clearPixel(self):
        self.pixel = []
    
    def setPixelRelative(self, pixel):
        for pix in pixel:
            pix.moveBy(self.pos.x, self.pos.y)
        self.pixel = pixel
        self.leftTop = self.calcLeftTop()
        self.rightBottom = self.calcRightBottom()
        
    def setBoard(self, board):
        self.board = board
    
    def draw(self, scene):
        for pix in self.pixel:
            gPixel = GraphicsPixel(pix)
            gPixel.setColor(self.color)
            scene.addItem(gPixel)
    
    def calcLeftTop(self):
        top = 1000
        left = 1000
        for pix in self.pixel:
            if pix.x < left:
                left = pix.x
            if pix.y < top:
                top = pix.y
        return Pos(left, top)
    def calcRightBottom(self):
        right = 0
        bottom = 0
        for pix in self.pixel:
            if pix.x > right:
                right = pix.x
            if pix.y > bottom:
                bottom = pix.y
        return Pos(right, bottom)

    def moveTo(self, pos):
        dPos = pos - self.pos
        self.pos = pos
        for pix in self.pixel:
            pix.moveBy(dPos.x, dPos.y)
        self.leftTop = self.calcLeftTop()
        self.rightBottom = self.calcRightBottom()
        
    
    def moveBy(self, pos):
        self.pos = self.pos + pos
        for pix in self.pixel:
            pix.moveBy(pos.x, pos.y)
        self.leftTop = self.calcLeftTop()
        self.rightBottom = self.calcRightBottom()
        
    def rotateClockwise(self):
        self.currentState += 1
        if self.currentState > self.maxState:
            self.currentState = 0
        for pix in self.pixel:
            if pix.graphicsPixel:
                pix.graphicsPixel.scene().removeItem(pix.graphicsPixel)
                del pix.graphicsPixel
        self.setPixelRelative(self.form(self.currentState))
        if self.board and self.board.graphicsBoard:
            self.draw(self.board.graphicsBoard)
        self.leftTop = self.calcLeftTop()
        self.rightBottom = self.calcRightBottom()

class Tile_I(Tile):
    def __init__(self, posX, posY):
        super(Tile_I,self).__init__(posX,posY)
        self.setPixelRelative(self.form(self.currentState))
        self.color = QtCore.Qt.red
        self.maxState = 1
    def form(self, state):
        if state == 0:
            return [Pixel(0,-1), Pixel(0,0), Pixel(0,1), Pixel(0,2)]
        elif state == 1:
            return [Pixel(-1,0), Pixel(0,0), Pixel(1,0), Pixel(2,0)]

class Tile_J(Tile):
    def __init__(self, posX, posY):
        super(Tile_J,self).__init__(posX,posY)
        self.setPixelRelative(self.form(self.currentState))
        self.color = QtCore.Qt.yellow
        self.maxState = 3
    def form(self, state):
        if state == 0:
            return [Pixel(0,-1), Pixel(0,0), Pixel(0,1), Pixel(-1,1)]
        elif state == 1:
            return [Pixel(1,0), Pixel(0,0), Pixel(-1,0), Pixel(-1,-1)]
        elif state == 2:
            return [Pixel(0,1), Pixel(0,0), Pixel(0,-1), Pixel(1,-1)]
        elif state == 3:
            return [Pixel(-1,0), Pixel(0,0), Pixel(1,0), Pixel(1,1)]

class Tile_L(Tile):
    def __init__(self, posX, posY):
        super(Tile_L,self).__init__(posX,posY)
        self.setPixelRelative(self.form(self.currentState))
        self.color = QtCore.Qt.blue        
        self.maxState = 3
    def form(self, state):
        if state == 0:
            return [Pixel(0,-1), Pixel(0,0), Pixel(0,1), Pixel(1,1)]
        elif state == 1:
            return [Pixel(1,0), Pixel(0,0), Pixel(-1,0), Pixel(-1,1)]
        elif state == 2:
            return [Pixel(0,1), Pixel(0,0), Pixel(0,-1), Pixel(-1,-1)]
        elif state == 3:
            return [Pixel(-1,0), Pixel(0,0), Pixel(1,0), Pixel(1,-1)]
        
class Tile_S(Tile):
    def __init__(self, posX, posY):
        super(Tile_S,self).__init__(posX,posY)
        self.setPixelRelative(self.form(self.currentState))
        self.color = QtCore.Qt.green
        self.maxState = 3
    def form(self, state):
        if state == 0:
            return [Pixel(-1,1), Pixel(0,1), Pixel(0,0), Pixel(1,0)]
        elif state == 1:
            return [Pixel(-1,-1), Pixel(-1,0), Pixel(0,0), Pixel(0,1)]
        elif state == 2:
            return [Pixel(1,-1), Pixel(0,-1), Pixel(0,0), Pixel(-1,0)]
        elif state == 3:
            return [Pixel(1,1), Pixel(1,0), Pixel(0,0), Pixel(0,-1)]

class Tile_T(Tile):
    def __init__(self, posX, posY):
        super(Tile_T,self).__init__(posX,posY)
        self.setPixelRelative(self.form(self.currentState))
        self.color = QtCore.Qt.white
        self.maxState = 3
    def form(self, state):
        if state == 0:
            return [Pixel(-1,0), Pixel(0,-1), Pixel(0,0), Pixel(1,0)]
        elif state == 1:
            return [Pixel(0,-1), Pixel(1,0), Pixel(0,0), Pixel(0,1)]
        elif state == 2:
            return [Pixel(1,0), Pixel(0,1), Pixel(0,0), Pixel(-1,0)]
        elif state == 3:
            return [Pixel(0,1), Pixel(-1,0), Pixel(0,0), Pixel(0,-1)]

class Tile_Z(Tile):
    def __init__(self, posX, posY):
        super(Tile_Z,self).__init__(posX,posY)
        self.setPixelRelative(self.form(self.currentState))
        self.color = QtCore.Qt.gray
        self.maxState = 3
    def form(self, state):
        if state == 0:
            return [Pixel(-1,0), Pixel(0,1), Pixel(0,0), Pixel(1,1)]
        elif state == 1:
            return [Pixel(0,-1), Pixel(-1,0), Pixel(0,0), Pixel(-1,1)]
        elif state == 2:
            return [Pixel(1,0), Pixel(0,-1), Pixel(0,0), Pixel(-1,-1)]
        elif state == 3:
            return [Pixel(0,1), Pixel(1,0), Pixel(0,0), Pixel(1,-1)]

class Tile_O(Tile):
    def __init__(self, posX, posY):
        super(Tile_O,self).__init__(posX,posY)
        self.setPixelRelative(self.form(self.currentState))
        self.color = QtCore.Qt.magenta
        self.maxState = 0
    def form(self, state):
        return [Pixel(0,0), Pixel(0,1), Pixel(1,0), Pixel(1,1)]
        
