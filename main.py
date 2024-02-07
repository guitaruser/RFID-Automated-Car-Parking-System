# import mysql.connector as mysql
from prettytable import PrettyTable
import methods 
# db = mysql.connect(
#     host = 'localhost',
#     user = 'root',
#     password = 'toor',
#     db = 'parking_system'
# )
''' Logic For Program '''

table_struct = PrettyTable(["SI","RFID","TYPE","IN TIME","OUT TIME"])

def get_rate(rfid):
    fixed_rate = 20
    time_now = methods.get_time()
    in_time = str(methods.get_in_time(rfid))
    rate = ((int(time_now[0:2]))-int(in_time[0:2]))*12
    return fixed_rate+rate

if __name__ == "__main__":
    while True:
        print('1. Park Car\n2. See Log\n3. Remove Car\n4. Exit')
        choice = int(input("Enter your choice: "))
        if choice == 1:
            rfid = input("Enter The Car RFID: ")
            if methods.check_emp(rfid):
                types = "Emp"
            else:
                types = "Cust"
            try:
                slot = methods.check_slot()
                if slot != -1:
                    methods.book_slot(slot)
                    try:
                        methods.store_time(rfid)
                        methods.store_car(rfid,types,slot)
                        print(f"CAR {rfid} IS SET TO PARK IN SLOT {slot}")
                    except Exception as e1:
                        print(e1)
            except Exception as e:
                print(e)       

        elif choice == 2:
            table_struct.clear_rows()
            log_files = methods.dump_log()
            table_struct.add_rows(log_files)
            print(table_struct)
            print('\n\n')
        
        elif choice == 3:
            rfid = input("Enter RFID OF car: ")
            if methods.check_emp(rfid):
                pass
            else:
                rate = get_rate(rfid)
                print(f"Please Pay {rate}\n")
            try:
                if methods.store_in_log(rfid):
                    if methods.flush_from_db(rfid):
                        print("Thank you, please procede")
                    else:
                        print("Something Went Wrong")
                else:
                    print("Something is wrong")
            except Exception as e:
                print(e)

        elif choice == 4:
            break

        else:
            print("Wrong Command! Try Again!\n")

    