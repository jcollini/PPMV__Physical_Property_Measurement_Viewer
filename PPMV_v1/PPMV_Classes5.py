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

class DataPPMS():
    #class loads and allows for editable PPMS data
    def __init__(self,DataLocTK,MachineTK):
        #empty dataset
        self.data=pd.DataFrame()
        
        #strings needed to load data
        self.filenameTK=DataLocTK
        self.machineTK=MachineTK
        
        #Parsing Directions
        #list containing parased labels
        self.parse_labels=[]
        #list containing the methods used for each parse
        self.parse_methods=[]
        #Methods:
        #Shift_Direction -- values change direction from neg to pos or vice verse
        #Shift_Dynamic -- values change from constant value to a changing value or vice versa
        
        self.parse_results=[]
        #Results (outcome of Methods)
        #Neg to Pos
        #Pos to Neg
        #Static to Dynamic
        #Dynamic to Static
        
        #list containing parsed pandas dataframes
        self.data_indexcuts=[]
        self.data_sections=[]
    
    def load_data(self):
        #Load only needed data. This overwrites current data
        self.data=ppmv.Read_PPMS_File(self.filenameTK.get(), self.machineTK.get())
        
    def get_axes(self,Xchoice,Ychoice):
        #returns a selected x and y choice
        
        #load current data
        self.load_data()
        data=self.data
        
        #grab just x and y axes
        Xdata=data[Xchoice.get()]
        Ydata=data[Ychoice.get()]
        
        return Xdata,Ydata
        
    
    #definition for adding cuts
    def add_parse(self,labelsTK,methodsTK):
        dividerNum=len(labelsTK)
        for i in range(dividerNum):
            self.parse_labels.append(labelsTK[i].get())
            self.parse_methods.append(methodsTK[i].get())
            
    def reset_parse(self):
        #resets the parse lists
        self.parse_labels=[]
        self.parse_methods=[]
        self.parse_results=[]
        
        
    def method_Shift_Direction(self,data,label):
        splitvalue=0.1
        
        
        #using the label, grab the column of data used to split
        Xdata=data[label]
        
        #determine current direction of data
        direction=ppmv.DetermineDirection(Xdata)
        print(direction)
        self.parse_results.append(direction)
        
        #Find index of split
        Index=ppmv.Split_Sets_Index_Reversed(Xdata,splitvalue,direction)
        
        
        #split the whole set and save split
        data2=data.iloc[(Index+1):,:]
        data1=data.iloc[0:(Index+1),:]
        
        
        print('data1 temp')
        print(data1.iloc[0:5,0])
        print('data2 temp')
        print(data2.iloc[0:5,0])
        
        #return the new data sets and index used to cut
        return Index,data1,data2
        
    #definition for creating parsed data based on loaded
    def parseData(self):
        #for each added parse instruction, parse the data. 
        ParseLength=len(self.parse_labels)
        
        #load current selected data and save a copy to work with
        self.load_data()
        data=self.data #grab a copy of the original data to manipulate
        
        for i in range(ParseLength):
            #pick method and parse
            if self.parse_methods[i]=='Shift_Direction':
                index,data1,data2=self.method_Shift_Direction(data,self.parse_labels[i])
                #now return the cut data set and index
                #also make data2 the new data for the next turn in the loop
                self.data_sections.append(data1)
                self.data_indexcuts.append(index)
                data=data2 #remaining dataset for the next cycle
            
            if self.parse_methods[i]=='Shift_Dynamic':
                #method goes here
                print('this method not ready yet')
        
        #after loop is done, add remaining dataset to the last dataset section
        self.data_sections.append(data)
        
        #add last label depending on last result
        if self.parse_methods[-1]=='Shift_Direction':
            #determine direction of last dataset and add it to results
            splitval=0.1
            direction=ppmv.DetermineDirection(self.data_sections[-1])
            print(direction)
            self.parse_results.append(direction)
                


class WidgetsPPMV():
    #class generates groups of commonly used widgets
    def __init__(self):
        #General padding to have frames match
        self.JobFrame_Ysize=56
        #Padding if there is missing lines for the explaination text
        self.LinePadding=12
        
        self.ExFrameY=5 #boarder space around export frame
        self.ExportPadding=50 #seperation of export buttons
        self.ExportBoarderX=20 #boarder space around export buttons
        self.ExportBoarderY=5 #boarder space around export buttons
        self.ExFrameY=5 #boarder space around export frame
        
        #Options for PPMS and MPMS systems
        self.optionsMachine=['9T-ACT','9T-R','14T-ACT','14T-R','Dynacool','MPMS3']
        self.dataNames=['Temperature (K)',
                    'Field (Oe)',
                    'theta (deg)',
                    'Bridge1_R (ohms)',
                    'Bridge2_R (ohms)',
                    'Bridge3_R (ohms)',
                    'AC Moment (emu)',
                    'DC Moment Fixed Ctr (emu)',
                    'DC Moment Free Ctr (emu)']
        
    def Create_Root(self,title,icon):
        #controls rool application window
        self.root=tk.Tk()
        self.root.title(title)
        self.root.iconbitmap(icon)
        
    def Create_Toplevel(self,title,icon):
        #controls the window for cooling and warming
        self.rootApp=tk.Toplevel()
        self.rootApp.title(title)
        self.rootApp.iconbitmap(icon)
        self.rootApp.grab_set() #places this window as a priority for events
    
    def Create_Header(self,MasterTK,title,row,column):
        self.Header_L=tk.Label(MasterTK,text=title)
        self.Header_L.grid(row=row,column=column,pady=(0,10))
        
    def Create_RootLoadFrame(self,MasterTK,row,column):
        self.LoadFrame=tk.LabelFrame(MasterTK,text='Load PPMS Data',padx=194)
        self.LoadFrame.grid(row=row,column=column,padx=10,sticky=tk.W)
    
        #Widgets and placement
        #file and machine selection for data
        self.Machine=tk.StringVar()
        self.Machine.set('9T-R')

        self.DataLoc=tk.StringVar()
        self.DataLoc.set('')
    
        self.DataDisplay=tk.StringVar()
        self.DataDisplay.set('      No Data Loaded      ')
    
        #load data widgets
        self.Load_B=tk.Button(self.LoadFrame,text="Load data")
        self.Load_B.grid(row=0,column=0)
    
        self.Loadcheck_L=tk.Label(self.LoadFrame,text='File:')
        self.Loadcheck_L.grid(row=0,column=1,padx=(20,0))
    
        self.Loadcheck_E=tk.Label(self.LoadFrame,textvariable=self.DataDisplay,bg='white')
        self.Loadcheck_E.grid(row=0,column=2)
    
    
        self.Loadmachine_L=tk.Label(self.LoadFrame,text='Machine and Puck Used:')
        self.Loadmachine_L.grid(row=0,column=3,padx=(20,0))
    
        self.Loadmachine_D=tk.OptionMenu(self.LoadFrame, self.Machine, *self.optionsMachine)
        self.Loadmachine_D.grid(row=0,column=4)
    
    def Create_LoadFrame(self,MasterTK,dataloc_i,machinetype_i,row,column):
        #creates standard loadframe use for applications
        self.LoadFrame=tk.LabelFrame(MasterTK,text='Check/Change Loaded Data')
        self.LoadFrame.grid(row=row,column=column,padx=10,pady=self.ExFrameY,sticky=tk.W)
        #LoadFrame.grid_configure(ipadx=300)
        
        #Widgets and placement
        #file and machine selection for data
        self.Machine=tk.StringVar()
        self.Machine.set(machinetype_i)
    
        self.DataLoc=tk.StringVar()
        self.DataLoc.set(dataloc_i)
        
        self.DataDisplay=tk.StringVar()
        self.DataDisplay.set(dataloc_i[0:10]+'.......'+dataloc_i[-10:])
        
        #load data widgets
        self.Load_B=tk.Button(self.LoadFrame,text="Load data")
        
        self.Load_B.grid(row=0,column=0)
        
        self.Loadcheck_L=tk.Label(self.LoadFrame,text='File:')
        self.Loadcheck_L.grid(row=0,column=1)
        
        self.Loadcheck_E=tk.Label(self.LoadFrame,textvariable=self.DataDisplay,bg='white')
        self.Loadcheck_E.grid(row=0,column=2)
        
        
        self.Loadmachine_L=tk.Label(self.LoadFrame,text='Machine and Puck Used:')
        self.Loadmachine_L.grid(row=0,column=3)
        
       
        self.Loadmachine_D=tk.OptionMenu(self.LoadFrame, self.Machine, *self.optionsMachine)
        self.Loadmachine_D.grid(row=0,column=4)
        
    def Create_EmptyPlot(self,MasterTK,row,column):
        #create plot and put on screen. Have it empty to start
        self.canvas,self.Fig,self.Plot,self.toolbarFrame=bt.Empty_Plot(MasterTK)
        #set plot to screen
        self.canvas.get_tk_widget().grid(row=row,column=column,columnspan=2)
    
    
        self.toolbarFrame.grid(row=row+1,column=column,columnspan=2)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        self.Update_Bplot=tk.Button(MasterTK,text='Update Plot')
        self.Update_Bplot.grid(row=3,column=2,sticky=tk.E)
    
    def Create_ExportFrame(self,MasterTK,row,column):
        self.ExportFrame=tk.LabelFrame(MasterTK,text='Save/Export')
        self.ExportFrame.grid(row=row,column=column,columnspan=2,pady=self.ExFrameY)    
        #create save button for plot
        self.SaveFig_B=tk.Button(self.ExportFrame,text='Save Figure')
        self.SaveFig_B.grid(row=0,column=0,padx=(self.ExportBoarderX,self.ExportPadding),pady=self.ExportBoarderY)
        self.Export_B=tk.Button(self.ExportFrame,text='Save CSV')
        self.Export_B.grid(row=0,column=1,padx=(self.ExportPadding,self.ExportBoarderX),pady=self.ExportBoarderY)
        
    def Create_CWSettings(self,MasterTK,row,column):
        self.SetFrame=tk.LabelFrame(MasterTK,text='Settings')
        self.SetFrame.grid(row=row,column=column)
        
        #1st direction: pick axes
        help1='Seperate your data into Cooling and Warming curves\nChoose your x and y axis to split up'
        self.Direction1=tk.Label(self.SetFrame,text=help1)
        self.Direction1.grid(row=0,column=0,columnspan=2)
        
        #x and y axis drop down menu selection
        self.Xchoice=tk.StringVar()
        self.Ychoice=tk.StringVar()
        
        #set each as the usualy starting ones
        self.Xchoice.set('Temperature (K)')
        self.Ychoice.set('Bridge1_R (ohms)')
        
        #make menus
        self.QuickP_Xchoice_L=tk.Label(self.SetFrame,text='x axis')
        self.QuickP_Xchoice_L.grid(row=1,column=0)
        
        self.QuickP_Ychoice_L=tk.Label(self.SetFrame,text='y axis')
        self.QuickP_Ychoice_L.grid(row=2,column=0,pady=(0,5))
       
        self.QuickP_Xchoice_D=tk.OptionMenu(self.SetFrame, self.Xchoice, *self.dataNames)
        self.QuickP_Xchoice_D.grid(row=1,column=1)
        self.QuickP_Ychoice_D=tk.OptionMenu(self.SetFrame, self.Ychoice, *self.dataNames)
        self.QuickP_Ychoice_D.grid(row=2,column=1,pady=(0,5))
        
        #Cooling and Warming radio buttons toggle
        self.Radio_L=tk.Label(self.SetFrame,text='Cooling/Warming toggle')
        self.Radio_L.grid(row=3,column=0,rowspan=2)
        
        #test label
        self.CW_Toggle=tk.BooleanVar()
        self.CW_Toggle.set(False)
        
    
        self.RadioOff=tk.Radiobutton(self.SetFrame,text='off',variable=self.CW_Toggle, value=False)
        self.RadioOff.grid(row=3,column=1,sticky=tk.W)
        
        self.RadioOn=tk.Radiobutton(self.SetFrame,text='on',variable=self.CW_Toggle, value=True)
        self.RadioOn.grid(row=4,column=1,sticky=tk.W)
    
        #make update button for plot below settings settings
        self.Update_Bset=tk.Button(self.SetFrame,text='Update Plot')
        self.Update_Bset.grid(row=5,column=0) 
        

class AppBox():
    
    
    
    def __init__(self,MasterTK,title,row,column):
        
        #General padding to have frames match
        self.JobFrame_Ysize=56
        #Padding if there is missing lines for the explaination text
        self.LinePadding=12
        
        self.ExFrameY=5 #boarder space around export frame
        self.ExportPadding=50 #seperation of export buttons
        self.ExportBoarderX=20 #boarder space around export buttons
        self.ExportBoarderY=5 #boarder space around export buttons
        self.ExFrameY=5 #boarder space around export frame
        
        #Options for PPMS and MPMS systems
        self.optionsMachine=['9T-ACT','9T-R','14T-ACT','14T-R','Dynacool','MPMS3']
        self.dataNames=['Temperature (K)',
                    'Field (Oe)',
                    'theta (deg)',
                    'Bridge1_R (ohms)',
                    'Bridge2_R (ohms)',
                    'Bridge3_R (ohms)',
                    'AC Moment (emu)',
                    'DC Moment Fixed Ctr (emu)',
                    'DC Moment Free Ctr (emu)']
        
        
        self.title=title
        self.row=row
        self.column=column
        self.MasterTK=MasterTK
        
    def Create_QuickPlot(self):
        self.PlotFrame=tk.LabelFrame(self.MasterTK,text='Plot Frame')
        self.PlotFrame.grid(row=self.row,column=self.column,padx=10,pady=10)
    
        #plot icon
        self.QuickP_icon=tk.Label(self.PlotFrame,text='***Plot Icon***')
        self.QuickP_icon.grid(row=0,column=0,columnspan=2)
    
        #plot explanation
        self.QuickP_explain=tk.Label(self.PlotFrame,text='Plot your loaded data.\nPick x and y axis from menu.')
        self.QuickP_explain.grid(row=1,column=0,columnspan=2)
        
        #plot button
        self.QuickP_B=tk.Button(self.PlotFrame,text='Quick Plot')
        self.QuickP_B.grid(row=2,column=0,columnspan=2)
        
        #x and y axis drop down menu selection
        self.Xchoice=tk.StringVar()
        self.Ychoice=tk.StringVar()
        #set each as the usualy starting ones
        self.Xchoice.set('Temperature (K)')
        self.Ychoice.set('Bridge1_R (ohms)')
        #make menus
        self.QuickP_Xchoice_L=tk.Label(self.PlotFrame,text='x axis')
        self.QuickP_Xchoice_L.grid(row=3,column=0)
    
        self.QuickP_Ychoice_L=tk.Label(self.PlotFrame,text='y axis')
        self.QuickP_Ychoice_L.grid(row=4,column=0,pady=(0,5))
        
        
        
        self.QuickP_Xchoice_D=tk.OptionMenu(self.PlotFrame, self.Xchoice, *self.dataNames)
        self.QuickP_Xchoice_D.grid(row=3,column=1)
        self.QuickP_Ychoice_D=tk.OptionMenu(self.PlotFrame, self.Ychoice, *self.dataNames)
        self.QuickP_Ychoice_D.grid(row=4,column=1,pady=(0,5))
        
        
    def Create_Export(self):
        self.ExportFrame=tk.LabelFrame(self.MasterTK,text='Export Frame')
        self.ExportFrame.grid(row=self.row,column=self.column,padx=10,pady=10)
    
        #explort icon and explanation
        self.Export_icon=tk.Label(self.ExportFrame,text='***Export Icon***')
        self.Export_icon.grid(row=0,column=0)
    
        self.Export_explain=tk.Label(self.ExportFrame,text='Export PPMS data \nto CSV.')
        self.Export_explain.grid(row=1,column=0)
    
        #Simple File Output button
        self.Export_file_B=tk.Button(self.ExportFrame,text='Export (.dat) data \n to (.csv)')
        self.Export_file_B.grid(row=2,column=0,pady=(self.JobFrame_Ysize,5),padx=45)
        
        
    def Create_Launcher(self,AppIcon,AppText):
        self.AppFrame=tk.LabelFrame(self.MasterTK,text=self.title)
        self.AppFrame.grid(row=self.row,column=self.column,padx=10,pady=10)
    
        #explort icon and explanation
        self.App_icon=tk.Label(self.AppFrame,text=AppIcon)
        self.App_icon.grid(row=0,column=0)
    
        self.App_explain=tk.Label(self.AppFrame,text=AppText)
        self.App_explain.grid(row=1,column=0)
    
        #Simple File Output button
        self.App_B=tk.Button(self.AppFrame,text=self.title)
        self.App_B.grid(row=2,column=0,pady=(self.JobFrame_Ysize,5),padx=32)
        
        