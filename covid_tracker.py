# 
# Author: Sachin Sharma
# Description: Register's the University to add themselves in the database
# Required Libraries: pymongo <pip install "pymongo[srv]">, 
# 

import string
import random
import ctypes
import tkinter as tk
from pymongo import MongoClient

#-----------------Connection to Database-----------------
client = MongoClient("mongodb+srv://admin:admin@cluster0.ya2jp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client["covid"]

#-----------------Setting up UI-----------------
root = tk.Tk()

#Get Screensize
user32 = ctypes.windll.user32
screensize = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

#Functions to setup UI
back_button = False
def setup_canvas():
    #Setup Canvas
    canvas = tk.Canvas(root, width=screensize[0]/5, height=screensize[1]/5, bg="#021C1E")
    canvas.grid(rowspan=4)

def setup_function(label, b1, b2, b3, b4):
    label.grid(column=0, row=2)

    b1.grid(column=0, row=3)
    b2.grid_remove()
    b3.grid_remove()
    b4.grid_remove()

#Called when the button register is pressed
def register_function(name, label, b1, b2, b3, b4):
    setup_function(label, b1, b2, b3, b4)
    name.config(text="Register University")
    name.grid(column=0, row=1)
    back_button = False

    print("Register Executed!")
    register_algo(name, label, b1, b2, b3, b4)

#Called when the button login university is pressed
def login_function(name, label, b1, b2, b3, b4):
    setup_function(label, b1, b2, b3, b4)
    name.config(text="Login University")
    name.grid(column=0, row=1)
    back_button = False

    print("Login Executed!")
    login_algo(name, label, b1, b2, b3, b4)

#Called when the button register student is pressed
def add_function(name, label, b1, b2, b3, b4):
    setup_function(label, b1, b2, b3, b4)
    name.config(text="Register Student")
    name.grid(column=0, row=1)
    back_button = False

    print("Add Student Executed!")
    add_student_algo(name, label, b1, b2, b3, b4)

def revert_function(name, label, b1, b2, b3, b4):
    name.config(text="COVID Tracker")
    name.grid(column=0, row = 0)

    label.grid_remove()

    b1.grid_remove()
    b2.grid(column=0, row=1)
    b3.grid(column=0, row=2)
    b4.grid(column=0, row=3)

    back_button = True


def button_setup():
    #Setup Program Name
    program_name = tk.Label(root, text="COVID Tracker", font=("Raleway",20), bg="#021C1E", fg="#ffffff")
    program_name.grid(column=0, row = 0)

    #Setup Label 
    label = tk.Label(root, text="Instructions in Terminal/Console!", font=("Raleway",12), bg="#021C1E", fg="#ffffff")

    #Setup Buttons
    button_back_text = tk.StringVar()
    button_back = tk.Button(root, command=lambda:revert_function(program_name, label, button_back, button_register, button_login, button_add) ,textvariable=button_back_text, font="Raleway", bg="#004445", fg="#ffffff", bd=0, activebackground="#021C1E", activeforeground="#ffffff")
    button_back_text.set("Back")

    button_register_text = tk.StringVar()
    button_register = tk.Button(root, command=lambda:register_function(program_name, label, button_back, button_register, button_login, button_add) ,textvariable=button_register_text, font="Raleway", bg="#004445", fg="#ffffff", bd=0, activebackground="#021C1E", activeforeground="#ffffff")
    button_register_text.set("Register University")

    button_login_text = tk.StringVar()
    button_login = tk.Button(root, command=lambda:login_function(program_name, label, button_back, button_register, button_login, button_add), textvariable=button_login_text, font="Raleway", bg="#2C7873", fg="#ffffff", bd=0, activebackground="#021C1E", activeforeground="#ffffff")
    button_login_text.set("Login University")

    button_add_text = tk.StringVar()
    button_add = tk.Button(root, command=lambda:add_function(program_name, label, button_back, button_register, button_login, button_add), textvariable=button_add_text, font="Raleway", bg="#004445", fg="#ffffff", bd=0, activebackground="#021C1E", activeforeground="#ffffff")
    button_add_text.set("Register Student")

    revert_function(program_name, label, button_back, button_register, button_login, button_add)

setup_canvas()
button_setup()

#----------------- Main Algorithm for Register, Login, Add -----------------

#Register Algorithm
def register_algo(name, label, b1, b2, b3, b4):

    #Take input from user regarding all the information needed to enter into the database for the University
    university_name = str(input("University Name: "))
    while(len(university_name) == 0):
        university_name = str(input("University Name: "))

    university_username = str(input("Username: "))
    while(len(university_username) == 0):
        university_username = str(input("Username: "))
    
    university_password = str(input("Password: "))
    while(len(university_password) == 0):
        university_password = str(input("Username: "))    
    
    university_confirm_password = str(input("Confirm Password: "))

    if(university_password != university_confirm_password):
        print("Password do not match -- Try logging in!")
        revert_function(name, label, b1, b2, b3, b4)
        return print("------------ University Registration Ended! ------------")

    #Confirm the registration to insert data into database
    confirm_register = str(input("Register? (yes or no): "))
    if(confirm_register.lower() == "yes"):
        print("------------Processing------------")
    else:
        print("------------ University Registration Ended! ------------")
        return revert_function(name, label, b1, b2, b3, b4)

    #Check if the username is already in the system if so then return back to main menu
    collection_uni = db["Universities"]
    result = collection_uni.find({"u_username" : university_username.lower()})
    in_list = True if len(list(result)) else False
    if(in_list):
        print("Username is in use -- Try logging in!")
        revert_function(name, label, b1, b2, b3, b4)
        return print("------------ University Registration Ended! ------------")


    #Generate a One time registration code for the University to give to the students to enter into the add student section
    one_time_id = 0
    code_assigned = False
    while(not code_assigned):
        one_time_id = id_generator()
        result = collection_uni.find({"u_register_code" : one_time_id})
        in_list = True if len(list(result)) else False
        if(not in_list):
            code_assigned = True

    #Put data into a dictionary for it to enter the database
    post = {
        "u_name" : university_name.lower(),
        "u_username" : university_username.lower(),
        "u_password" : university_password,
        "u_register_code" : one_time_id
    }

    collection_uni = db["Universities"]

    #Enter data into database
    collection_uni.insert_one(post)

    print("University Registration Complete!")
    print("Student Registration ID: " + one_time_id.upper())
    revert_function(name, label, b1, b2, b3, b4)
    print("------------ University Registration Ended! ------------")

#Login Algorithm
def login_algo(name, label, b1, b2, b3, b4):
    
    #Get information from user regarding login information
    university_username = str(input("Username: "))
    university_password = str(input("Password: "))

    print("+ Processing +")

    #Check if the Username and provided was valid if so then it will user into the system
    collection_uni = db["Universities"]
    results = collection_uni.find({"u_username" : university_username.lower()})
    username_found = False
    university_info = {}
    for result in results:
        university_info = result
        username_found = True
        if(result["u_password"] != university_password):
            print("Password was incorrect -- Try again!")
            revert_function(name, label, b1, b2, b3, b4)
            return print("------------ Login University Ended! ------------")
    if(not username_found):
        print("Username was not found -- Try again!")
        revert_function(name, label, b1, b2, b3, b4)
        return print("------------ Login Univeristy Ended! ------------")

    print("------------ Login Successful! ------------")

    collection_students = db["Students"]
    results = collection_students.find({"s_register_code" : university_info["u_register_code"]})
    counter = 0
    for result in results:
        counter += 1

    print("Students Currectly Vaccinated: " + str(counter))
    print("+ More info COMING SOON! +")
    revert_function(name, label, b1, b2, b3, b4)
    return print("------------ Login Univeristy Ended! ------------")

#Student Registration Algorithm
def add_student_algo(name, label, b1, b2, b3, b4):

    #Get information from student to enter into the database
    student_firstname = str(input("First Name: "))
    while(len(student_firstname) == 0):
        student_firstname = str(input("reenter First Name: "))

    student_lastname = str(input("Last Name: "))
    while(len(student_lastname) == 0):
        student_lastname = str(input("reenter Last Name: "))

    student_id_no = int(input("Student ID Number: "))
    while(len(str(student_id_no)) == 0):
        student_id_no = int(input("reenter Student ID Number: "))

    #Check if the provided student id number is not repeated in the database
    collection_students = db["Students"]
    results = collection_students.find({"s_id_no" : student_id_no})
    in_list = True if len(list(results)) else False
    if(in_list):
        print("Student is already registered")
        revert_function(name, label, b1, b2, b3, b4)
        return print("------------ Student Registration Ended! ------------")

    student_register_code = str(input("University Registration Number: "))

    #Check if the registration number provided by the student exists in the university's collection
    collection_uni = db["Universities"]
    results = collection_uni.find({"u_register_code" : student_register_code})
    in_list = True if len(list(results)) else False
    if(not in_list):
        print("University Code Does not Exist -- Try again!")
        revert_function(name, label, b1, b2, b3, b4)
        return print("------------ Student Registration Ended! ------------")

    student_street_add = str(input("Home Address - Street: "))
    while(len(student_street_add) == 0):
        student_street_add = str(input("reenter Home Address - Street: "))

    student_city_add = str(input("Home Address - City: "))
    while(len(student_city_add) == 0):
        student_city_add = str(input("reenter Home Address - City: "))

    student_state_add = str(input("Home Address - State: "))
    while(len(student_state_add) == 0):
        student_state_add = str(input("reenter Home Address - State: "))

    student_zipcode_add = str(input("Home Address - ZipCode: "))
    while(len(student_zipcode_add) == 0):
        student_zipcode_add = str(input("reenter Home Address - ZipCode: "))

    student_phone_No = int(input("Phone #: "))
    while(len(str(student_phone_No)) == 0):
        student_phone_No = int(input("reenter Phone #: "))

    #Confirm the registration to insert data into database
    confirm_register = str(input("Register? (yes or no): "))
    if(confirm_register.lower() == "yes"):
        print("------------ Processing ------------")
    else:
        print("------------ Student Registration Ended! ------------")
        return revert_function(name, label, b1, b2, b3, b4)

    #Put together all the data provided by the student into a dictionary to be entered into the database
    post = {
        "s_first_name" : student_firstname,
        "s_last_name" : student_lastname,
        "s_id_no" : student_id_no,
        "s_register_code" : student_register_code,
        "s_street_add" : student_street_add,
        "s_city_add" : student_city_add,
        "s_state_add" : student_state_add,
        "s_zipcode_add" : student_zipcode_add,
        "s_phone_no" : student_phone_No
    }

    collection_students.insert_one(post)
    print("Student Registration Complete!")
    revert_function(name, label, b1, b2, b3, b4)
    print("------------ Student Registration Ended! ------------")
    
def id_generator(size=5, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

root.mainloop()