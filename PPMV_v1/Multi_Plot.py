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
    
    
  

def App_MultiPlot():
    
    #create app object
    MP=cl.WidgetsPPMV()
    MP.Create_Toplevel('PPMV Multi-Plot', 'QMC_Temp.ico')
    
    
    ####Header widget
    MP.Create_Header(MP.rootApp, 'PPMV Multi-Plot', 0, 0)
    
    ####Directions widget
    MP.Create_MultiPlotDirections(MP.rootApp, 1, 0)
    
    ####Empty Plot widget
    MP.Create_EmptyPlot(MP.rootApp, 2, 1, 2, 2)
    MP.Update_Bplot.configure(command=lambda: bt.Button_UpdatePlotMP(MP.canvas,
                                                                  MP.Plot,
                                                                  MP.Fig,
                                                                  MP.Xchoice,
                                                                  MP.Ychoice,
                                                                  MP.FileVar_ref,
                                                                  MP.MachineVar_ref,
                                                                  MP.MarkerVar_ref,
                                                                  MP.ColorVar_ref,
                                                                  MP.LegendVar_ref,
                                                                  MP.DataVar_ref)) 
    
    ####Load File Settings
    MP.Create_MultiPlotSettingsFrame(MP.rootApp, 2, 0)
    
    ####Plot Settings
    MP.Create_PlotSettingsFrame(MP.rootApp, 3, 0)
    
    MP.Update_Bsettings.configure(command=lambda: bt.Button_UpdatePlotMP(MP.canvas,
                                                                  MP.Plot,
                                                                  MP.Fig,
                                                                  MP.Xchoice,
                                                                  MP.Ychoice,
                                                                  MP.FileVar_ref,
                                                                  MP.MachineVar_ref,
                                                                  MP.MarkerVar_ref,
                                                                  MP.ColorVar_ref,
                                                                  MP.LegendVar_ref,
                                                                  MP.DataVar_ref)) 
    
    