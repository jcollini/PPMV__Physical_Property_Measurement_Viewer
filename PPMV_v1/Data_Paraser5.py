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


import Button_Functions5 as bt
import PPMV_Jobs5 as ppmv
import PPMV_Classes5 as cl

import Cooling_Warming5 as cw
import Data_Paraser5 as dp




    
def Button_UpdatePlotDP(canvas_PLT,Plot_PLT,Data_CL,XchoiceTK,YchoiceTK,DP_Label_ref,DP_Method_ref):
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
        
            Plot_PLT.plot(Xdata,Ydata,label='Section '+str(i+1)+': '+Data_CL.parse_results[i])
            Plot_PLT.set_xlabel(Xname)
            Plot_PLT.set_ylabel(Yname)
            Plot_PLT.legend(loc='best')
                
            
            
    else:
        #otherwise, just plot the data as is
        data=Data_CL.data
        print(data.columns)
        
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
    
    
  

def App_DataParaser(DataLoc,MachineType):
    
    #create CL object for the window
    DP=cl.WidgetsPPMV()
    DP.Create_Toplevel('PPMV Data Parser', 'QMC_Temp.ico')
   

####Header widget
    DP.Create_Header(DP.rootApp, 'PPMV Data Parser', 0, 0)
   
    
    
    
####Load Frame
    DP.Create_LoadFrame(DP.rootApp, DataLoc, MachineType, 1, 0)
    
    
    #show load buttons and import load from the previous window
    #load data widgets
    DP.Load_B.configure(command=lambda: bt.Button_LoadData(DP.rootApp, 
                                                           DP.DataLoc, 
                                                           DP.DataDisplay, 
                                                           DP.Machine, 
                                                           Data))
    
    
    
   
    

####Plotting
    DP.Create_EmptyPlot(DP.rootApp, 2, 1, 3,2)
    #update plot
    DP.Update_Bplot.configure(command=lambda: Button_UpdatePlotDP(DP.canvas, 
                                                                  DP.Plot, 
                                                                  Data, 
                                                                  DP.Xchoice, 
                                                                  DP.Ychoice, 
                                                                  DP.Labels_ref,
                                                                  DP.Methods_ref))
    
####PlotFrame
    DP.Create_PlotSettingsFrame(DP.rootApp, 2, 0)
    
    #update plot
    DP.Update_Bsettings.configure(command=lambda: Button_UpdatePlotDP(DP.canvas, 
                                                                  DP.Plot, 
                                                                  Data, 
                                                                  DP.Xchoice, 
                                                                  DP.Ychoice, 
                                                                  DP.Labels_ref,
                                                                  DP.Methods_ref))
    
   
    
    
####Parsing Settings Frame
    
    #directions for user
    Explain_L=tk.Label(DP.rootApp,text='For each divider, select the data \nused to split and the method for splitting')
    Explain_L.grid(row=3,column=0)
    DP.Create_ParseSettingsFrame(DP.rootApp, 4, 0)
    
    
    DP.Add_Row_B.configure(command=lambda: DP.add_parse_section(DP.ParseFrame))
    
    DP.Remove_Row_B.configure(command=lambda: DP.remove_parse_section(DP.ParseFrame))
    
    

####Data Object for window
    Data=cl.DataPPMS(DP.DataLoc,DP.Machine)

    
    
    
    
    
    

