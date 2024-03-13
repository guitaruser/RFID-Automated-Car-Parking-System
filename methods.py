import mysql.connector as mysql
from datetime import datetime
import csv
mydb = mysql.connect(
    host = 'localhost',
    username = 'root',
    password = 'toor',
    db = 'parking_system'
);
trial_text = "This works"
myCur = mydb.cursor()

''' Function to Flush The Log DB '''
def flush_db():
    try:
        myCur.execute(f'DELETE FROM log')
        myCur.execute(f'ALTER TABLE log AUTO_INCREMENT=1;')
        mydb.commit()
        
    except Exception as e:
        mydb.rollback()
        print(e)


''' Function to dump log from DB to a file '''
def dump_log_to_file():
    try:
        file = open('trial.csv','a',newline='')
        writer = csv.writer(file)
        datas = dump_log()
        writer.writerows(datas)
        file.close()
        flush_db()
    except Exception as E:
        print(E)
        return -1

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
        return True
    except:
        print("Didn't work")
        mydb.rollback()
        return False

''' Function to store the car details in parked_cars ''' 
def store_car(rfid, types, slot):
    try:
        myCur.execute(f'INSERT INTO parked_cars(RFID, type, SLOT) VALUES("{rfid}","{types}",{slot})')
        mydb.commit()
        return True
    except:
        return False

''' Function to store the Time when a car enters parking lot ''' 
def store_time(rfid):
    try:
        now_time = get_time()
        myCur.execute(f'INSERT INTO in_time(RFID, in_time) VALUES("{rfid}","{now_time}")')
        mydb.commit()
        return True
    except:
        return False

''' Function to get the Time when a car enters parking lot ''' 
def get_in_time(rfid):
    try:
        myCur.execute(f'select in_time from in_time where RFID = "{rfid}"')
        in_time = myCur.fetchone()[0]      
        return in_time
    except:
        return -1 

''' Function to store the car details in log ''' 
def store_in_log(rfid):
    try:
        if check_emp(rfid):
            types = "Emp"
        else:
            types = "Cust"
        # types = "Cust"
        in_time = get_in_time(rfid)
        out_time = get_time()
        myCur.execute(f'INSERT INTO log(RFID, type, in_time, out_time) values("{rfid}","{types}","{in_time}","{out_time}");')
        mydb.commit()
        return True
    except:
        return False

''' Function to remove the car details from everywhere not needed ''' 
def flush_from_db(rfid):
    try:
        myCur.execute(f'SELECT slot from parked_cars where RFID="{rfid}"')
        slot = myCur.fetchall()[0][0]
        myCur.execute(f'UPDATE slots SET is_empty=1 WHERE slot={slot}')
        myCur.execute(f'DELETE FROM in_time where RFID = "{rfid}"')
        myCur.execute(f'DELETE FROM parked_cars where RFID = "{rfid}"')
        mydb.commit()
        return True
    except Exception as e:
        mydb.rollback()
        return False
    
''' Function to get all info from log ''' 
def dump_log():
    try:
        myCur.execute(f'select * from log')
        log = myCur.fetchall()    
        return log
    except:
        return -1 
    
''' Function to Calculate Rate ''' 
def get_rate(rfid):
    fixed_rate = 20
    time_now = get_time()
    in_time = str(get_in_time(rfid))
    rate = ((int(time_now[0:2]))-int(in_time[0:2]))*12
    return fixed_rate+rate

# Checking
# if check_emp('RFID0002'):
#     print('Valid EMP')
# else:
#     print('Not an emp')
# # print(check_slot())  
# store_car('RFID0007', 'CUST', 2)
# book_slot(1)
# print(get_time())
# store_time("RFID0001")
# print(store_in_log("RFID0003"))
# flush_from_db("RFID0007")
dump_log_to_file()