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
import Multi_Plot as mp
import ADR_Process as adr
"""
Designer and Programer: John Collini
Front end design for PPMV (Physical Property Measurement Viewer)
Style is a LAUNCHER

Main controls the tkinter widgets and places them onto the screen

"""
    



#Needed Functions for buttons and selections


if __name__=='__main__':

    #Generate root and data
    PPMV=cl.WidgetsPPMV()
    
####Root window characteristics
    PPMV.Create_Root('Physical Property Measurement Viewer (PPMV)', 'QMC_Temp.ico')
    
    #Header widget
    PPMV.Create_Header(PPMV.root,'Physical Property Measurement Viewer (PPMV)' , 0, 0)
    

####Load Frame
    PPMV.Create_RootLoadFrame(PPMV.root, 1, 0)
    
    PPMV.Load_B.configure(command=lambda: bt.Button_LoadData(PPMV.root,
                                                             PPMV.DataLoc,
                                                             PPMV.DataDisplay,
                                                             PPMV.Machine,
                                                             Data))
   

####Jobs Frame 
    JobsFrame=tk.LabelFrame(PPMV.root)
    JobsFrame.grid(row=2,column=0,padx=10,pady=(0,10),sticky=tk.W)
    
####quick plot frame and widges
    PlotApp=cl.AppBox(JobsFrame,'Plot Frame','Icon_Quick_Plot.png', 0, 0)
    PlotApp.Create_QuickPlot()
    
    #plot button
    PlotApp.QuickP_B.configure(command=lambda: bt.Button_QuickPlot(Data, 
                                                           PlotApp.Xchoice, 
                                                           PlotApp.Ychoice))
    
####Export CSV Frame
    ExpApp=cl.AppBox(JobsFrame, 'Export Frame','Icon_Quick_Export.png', 0, 1)
    ExpApp.Create_Export()
    
    #Simple File Output button
    ExpApp.Export_file_B.configure(command=lambda: bt.Button_QuickSave_CSV(Data))
    
    
####Cooling and Warming Frame
    CWApp=cl.AppBox(JobsFrame, 'Cooling and Warming','Icon_CW.png', 0, 2)
    CWApp.Create_Launcher('Seperating and plotting cooling \nand warming curves')
    
    #Simple File Output button
    CWApp.App_B.configure(command=lambda: cw.App_CoolingWarming(PPMV.DataLoc.get(), PPMV.Machine.get()))
    
    
####Magnetoresistance Frame'
    MagApp=cl.AppBox(JobsFrame,'Magnetoresistance','Icon_MR.png',0,3)
    MagApp.Create_Launcher('Seperating and plotting \nmagnetoresistance curves')
    
    

####Advanced Plot Frame
    MultiPlotApp=cl.AppBox(JobsFrame, 'Multi Plotting','Icon_MP.png', 1, 0)
    MultiPlotApp.Create_Launcher('Application for plotting\nmultiple data sets together')
    
    MultiPlotApp.App_B.configure(command=lambda: mp.App_MultiPlot())
    
    

####Custom PPMS File Editor 
    CustomApp=cl.AppBox(JobsFrame, 'Parse Data','Icon_DP.png', 1, 1)
    CustomApp.Create_Launcher('Application for editting \nand parsing PPMS data')
    
    CustomApp.App_B.configure(command=lambda: dp.App_DataParaser(PPMV.DataLoc.get(), PPMV.Machine.get()))

####Magnetometery Frame
    ChiApp=cl.AppBox(JobsFrame, 'Magnetometry','Icon_Chi.png', 1, 2)
    ChiApp.Create_Launcher('Simple manipulation for\nMPMPS files')
    
    #Simple File Output button
    ChiApp.App_B.configure(command=lambda: chi.App_Magnetometry(PPMV.DataLoc.get(), PPMV.Machine.get()))
    
####ADR Frame
    ADRApp=cl.AppBox(JobsFrame, 'ADR Processing','Icon_Empty.png', 1, 3)
    ADRApp.Create_Launcher('Process ADR datafiles\n')
    
    #Simple File Output button
    ADRApp.App_B.configure(command=lambda: adr.App_ADRProcess())
    
       
    

####Loaded Data
    Data=cl.DataPPMS(PPMV.DataLoc, PPMV.Machine)
    

    


    
    
    
    
    
    
    
    
    
    
    
    
    
    #Run Window
    PPMV.root.mainloop()