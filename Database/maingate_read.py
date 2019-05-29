import mysql.connector as mysql
import logging
import csv
loggingFormat='%(levelname)s %(user)-8s %(asctime)-15s %(message)s'
logging.basicConfig(format=loggingFormat,filename="./dblog.txt",filemode="a")
data={"user":"MYSQL"}
try:
    connection=mysql.connect(user='Director',host='localhost',password='SaminSky1', db='python')
except Exception as err:
    print("============ INITIALIZATION ERROR ==========")
    print("Please look at dblog.txt for error")
    logging.error(f"The problem is {err}",extra=data)
else:
    success="Successful login to mysql database"
    logging.info(f"{success}",extra=data)
    uid    =input("Please input uid Number: ")
    select_all="select * from maingate;"
    cur     =connection.cursor(buffered=True)
    cur.execute(select_all)
    all_results=cur.fetchall()
    print(all_results)
    with open('display.csv','w') as f:
        fWrite=csv.writer(f)
        fWrite.writerows(all_results)
    sql     ="select * from maingate where uid=%s;"
    #sql="""select * from maingate"""
    try:
        result=cur.execute(sql,(uid,))
        result=cur.fetchone()[6]
    except Exception as err1:
        print("============= QUERY ERROR =================")
        print('Please look at dblog.txt for error')
        logging.error(f"The problem is {err1}",extra=data)
    else:
        if result=='yes':
            sql1    ="update maingate set checkedIn='no',timeOut=now() where uid=%s"
        else:
            sql1    ="update maingate set checkedIn='yes',timeIn=now() where uid=%s"
        cur.execute(sql1,(uid,))
        connection.commit()
        connection.close()