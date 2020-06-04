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


def App_CoolingWarming(dataloc,machinetype):

    
    #create CW object and window
    CW=cl.WidgetsPPMV()
    CW.Create_Toplevel('PPMV Cooling and Warming', 'QMC_Temp.ico')
  

    
####Header widget
    CW.Create_Header(CW.rootApp,'PPMV Cooling and Warming',0,0)
    
####Load Frame
    #create loadframe and everything inside it
    CW.Create_LoadFrame(CW.rootApp,dataloc,machinetype,1,0)
    
    
    CW.Load_B.configure(command=lambda: bt.Button_LoadData(CW.rootApp, 
                                                           CW.DataLoc, 
                                                           CW.DataDisplay, 
                                                           CW.Machine, 
                                                           Data))
    
    
####Plotting
    CW.Create_EmptyPlot(CW.rootApp,2,1)
    
    
####Save/Export frame
    CW.Create_ExportFrame(CW.rootApp,1,1)
    CW.SaveFig_B.configure(command=lambda: bt.Button_SaveFig(CW.Fig))
    
    
    #create export CVS button
    CW.Export_B.configure(command=lambda: bt.Button_ExportCW_CSVs(CW.rootApp, 
                                                                  Data, 
                                                                  CW.Xchoice, 
                                                                  CW.Ychoice, 
                                                                  CW.CW_Toggle))
    
    
    
   
    
    
    
####Cooling and Warming Settings Frame
    CW.Create_CWSettings(CW.rootApp,2,0)
    CW.Update_Bset.configure(command=lambda:bt.Button_UpdatePlotCW(CW.rootApp, 
                                                                   CW.canvas,
                                                                   CW.Plot,
                                                                   Data, 
                                                                   CW.Xchoice, 
                                                                   CW.Ychoice, 
                                                                   CW.CW_Toggle))
    
    #make update button below the plot
    Update_B=tk.Button(CW.rootApp,text='Update Plot',command=lambda:bt.Button_UpdatePlotCW(CW.rootApp, 
                                                                                     CW.canvas,
                                                                                     CW.Plot, 
                                                                                     Data, 
                                                                                     CW.Xchoice, 
                                                                                     CW.Ychoice, 
                                                                                     CW.CW_Toggle))
    Update_B.grid(row=3,column=2,sticky=tk.E)

    
    
    
####Data Object for window
    Data=cl.DataPPMS(CW.DataLoc,CW.Machine)
    
    
    
    
    
        
    
    
