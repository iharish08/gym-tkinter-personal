from tkinter import *
from tkinter import messagebox
import mysql.connector
from tkinter import ttk
from PIL import Image, ImageTk

connect = mysql.connector.connect(host="localhost", user="root", password="Harish@08", database="gym")
curs = connect.cursor()

# Function to handle unread results
def handle_unread_results(cursor):
    while cursor.nextset():
        pass

# User table
try:
    curs.execute("DESCRIBE users")
    handle_unread_results(curs)
except:
    curs.execute("""
                CREATE TABLE users(
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(20) NOT NULL,
                password VARCHAR(20) NOT NULL)""")
    connect.commit()

# Client table
try:
    curs.execute("DESCRIBE client_details")
    handle_unread_results(curs)
except:
    curs.execute("""
                CREATE TABLE client_details(
                Client_ID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(20),
                Age VARCHAR(10),
                Gender VARCHAR(7),
                Email VARCHAR(30),
                Ph_no VARCHAR(11),
                Address VARCHAR(20),
                Weight VARCHAR(10),
                Height VARCHAR(10),
                Type VARCHAR(20))""")
    connect.commit()

# Trainer table
try:
    curs.execute("DESCRIBE trainer_details")
    handle_unread_results(curs)
except:
    curs.execute("""
                 CREATE TABLE trainer_details(
                Trainer_ID INT AUTO_INCREMENT PRIMARY KEY,
                Trainer_Name VARCHAR(20),
                Email VARCHAR(30),
                Ph_no VARCHAR(15),
                Trainer_Address VARCHAR(30),
                Trainer_Type VARCHAR(30))""")
    connect.commit()

def register_user(username, password):
    try:
        curs.execute("""
                     INSERT INTO users(username, password)
                     VALUES(%s, %s) """, (username, password))
        connect.commit()
        messagebox.showinfo("Success", "User registered Successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error:{err}")

def validate_login(username, password):
    try:
        curs.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        result = curs.fetchone()
        handle_unread_results(curs)
        if result:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return False

def register_trainer():
    try:
        curs.execute("INSERT INTO trainer_details(Trainer_Name, Email, Ph_no, Trainer_Address, Trainer_Type) VALUES(%s, %s, %s, %s, %s)",
                     (e1.get(), e2.get(), e3.get(), e4.get(), e5.get()))
        connect.commit()
        messagebox.showinfo("Success", "Trainer registered successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

def client_registration():
    try:
        curs.execute("INSERT INTO client_details(Name, Age, Gender, Email, Ph_no, Address, Weight, Height, Type) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                     (et1.get(), et2.get(), et3.get(), et4.get(), et5.get(), et6.get(), et7.get(), et8.get(), et9.get()))
        connect.commit()
        messagebox.showinfo("Success", "Client registered successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

def Clear(entries):
    for entry in entries:
        entry.delete(0, END)

# Client window
def port3():
    gym = Toplevel()
    gym.title("Ronic Fitness Zone")
    gym.geometry("1530x900")

    labels = ["Client Details", "Client id :", "Name :", "Age :", "Gender :", "Email :", "Ph No :", "Address :", "Weight :", "Height :", "Type :"]
    for i, text in enumerate(labels):
        Label(gym, text=text).grid(row=i+1, column=1)

    global et1, et2, et3, et4, et5, et6, et7, et8, et9,et10
    et1, et2, et3, et4, et5, et6, et7, et8, et9,et10 = [Entry(gym) for _ in range(10)]
    entries = [et1, et2, et3, et4, et5, et6, et7, et8, et9,et10]
    for i, entry in enumerate(entries):
        entry.grid(row=i+2, column=2)
    Button(gym, text="Submit Here", command=client_registration).grid(row=13, column=1, pady=5)
    Button(gym, text="Clear", command=lambda: Clear(entries)).grid(row=13, column=2, pady=5)
    Button(gym, text="Exit", command=gym.destroy).grid(row=13, column=3, pady=5)

    gym.config()

# Trainer window
def port2():
    trainer = Toplevel()
    trainer.title("Trainer's Port")
    trainer.geometry("1530x900")

    labels = ["Trainer Details :", "Trainer ID :", "Trainer Name :", "Email :", "Ph_no :", "Trainer Address :", "Trainer Type :"]
    for i, text in enumerate(labels):
        Label(trainer, text=text).grid(row=i+1, column=1)

    global e1, e2, e3, e4, e5,e6
    e1, e2, e3, e4, e5,e6= [Entry(trainer) for _ in range(6)]
    entries = [e1, e2, e3, e4, e5,e6]
    for i, entry in enumerate(entries):
        entry.grid(row=i+2, column=2)

    Button(trainer, text="     Submit     ", command=register_trainer).grid(row=8, column=0)
    Button(trainer, text="     Clear      ", command=lambda: Clear(entries)).grid(row=8, column=1)
    Button(trainer, text="     Exit       ", command=trainer.destroy).grid(row=8, column=2)
    trainer.config()

# Type window
def port1():
    global a
    type = Toplevel()
    type.title("Type")
    lf = LabelFrame(type, padx=20, pady=100)
    lf.pack(side="left")

    Label(lf, text="Type :", state=NORMAL).pack(pady=50)
    a = ttk.Combobox(lf)
    a['value'] = ("Trainer", "Client")
    a.pack(pady=50)

    Button(lf, text="     Submit     ", command=submit).pack(pady=50)
    Button(lf, text="     Exit       ", command=type.destroy).pack(pady=50)

    type.geometry("1530x900")

def submit():
    if a.get() == "Client":
        port3()
    elif a.get() == "Trainer":
        port2()

# Main page
def login():
    username = e1.get()
    password = e2.get()
    if validate_login(username, password):
        port1()
    else:
        messagebox.showerror("Error", "Invalid username or password")

def registration():
    reg = Toplevel()
    reg.title("Register")
    reg.geometry("400x300")

    Label(reg, text="Username:").pack(pady=10)
    reg_username = Entry(reg)
    reg_username.pack(pady=10)

    Label(reg, text="Password:").pack(pady=10)
    reg_password = Entry(reg, show="*")
    reg_password.pack(pady=10)

    def register():
        username = reg_username.get()
        password = reg_password.get()
        register_user(username, password)

    Button(reg, text="     Register     ", command=register).pack(pady=20)
    Button(reg, text="     Close        ", command=reg.destroy).pack(pady=10)

main = Tk()
main.title("Ronic Fitness Login")
main.geometry("1530x900")

Label(main, text="User Id").pack(pady=10)
e1 = Entry(main)
e1.pack(pady=10)
Label(main, text="Password").pack(pady=10)
e2 = Entry(main, show="*")
e2.pack(pady=10)

Button(main, text="     Login      ", command=login).pack(pady=20)
Button(main, text="     Register   ", command=registration).pack(pady=10)
Button(main, text="     Exit       ", command=main.destroy).pack(pady=10)
main.config()
main.mainloop()
