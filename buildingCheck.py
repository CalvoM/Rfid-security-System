import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import mysql.connector as dbSql
from IbmCosPic import IbmCosPic
continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
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
            status_check="select * from maingate where uid=%s;"
            curs.execute(status_check,(uid1,))
            mainResult=curs.fetchone()

            if mainResult is None:
                print('Not registered in main Register.VISITOR!')
            else:
                checking_statement="select checkedIn from building where uid=%s;"
                curs.execute(checking_statement,(uid1,))
                result=curs.fetchone()
                connection.commit()
                if result is None:
                    insert_statement="insert into building(uid,timeIn,checkedIn) values(%s,now(),'yes');"
                    curs.execute(insert_statement,(uid1,))
                    connection.commit()
                else:
                    result=result[0]
                    if result=='yes':
                        time_check="select time_to_sec(timediff(now(),timeIn)) from building where uid=%s;"
                        curs.execute(time_check,(uid1,))
                        time_diff=curs.fetchone()[0]
                        if time_diff <15:
                            print('Insufficient Time To update!')
                        else:
                            update_statement="update building set checkedIn='no',timeOut=now() where uid=%s;"
                            curs.execute(update_statement,(uid1,))
                    elif result=='no':
                        time_check="select time_to_sec(timediff(now(),timeOut)) from building where uid=%s;"
                        curs.execute(time_check,(uid1,))
                        time_diff=curs.fetchone()[0]
                        if time_diff <15:
                            print('Insufficient Time to update!')
                        else:
                            update_statement="update building set checkedIn='yes',timeIn=now() where uid=%s;"
                            curs.execute(update_statement,(uid1,))
                            picture_capture="select profilePicture from maingate where uid=%s;"
                            curs.execute(picture_capture,(uid1,))
                            picName=curs.fetchone()[0]+'.jpg'
                            print(picName)
                            pic_display=IbmCosPic()
                            pic_display.ibm_download_pic('personpictures','Image/'+picName)
                    connection.commit()
                    connection.close()
            print('DB DONE')  
        else:
            print "Authentication error"
        time.sleep(1)

