import numpy as np
import matplotlib
matplotlib.use('TkAgg')               	        # tell matplotlib to work with Tkinter
import tkinter as tk                      	# normal import of tkinter for GUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Canvas widget
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect("Lab3.db")
cur = conn.cursor()

def plotSalary():
    cur.execute("SELECT Name, MedianPay FROM DATA ORDER BY MedianPay")
    result = cur.fetchall()
    plt.barh([r[0] for r in result], [r[1] for r in result], align = "center")
    plt.title("2018 Median Pay")

def plotGrowthRate():
    cur.execute("SELECT Name, Outlook FROM DATA ORDER BY OUTLOOK")
    result = cur.fetchall()
    plt.barh([r[0] for r in result], [r[1] for r in result], align = "center")
    plt.title("2018 Growth Rate")
    
class mainWin(tk.Tk):
    def __init__(self):
        super().__init__()
        textlst = ['By salary', 'By growth rate', 'By degree']
        fctlst = [plotSalary, plotGrowthRate, plotGrowthRate]
        for i in range(len(textlst)):
            tk.Button(self, text = textlst[i], command=lambda:plotWin(self).plot(fctlst[i])).grid(row = 0, column = i)
            
class plotWin(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Plotting Window")
        self.fig = plt.figure(figsize=(7, 7))
    def plot(self, someFunc, *args, **kwargs):
        someFunc(*args, **kwargs)
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()
        
mWin = mainWin()
mWin.mainloop()
conn.commit()
conn.close()