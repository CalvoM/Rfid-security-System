from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

class RegistrationApp(QWidget):
    def __init__(self):
        super(RegistrationApp,self).__init__()
        self.title  ="STUDENT REGISTRATION"
        self.top    =100;
        self.left   =100;
        self.InitWindow()
    def InitWindow(self):
        self.fBox=QFormLayout()
        self.firstName()
        self.secondName()
        self.regNumber()
        self.picturePick()
        self.submitButton()
        self.setWindowTitle(self.title)
        self.setGeometry(self.top,self.left,600,600)
        self.setLayout(self.fBox)
        self.show()
    def firstName(self):
        self.fnameLabel =QLabel("First Name:")
        self.fnameLine  =QLineEdit()
        self.fBox.addRow(self.fnameLabel,self.fnameLine)
    
    def secondName(self):
        hBox1=QHBoxLayout()
        self.snameLabel =QLabel("Second name:")
        self.snameLine  =QLineEdit()
        self.fBox.addRow(self.snameLabel,self.snameLine)
        
    def regNumber(self):
        self.snameLabel =QLabel("Registration Number:")
        self.snameLine  =QLineEdit()
        self.snameLine.setAlignment(Qt.AlignRight)
        self.fBox.addRow(self.snameLabel,self.snameLine)
    
    def picturePick(self):
        hBox1=QHBoxLayout()
        self.contents=QLineEdit()
        self.contents .setAlignment(Qt.AlignRight)
        self.pnameLabel =QLabel("Profile Picture:")
        self.pnameButton=QPushButton('Select Profile Picture')
        self.pnameButton.clicked.connect(self.getProfilePic)
        self.fBox.addRow(self.pnameLabel,self.pnameButton)
        self.fBox.addRow(QLabel('File name:'),self.contents)
    
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
        self.btn.setGeometry(50,100,20,30)
        self.fBox.addRow(self.btn)
        self.btn.setStyleSheet("background-color:green;color:yellow")
        self.btn.clicked.connect(self.finishStuff)
    
    def finishStuff(self):
        self.msg=QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText('REGISTRATION COMPLETE!')
        self.msg.setInformativeText('The database has been successfully updated!')
        self.msg.exec_()
#begin GUI App
#begin GUI App
if __name__=='__main__':
    App=QApplication(sys.argv)
    window=RegistrationApp()
    sys.exit(App.exec_())
