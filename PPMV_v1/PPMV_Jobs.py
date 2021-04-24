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



################################################################################
##################################Base Functions################################
################################################################################

#Functions that assist with basic tasks, such as grabbing data from machines,
#basic plotting, fitting, and calculation. These functions are combined to form
#the user friendly "Jobs" functions

def Read_PPMS_File(DAT_name,MachineType):
    #Function reads in file and returns needed parameters based on the machine
    #used and the bridges used
    #make sure to keep header for pandas usage
   
    if MachineType in ['9T-ACT','14T-ACT']:
        headerskip=25
        #Pull coulums: [Temp (K),Field(Ore), Sample Orientation (deg angle)]
        cols=[1,3,4,5,12,13]
    elif MachineType in ['9T-R','14T-R']: 
        headerskip=31
        cols=['Time Stamp (sec)',
              'Temperature (K)',
              'Magnetic Field (Oe)',
              'Sample Position (deg)',
              'Bridge 1 Resistance (Ohms)',
              'Bridge 2 Resistance (Ohms)',
              'Bridge 3 Resistance (Ohms)',]
    elif MachineType in ['Dynacool']:
        headerskip=30
        cols=['Time Stamp (sec)',
              'Temperature (K)',
              'Magnetic Field (Oe)',
              'Sample Position (deg)',
              'Bridge 1 Resistance (Ohms)',
              'Bridge 2 Resistance (Ohms)',
              'Bridge 3 Resistance (Ohms)',]
    elif MachineType in ['MPMS3']:
        headerskip=40
        cols=["Time Stamp (sec)",
              "Temperature (K)",
              "Magnetic Field (Oe)",
              "Moment (emu)",
              "AC Moment (emu)",
              "AC Phase (deg)",
              "AC Susceptibility (emu/Oe)",
              "AC X' (emu/Oe)",
              "AC X'' (emu/Oe)",
              "AC Drive (Oe)",
              "AC Frequency (Hz)",
              "DC Moment Fixed Ctr (emu)",
              "DC Moment Free Ctr (emu)"]
    elif MachineType in ['PPMV']:
        #file made by PPMV programs
        headerskip=None
        dataTemp=pd.read_csv(DAT_name)
        cols=dataTemp.columns
    else:
        NameError('Please specify MachineType as 9T, 14T, or Dynacool or _ACT varient')
    
        
    #Now load in the file and return as a Pandas data frame. 
    data=pd.read_csv(DAT_name,skiprows=headerskip,usecols=cols)
    #use cols list as new columns names
    #fix error with ACT! it uses ohm and not Ohms
    if MachineType in ['9T-ACT','14t-ACT']:
        cols=['Time Stamp (sec)',
              'Temperature (K)',
              'Magnetic Field (Oe)',
              'Sample Position (deg)',
              'Bridge 1 Resistance (Ohms)',
              'Bridge 2 Resistance (Ohms)']
        
    data.columns=cols
   
   #fill all NaNs with zeros
    data.fillna(0, inplace=True)
    
    return data

def Fill_Data(data):
    #fills in the missing bridges with zeros for your data file
    
    #Fill data with zeros at the end to make full size
    FillLength=data.shape[0]
    FillZeros=np.zeros((FillLength,1))
    
    while data.shape[1]<7:
        #add on column of zeros
        Newdata=np.hstack((data,FillZeros))
        data=Newdata
        
    return data


def Split_Sets_Index_Reversed(x_data,SplitVal,Reversal):
    #Finds index where a parameter is reversed (say between a cool down and warm up)
    xsize=len(x_data)
    for i in range(xsize):
        #find where index has been reversed. either 'down to up' or 'up to down'
        difference=x_data.iloc[i+1]-x_data.iloc[i]
        #print(difference)
        if Reversal=='down to up':
            if difference>SplitVal:
                CutIndex=i
                break
        elif Reversal == 'up to down':
            if difference<SplitVal:
                CutIndex=i
                break
            
    return CutIndex

def Split_Sets_Index_Dynamic(x_data,SplitVal,ShiftType):
    #finds the index where a data parameter changes from static to dynamic or vice versa
    xsize=len(x_data)
    print('SplitVal is'+str(SplitVal))
    for i in range(xsize):
        #determine where data changed, depending on ShiftType
        difference=np.absolute(x_data.iloc[i+1]-x_data.iloc[i])
        
        if ShiftType=='Static to Dynamic':
            if difference > SplitVal*200: #make sure you exceed static limit
                print('I made a cut for a difference of '+str(difference))
                CutIndex=i
                break
        elif ShiftType=='Dynamic to Static':
            if difference < SplitVal*0.01: #the next one falls well below the usual change
                CutIndex=i
                break
    
    return CutIndex

def DetermineDirection(x_data):
    #determins first direction of a given data that has reversals
    #use average difference of first few points
    x_dir_lst=[]
    for i in range(5):
        x_dir_lst.append(x_data.iloc[0]-x_data.iloc[i+1])
    
    x_dir=np.mean(x_dir_lst)
    print('Data average difference is '+str(x_dir))    
    #now determine direction the begining of the data is moving in    
    if x_dir>0:
        direction='down to up'
    elif x_dir<0:
        direction='up to down'
    else:
        print('Error: data is not changing direction')
    return direction

def DetermineDynamic(x_data):
   x_dir_lst=[]
   for i in range(5):
        x_dir_lst.append(x_data.iloc[i]-x_data.iloc[i+1])
    
   x_dir=np.absolute(np.mean(x_dir_lst))
   print('Data average difference is '+str(x_dir)) 
   
        
    #determine if the number is really chnaging or not
   threshold=0.02
   if x_dir<=threshold:
       dynamic='Static to Dynamic'
   else:
       dynamic='Dynamic to Static'
        
   return dynamic,x_dir    
    


################################################################################
#############################Pre-Select Jobs####################################
################################################################################



def Job_QuickPlot(Xdata,Ydata,Xname='',Yname=''):
    #Quick Plot function for Quick Plot button
    #First, load data
    #We need which bridge to grab for bridge numbers, if selected
 
    plt.figure()
    plt.plot(Xdata,Ydata,'.')
    plt.xlabel(Xname,fontsize=12)
    plt.ylabel(Yname,fontsize=12)
    plt.title('')
    plt.tight_layout()
    plt.show()
    




def Job_CW_Split_Data(Xdata,Ydata):
    data=pd.concat([Xdata,Ydata],axis=1) #pandas way to combine two series into dataframe
    
    
    SplitVals=0.1
    
    #determine direction of data
    direction=DetermineDirection(Xdata)
    print(direction)
    
    #Find index of split
    Index=Split_Sets_Index_Reversed(Xdata,SplitVals,direction)
    
    
    #split the whole set and save split, (save last one if you are on the last cycle)
    data2=data.iloc[(Index+1):,:]
    data1=data.iloc[0:(Index+1),:]
    #saves new data for next cycle
    data=data2
    
    print('data1 temp')
    print(data1.iloc[0:5,0])
    print('data2 temp')
    print(data2.iloc[0:5,0])
    
    
    
    X1,Y1=data1.iloc[:,0],data1.iloc[:,1]
    X2,Y2=data2.iloc[:,0],data2.iloc[:,1]
    
    return X1,Y1,X2,Y2
    

def Job_CalcMU(M,massSample,massMolar):
    #calculates Mu from M,massSample, massMolar for magnetometry
    #plot and save data from an MPMS
    #massSample in g
    #massMolas in g
    
    #convert M [emu] to Mu [emu/mole]
    #check for non-zero entries
    if massMolar:
        if massSample:
            MU=M*massMolar/massSample
        else:
            print('ERROR: Sample Mass is 0')
    else:
        print('ERROR: Molar Mass of Sample is 0')
        
        
    return MU

def Job_CalcChi(Field,M,massSample,massMolar):
    #convert M [emu] to Chi [emu/mole/Oe]
    if massMolar:
        if massSample:
            Chi=M*massMolar/massSample/Field
        else:
            print('ERROR: Sample Mass is 0')
    else:
        print('ERROR: Molar Mass of Sample is 0')
        
    return Chi