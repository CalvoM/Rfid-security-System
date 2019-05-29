import mysql.connector as dbSql
from PyQt5.QtWidgets import QApplication
from ImageDisplay import ImgDisp
import sys
import time

try:
    connection=dbSql.connect(host='localhost',user='Director',password='SaminSky1',db='python')
except Exception as err:
    print(err)
else:
    cursor                  =connection.cursor(buffered=True)
    create_table_statement  ="create table if not exists building(uid varchar(20),timeIn timestamp,timeOut timestamp,buildingName varchar(20),checkedIn enum('yes','no'));"
    cursor.execute(create_table_statement)
    uid                     =input('Please Enter your UID Number:')
    select_statement        ="select ProfilePic from maingate where uid=%s;"
    cursor.execute(select_statement,(uid,))
    picture         =cursor.fetchone()[0]
    if picture is None:
        print(f'No Picture found for the uid number {uid}')
    else:
        print(f'Successfully found the Profile picture for {uid}')
        App             =QApplication(sys.argv)
        window          =ImgDisp(picture)
        App.exec_()
        checking_statement="select checkedIn from building where uid=%s and buildingName='ELB';"
        cursor.execute(checking_statement,(uid,))
        checkResult=cursor.fetchone()
        if checkResult==None:
            insert_statement="insert into building(uid,timeIn,buildingName,checkedIn) values(%s,now(),'ELB','yes');"
            cursor.execute(insert_statement,(uid,))
            connection.commit()
        else:
            if checkResult[0]=='yes':
                update_statement="update building set checkedIn='no',timeOut=now();"
            else:
                update_statement="update building set checkedIn='yes',timeIn=now();"
            cursor.execute(update_statement)
            connection.commit()
        connection.close()