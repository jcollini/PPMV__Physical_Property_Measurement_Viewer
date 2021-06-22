# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 11:49:22 2020

@author: jccol
"""


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
    
    
  

def App_ADRProcess():
    
    #create app object
    ADR=cl.WidgetsPPMV()
    ADR.Create_Toplevel('PPMV ADR Processing', 'QMC_Temp.ico')
    
    
    ####Header widget
    ADR.Create_Header(ADR.rootApp, 'PPMV ADR Processing', 0, 0)
    
    
    ####Empty Plot widget
    ADR.Create_ADREmptyPlot(ADR.rootApp, 2, 0, 1, 3)
    ADR.Create_ADREmptyPlot2(ADR.rootApp, 2, 3, 1, 3)
    
    ####Load Data frame
    ADR.Create_ADRLoadFrame(ADR.rootApp, 1, 0)
    
    ADR.Load_B.configure(command=lambda: bt.Button_LoadData(ADR.rootApp, 
                                                           ADR.DataLoc, 
                                                           ADR.DataDisplay, 
                                                           ADR.Machine, 
                                                           Data))
    
    ####Settings Frames
    ADR.Create_ADR1SampleFrame(ADR.rootApp, 4, 0)
    ADR.Create_ADR2SampleFrame(ADR.rootApp, 4, 4)
    
    ADR.Update1_B.configure(command=lambda: bt.Button_UpdateADRPlot(Data, 
                                                                    1, 
                                                                    ADR.canvas, 
                                                                    ADR.Plot, 
                                                                    ADR.Fig, 
                                                                    ADR.X1))
    
    ADR.Update2_B.configure(command=lambda: bt.Button_UpdateADRPlot(Data, 
                                                                    2, 
                                                                    ADR.canvas2, 
                                                                    ADR.Plot2, 
                                                                    ADR.Fig2, 
                                                                    ADR.X2))
    ####Export Frame
    ADR.Create_ExportFrame(ADR.rootApp, 1, 3)
    
    ADR.SaveFig_B.configure(command=lambda: bt.Button_SaveFigADR(ADR.Fig,
                                                                 ADR.Fig2))
    
    ADR.Export_B.config(command=lambda: bt.Button_ExportADR_CSVs(Data))
    
    
    ####Data Object for window
    Data=cl.DataPPMS(ADR.DataLoc,ADR.Machine)
    
   