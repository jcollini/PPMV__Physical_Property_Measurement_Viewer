##PPMV Jobs now with Pandas to make it easier
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from scipy.optimize import curve_fit
from random import randint
from matplotlib.figure import Figure



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
   
    if MachineType in ['9T-ACT','14t-ACT']:
        headerskip=25
        #Pull coulums: [Temp (K),Field(Ore), Sample Orientation (deg angle)]
        cols=[3,4,5]
    elif MachineType in ['9T-R','14T-R']: 
        headerskip=31
        cols=[3,4,5]
    elif MachineType in ['Dynacool']:
        headerskip=30
        cols=[3,4,5]
    else:
        NameError('Please specify MachineType as 9T, 14T, or Dynacool or _ACT varient')
    

    ##specify which birdges to extract for Resistance
    if MachineType in ['9T-ACT','14t-ACT']:
       cols=cols+[12,13]
       
    else:
       cols=cols+[19,20,21]
        
    #Now load in the file and return as a Pandas data frame. 
    #The order of data is [Temp (K),Field(Ore), Sample Orientation (deg angle), R (first birdge given), R (second bridge given), etc)
    data=pd.read_csv(DAT_name,skiprows=headerskip,usecols=cols)
   
   #rename columns so that it is universal
    if MachineType in ['9T-ACT','14t-ACT']:
       #skip bridge 3 for ACT pucks
       data.columns=['Temperature (K)','Field (Oe)', 'theta (deg)', 'Bridge1_R (ohms)','Bridge2_R (ohms)']
    else:
       data.columns=['Temperature (K)','Field (Oe)', 'theta (deg)', 'Bridge1_R (ohms)','Bridge2_R (ohms)','Bridge3_R (ohms)']
       
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
        else:
            if difference<SplitVal:
                CutIndex=i
                break
            
    return CutIndex

################################################################################
#############################Pre-Select Jobs####################################
################################################################################



def Job_QuickPlot(DAT_name,MachineType,Xaxis,Yaxis):
    #Quick Plot function for Quick Plot button
    #First, load data
    #We need which bridge to grab for bridge numbers, if selected
 
  
    
    #read in data as a pandas dataframe    
    data=Read_PPMS_File(DAT_name,MachineType)
   
    
    #grab needed data for x and y axis using Xaxis name to get the column and name the axis
    
    Xdata=data[Xaxis]
    Xname=Xaxis
        
    Ydata=data[Yaxis]
    Yname=Yaxis
    
   
    plt.figure()
    plt.plot(Xdata,Ydata,'-')
    plt.xlabel(Xname,fontsize=12)
    plt.ylabel(Yname,fontsize=12)
    plt.title('')
    plt.tight_layout()
    plt.show()
    




def Job_CW_Split_Data(Xdata,Ydata):
    data=pd.concat([Xdata,Ydata],axis=1) #pandas way to combine two series into dataframe
    
    
    SplitVals=0.1
    
    #Find index of split
    Index=Split_Sets_Index_Reversed(Xdata,SplitVals,'down to up')
    
    
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
    
    
    