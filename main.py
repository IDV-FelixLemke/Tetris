import sys, random, os
from PyQt5 import QtWidgets, QtGui, QtCore

from board import *
from game import Game

saveFile = './AIsave.py'

class BoardView(QtWidgets.QGraphicsView):
    def __init__(self, scene, board):
        super(BoardView, self).__init__(scene)
        self.board = board
    def resizeEvent(self, event):
        self.fitInView(0, 0, self.board.w, self.board.h, QtCore.Qt.KeepAspectRatio)
        super(BoardView, self).resizeEvent(event)
        
class App(QtWidgets.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.build_ui()
        
        self.newGame()
                
    def gameEnded(self):
        self.label.setText("Verloren")

    def newGame(self):
        self.game = Game(self.board, self)
        self.game.score = 0
        self.newScore(0)

        self.game.startGame(100)


    def newScore(self, score):
        self.scoreLabel.setText("Score: " + str(score))

    def build_ui(self):
        # build a main GUI window
        self.main_window = QtWidgets.QMainWindow()
        self.central_widget = QtWidgets.QWidget()

        # devide game layout into board and information section
        hBox = QtWidgets.QHBoxLayout()
        self.central_widget.setLayout(hBox)

        self.board = Board()
        self.scene = GraphicsBoard(self.board)
        self.scene.drawBorders()
                        
        view = BoardView(self.scene, self.board)
        view.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.black))
        hBox.addWidget(view)
        view.fitInView(0, 0, self.board.w, self.board.h, QtCore.Qt.KeepAspectRatio)

        # add a label to the main window
        self.label = QtWidgets.QLabel('Go Go')
        hBox.addWidget(self.label)
        self.scoreLabel = QtWidgets.QLabel("Score: 0")
        hBox.addWidget(self.scoreLabel)

        self.central_widget.keyPressEvent = self.keyPressEvent

        self.main_window.setWindowTitle('Tetris')
        self.main_window.setCentralWidget(self.central_widget)
        self.main_window.show()
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_A:
            self.game.moveDir = Pos(-1,0)
        elif event.key() == QtCore.Qt.Key_D:
            self.game.moveDir = Pos(1,0)
        elif event.key() == QtCore.Qt.Key_W:
            self.game.rotate = True
        event.accept()
    
if __name__ == '__main__':
    random.seed()
    
    app = App(sys.argv)
    sys.exit(app.exec_())
    
