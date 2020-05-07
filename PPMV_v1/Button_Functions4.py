import tkinter as tk

import PPMV_Jobs4 as ppmv

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from tkinter import filedialog
#Modual for button functions in PPMV

def Button_LoadData(MasterTK,Load_EntryTK):
    #button to grab datafile location
    #
    #--MasterTK is Tk window locaion of buttton
    #--Load_EntryTK is Tk variable for load path
    #
    #Start at desktop
    file_location='::{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}'
    MasterTK.filename=filedialog.askopenfilename(initialdir=file_location,title='Select a file',filetypes=(('PPMS files','*.dat'),('all files','*.*')))
    
    #update the entry with the new file. Clear it first
    Load_EntryTK.delete(0,tk.END)
    Load_EntryTK.insert(0,MasterTK.filename)
    
    
    
def Button_QuickPlot(Load_EntryTK,MachineTK,XchoiceTK,YchoiceTK):
    #button for quick plot
    #
    #--Load_EntryTK is Tk variable for load path
    #--MachineTK is Tk variable for machine type
    #--XchoiceTK and YchoiceTK are Tk variables for names of x and y axis of a dataset
    ppmv.Job_QuickPlot(Load_EntryTK.get(),MachineTK.get(),XchoiceTK.get(),YchoiceTK.get())
    
def Button_QuickSave_CSV(Load_EntryTK,MachineTK):
    #Button to quickly save loaded file
    #
    #--Load_EntryTK is Tk variable for load path
    #--MachineTK is Tk variable for machine type
    #
    #grab loaded PPMS file dataframe
    PPMS_File=Load_EntryTK.get()
    MachineType=MachineTK.get()
    data=ppmv.Read_PPMS_File(PPMS_File,MachineType)
    
    #Grab the file location and name from the user
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv',filetypes=(('csv','*.csv'),('all files','*.*')))
                                    
    data.to_csv (export_file_path, index = False, header=True)
    
def Button_ExportCW_CSVs():
    #example stuff
    tk.Label()


def Button_UpdatePlot(MasterTK,canvas_PLT,Plot_PLT,Load_EntryTK,MachineTK,XchoiceTK,YchoiceTK,CW_Toggle,empty=False):
    #Updates figures for CW plots (potentially more?)
    #
    #New Variable types:
    #Fig_PLT is a figure object from matplotlib.figure
    #CW_Toggle is boolean which turns the cooling/warming seperation off and on
    
    #clear given plot
    Plot_PLT.clear()
    print(CW_Toggle.get())
        
    #Load data
    data=ppmv.Read_PPMS_File(Load_EntryTK.get(),MachineTK.get())
    
    #Grab wanted axis anmes and data, convert to numpy
    Xdata=data[XchoiceTK.get()]
    Xname=XchoiceTK.get()
        
    Ydata=data[YchoiceTK.get()]
    Yname=YchoiceTK.get()
    
    #Plot data depending on toggle
    if CW_Toggle.get():
        #Split data
        X1,Y1,X2,Y2=ppmv.Job_CW_Split_Data(Xdata, Ydata)
        #overwrite original fig and plot with new split data
        Plot_PLT.plot(X1,Y1,'b',label='cool down')
        Plot_PLT.plot(X2,Y2,'r',label='warm up')
        Plot_PLT.legend(loc='best')
        Plot_PLT.set_xlabel(Xname)
        Plot_PLT.set_ylabel(Yname)
    else:
        #overwrite original fig and plot with unsplit data
        Plot_PLT.plot(Xdata,Ydata)
        Plot_PLT.set_xlabel(Xname)
        Plot_PLT.set_ylabel(Yname)
        
    
    #redraw canvas with ticks inside
    Plot_PLT.tick_params(direction='in')
    
    Plot_PLT.relim()
    Plot_PLT.autoscale()
    canvas_PLT.draw()
        
    
    
    
        
    
def Button_SaveFig(Fig_PLT):
    
    
    #Grab the file location and name from the user
    export_file_path = filedialog.asksaveasfilename(defaultextension='.png',filetypes=(('png','*.png'),('all files','*.*')))
                                    
    Fig_PLT.savefig(export_file_path)
    

    
def Empty_Plot(MasterTK):
    #creates a blank plot for use on a screen for a given Master
    #generate figure 
    fig=Figure()
    
    ax=fig.add_subplot()
    canvas=FigureCanvasTkAgg(fig,master=MasterTK)
    canvas.draw()
    
    
    return canvas,fig,ax