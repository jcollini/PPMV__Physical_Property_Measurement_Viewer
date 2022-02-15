import tkinter as tk
import matplotlib.pyplot as plt
#from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
import numpy as np


# =============================================================================
# def new_plot(canvas):
#     canvas.get_tk_widget().grid_forget()
#     
#     x=np.arange(0,520,1)
#     y=np.cos(np.deg2rad(x))
# 
#     #make plot 
#     fig=Figure()
#     fig.add_subplot(1,1,1).plot(x,y)
# 
#     canvas=FigureCanvasTkAgg(fig,master=root)
#     canvas.draw()
#     canvas.get_tk_widget().grid(row=0,column=0,columnspan=2)
# 
# =============================================================================

#Make a matplotlib plot in a tkinter window

root=tk.Tk()
root.title('Matplotlib in window')

#make fake data
x=np.arange(0,4,0.01)
y=x**2

#make plot 
fig=plt.figure()
plt.plot(x,y)

canvas=FigureCanvasTkAgg(fig,master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=0,column=0,columnspan=2)





#making a button to check
b=tk.Button(root,text='quit here',command=root.destroy)
b.grid(row=1,column=0)

b2=tk.Button(root,text='make new plot')
b2.grid(row=1,column=1)

#make tool bar
toolbarFrame = tk.Frame(root)
toolbarFrame.grid(row=2,column=0,columnspan=2)
toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

root.mainloop()
