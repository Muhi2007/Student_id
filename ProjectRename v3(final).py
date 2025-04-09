# -*- coding: utf-8 -*-
import sys
import os
import random as rd
import tkinter as tk
from tkinter import messagebox
import csv
global forbidden_list 
forbidden_list = []


#For chaning concole encoding to UTF-8(In case anyone used an foregin name)
sys.stdout.reconfigure(encoding='utf-8')

def unikalID(items):
    x = rd.randint(1000, 10000)
    while x in forbidden_list and x not in items:

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
    k = 0
    idFile = os.path.join(yol, "id_map.csv") 
    names = os.listdir(yol)

    #Creates a cvs file for storing all the names with their IDs
    with open(idFile, "w", encoding= "utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Original Name", "ID"])

        for i in names:
            if os.path.isdir(os.path.join(yol, i)): 
                k += 1
                uniq = unikalID(os.listdir(yol))
                old = os.path.join(yol, i)
                new = os.path.join(yol, uniq)

                os.rename(old, new)
                writer.writerow([i, uniq])
        writer.writerow(["k= ", k])
        
    forbidden_list.clear()
    root.after(1000, lambda: label.config(text="Finished!"))


#Function for decoding the random names
def mainDecoding(yol):
    idList = []
    finalList = []
    items = os.listdir(yol)
    items.remove('id_map.csv')

    #For getting all the data from CVS file
    with open(idFile, "r", encoding= "utf-8", newline="") as file:
        reader = csv.reader(file)

        for i in reader:
            idList.append(i)

    k = int(idList[len(idList)-1][1])
    idList.pop(len(idList)-1)
    idList.pop(0)
    
    for i in range(len(idList)):
        m = idList[i]

        if m[0] not in items:
            if m[1] in items:
                k -=1
                os.rename(os.path.join(yol, m[1]), os.path.join(yol, m[0]))
        else:
            if k != 0:
                finalList.append(m)

    if k == 0:
        os.remove(os.path.join(yol, 'id_map.csv'))
    else:
        with open(idFile, "w", encoding= "utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Used", "ID"])

            for i in finalList:
                writer.writerow(i)
            writer.writerow(["k= ", k])
    if finalList:
        logs.config(text=f"Could not rename: \n{finalList}")
    else:
        logs.config(text="")
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

logs = tk.Label(root, font=("Arial", 12, "bold"), bg= root["bg"])
logs.pack(pady=5)

root.mainloop()