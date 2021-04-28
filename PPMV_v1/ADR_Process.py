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
    
    ####Settings Frames
    ADR.Create_ADR1SampleFrame(ADR.rootApp, 4, 0)
    ADR.Create_ADR2SampleFrame(ADR.rootApp, 4, 4)
    
    ####Export Frame
    ADR.Create_ExportFrame(ADR.rootApp, 1, 3)
    
   