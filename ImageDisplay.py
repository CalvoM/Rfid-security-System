from PyQt4 import QtGui
from PyQt4.QtGui import *
import sys

class ImageDisplay(QWidget):
    def __init__(self,img):
        super(ImageDisplay,self).__init__()
        self.img    =img
        self.title  ="Profile Picture Image"
        self.top    =100;
        self.left   =100;
        self.InitWindow()
    def InitWindow(self):
        self.label=QLabel(self)
        self.label.setPixmap(QPixmap(self.img))
        self.label.setGeometry(1,1,1280,960)
        self.setWindowTitle(self.title)
        self.setGeometry(self.top,self.left,765,606)
        self.show()
