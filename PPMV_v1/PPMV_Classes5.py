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
                


class WidgetsPPMS():
    #class generates groups of commonly used widgets
    def __init__(self):
        self.ExFrameY=5 #boarder space around export frame
    
    def Create_LoadFrame(self,MasterTK,dataloc_i,machinetype_i):
        #creates standard loadframe use for applications
        self.LoadFrame=tk.LabelFrame(MasterTK,text='Check/Change Loaded Data')
        self.LoadFrame.grid(row=1,column=0,padx=10,pady=self.ExFrameY,sticky=tk.W)
        #LoadFrame.grid_configure(ipadx=300)
        
        #Widgets and placement
        #file and machine selection for data
        self.Machine=tk.StringVar()
        self.Machine.set(machinetype_i)
    
        self.DataLoc=tk.StringVar()
        self.DataLoc.set(machinetype_i)
        
        self.DataDisplay=tk.StringVar()
        self.DataDisplay.set('      No Data Loaded      ')
        
        #load data widgets
        self.Load_B=tk.Button(self.LoadFrame,text="Load data")
        
        self.Load_B.grid(row=0,column=0)
        
        self.Loadcheck_L=tk.Label(self.LoadFrame,text='File:')
        self.Loadcheck_L.grid(row=0,column=1)
        
        self.Loadcheck_E=tk.Label(self.LoadFrame,textvariable=self.DataDisplay,bg='white')
        self.Loadcheck_E.grid(row=0,column=2)
        
        
        self.Loadmachine_L=tk.Label(self.LoadFrame,text='PPMS and Puck Used:')
        self.Loadmachine_L.grid(row=0,column=3)
        
        optionsMachine=['9T-ACT','9T-R','14T-ACT','14T-R','Dynacool']
        self.Loadmachine_D=tk.OptionMenu(self.LoadFrame, self.Machine, *optionsMachine)
        self.Loadmachine_D.grid(row=0,column=4)
                    