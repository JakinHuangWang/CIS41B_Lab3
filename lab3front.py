"""LAB 3 Front
Author: Jakin Wang
OS: Mac OSX
IDE: Wings IDE
Date: 05/17/2019
Description: Uses the database we create to construct a set of GUIs for the user the access
"""
import numpy as np
import matplotlib
matplotlib.use('TkAgg')               	        
import tkinter as tk                      	
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect("Lab3.db")
cur = conn.cursor()
 
#Class mainWin is the Main Window for our GUI, it consists of three buttons:
#By salary, By growth rate, and By degree
class mainWin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("High Tech Jobs")
        tk.Button(self, text = "By salary" , command=lambda:plotWin(self).plot(plotTwo, "Dollars")).grid(row = 0, column = 0)
        tk.Button(self, text = "By growth rate", command=lambda:plotWin(self).plot(plotTwo, "Percentage")).grid(row = 0, column = 1)
        tk.Button(self, text = "By degree", command=lambda:dialogueWin(self).create(self)).grid(row = 0, column = 2)
        
#Class plotWin is the plotting Window for our GUI, it performs both plottings
class plotWin(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Plotting For High Tech Jobs")
        self.fig = plt.figure(figsize = (8,8))
        self.grab_set()
        self.focus_set()        
    def plot(self, someFunc, *args,  **kwargs):
        someFunc(*args, **kwargs)
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()

#Function plotTwo plots two similar graphs: 2018 Median Pay and Job Outlook 2016-26
def plotTwo(label):
    if label == 'Dollars':
        cur.execute("SELECT {} FROM FIELDNAMES".format("C1"))
        plt.title(cur.fetchone()[0])
        cur.execute("SELECT Name, MedianPay FROM DATA ORDER BY MedianPay")
    else:
        cur.execute("SELECT {} FROM FIELDNAMES".format("C6"))
        plt.title(cur.fetchone()[0])
        cur.execute("SELECT Name, Outlook FROM DATA ORDER BY Outlook")
    result = cur.fetchall()
    xlst = [r[0] for r in result]
    ylst = [r[1] for r in result]
    plt.barh(np.arange(10), ylst, align = "center")
    plt.yticks(np.arange(10), xlst, wrap=True, fontsize=6, verticalalignment='center')
    plt.xlabel(label)

#Class dialogueWin is the dialogue Window that gives the users 4 Entry-Level Education to choose from
class dialogueWin(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Choose Entry Degree")
        self.grab_set()
        self.focus_set()
    def create(self, master):
        cur.execute("SELECT NAME FROM EDUCATION")
        result = cur.fetchall()
        textLst = [r[0] for r in result]
        controlVar = tk.IntVar()
        rbLst = [tk.Radiobutton(self, text=textLst[i], variable=controlVar, value=i+1) 
                 for i in range(len(textLst))]
        for RB in rbLst:
            RB.grid(sticky = 'w')
        tk.Button(self, text="OK", command = lambda:displayWin(master).show(controlVar.get(), self)).grid()
            
#After the user has chosen an option from the dialogue Window,
#Class displayWin displays a listbox including all the jobs with the same Entry-Level Educations
class displayWin(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.focus_set()
    def show(self, number, dWin):
        dWin.destroy()
        cur.execute("SELECT NAME FROM EDUCATION WHERE ID = ?", (number, ))
        self.title("Minimum Degree: " + cur.fetchone()[0])
        cur.execute("SELECT NAME FROM DATA WHERE ENTRYLEVEL = ?", (number,))
        result = cur.fetchall()
        textLst = [r[0] for r in result]
        LB = tk.Listbox(self, height = 10, width = 50)
        for i in range(len(textLst)):
            LB.insert(i+1, textLst[i])
        LB.grid()
                       
mWin = mainWin()
mWin.mainloop()
conn.commit()
conn.close()