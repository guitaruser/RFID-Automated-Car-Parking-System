import mysql.connector as mysql
from datetime import datetime
mydb = mysql.connect(
    host = 'localhost',
    username = 'root',
    password = 'toor',
    db = 'parking_system'
);

myCur = mydb.cursor()

''' Function to get the current time in HH:MM:SS Format '''
def get_time():
    try:
        c = datetime.now()
        current_time = c.strftime('%H:%M:%S')
        return current_time
    except:
        return -1

''' Function to check if the car belongs to an emp '''
def check_emp(rfid):
    myCur.execute(f'SELECT * from emp where RFID="{rfid}"')
    records = myCur.fetchall()
    if records != []:
        return True
    else:
        return False

''' Function to check which slots are available and allot one '''
def check_slot():
    myCur.execute(f'SELECT slot from slots where is_empty = 1')
    slot_result = myCur.fetchall()
    if slot_result == []:
        return -1
    else:
        return slot_result[0][0]
    
''' Function to book a slot '''
def book_slot(slot_no):
    try:
        myCur.execute(f'UPDATE slots SET is_empty=0 where slot = {int(slot_no)}')
        mydb.commit()
        print(f"Slot {slot_no} is booked, please procede")
    except:
        print("Didn't work")
        mydb.rollback()

''' Function to store the car details in parked_cars ''' 
def store_car(rfid, type, slot):
    try:
        myCur.execute(f'INSERT INTO parked_cars(RFID, type, SLOT) VALUES("{rfid}","{type}",{slot})')
        mydb.commit()
        return True
    except:
        return False

# Checking
# if check_emp('RFID0002'):
#     print('Valid EMP')
# else:
#     print('Not an emp')
# print(check_slot())  
# store_car('RFID0007', 'CUST', 2)
# book_slot(1)
    
get_time()