import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from random import randint


################################################################################
##################################Base Functions################################
################################################################################

#Functions that assist with basic tasks, such as grabbing data from machines,
#basic plotting, fitting, and calculation. These functions are combined to form
#the user friendly "Jobs" functions

def Read_PPMS_File(DAT_name,MachineType,BridgeNums=[0,0]):
    #Function reads in file and returns needed parameters based on the machine
    #used and the bridges used
   
   if MachineType==('9T-ACT' or '14t-ACT'):
       headerskip=26
        #Pull coulums: [Temp (K),Field(Ore), Sample Orientation (deg angle)]
       cols=[3,4,5]
   elif MachineType==('9T-R' or '14T-R'): 
        headerskip=32
        cols=[3,4,5]
   elif MachineType=='Dynacool':
        headerskip=31
        cols=[3,4,5]
   else:
        NameError('Please specify MachineType as 9T, 14T, or Dynacool or _ACT varient')
    

    ##specify which birdges to extract for Linear Resistivity
   if MachineType==('9T-ACT' or '14t-ACT'):
       
       if 1 in BridgeNums:
            cols.append(12)
       if 2 in BridgeNums:
            cols.append(13)
   else:
       
        
        if 1 in BridgeNums:
            cols.append(19)
        if 2 in BridgeNums:
            cols.append(20)
        if 3 in BridgeNums:
            cols.append(21)
        if 4 in BridgeNums:
            cols.append(22)
        
    
    
    #Now load in the file. The order of data is [Temp (K),Field(Ore), Sample Orientation (deg angle), R (first birdge given), R (second bridge given), etc)
    #So if you only used bridge 3, it will be the FIRST R shown.
   
   data=np.loadtxt(DAT_name,skiprows=headerskip,usecols=cols,delimiter=',')
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


################################################################################
#############################Pre-Select Jobs####################################
################################################################################



def Job_QuickPlot(DAT_name,MachineType,Xaxis,Yaxis):
    #Quick Plot function for Quick Plot button
    #First, load data
    #We need which bridge to grab for bridge numbers, if selected
 
    Bridges=[]
    if Xaxis=='R_bridge1' or Yaxis=='R_bridge1':
      
        Bridges.append(1)
    elif Xaxis=='R_bridge2' or Yaxis=='R_bridge2':
        Bridges.append(2)
    elif Xaxis=='R_bridge3' or Yaxis=='R_bridge3':
        Bridges.append(3)
    
        
    data=Read_PPMS_File(DAT_name,MachineType,BridgeNums=Bridges)
    data=Fill_Data(data)
    
    #grab needed data for x and y axis
    
    if Xaxis=='T':
        Xdata=data[:,0]
        Xname='Temp (K)'
        
    elif Xaxis=='H':
        Xdata=data[:,1]
        Xname='Field (Oe)'
        
    elif Xaxis=='theta':
        Xdata=data[:,2]
        Xname=r'$\theta$ (Oe)'
        
    elif Xaxis in['R_bridge1','R_bridge2','R_bridge3']:
        Xdata=data[:,3]
        
        if Xaxis=='R_bridge1':
            Xname='R bridge1 (ohms)'
        elif Xaxis=='R_bridge2':
            Xname='R bridge2 (ohms)'
        elif Xaxis=='R_bridge3':
            Xname='R bridge3 (ohms)'
    
    
    if Yaxis=='T':
        Ydata=data[:,0]
        Yname='Temp (K)'
    elif Xaxis=='H':
        Ydata=data[:,1]
        Yname=='Field (Oe)'
    elif Yaxis=='theta':
        Ydata=data[:,2]
        Yname==r'$\theta$ (Oe)'
    elif Yaxis in['R_bridge1','R_bridge2','R_bridge3']:
        Ydata=data[:,3]
        if Yaxis=='R_bridge1':
            Yname='R bridge1 (ohms)'
        elif Yaxis=='R_bridge2':
            Yname='R bridge2 (ohms)'
        elif Yaxis=='R_bridge3':
            Yname='R bridge3 (ohms)'
    
    #plot data
    plt.figure()
    plt.plot(Xdata,Ydata,'-')
    plt.xlabel(Xname,fontsize=12)
    plt.ylabel(Yname,fontsize=12)
    plt.title('')
    plt.tight_layout()
    plt.show()
    
