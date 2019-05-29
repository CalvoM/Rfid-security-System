import mysql.connector

config = {  
    'user': 'admin',
    'password': 'LBHASMXVRIHBREST',
    'host': 'sl-eu-lon-2-portal.10.dblayer.com',
    'port': 27843,
    'database': 'compose',

    # Create SSL connection with the self-signed certificate
    # 'ssl_verify_cert': True,
    # 'ssl_ca': 'cert.pem'
}
try:
    conn = mysql.connector.connect(**config)  
except Exception as e:
    print("Error")
    print(e)
else:
    # cur     = connect.cursor()  
    # result  =cur.execute("create table if not exists one (index_number int(11) not null auto_increment,firstName varchar(20),secondName varchar(20), age int(6),primary key(index_number));")

    # # for row in cur:  
    # #     print(row[0])
    # print(result)
    # connect.close()
    num=int(input("How many entries do you expect?"))
    cur         =conn.cursor()
    firstName   =[]
    secondName  =[]
    uid         =[]
    registrationNumber=[]
    sql="create table if not exists mainGate(uid varchar(20) not null,firstName char(16),secondName char(16),registrationNumber varchar(20),checkedIn enum('yes','no'),primary key(uid));"
    cur.execute(sql)
    for x in range(num):
        print(f"================== Entry{x+1} ===================")
        fName               =input('Enter your first name: ')
        firstName.append(fName)
        secName             =input('Enter your second name: ')
        secondName.append(secName)
        uidNum              =input('Enter UID number: ')
        uid.append(uidNum)
        regNumber           =input('Enter your registration Number: ')
        registrationNumber.append(regNumber)
        sql2    ="insert into mainGate (uid,firstName,secondName,registrationNumber,checkedIn) values(%s,%s,%s,%s,'yes');"
        cur.execute(sql2,(uidNum,fName,secName,regNumber))
        conn.commit()
    ####
    # sql="create table if not exists mainGate(uid varchar(20) not null,firstName char(16),secondName char(16),registrationNumber varchar(20),checkedIn enum('yes','no'),primary key(uid));"
    # cur.execute(sql)
    # sql2    ="insert into mainGate (uid,firstName,secondName,registrationNumber,checkedIn) values(%s,%s,%s,%s,'yes');"
    # cur.execute(sql2,(uid[0],firstName[0],secondName[0],registrationNumber[0]))
    # conn.commit()
    # for x in range(num):
    #     sql2    ="insert into mainGate (uid,firstName,secondName,registrationNumber,checkedIn) values(%s,%s,%s,%s,'yes');"
    #     cur.execute(sql2,(uid[x],firstName[x],secondName[x],registrationNumber[x]))
    #     conn.commit()
    conn.close()
