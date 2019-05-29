#import pymysql as mysql
import mysql.connector as mysql
try:
    conn=mysql.connect(host='localhost',user='Director',password='SaminSky1',db='python')
except Exception as e: 
    print(e)
else:
    num=int(input("How many entries do you expect?"))
    cur         =conn.cursor(buffered=True)
    firstName   =[]
    secondName  =[]
    uid         =[]
    registrationNumber=[]
    for x in range(num):
        print(f"================== Entry{x+1} ===================")
        fName               =str(input('Enter your first name: '))
        firstName.append(fName)
        secName             =str(input('Enter your second name: '))
        secondName.append(secName)
        uidNum              =str(input('Enter UID number: '))
        uid.append(uidNum)
        regNumber           =str(input('Enter your registration Number: '))
        registrationNumber.append(regNumber)

    sql="create table if not exists maingate(uid varchar(20) primary key,firstName char(16),secondName char(16),registrationNumber varchar(20),timeIn timestamp,timeOut timestamp,checkedIn enum('yes','no'));"
    cur.execute(sql)
    for x in range(num):
        sql2    ="select firstName,secondName from maingate where uid=%s;"
        cur.execute(sql2,(uid[x],))
        name=cur.fetchone()
        if name is not None:
            print(f'The Uid {uid[x]} is registered already')
            continue
        else:
            sql3    ="select firstName,secondName from maingate where registrationNumber=%s;"
            cur.execute(sql3,(registrationNumber[x],))
            number=cur.fetchone()
            if number is not None:
                print(f'The registration Number {registrationNumber[x]} is already registered in the system')
                continue
            else:
                sql4    ="insert into maingate (uid,firstName,secondName,registrationNumber,timeIn,checkedIn) values(%s,%s,%s,%s,now(),'yes');"
                cur.execute(sql4,(uid[x],firstName[x],secondName[x],registrationNumber[x]))
                conn.commit()
    conn.close()
