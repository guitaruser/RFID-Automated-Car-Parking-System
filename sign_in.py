import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter.messagebox import *
from PIL import Image, ImageTk
import methods

class Login:
    def __init__(self,root):

        # 2D list of users
        self.users = [['user','pass']]

        # Tkinter FrontEnd
        self.root = root
        self.root.title('Admin Login System')
        self.root.geometry('1199x600+100+50')
        #self.root.resizable(False,False)

        # Loading Image
        # self.original_image = Image.open("C://Users//kstar//Documents//DBMS Project//modern-login//bg.png")
        # self.bg = tk.PhotoImage(self.original_image)
        self.bg = tk.PhotoImage(file='bg.png')

        # Label to put the image on
        self.bg_image = tk.Label(root,image=self.bg)
        self.bg_image.place(x=0,y=0,relwidth=1,relheight=1)

        # Login Frame
        frame_login = tk.Frame(self.root,bg='white')
        frame_login.place(x=150,y=150,height=340,width=500)

        # Top Title Area
        title_label = tk.Label(frame_login,text='Admin Login',font=('Helvetica',35,'bold'),bg='White',fg='#005B96')
        title_label.place(x=100,y=20)

        # message_label = tk.Label(frame_login,text='Admin Login Area',font=('Gouly old style',15,'bold'),bg='White',fg='#005B96')
        # message_label.place(x=140,y=80)

        # Username
        username_label = tk.Label(frame_login,text='Username',font=('Gouly old style',12),bg='White',fg='Black')
        username_label.place(x=60,y=120)

        self.username_entry = tk.Entry(frame_login,font=('times new roman',15),bg='#005B96',fg='White')
        self.username_entry.place(x=60,y=150,width=350,height=35)

        # password
        password_label = tk.Label(frame_login,text='Password',font=('Gouly old style',12),bg='White',fg='Black')
        password_label.place(x=60,y=200)

        self.password_entry = tk.Entry(frame_login,font=('times new roman',15),bg='#005B96',fg='White')
        self.password_entry.place(x=60,y=230,width=350,height=35)

        # forgot password button
        forget_button = tk.Button(frame_login,text='Forget Password?',font=('times new roman',10),borderwidth=0,bg='White',fg='#005B96')
        forget_button.place(x=60,y=270)

        # submit button
        submit_button = tk.Button(self.root,text='Login',font=('times new roman',20,'bold'),bg='#005B96',fg='White',relief='raised',command=self.login)
        submit_button.place(x=300,y=470,width=180,height=40)

    def clear_screen(self):
        # self.root.quit()
        # self.main.iconify()
        item_list = self.root.winfo_children()
        for widget in item_list:
            widget.destroy()
        Admin_work(self.root)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == '' or password == '':
            showerror('Empty','Entry is Empty! Please Enter Username and Password')
        else:
            for user in self.users:
                if username == user[0] and password == user[1]:
                    showinfo('Correct',f'Welcome Admin\nSigning you in...')
                    self.username_entry.delete(0,tk.END)
                    self.password_entry.delete(0,tk.END)
                    self.clear_screen()
                    break
                elif username == user[0] and password != user[1]:
                    showerror('Wrong password','Wrong password Entered, Please try again')
                    self.password_entry.delete(0,tk.END)
                    break
            else:
                showerror('User Not Found','This Account Doesnt exist. Please Sign Up')

class Admin_work(Login):
    def __init__(self, root):
        self.root = root
        self.root.title('Admin Login System')
        self.root.geometry('1000x600+100+50')
        self.bg = tk.PhotoImage(file='bg.png')

        title_label = tk.Label(self.root,text='Please Select An Action',font=('Helvetica',35,'bold'),fg='#005B96')
        title_label.place(x=240,y=80)

        park_car_button = tk.Button(self.root,text='Park Car',font=('times new roman',10),height= 10, width=10,bg='#005B96',fg='#FFFFFF',command=self.park_car)
        park_car_button.place(x=250,y=200)

        remove_car_button = tk.Button(self.root,text='Remove Car',font=('times new roman',10),height= 10, width=10,bg='#005B96',fg='#FFFFFF',command=self.remove_car)
        remove_car_button.place(x=350,y=200)

        see_log_button = tk.Button(self.root,text='See Log',font=('times new roman',10),height= 10, width=10,bg='#005B96',fg='#FFFFFF',command=self.see_log)
        see_log_button.place(x=450,y=200)

        export_log_button = tk.Button(self.root,text='Export Log',font=('times new roman',10),height= 10, width=10,bg='#005B96',fg='#FFFFFF',command=self.copy_log)
        export_log_button.place(x=550,y=200)

        quit_button = tk.Button(self.root,text='Quit',font=('times new roman',10),height= 10, width=10,bg='#005B96',fg='#FFFFFF',command=self.root.quit)
        quit_button.place(x=650,y=200)

    def park_car(self):
        splash_screen = tk.Toplevel()
        splash_screen.geometry("900x600+150+150")
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
            else:
                showerror("Error","All Slots are Full")
        except Exception as e:
            print(e)

    def remove_car(self):
        splash_screen_2 = tk.Toplevel()
        splash_screen_2.geometry("900x600+150+150")
        title_label = tk.Label(splash_screen_2,text='Please Keep RFID',font=('Helvetica',35,'bold'),fg='#005B96')
        title_label.place(x=240,y=80)
        rfid = input("Enter RFID OF car: ")
        if methods.check_emp(rfid):
            pass
        else:
            rate = methods.get_rate(rfid)
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

    def see_log(self):
        log_files = methods.dump_log()
        splash_screen_3 = tk.Toplevel()
        splash_screen_3.geometry("700x400+150+150")
        style = ttk.Style(splash_screen_3)
        style.theme_use("clam")
        ttk.Style().configure("Treeview", background="black",foreground="white", fieldbackground="black")
        trv = ttk.Treeview(splash_screen_3)

        # setting columns
        trv['columns'] = ('SI','RFID','TYPE','IN TIME','OUT TIME')

        # formatting columns
        # ! #0 is phantom column given by treeview 
        trv.column('#0',width=0,minwidth=0)
        trv.column('SI',anchor=CENTER,width=120)
        trv.column('RFID',anchor=CENTER,width=120)
        trv.column('TYPE',anchor=CENTER,width=120)
        trv.column('IN TIME',anchor=CENTER,width=120)
        trv.column('OUT TIME',anchor=CENTER,width=120)


        trv.heading('#0',text='')
        trv.heading('SI',text='SI')
        trv.heading('RFID',text='RFID')
        trv.heading('TYPE',text='TYPE')
        trv.heading('IN TIME',text='IN TIME')
        trv.heading('OUT TIME',text='OUT TIME')


        trv.place(x=50,y=50)

        for row in log_files:
            trv.insert(parent='',index='end',values=row)

        quit_button_3 = tk.Button(splash_screen_3,text='Quit',font=('times new roman',10),height= 3, width=10,bg='#005B96',fg='#FFFFFF',command=splash_screen_3.destroy)
        quit_button_3.place(x=320,y=290)

    def copy_log(self):
        pass


root = tk.Tk()
root_obj = Login(root)
root.mainloop()