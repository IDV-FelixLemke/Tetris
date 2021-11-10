from PyQt5 import QtWidgets, QtGui, QtCore

class Pixel:
    graphicsPixel = None
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.graphicsPixel = None
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def setGraphicsPixel(self, gPixel):
        self.graphicsPixel = gPixel

    def moveTo(self, x, y):
        self.x = x
        self.y = y
        if self.graphicsPixel:
            self.graphicsPixel.setPos(self.x, self.y)
    
    def moveBy(self, dx, dy):
        self.x += dx
        self.y += dy
        if self.graphicsPixel:
            self.graphicsPixel.setPos(self.x,self.y) #(self.x, self.y)
    
class GraphicsPixel(QtWidgets.QGraphicsRectItem):
    def __init__(self, pixel):
        super(GraphicsPixel, self).__init__(0, 0, 1, 1)
        self.setPos(pixel.x, pixel.y)
        self.pixel = pixel
        self.pixel.setGraphicsPixel(self)
        pen = QtGui.QPen(QtCore.Qt.cyan)
        pen.setWidth(0)
        self.setPen(pen)
    
    def setColor(self, color):
         self.setBrush(QtGui.QBrush(color))
        
