#Needed Classes for PPMV
import pandas as pd

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from tkinter import filedialog

import PPMV_Jobs4 as ppmv


class PPMSData():
    #class loads and allows for editable PPMS data
    def __init__(self):
        #empty dataset
        self.data=pd.DataFrame()
        
        #Parsing Directions
        #list containing parased labels
        self.parse_labels=[]
        #list containing the methods used for each parse
        self.parse_methods=[]
        #Methods:
        #Shift_Direction -- values change direction from neg to pos or vice verse
        #Shift_Dynamic -- values change from constant value to a changing value or vice versa
        
        #list continating absolute split value changes
        self.parse_values=[]
        
        #list containing parsed pandas dataframes
        self.data_indexcuts=[]
        self.data_sections=[]
    
    def load_data(self,DataLoc,MachineType):
        #Load only needed data. This overwrites current data
        self.data=ppmv.Read_PPMS_File(DataLoc, MachineType)
        
    
    #definition for adding cuts
    def add_parse(self,label,method,splitvalue):
        self.parse_labels.append(label)
        self.parse_methods.append(method)
        self.parse_values.append(splitvalue)
        
    def method_Shift_Direction(data,label,splitvalue):
        #using the label, grab the column of data used to split
        Xdata=data[label]
        
        #determine current direction of data
        direction=ppmv.DetermineDirection(Xdata)
        print(direction)
        
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
        #for each added parse instruction, parse the data. Subtract 1 to save the remaining data for last
        ParseLength=len(self.parse_labels)-1
        data=self.data #grab a copy of the original data to manipulate
        
        for i in range(ParseLength):
            #pick method and parse
            if self.parse_methods[i]=='Shift_Direction':
                index,data1,data2=self.method_Shift_Direction(data,self.parse_labels[i],self.parse_values[i])
                #now return the cut data set and index
                #also make data2 the new data for the next turn in the loop
                self.data_sections.append(data1)
                self.data_indexcuts.append(index)
                data=data2 #remaining dataset for the next cycle
            
            if self.parse_method[i]=='Shift_Dynamic':
                #method goes here
                print('this method not ready yet')
        
        #after loop is done, add remaining dataset to the last dataset section
        self.data_sections.append(data)
                
                
                