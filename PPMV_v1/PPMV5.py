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
"""
Designer and Programer: John Collini
Front end design for PPMV (Physical Property Measurement Viewer)
Style is a LAUNCHER

Main controls the tkinter widgets and places them onto the screen

"""
    



#Needed Functions for buttons and selections


if __name__=='__main__':


    
####Root window characteristics
    root=tk.Tk()
    root.title('Physical Property Measurement Viewer (PPMV)')
    root.iconbitmap('QMC_Temp.ico')
    
    #Header widget
    Header_L=tk.Label(root,text='Physical Property Measurement Viewer (PPMV)')
    Header_L.grid(row=0,column=0,pady=(0,10))
    

####General Settings
    #General padding to have frames match
    JobFrame_Ysize=56
    #Padding if there is missing lines for the explaination text
    LinePadding=12
        

####Load Frame
    LoadFrame=tk.LabelFrame(root,text='Load PPMS Data',padx=205)
    LoadFrame.grid(row=1,column=0,padx=10,sticky=tk.W)
    
    #Widgets and placement
    #file and machine selection for data
    Machine=tk.StringVar()
    Machine.set('9T-R')

    DataLoc=tk.StringVar()
    DataLoc.set('')
    
    DataDisplay=tk.StringVar()
    DataDisplay.set('      No Data Loaded      ')
    
    #load data widgets
    Load_B=tk.Button(LoadFrame,text="Load data",command=lambda: bt.Button_LoadData(root,
                                                                                   DataLoc,
                                                                                   DataDisplay,
                                                                                   Machine,
                                                                                   Data))
    Load_B.grid(row=0,column=0)
    
    Loadcheck_L=tk.Label(LoadFrame,text='File:')
    Loadcheck_L.grid(row=0,column=1,padx=(20,0))
    
    Loadcheck_E=tk.Label(LoadFrame,textvariable=DataDisplay,bg='white')
    Loadcheck_E.grid(row=0,column=2)
    
    
    Loadmachine_L=tk.Label(LoadFrame,text='PPMS and Puck Used:')
    Loadmachine_L.grid(row=0,column=3,padx=(20,0))
    
    optionsMachine=['9T-ACT','9T-R','14T-ACT','14T-R','Dynacool']
    Loadmachine_D=tk.OptionMenu(LoadFrame, Machine, *optionsMachine)
    Loadmachine_D.grid(row=0,column=4)

####Jobs Frame 
    JobsFrame=tk.LabelFrame(root,text='Jobs Frame')
    JobsFrame.grid(row=2,column=0,padx=10,pady=(0,10),sticky=tk.W)
    #JobsFrame.grid_configure(ipadx=85)
    
####quick plot frame and widges
    PlotFrame=tk.LabelFrame(JobsFrame,text='Plot Frame')
    PlotFrame.grid(row=0,column=0,padx=10,pady=10)
    
    #plot icon
    QuickP_icon=tk.Label(PlotFrame,text='***Plot Icon***')
    QuickP_icon.grid(row=0,column=0,columnspan=2)
    
    #plot explanation
    QuickP_explain=tk.Label(PlotFrame,text='Plot your loaded data.\nPick x and y axis from menu.')
    QuickP_explain.grid(row=1,column=0,columnspan=2)
    
    #plot button
    QuickP_B=tk.Button(PlotFrame,text='Quick Plot',command=lambda: bt.Button_QuickPlot(Data, 
                                                                               Xchoice, 
                                                                               Ychoice))
    QuickP_B.grid(row=2,column=0,columnspan=2)
    
    #x and y axis drop down menu selection
    Xchoice=tk.StringVar()
    Ychoice=tk.StringVar()
    #set each as the usualy starting ones
    Xchoice.set('Temperature (K)')
    Ychoice.set('Bridge1_R (ohms)')
    #make menus
    QuickP_Xchoice_L=tk.Label(PlotFrame,text='x axis')
    QuickP_Xchoice_L.grid(row=3,column=0)
    
    QuickP_Ychoice_L=tk.Label(PlotFrame,text='y axis')
    QuickP_Ychoice_L.grid(row=4,column=0,pady=(0,5))
   
    QuickP_Xchoice_D=tk.OptionMenu(PlotFrame, Xchoice, 'Temperature (K)',
                                   'Field (Oe)',
                                   'theta (deg)',
                                   'Bridge1_R (ohms)',
                                   'Bridge2_R (ohms)',
                                   'Bridge3_R (ohms)')
    QuickP_Xchoice_D.grid(row=3,column=1)
    QuickP_Ychoice_D=tk.OptionMenu(PlotFrame, Ychoice, 'Temperature (K)',
                                   'Field (Oe)',
                                   'theta (deg)',
                                   'Bridge1_R (ohms)',
                                   'Bridge2_R (ohms)',
                                   'Bridge3_R (ohms)')
    QuickP_Ychoice_D.grid(row=4,column=1,pady=(0,5))
    
####Export CSV Frame   
    ExportFrame=tk.LabelFrame(JobsFrame,text='Export Frame')
    ExportFrame.grid(row=0,column=1,padx=10,pady=10)
    
    #explort icon and explanation
    Export_icon=tk.Label(ExportFrame,text='***Export Icon***')
    Export_icon.grid(row=0,column=0)
    
    Export_explain=tk.Label(ExportFrame,text='Export PPMS data \nto CSV.')
    Export_explain.grid(row=1,column=0)
    
    #Simple File Output button
    Export_file_B=tk.Button(ExportFrame,text='Export (.dat) data \n to (.csv)',command=lambda: bt.Button_QuickSave_CSV(Data))
    Export_file_B.grid(row=2,column=0,pady=(JobFrame_Ysize,5),padx=45)
    
    
####Cooling and Warming Frame
    CWFrame=tk.LabelFrame(JobsFrame,text='Cooling and Warming')
    CWFrame.grid(row=0,column=2,padx=10,pady=10)
    
    #explort icon and explanation
    CW_icon=tk.Label(CWFrame,text='***CW Icon***')
    CW_icon.grid(row=0,column=0)
    
    CW_explain=tk.Label(CWFrame,text='Application for seperating \nand plotting cooling \nand warming curves')
    CW_explain.grid(row=1,column=0)
    
    #Simple File Output button
    CW_B=tk.Button(CWFrame,text='Cooling and Warming',command=lambda: cw.App_CoolingWarming(DataLoc.get(), Machine.get()))
    CW_B.grid(row=2,column=0,pady=(JobFrame_Ysize,5),padx=32)
    
####Magnetoresistance Frame
    MRFrame=tk.LabelFrame(JobsFrame,text='Magnetoresistance')
    MRFrame.grid(row=0,column=3,padx=10,pady=10)
    
    #explort icon and explanation
    MR_icon=tk.Label(MRFrame,text='***MR Icon***')
    MR_icon.grid(row=0,column=0)
    
    MR_explain=tk.Label(MRFrame,text='Application for seperating \n and plotting \nmagnetoresistance curves')
    MR_explain.grid(row=1,column=0)
    
    #Simple File Output button
    MR_B=tk.Button(MRFrame,text='Magnetoresistance')
    MR_B.grid(row=2,column=0,pady=(JobFrame_Ysize,5),padx=32)
    

####Advanced Plot Frame
    AdvPlotFrame=tk.LabelFrame(JobsFrame,text='Advanced Plotting')
    AdvPlotFrame.grid(row=1,column=0,padx=10,pady=10)
    
    #explort icon and explanation
    AdvPlot_icon=tk.Label(AdvPlotFrame,text='***Adv Plot Icon***')
    AdvPlot_icon.grid(row=0,column=0)
    
    AdvPlot_explain=tk.Label(AdvPlotFrame,text='Application showing advanced \nplot settings for data\n')
    AdvPlot_explain.grid(row=1,column=0)
    
    #Simple File Output button
    AdvPlot_B=tk.Button(AdvPlotFrame,text='Advanced Plot')
    AdvPlot_B.grid(row=2,column=0,pady=(JobFrame_Ysize,5),padx=32)
    

####Custom PPMS File Editor 
    CustomFrame=tk.LabelFrame(JobsFrame,text='Parse PPMS File')
    CustomFrame.grid(row=1,column=1,padx=10,pady=10)
    
    #explort icon and explanation
    Custom_icon=tk.Label(CustomFrame,text='***Parse Icon***')
    Custom_icon.grid(row=0,column=0)
    
    Custom_explain=tk.Label(CustomFrame,text='Application for editting \nand parsing PPMS data\n')
    Custom_explain.grid(row=1,column=0)
    
    #Simple File Output button
    Custom_B=tk.Button(CustomFrame,text='Parse Data',command=lambda: dp.App_DataParaser(Loadcheck_E.get(), Machine.get()))
    Custom_B.grid(row=2,column=0,pady=(JobFrame_Ysize,5),padx=70)
    

####Loaded Data
    Data=cl.DataPPMS(DataLoc, Machine)
    

    


    
    
    
    
    
    
    
    
    
    
    
    
    
    #Run Window
    root.mainloop()