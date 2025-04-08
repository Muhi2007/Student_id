# -*- coding: utf-8 -*-
import sys
import os
import random as rd
import tkinter as tk
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

def startNaming():
    yol = entry.get()
    if os.path.exists(yol):
        label.config(text= "Running...")
        mainFunction(yol)

    else:
        label.config(text= "Error: \n Wrong destination")

def mainFunction(yol):
    names = os.listdir(yol)
    print(names)
    with open(os.path.join(yol, "id_map.csv"), "w", encoding= "utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Original Name", "ID"])

        for i in names:
            if "." not in i: 
                print(i)
                uniq = unikalID()
                old = os.path.join(yol, i)
                new = os.path.join(yol, uniq)

                os.rename(old, new)
                writer.writerow([i, uniq])
    root.after(1000, lambda: label.config(text="Finished!"))


root = tk.Tk()
root.geometry("500x600")
root.title("RandomNamer")
root.configure(bg="lightblue")
root.bind("<Return>", lambda event: button.invoke())

entry = tk.Entry(root, width = 40, font=("Arial", 15, "bold"), fg="White", bg="Grey")
entry.pack(pady = 25)
entry.insert(0, "Enter the destination of the file to modify")

label = tk.Label(root, font=("Arial", 12, "bold"), bg= root["bg"])
label.pack(pady = 15)

button = tk.Button(root, width= 20 , font=("Arial", 13, "bold"), text = "Start", command= startNaming)
button.pack(pady = 15)



root.mainloop()

