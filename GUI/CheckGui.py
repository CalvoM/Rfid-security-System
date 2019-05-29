import sys
import os
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class StopCheck(QWidget):
    def __init__(self):
        super(StopCheck,self).__init__()
        self.title  ="CHECK POINT RECOGNITION"
        self.height =350
        self.width  =350
        self.top    =100
        self.left   =100
        self.initWindow()
    
    def initWindow(self):
        self.fbox=QGridLayout()
        self.firstNameLabelling()
        self.registrationNumberLabelling()
        self.secondNameLabelling()
        self.errorLabel()
        self.setWindowTitle(self.title)
        self.setGeometry(self.top,self.left,self.width,self.height)
        self.setLayout(self.fbox)
        self.show()
    
    def firstNameLabelling(self):
        self.fNameLabel     =QLabel('FIRST NAME:')
        self.unFNameLabel   =QLineEdit()
        self.fbox.addWidget(self.fNameLabel,0,0)
        self.fbox.addWidget(self.unFNameLabel,0,1)

    def secondNameLabelling(self):
        self.sNameLabel     =QLabel('SECOND NAME:')
        self.unSNameLabel   =QLineEdit()
        self.fbox.addWidget(self.sNameLabel,1,0)
        self.fbox.addWidget(self.unSNameLabel,1,1)
    
    def registrationNumberLabelling(self):
        self.regNumLabel    =QLabel('REGISTRATION NUMBER:')
        self.unregNumLabel  =QLineEdit()
        self.fbox.addWidget(self.regNumLabel,2,0)
        self.fbox.addWidget(self.unregNumLabel,2,1)
    
    def errorLabel(self):
        self.errorNoticeLabel=QLabel('ERROR')
        self.errorLine       =QTextEdit()
        self.fbox.addWidget(self.errorNoticeLabel,3,0)
        self.fbox.addWidget(self.errorLine,4,1)


App=QApplication(sys.argv)
stop=StopCheck()
stop.errorLine.setText("<font color=red size=10>Hey</font>")
sys.exit(App.exec_())
