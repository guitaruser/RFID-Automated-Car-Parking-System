# import mysql.connector as mysql

# mydb = mysql.connect(
#     host = 'localhost',
#     username = 'root',
#     password = 'toor',
#     db = 'parking_system'
# );

# myCur = mydb.cursor()
# myCur.execute("SHOW TABLES;")
# tables = myCur.fetchall()
# for table in tables:
#     print(table)

import methods

def get_rate(rfid):
    fixed_rate = 20
    time_now = methods.get_time()
    in_time = str(methods.get_in_time(rfid))
    rate = ((int(time_now[0:2]))-int(in_time[0:2]))*12
    return fixed_rate+rate

print(get_rate("RFID0006"))