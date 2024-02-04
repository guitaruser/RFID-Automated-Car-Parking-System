import mysql.connector as mysql

mydb = mysql.connect(
    host = 'localhost',
    username = 'root',
    password = 'toor',
    db = 'parking_system'
);

myCur = mydb.cursor()
myCur.execute("SHOW TABLES;")
tables = myCur.fetchall()
for table in tables:
    print(table)
