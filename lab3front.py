"""LAB 2Author: Jakin Wang
OS: Mac OSX
IDE: Wings IDE
Date: 05/04/2019
Description: Scrape the Web, Create a database, and using the database to perform data analysis and data plotting
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

#Function plotTwo plots two similar graphs: 2018 Median Pay and Job Outlook 2016-26
def plotTwo(label):
    if label == 'Dollars':
        plt.title(cur.execute("SELECT {} FROM FIELDNAMES".format("C1")))
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
    plt.yticks(np.arange(10), ['\n'.join(x.split()) for x in xlst], fontsize = 8)
    plt.xlabel(label)
 
#Class mainWin is the Main Window for our GUI, it consists of three buttons:
#By salary, By growth rate, and By degree
class mainWin(tk.Tk):
    def __init__(self):
        super().__init__()
        tk.Button(self, text = "By salary" , command=lambda:plotWin(self).plot(plotTwo, "Dollars")).grid(row = 0, column = 0)
        tk.Button(self, text = "By growth rate", command=lambda:plotWin(self).plot(plotTwo, "Percentage")).grid(row = 0, column = 1)
        tk.Button(self, text = "By degree", command=lambda:dialogueWin(self).create()).grid(row = 0, column = 2)

#Class plotWin is the plotting Window for our GUI, it performs both plottings
class plotWin(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Plotting Window")
        self.fig = plt.figure(figsize = (10, 10))
        self.grab_set()
        self.focus_set()        
    def plot(self, someFunc, *args,  **kwargs):
        someFunc(*args, **kwargs)
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()

#Class dialogueWin is the dialogue Window that gives the users 4 Entry-Level Education to choose from
class dialogueWin(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Dialogue Window")        
    def create(self):
        cur.execute("SELECT NAME FROM EDUCATION")
        result = cur.fetchall()
        textLst = [r[0] for r in result]
        controlVar = tk.IntVar()
        rbLst = [tk.Radiobutton(self, text=textLst[i], variable=controlVar, value=i+1, command = lambda:displayWin(self).show(controlVar.get())) for i in range(len(textLst))]
        for RB in rbLst:
            RB.grid()
            
#After the user has chosen an option from the dialogue Window,
#Class displayWin displays a listbox including all the jobs with the same Entry-Level Educations
class displayWin(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Display Window")
        self.focus_set()
    def show(self, number):
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