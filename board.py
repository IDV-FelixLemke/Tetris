from PyQt5 import QtWidgets, QtGui, QtCore
from tile import *

class Board:
    def __init__(self):
        self.tile = None
        self.pixellist = []
        self.graphicsBoard = None
        self.w = 12
        self.h = 26
        
        self.grid = [ [0 for i in range(self.h)] for j in range(self.w) ]
        
        # some statistic variables to improve performance
        self.pixelMaxTop = self.h
        self.pixelMinTop = 0
        
    def addTile(self, tile):
        self.tile = tile
        tile.setBoard(self)
        if self.graphicsBoard:
            tile.draw(self.graphicsBoard)
    
    def setGraphicsBoard(self, graphicsBoard):
        self.graphicsBoard = graphicsBoard
    
    def clear(self):
        for pixel in self.pixellist:
            if self.graphicsBoard and pixel.graphicsPixel:
                self.graphicsBoard.removeItem(pixel.graphicsPixel)
            if pixel.graphicsPixel:
                del pixel.graphicsPixel
            del pixel
        self.pixellist = []        
        self.grid = [ [0 for i in range(self.h)] for j in range(self.w) ]
    
    def checkCollision(self, tile, offset, rotation = False):
        testpixel = []
        if rotation == True:
            state = tile.currentState + 1
            if state > tile.maxState:
                state = 0
            for pix in tile.form(state):
                newpix = Pixel(pix.x + tile.pos.x, pix.y + tile.pos.y)
                testpixel.append(newpix)
        else:
            testpixel = tile.pixel
        for pix in testpixel:
            if pix.x + offset.x < 0:
                return True
            if pix.x + offset.x >= self.w:
                return True
            if pix.y + offset.y >= self.h:
                return True
            #if Pixel(pix.x+offset.x, pix.y+offset.y) in self.pixellist:
            if pix.y + offset.y >= 0 and self.grid[pix.x + offset.x][pix.y + offset.y] == 1:
                return True
        return False
        
    def fixTile(self, extile = None):
        tile = extile
        if not tile:
            tile = self.tile
            self.tile = None
        for pix in tile.pixel:
            if pix.y < 0:
                #tile.clearPixel()
                del tile
                return 1
            self.pixellist.append(pix)
            self.grid[pix.x][pix.y] = 1
            if pix.y < self.pixelMaxTop:
                self.pixelMaxTop = pix.y
        tile.clearPixel()
        del tile
        return 0
    
    def clearRows(self):
        numberOfClears = 0
        row = self.h - 1
        while row >= 0:
            foundCompleteRow = True
            for col in range(self.w):
                #if not Pixel(col,row) in self.pixellist:
                if self.grid[col][row] == 0:
                    foundCompleteRow = False
                    break
            if foundCompleteRow:
                self.clearRow(row)
                numberOfClears += 1
            else:
                row -= 1
        return numberOfClears
    
    def clearRow(self, row):
        for r in range(row, -1, -1):
            for c in range(self.w):
                self.grid[c][r] = self.grid[c][r-1] if r > 0 else 0
        if self.graphicsBoard:
            for pix in self.pixellist:
                if pix.y == row:
                    self.graphicsBoard.removeItem(pix.graphicsPixel)
        self.pixellist[:] = [pix for pix in self.pixellist if not pix.y == row]
        for pix in self.pixellist:
            if pix.y < row:
                pix.moveBy(0,1)

    def printGrid(self):
        for r in range(self.h):
            for c in range(self.w):
                print("o" if self.grid[c][r] == 0 else "X", end = '')
            print('')

    
class GraphicsBoard(QtWidgets.QGraphicsScene):
    def __init__(self, board):
        super(GraphicsBoard, self).__init__(0,0,board.w, board.h)
        self.board = board
        self.board.setGraphicsBoard(self)
    
    def drawBorders(self):
        pen = QtGui.QPen()
        pen.setWidth(0) 
        pen.setColor(QtGui.QColor(0,255,255))
        
        h = self.board.h
        w = self.board.w
        self.addLine(0, 0, w, 0, pen)
        self.addLine(0, h, w, h, pen)
        self.addLine(w, 0, w, h, pen)
        self.addLine(0, 0, 0, h, pen)
