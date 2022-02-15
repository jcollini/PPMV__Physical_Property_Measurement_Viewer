import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
import numpy as np


def move_plot(ax,canvas):
    
    #new data
    x=np.arange(0,520,1)
    y=np.cos(np.deg2rad(x))

    #update axis
    ax.clear()
    ax.plot(x,y)
    ax.relim()
    ax.autoscale()
    
    #update canvas
    canvas.draw()
    
#Make a matplotlib plot in a tkinter window

root=tk.Tk()
root.title('Matplotlib in window')

#make fake data
x=np.arange(0,4,0.01)
y=x**2

#make plot 
fig=Figure()
#can also do tight layout option here, if needed
fig.tight_layout()

#how to create plot and add to it
MyPlot=fig.add_subplot()
MyPlot.plot(x,y,label='this is data')
MyPlot.set_xlabel('x axis')
MyPlot.set_title('title')
MyPlot.legend(loc='best')
MyPlot.tick_params(direction='in')

canvas=FigureCanvasTkAgg(fig,master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=0,column=0,columnspan=2)





#making a button to check
b=tk.Button(root,text='quit here',command=root.destroy)
b.grid(row=1,column=0)

b2=tk.Button(root,text='make new plot',command=lambda: new_plot(fig,MyPlot,canvas))
b2.grid(row=1,column=1)

#make tool bar
toolbarFrame = tk.Frame(root)
toolbarFrame.grid(row=2,column=0,columnspan=2)
toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

root.mainloop()