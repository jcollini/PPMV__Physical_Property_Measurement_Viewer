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

def App_Magnetometry(dataloc,machinetype):
    
    #create CW object and window
    CW=cl.WidgetsPPMV()
    CW.Create_Toplevel('PPMV Magnetometry', 'QMC_Temp.ico')
  

    
####Header widget
    CW.Create_Header(CW.rootApp,'PPMV Magnetometry',0,0)
    
####Load Frame
    #create loadframe and everything inside it
    CW.Create_LoadFrame(CW.rootApp,dataloc,machinetype,1,0)
    
    
    CW.Load_B.configure(command=lambda: bt.Button_LoadData(CW.rootApp, 
                                                           CW.DataLoc, 
                                                           CW.DataDisplay, 
                                                           CW.Machine, 
                                                           Data))
    
    
####Plotting
    CW.Create_EmptyPlot(CW.rootApp,2,1,1,2)
    
    
####Save/Export frame
    CW.Create_ExportFrame(CW.rootApp,1,1)
    CW.SaveFig_B.configure(command=lambda: bt.Button_SaveFig(CW.Fig))
    

####Settings Frame
    CW.Create_ChiSettingsFrame(CW.rootApp, 2, 0)
    
    

####Data Object for window
    Data=cl.DataPPMS(CW.DataLoc,CW.Machine)
   