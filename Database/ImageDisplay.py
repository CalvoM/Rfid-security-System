from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication,QMainWindow,QLabel
from PyQt5.QtGui import QPixmap
import sys

class ImgDisp(QMainWindow):
    def __init__(self,img):
        super().__init__()
        self.img=img
        self.title ="Profile Picture Image"
        self.top   =100
        self.left  =100
        self.InitWindow()

    def InitWindow(self):
        self.label=QLabel(self)
        self.label.setPixmap(QPixmap(self.img))
        self.label.setGeometry(1,1,763,604)
        self.setWindowTitle(self.title)
        self.setGeometry(self.top,self.left,765,606)
        self.show()

# App=QApplication(sys.argv)
# window=ImgDisp()
# sys.exit(App.exec_())