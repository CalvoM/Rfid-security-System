import mysql.connector as dbSql
from PyQt5.QtWidgets import QApplication
from ImageDisplay import ImgDisp
import sys
try:
    connection  =dbSql.connect(host='localhost',user='Director',password='SaminSky1',db='python')
except Exception as err:
    print(err)
else:
    cursor          =connection.cursor(buffered=True)
    # alter_statement ="alter table maingate add ProfilePic varchar(20);"
    # cursor.execute(alter_statement)
    insert_statement="update maingate set ProfilePic='./ProfPic1.jpg' where firstName='Calvin';"
    cursor.execute(insert_statement)
    connection.commit()
    select_statement="select ProfilePic from mainGate where firstName='Calvin';"
    cursor.execute(select_statement)
    pic             =cursor.fetchone()
    print(pic[0])
    App =QApplication(sys.argv)
    win =ImgDisp(pic[0])
    sys.exit(App.exec_())
    connection.close()