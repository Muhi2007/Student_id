# -*- coding: utf-8 -*-
import sys
import os
import random as rd
import tkinter as tk
from tkinter import messagebox
import csv
forbidden_list = []


#For chaning concole encoding to UTF-8(In case anyone used an foregin name)
sys.stdout.reconfigure(encoding='utf-8')

def unikalID():
    x = rd.randint(1000, 10000)
    while x in forbidden_list:
        x = rd.randint(1000, 10000)
    forbidden_list.append(x)
    return str(x)

def starting():
    yol = entry.get()
    global idFile
    idFile = os.path.join(yol, "id_map.csv")
    result = messagebox.askyesno("Do you want to run code?", f"{yol} \n Do you sure about this destination?")
    if result:
        if os.path.exists(yol):
            label.config(text="Running...")
            if os.path.exists(idFile):
                mainDecoding(yol)
            else:
                mainFunction(yol)
        else:
            label.config(text="Error: \nWrong path")
    else:
        label.config(text="Cancelled")


#Function for giving random names
def mainFunction(yol):
    idFile = os.path.join(yol, "id_map.csv") 
    names = os.listdir(yol)

    #Creates a cvs file for storing all the names with their IDs
    with open(idFile, "w", encoding= "utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Original Name", "ID"])

        for i in names:
            if "." not in i: 
                uniq = unikalID()
                old = os.path.join(yol, i)
                new = os.path.join(yol, uniq)

                os.rename(old, new)
                writer.writerow([i, uniq])
    root.after(1000, lambda: label.config(text="Finished!"))


#Function for decoding the random names
def mainDecoding(yol):
    idList = []
    items = os.listdir(yol)
    items.remove('id_map.csv')
    #For getting all the data from CVS file
    with open(idFile, encoding= "utf-8", newline="") as file:
        reader = csv.reader(file)
        for i in reader:
            idList.append(i)

    idList.pop(0)
    
    for i in range(len(idList)):
        m = idList[i]
        if m[1] in items:
            os.rename(os.path.join(yol, m[1]), os.path.join(yol, m[0]))
    

    if len(idList) == len(items):
        os.remove(os.path.join(yol, 'id_map.csv'))
        
    root.after(1000, lambda: label.config(text="Finished!"))
    

#Tkinter for creating the interface
root = tk.Tk()

root.geometry("500x600")
root.title("RandomNamer")
root.configure(bg="lightblue")
root.resizable(False, False)
root.bind("<Return>", lambda event: button.invoke())

entry = tk.Entry(root, width = 40, font=("Arial", 15, "bold"), fg="White", bg="Grey")
entry.pack(pady = 25)
entry.insert(0, "Input file destination")

label = tk.Label(root, font=("Arial", 12, "bold"), bg= root["bg"])
label.pack(pady = 15)

button = tk.Button(root, width= 25 , font=("Arial", 13, "bold"), text = "START", command= starting)
button.pack(pady = 15)

root.mainloop()