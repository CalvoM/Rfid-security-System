from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import cv2
import capturePhoto

class RegistrationApp(QDialog):
    def __init__(self):
        super(RegistrationApp,self).__init__()
        self.title  ="STUDENT REGISTRATION"
        self.top    =100
        self.left   =100
        self.width  =500
        self.height =50
        self.InitWindow()
    def InitWindow(self):
        self.fBox=QGridLayout()
        self.firstName()
        self.secondName()
        self.regNumber()
        self.picturePick()
        self.submitButton()
        self.pictureButton()
        self.setWindowTitle(self.title)
        self.setGeometry(self.top,self.left,self.width,self.height)
        self.setLayout(self.fBox)
        self.show()
    def firstName(self):
        self.fnameLabel =QLabel("First Name:")
        self.fnameLine  =QLineEdit()
        self.fnameLabel.setFrameStyle(QFrame.Sunken)
        self.fBox.addWidget(self.fnameLabel,0,0)
        self.fBox.addWidget(self.fnameLine,0,1)
    
    def secondName(self):
        self.snameLabel =QLabel("Second name:")
        self.snameLine  =QLineEdit()
        self.fBox.addWidget(self.snameLabel,1,0)
        self.fBox.addWidget(self.snameLine,1,1)
        
    def regNumber(self):
        self.regnameLabel =QLabel("Registration Number:")
        self.regnameLine  =QLineEdit()
        self.regnameLine.setAlignment(Qt.AlignRight)
        self.fBox.addWidget(self.regnameLabel,2,0)
        self.fBox.addWidget(self.regnameLine,2,1)
    
    def picturePick(self):
        hBox1=QHBoxLayout()
        self.contents=QLineEdit()
        self.contents .setAlignment(Qt.AlignRight)
        self.pnameLabel =QLabel("Profile Picture:")
        self.pnameButton=QPushButton('Select Profile Picture')
        self.pnameButton.clicked.connect(self.getProfilePic)
        self.fBox.addWidget(self.pnameLabel,3,0)
        self.fBox.addWidget(self.pnameButton,3,1)
        self.fBox.addWidget(QLabel('File name:'),4,0)
        self.fBox.addWidget(self.contents,4,1)
    
    def getProfilePic(self):
        dlg=QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter("Profile Picture (*.jpg)")
        filename=QStringList()
        if dlg.exec_():
            filename=dlg.selectedFiles()
            f=open(filename[0],'r')
            with f:
                data=f.read()
                self.contents.setText(filename[0])
        
    def submitButton(self):
        self.btn=QPushButton('REGISTER')
        self.fBox.addWidget(self.btn,6,0)
        self.btn.setStyleSheet("background-color:green;color:yellow")
        self.btn.clicked.connect(self.finishStuff)
    
    def finishStuff(self):
        self.msg=QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText('REGISTRATION COMPLETE!')
        self.msg.setInformativeText('The database has been successfully updated!')
        self.msg.exec_()
    
    def pictureButton(self):
        self.picBtn=QPushButton('PROFILE PICTURE CAPTURE')
        self.fBox.addWidget(self.picBtn,5,0)
        self.picBtn.clicked.connect(self.capturePicture)
    
    def capturePicture(self):
        cap=cv2.VideoCapture(0)

        while True:
            ret,frame=cap.read()
            cv2.imshow('img1',frame)
            k=cv2.waitKey(1)
            if k ==32:
                cv2.imwrite('Calvin.jpg',frame)
                cv2.destroyAllWindows()
                break
            elif k==ord('c'):
                print('Hey')
        cap.release()
#begin GUI App
#begin GUI App
if __name__=='__main__':
    App=QApplication(sys.argv)
    window=RegistrationApp()
    sys.exit(App.exec_())
