"""
Imports needed for all applications
"""

import tkinter as tk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from tkinter import filedialog
from scipy.optimize import curve_fit
from random import randint
from PIL import Image,ImageTk


import Button_Functions as bt
import PPMV_Jobs as ppmv
import PPMV_Classes as cl

import Cooling_Warming as cw
import Data_Paraser as dp
import Magnetometry as chi
"""
Variable Input Names
<object> variables:
--DataCL: DataPPMS object that holds data atributes from experiment
--MasterTK: window or frame needed for the action
--DataLocTK: string object for the filepath
--DataDisplayTK: string object for shorten filepath for display only
--MachineTK: string object for the machinetype used to collect the data
--XchoiceTK: string object for selected the x axis of from DataCL
--YchoiceTK: "" for y axis
--FigPLT: MatPlotLib figure object
--PlotPLT: MatPlotLib axes object, joined to FigPLT
--CanvasPLT: MatPlotLib Canvas object housing PlotPLT and FigPLT
"""




"""
####Button Functions####

Functions for activating buttons
Generally Button Functions, 
-- should be taking in only objects
-- grabbing and changing data and atributes of objects
-- not returning any values  

Input variables denote which type of object they are by the ending capital letters
--TK is tkinter object
--CL is DataPPMS object
--PLT is Matplotlib object
"""


    
def Button_LoadData(MasterTK,DataLocTK,DataDisplayTK,MachineTK,DataCL):
    #button to grab datafile location
    #
    #--MasterTK is Tk window locaion of buttton
    #--Load_EntryTK is Tk variable for load path
    #--DataCL is the PPMSData object you will load data into
    #
    #Start at desktop
    file_location='::{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}'
    MasterTK.filename=filedialog.askopenfilename(initialdir=file_location,title='Select a file',filetypes=(('PPMS and MPMS files','*.dat'),('all files','*.*')))
    fn=MasterTK.filename
    
    #update the entry with the new file. Clear it first
    DataLocTK.set(fn)
    DataDisplayTK.set(fn[0:10]+'.......'+fn[-10:])
    
    
    
def Button_QuickPlot(DataCL,XchoiceTK,YchoiceTK):
    #button for quick plot
    #
    #--Load_EntryTK is Tk variable for load path
    #--MachineTK is Tk variable for machine type
    #--XchoiceTK and YchoiceTK are Tk variables for names of x and y axis of a dataset
    
    #Load current data
    DataCL.load_data()
    
    #get Xdata and Ydata
    Xdata,Ydata=DataCL.get_axes(XchoiceTK,YchoiceTK)
    
    #quickplot data
    ppmv.Job_QuickPlot(Xdata,Ydata,XchoiceTK.get(),YchoiceTK.get())
    
def Button_QuickSave_CSV(DataCL):
    #Button to quickly save loaded file
    #
    #--Load_EntryTK is Tk variable for load path
    #--MachineTK is Tk variable for machine type
    #
    #Load the current data
    DataCL.load_data()
    
    #Grab the file location and name from the user
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv',filetypes=(('csv','*.csv'),('all files','*.*')))
                                    
    DataCL.data.to_csv (export_file_path, index = False, header=True)
    
def Button_ExportCW_CSVs(MasterTK,DataCL,XchoiceTK,YchoiceTK,CW_Toggle):
    
    
    #Grab wanted axis anmes and data, convert to numpy
    Xdata,Ydata=DataCL.get_axes(XchoiceTK,YchoiceTK)
    
    #Plot data depending on toggle
    if CW_Toggle.get():
        #Split data
        X1,Y1,X2,Y2=ppmv.Job_CW_Split_Data(Xdata, Ydata)
        
        #package each set into new datasets
        data1=pd.concat([X1,Y1],axis=1)
        data2=pd.concat([X2,Y2],axis=1)
        
        #Ask user for basefilename
        base_file_path = filedialog.asksaveasfilename(filetypes=(('Enter one name',''),('Enter one name','')))
        
        #determine direction for naming scheme
        direction=ppmv.DetermineDirection(X1)
        
        if direction=='down to up':
            fn1=base_file_path+'_Cooling.csv'
            fn2=base_file_path+'_Warming.csv'
        elif direction=='up to down':
            fn1=base_file_path+'_Warming.csv'
            fn2=base_file_path+'_Cooling.csv'
        
        #save each dataset
        data1.to_csv(fn1,index=False)
        data2.to_csv(fn2,index=False)
        
        
       
    else:
        #warn user that CW toggle is off
        tk.messagebox.showwarning('Warning','Please turn on the cooling/warming toggle\nto use this feature')
        
def Button_ExportDP_CSVs(Data_CL,DP_Label_ref,DP_Method_ref,DP_Legends_ref):
    
   
    
    #load current data
    Data_CL.load_data()
    
    
    #use dividers, if avaliable
    if DP_Label_ref:
         #Ask user for basefilename
        base_file_path = filedialog.asksaveasfilename(filetypes=(('Enter one name',''),('Enter one name','')))
        
        #reset parse lists
        Data_CL.reset_parse()
        
        #add current lists of methods and labels to data class
        Data_CL.add_parse(DP_Label_ref, DP_Method_ref)
        
        #run class method to parseData with current info
        Data_CL.parseData()
        
        #Export each set to a csv file
        plotNum=len(DP_Label_ref)+1
        for i in range(plotNum):
            print('Saving CSV section '+str(i+1))
            data=Data_CL.data_sections[i]
            
            #use the usernames for labels, if given
            if DP_Legends_ref[i].get() != 'Insert Data Name':
                fn=base_file_path+DP_Legends_ref[i].get()+'.csv'
            else:
                fn=base_file_path+'Section_'+str(i+1)+'_'+Data_CL.parse_results[i]
            
            #save with final filename
            data.to_csv(fn,index=False)
            
            
                
            
            
    else:
       print('please use a divider to use this feature')

def Button_UpdatePlotCW(MasterTK,canvas_PLT,Fig_PLT,Plot_PLT,DataCL,XchoiceTK,YchoiceTK,CW_Toggle,empty=False):
    #Updates figures for CW plots (potentially more?)
    #
    #New Variable types:
    #Fig_PLT is a figure object from matplotlib.figure
    #CW_Toggle is boolean which turns the cooling/warming seperation off and on
    
    #clear given plot
    Plot_PLT.clear()
    
        
    Xdata,Ydata=DataCL.get_axes(XchoiceTK,YchoiceTK)
    
    #Plot data depending on toggle
    if CW_Toggle.get():
        #Split data
        X1,Y1,X2,Y2=ppmv.Job_CW_Split_Data(Xdata, Ydata)
        #overwrite original fig and plot with new split data
        Plot_PLT.plot(X1,Y1,'b.',label='cool down')
        Plot_PLT.plot(X2,Y2,'r.',label='warm up')
        Plot_PLT.legend(loc='best')
        Plot_PLT.set_xlabel(XchoiceTK.get())
        Plot_PLT.set_ylabel(YchoiceTK.get())
    else:
        #overwrite original fig and plot with unsplit data
        Plot_PLT.plot(Xdata,Ydata,'.')
        Plot_PLT.set_xlabel(XchoiceTK.get())
        Plot_PLT.set_ylabel(YchoiceTK.get())
        
    
    #redraw canvas with ticks inside
    Plot_PLT.tick_params(direction='in')
    
    Plot_PLT.relim()
    Plot_PLT.autoscale()
    Fig_PLT.tight_layout()
    canvas_PLT.draw()
        
    
    
    
        
    
def Button_SaveFig(Fig_PLT):
    
    
    #Grab the file location and name from the user
    export_file_path = filedialog.asksaveasfilename(defaultextension='.png',filetypes=(('png','*.png'),('all files','*.*')))
                                    
    Fig_PLT.savefig(export_file_path)
    

    
    
def Button_UpdatePlotDP(canvas_PLT,Plot_PLT,Data_CL,XchoiceTK,YchoiceTK,DP_Label_ref,DP_Method_ref,DP_Legends_ref):
    #load current data
    Data_CL.load_data()
    
    #clear current plot
    Plot_PLT.clear()
    
    #use dividers, if avaliable
    if DP_Label_ref:
        #reset parse lists
        Data_CL.reset_parse()
        
        #add current lists of methods and labels to data class
        Data_CL.add_parse(DP_Label_ref, DP_Method_ref)
        
        #run class method to parseData with current info
        Data_CL.parseData()
        
        #Plot Individual Data Sections
        plotNum=len(DP_Label_ref)+1
        for i in range(plotNum):
            print(i)
            data=Data_CL.data_sections[i]
            
            #grab needed data
            Xdata=data[XchoiceTK.get()]
            Xname=XchoiceTK.get()
        
            Ydata=data[YchoiceTK.get()]
            Yname=YchoiceTK.get()
            
            #if user has a legend name, place that inside instead
            if DP_Legends_ref[i].get() != 'Insert Data Name':
                Plot_PLT.plot(Xdata,Ydata,label=DP_Legends_ref[i].get())
            else:
                Plot_PLT.plot(Xdata,Ydata,label='Section '+str(i+1)+': '+Data_CL.parse_results[i])
            Plot_PLT.set_xlabel(Xname)
            Plot_PLT.set_ylabel(Yname)
            Plot_PLT.legend(loc='best')
            
                
            
            
    else:
        #otherwise, just plot the data as is
        data=Data_CL.data
        #print(data.columns)
        
        #grab needed data
        Xdata=data[XchoiceTK.get()]
        Xname=XchoiceTK.get()
        
        Ydata=data[YchoiceTK.get()]
        Yname=YchoiceTK.get()
        
        Plot_PLT.plot(Xdata,Ydata)
        Plot_PLT.set_xlabel(Xname)
        Plot_PLT.set_ylabel(Yname)
        
    #redraw canvas with ticks inside
    Plot_PLT.tick_params(direction='in')
    
    Plot_PLT.relim()
    Plot_PLT.autoscale()
    canvas_PLT.draw()
    
    
def Button_UpdatePlotChi(canvas_PLT,Plot_PLT,DataCL,XchoiceTK,YchoiceTK,massSampleTK,massMolarTK,Chi_toggleTK):
    #Plotting for Mganetometry program. Updates data for magnetic settings
    
    #clear given plot
    Plot_PLT.clear()
    
    Xdata,Ydata=DataCL.get_axes(XchoiceTK,YchoiceTK)
    Field=DataCL.data['Field (Oe)']
    
    #Transform data depending on settings
    
    if Chi_toggleTK.get() == 'M (emu)':
        #no change
        x=Xdata
        y=Ydata
        
    elif Chi_toggleTK.get() == 'Mu (emu/mole)':
        #calc new y data for Mu
        MU=ppmv.Job_CalcMU(Xdata, Ydata, massSampleTK.get(), massMolarTK.get())
        
        x=Xdata
        y=MU
    
    elif Chi_toggleTK.get() == 'Chi (emu/[mole Oe])':
        Chi=ppmv.Job_CalcChi(Xdata, Field, Ydata, massSampleTK.get(), massMolarTK.get())
        
        x=Xdata
        y=Chi
        
    
    #Update plot with new axes and labels
    


"""
#### Object Creation Functions ####

These create several sets of objects that get commonly placed and tied together for
various PPMV applications. These can generate matplotlib objects, tkinter objects, and more.

functions return the needed widgets and objects associated with them
"""



    
def Empty_Plot(MasterTK):
    #creates a blank plot for use on a screen for a given Master
    #generate figure 
    fig=Figure()
    
    ax=fig.add_subplot()
    canvas=FigureCanvasTkAgg(fig,master=MasterTK)
    canvas.draw()
    
    toolbarFrame = tk.Frame(MasterTK)
    
    
    return canvas,fig,ax,toolbarFrame


