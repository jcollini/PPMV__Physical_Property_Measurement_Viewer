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
    DP.Update_Bplot.configure(command=lambda: bt.Button_UpdatePlotDP(DP.canvas, 
                                                                  DP.Plot,
                                                                  DP.Fig,
                                                                  Data, 
                                                                  DP.Xchoice, 
                                                                  DP.Ychoice, 
                                                                  DP.Labels_ref,
                                                                  DP.Methods_ref,
                                                                  DP.Divider_Legend_names))
    
####PlotFrame
    DP.Create_PlotSettingsFrame(DP.rootApp, 2, 0)
    
    #update plot
    DP.Update_Bsettings.configure(command=lambda: bt.Button_UpdatePlotDP(DP.canvas, 
                                                                  DP.Plot,
                                                                  DP.Fig,
                                                                  Data, 
                                                                  DP.Xchoice, 
                                                                  DP.Ychoice, 
                                                                  DP.Labels_ref,
                                                                  DP.Methods_ref,
                                                                  DP.Divider_Legend_names))
    

####Save/Export frame
    DP.Create_ExportFrame(DP.rootApp,1,1)
    DP.SaveFig_B.configure(command=lambda: bt.Button_SaveFig(DP.Fig))
    DP.Export_B.configure(command=lambda: bt.Button_ExportDP_CSVs(Data, 
                                                                     DP.Labels_ref, 
                                                                     DP.Methods_ref, 
                                                                     DP.Divider_Legend_names))
    
    
    
    
    
   
    
    
####Parsing Settings Frame
    
    #directions for user
    DP.Create_ParseSettingsFrame(DP.rootApp, 3, 0)
    
    
    DP.Add_Row_B.configure(command=lambda: DP.add_parse_section(DP.ParseFrame))
    
    DP.Remove_Row_B.configure(command=lambda: DP.remove_parse_section(DP.ParseFrame))
    
    

####Data Object for window
    Data=cl.DataPPMS(DP.DataLoc,DP.Machine)

    
    
    
    
    
    

