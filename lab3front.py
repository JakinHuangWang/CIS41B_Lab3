import numpy as np
import matplotlib
matplotlib.use('TkAgg')               	        # tell matplotlib to work with Tkinter
import tkinter as tk                      	# normal import of tkinter for GUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Canvas widget
import matplotlib.pyplot as plt

def plotSome():
    x = np.linspace(-5, 5, 100)
    plt.plot(x, x**2, '-g')
    
class mainWin(tk.Tk):
    def __init__(self):
        super().__init__()
        textLst = ['By salary', 'By growth rate', 'By degree']
        for i in range(len(textLst)):
            tk.Button(self, text = textLst[i], command=lambda:plotWin(self).plot(plotSome)).grid(row = 0, column = i)
            
class plotWin(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Plotting Window")
        self.fig = plt.figure(figsize=(7, 7))
    def plot(self, someFunc):
        result = someFunc()
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw() 
mWin = mainWin()
mWin.mainloop()