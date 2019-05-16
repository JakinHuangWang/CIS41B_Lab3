import numpy as np
import matplotlib
matplotlib.use('TkAgg')               	        # tell matplotlib to work with Tkinter
import tkinter as tk                      	# normal import of tkinter for GUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Canvas widget
import matplotlib.pyplot as plt

class mainWin(tk.Tk):
    def __init__(self):
        super().__init__()
        textLst = ['By salary', 'By growth rate', 'By degree']
        for i in range(len(textLst)):
            tk.Button(self, text = textLst[i]).grid(row = 0, column = i)

mWin = mainWin()
mWin.mainloop()