#!/usr/bin/env python

from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import RPi.GPIO as GPIO
import MFRC522
import signal
import time
from IbmCosPic import IbmCosPic
import mysql.connector as dbSql

class RegistrationApp(QWidget):
    def __init__(self,uid1,uid,Mifare):
        super(RegistrationApp,self).__init__()
        self.title  ="STUDENT REGISTRATION"
        self.uid1=uid1
        self.MIFAREReader=Mifare
        self.top    =100;
        self.left   =100;
        self.config={'user':'admin','password':'LBHASMXVRIHBREST','host':'sl-eu-lon-2-portal.10.dblayer.com','port':27843,'database':'compose'}
        self.connection=dbSql.connect(**self.config)
        self.cursor=self.connection.cursor(buffered=True)
        self.InitWindow()
        
    def InitWindow(self):
        self.fBox=QFormLayout()
        self.firstName()
        self.secondName()
        self.regNumber()
        self.picturePick()
        self.submitButton()
        self.setWindowTitle(self.title)
        self.setGeometry(self.top,self.left,1280,960)
        self.setLayout(self.fBox)
        self.show()
        
    def firstName(self):
        self.fnameLabel =QLabel("First Name:")
        self.fnameLine  =QLineEdit()
        self.fnameLine.editingFinished.connect(self.dbFirstName)
        self.fBox.addRow(self.fnameLabel,self.fnameLine)
        
    def dbFirstName(self):
        self.fName=str(self.fnameLine.text())
        data1=self.fName
        data=[]
        if not(len(data1)==16):
            lack=16-len(data1)
            data1=data1+"#"*lack
        # Fill the data with 0xFF
        for x in range(0,16):
            data.append(ord(data1[x]))
        self.MIFAREReader.MFRC522_Write(8,data)
        
    def secondName(self):
        hBox1=QHBoxLayout()
        self.snameLabel =QLabel("Second name:")
        self.snameLine  =QLineEdit()
        self.snameLine.editingFinished.connect(self.dbSecondName)
        self.fBox.addRow(self.snameLabel,self.snameLine)
        
    def dbSecondName(self):
        self.secName=str(self.snameLine.text())
        data1=self.secName
        data=[]
        if not(len(data1)==16):
            lack=16-len(data1)
            data1=data1+"#"*lack
        # Fill the data with 0xFF
        for x in range(0,16):
            data.append(ord(data1[x]))
        self.MIFAREReader.MFRC522_Write(9, data)
        
    def regNumber(self):
        self.regnameLabel =QLabel("Registration Number:")
        self.regnameLine  =QLineEdit()
        self.regnameLine.editingFinished.connect(self.dbRegNum)
        self.regnameLine.setAlignment(Qt.AlignRight)
        self.fBox.addRow(self.regnameLabel,self.regnameLine)
        
    def dbRegNum(self):
        self.regNum=str(self.regnameLine.text())
        data1=self.regNum
        data=[]
        if not(len(data1)==16):
            lack=16-len(data1)
            data1=data1+"#"*lack
        # Fill the data with 0xFF
        for x in range(0,16):
            data.append(ord(data1[x]))
        self.MIFAREReader.MFRC522_Write(10, data)
    
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
        
        create_statement="create table if not exists mainGate(uid varchar(20) not null,firstName char(20) not null,secondName char(20) not null,registrationNumber varchar(20) not null,profilePicture varchar(25) not null,timeIn timestamp,timeOut timestamp default '1970-01-01 00:00:01' ,checkedIn enum('yes','no'),primary key(uid));"
        self.cursor.execute(create_statement)
        check_statement="select uid from maingate where registrationNumber=%s;" 
        self.cursor.execute(check_statement,(self.regNum,))
        regNumber=self.cursor.fetchone()
        if regNumber is not None:
            print('The registration Number {0} exists'.format(self.regNum))
            ledNo(LED_RED,3)
            self.msg=QMessageBox()
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setText('REGISTRATION ERROR')
            self.msg.setInformativeText('The registration Number {0} exists'.format(self.regNum))
            self.msg.exec_()
        else:
            print('Inserting') 
            sql_statement2="insert into mainGate(uid,firstName,secondName,registrationNumber,profilePicture,timeIn,checkedIn) values(%s,%s,%s,%s,%s,now(),'yes')"
            self.cursor.execute(sql_statement2,(self.uid1,self.fName,self.secName,self.regNum,self.uid1))
            one=IbmCosPic()
            print(self.uid1)
            one.ibm_upload_pic('personpictures','./Image/'+self.uid1+'.jpg')
            self.connection.commit()
            self.connection.close()
            self.MIFAREReader.MFRC522_StopCrypto1()
            ledGo(LED_GREEN,2)
            self.msg=QMessageBox()
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText('REGISTRATION COMPLETE!')
            self.msg.setInformativeText('The database has been successfully updated!')
            self.msg.exec_()
            continue_reading = False
            time.sleep(2)
            print('\n')

continue_reading = True
LED_GREEN=40
LED_RED=29
def ledNo(PORT_RED,DELAY):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PORT_RED,GPIO.OUT)
    GPIO.output(PORT_RED,1)
    time.sleep(DELAY)
    GPIO.output(PORT_RED,0)
def ledGo(PORT_GREEN,DELAY):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PORT_GREEN,GPIO.OUT)
    GPIO.output(PORT_GREEN,1)
    time.sleep(DELAY)
    GPIO.output(PORT_GREEN,0)

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()



# Capture SIGINT for cleanup when the script is aborted
MIFAREReader = MFRC522.MFRC522()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
        ledGo(LED_GREEN,2)
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        # Print UID
        print "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])
        uid1="".join(str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3]))
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 9, key, uid)
        print "\n"
        status=0
        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            App=QApplication(sys.argv)
            window=RegistrationApp(uid1,uid,MIFAREReader)
            sys.exit(App.exec_())
            # Variable for the data to write
         ###################################################################################################################
##            data1 = str(raw_input("Enter your name"))
##            fName=data1
##            data=[]
##            if not(len(data1)==16):
##                lack=16-len(data1)
##                data1=data1+"#"*lack
##            # Fill the data with 0xFF
##            for x in range(0,16):
##                data.append(ord(data1[x]))
##
##            print "Writing first name to system"
##            ledGo(LED_GREEN,2)
##            # Write the data
##            MIFAREReader.MFRC522_Write(8, data)
##            print "\n"
##            ###########################################################################################################
##            data1 = str(window.snameLine.text())   
##            secName=data1
##            data=[]
##            if not(len(data1)==16):
##                lack=16-len(data1)
##                data1=data1+"#"*lack
##            # Fill the data with 0xFF
##            for x in range(0,16):
##                data.append(ord(data1[x]))
##
##            print "Writing second name to system"
##            ledGo(LED_GREEN,2)
##           # Write the data
##            MIFAREReader.MFRC522_Write(9, data)
##            print "\n"
###############################################################################################################
##            data1 = str(window.regnameLine.text())
##            regNum=data1
##            data=[]
##            if not(len(data1)==16):
##                lack=16-len(data1)
##                data1=data1+"#"*lack
##            # Fill the data with 0xFF
##            for x in range(0,16):
##                data.append(ord(data1[x]))
##
##            print "Writing registration number to system"
##            ledGo(LED_GREEN,2)
##          # Write the data
##            MIFAREReader.MFRC522_Write(10, data)
##            print "\n"
            window.finishStuff()
##            MIFAREReader.MFRC522_StopCrypto1()
##            continue_reading = False
##            time.sleep(2)
##            print('\n')
            #################################################################################################
           #######################################################################################################
           # Stop
##            create_statement="create table if not exists maingate(uid varchar(20) not null,firstName char(20) not null,secondName char(20) not null,registrationNumber varchar(20) not null,profilePicture varchar(25) not null,timeIn timestamp,timeOut timestamp default '1970-01-01 00:00:01' ,checkedIn enum('yes','no'),primary key(uid));"
##            cursor.execute(create_statement)
##            check_statement="select uid from maingate where registrationNumber=%s;" 
##            cursor.execute(check_statement,(regNum,))
##            regNumber=cursor.fetchone()
##            if regNumber is not None:
##                print('The registration Number {0} exists'.format(regNum))
##                ledNo(LED_RED,3)
##            else:
##                print('Inserting') 
##                sql_statement2="insert into maingate(uid,firstName,secondName,registrationNumber,profilePicture,timeIn,checkedIn) values(%s,%s,%s,%s,%s,now(),'yes')"
##                cursor.execute(sql_statement2,(uid1,fName,secName,regNum,uid1))
##                one=IbmCosPic()
##                print(uid1)
##                one.ibm_upload_pic('personpictures','./Image/'+uid1+'.jpg')
##                connection.commit()
##                connection.close()
              

            # Make sure to stop reading for cards
                
        else:
            print "Authentication error"
            ledNo(LED_RED,3)

