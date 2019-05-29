#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Mario Gomez <mario.gomez@teubi.co>
#
#    This file is part of MFRC522-Python
#    MFRC522-Python is a simple Python implementation for
#    the MFRC522 NFC Card Reader for the Raspberry Pi.
#
#    MFRC522-Python isffree software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MFRC522-Python is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with MFRC522-Python.  If not, see <http://www.gnu.org/licenses/>.
#

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import mysql.connector as dbSql
from IbmCosPic import IbmCosPic

continue_reading = True

LED_GREEN=40
LED_RED  =29

# Capture SIGINT for cleanup when the script is aborted
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

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
config={
    "user":"admin",
    "password":"LBHASMXVRIHBREST",
    "host":"sl-eu-lon-2-portal.9.dblayer.com",
    "database":"compose",
    "port":27843
   # "ssl_verify_cert":True,
    #"ssl_ca":"cert.pem"
    }


# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Tumekucheki Cardi"
        ledGo(LED_GREEN,2)
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])
    
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 9, key, uid)
        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            print("First Name: ")
            fName=MIFAREReader.MFRC522_Read(8)
            print(fName)
            print('\n')
            print("Second Name: ")
            secName=MIFAREReader.MFRC522_Read(9)
            print(secName)
            print('\n')
            print("Registration Number: ")
            regNum=MIFAREReader.MFRC522_Read(10)
            print(regNum)
            print('\n')
            uid1="".join(str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3]))
            MIFAREReader.MFRC522_StopCrypto1()
            connection=dbSql.connect(**config)
            curs=connection.cursor(buffered=True)
            checking_statement="select checkedIn from mainGate where uid=%s;"
            curs.execute(checking_statement,(uid1,))
            result=curs.fetchone()
            if result is None:
                print('Not found in the registration.VISITOR!!')
                ledNo(LED_RED,3)
            else:
                result=result[0]
                if result=='yes':
                    time_check="select time_to_sec(timediff(now(),timeIn)) from mainGate where uid=%s;"
                    curs.execute(time_check,(uid1,))
                    time_diff=curs.fetchone()[0]
                    if time_diff <15:
                        print('The time difference is small for update')
                        ledNo(LED_RED,2)
                    else:
                        update_statement="update mainGate set checkedIn='no',timeOut=now() where uid=%s;"
                        curs.execute(update_statement,(uid1,))
                elif result=='no':
                    time_check="select time_to_sec(timediff(now(),timeOut)) from mainGate where uid=%s;"
                    curs.execute(time_check,(uid1,))
                    time_diff=curs.fetchone()[0]
                    if time_diff <15:
                        print('The time difference is small for update')
                        ledNo(LED_RED,2)
                    else:
                        update_statement="update mainGate set checkedIn='yes',timeIn=now() where uid=%s;"
                        curs.execute(update_statement,(uid1,))
                        picture_capture="select profilePicture from mainGate where uid=%s;"
                        curs.execute(picture_capture,(uid1,))
                        picName=curs.fetchone()[0]+'.jpg'
                        print(picName)
                        pic_display=IbmCosPic()
                        pic_display.ibm_download_pic('personpictures','Image/'+picName)
                connection.commit()
                connection.close()
            print('DB DONE')  
            ledGo(40,3)
        else:
            print "Authentication error"
        time.sleep(1)

