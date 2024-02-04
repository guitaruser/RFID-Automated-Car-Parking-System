import mysql.connector as mysql

db = mysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'toor',
    db = 'parking_system'
)

print(db)