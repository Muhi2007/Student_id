# -*- coding: utf-8 -*-
import sys
import os
import random as rd
import tkinter as tk
from tkinter import messagebox
import csv
import random
global forbidden_list 
forbidden_list = []
x = 100

#For chaning concole encoding to UTF-8(In case anyone used an foregin name)
sys.stdout.reconfigure(encoding='utf-8')

def is_valid_id_file(idFile):
    if not os.path.exists(idFile):
        return False
    
    with open(idFile, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)
        
        # Make sure it has at least header + 1 row + final count
        return len(rows) >= 3 and rows[0][0].lower() in ["original name", "id"]


def unikalID(items, x):
    while x in forbidden_list or str(x) in items:
        x += 1
    forbidden_list.append(x)
    return str(x)

def is_file_open(yol):
    try:
        with open(yol, "a+"):
            return False
    except PermissionError:
        return True

def check_for_open_files(yol):
    for root, dirs, files in os.walk(yol):
        for file in files:
            full_path = os.path.join(root, file)
            if is_file_open(full_path):
                return True
            
    return False

def is_number(x):
    s = 0
    f = len(x)
    for i in x:
        if "0" <= i <= "9":
            s +=1
    if s == f:
        return True
    else:
        return False
    
def is_folder_number(yol):
    items = os.listdir(yol)
    x = 0
    f = 0
    for i in items:
        if os.path.isdir(os.path.join(yol, i)):
            x += 1
            if is_number(i):
                f += 1
    print(x, f)
    if x == f:
        return False
    else:
        return True
            

def starting():
    yol = entry.get()
    idFile = os.path.join(yol, "id_map.csv")

    if os.path.exists(yol):
        if messagebox.askyesno("Do you want to run code?", f"{yol} \n Are you sure about this destination?"):
            if is_valid_id_file(idFile) and not is_folder_number(yol):
                mainDecoding(yol)
            else:    
                mainCoding(yol)
            label.config(text="Running...")
        else:
            label.config(text="Cancelled")
    else:
        label.config(text="Error: \nWrong path")


#Function for giving ordered names
def mainCoding(yol):
    idFile = yol + "\\" + "id_map.csv"
    names = os.listdir(yol)

    #Creates a cvs file for storing all the names with their IDs
    if not is_file_open(idFile):
        if is_valid_id_file(idFile):
            with open(idFile, "r+", encoding="utf-8", newline="") as file:
                reader = csv.reader(file)
                rows = list(reader)
                print(rows)
                finalRow = rows[-1]
                k = int(finalRow[1])
                rows.pop(-1)

                for i in names:
                    if os.path.isdir(os.path.join(yol, i)):
                        if not check_for_open_files(os.path.join(yol, i)):
                            if not is_number(i):
                                uniq = unikalID(names, x)

                                rows.append([i, uniq])
                                old = os.path.join(yol, i)
                                new = os.path.join(yol, uniq)
                                k += 1

                                os.rename(old, new)

                rows.append(["k= ", k])
                file.seek(0)
                writer = csv.writer(file)
                writer.writerows(rows)
                file.truncate()
    
        else:
            k = 0
            with open(idFile, "w+", encoding= "utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Original Name", "ID"])

                for i in names:
                    if os.path.isdir(os.path.join(yol, i)):
                        if not check_for_open_files(os.path.join(yol, i)): 
                            k += 1
                            uniq = unikalID(names, x)
                            old = os.path.join(yol, i)
                            new = os.path.join(yol, uniq)

                            os.rename(old, new)
                            writer.writerow([i, uniq])
                writer.writerow(["k= ", k])
                
            forbidden_list.clear()
            root.after(1000, lambda: label.config(text="Finished!"))

    else:
        label.config(text="Finised (With exceptions)")
        logs.config(text="Error: \n One file is open at the give destination")


#Function for decoding the random names
def mainDecoding(yol):
    idFile = os.path.join(yol, 'id_map.csv')
    idList = []
    finalList = []
    items = os.listdir(yol)
    items.remove('id_map.csv')

    #For getting all the data from CVS file
    if not is_file_open(os.path.join(yol, "id_map.csv")):
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
                if m[1] in items and not check_for_open_files(os.path.join(yol, m[1])):
                    k -=1
                    os.rename(os.path.join(yol, m[1]), os.path.join(yol, m[0]))
                else:
                    finalList.append(m)
            else:
                finalList.append(m)

        if k == 0:
            b = str(random.random())
            b = b[2:]
            os.rename(os.path.join(yol, 'id_map.csv'), os.path.join(yol, f'id_map(Used){b}.csv'))
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
    else:
        label.config(text="Finised (With exceptions)")
        logs.config(text="Error: \n One file is open at the give destination")
    

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