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
        self.data=ppmv.Read_PPMV_File(self.filenameTK.get())
        
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
        self.data_sections=[]
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
        Xdata1=data1[label]
        print(Xdata1[0:5])
        print('data2 temp')
        Xdata2=data2[label]
        print(Xdata2[0:5])
        
        #return the new data sets and index used to cut
        return Index,data1,data2
    
    def method_Shift_Dynamic(self,data,label):
        
        #Grab column used to split
        Xdata=data[label]
        
        direction,Xdata_avg=ppmv.DetermineDynamic(Xdata)
            
        print(direction)
        self.parse_results.append(direction)
        
        #find index of split
        Index=ppmv.Split_Sets_Index_Dynamic(Xdata, Xdata_avg, direction)
        
        #split the whole set and save split
        data2=data.iloc[(Index+1):,:]
        data1=data.iloc[0:(Index+1),:]
        
        
        print('data1 temp')
        Xdata1=data1[label]
        print(Xdata1[0:5])
        print('data2 temp')
        Xdata2=data2[label]
        print(Xdata2[0:5])
        
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
                index,data1,data2=self.method_Shift_Dynamic(data,self.parse_labels[i])
                #now return the cut data set and index
                #also make data2 the new data for the next turn in the loop
                self.data_sections.append(data1)
                self.data_indexcuts.append(index)
                data=data2 #remaining dataset for the next cycle
        
        #after loop is done, add remaining dataset to the last dataset section
        self.data_sections.append(data)
        
        #add last label depending on last result
        if self.parse_methods[-1]=='Shift_Direction':
            #determine direction of last dataset and add it to results
            data=self.data_sections[-1]
            Xdata=data[self.parse_labels[-1]]
            direction=ppmv.DetermineDirection(Xdata)
            print(direction)
            self.parse_results.append(direction)
            
        #add last label depending on last result
        if self.parse_methods[-1]=='Shift_Dynamic':
            print('shifting dynamic')
            #determine direction of last dataset and add it to results
            #Grab column used to split
        
            data=self.data_sections[-1]
            Xdata=data[self.parse_labels[-1]]
            
            direction,x_dir=ppmv.DetermineDynamic(Xdata)
            
            
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
        self.optionsMachine=['9T-ACT','9T-R','14T-ACT','14T-R','Dynacool','MPMS3','PPMV']
        self.dataNames=['Time Stamp (sec)',
                             'Temperature (K)',
                             'Magnetic Field (Oe)',
                             'Sample Position (deg)',
                             'Bridge 1 Resistance (Ohms)',
                             'Bridge 2 Resistance (Ohms)',
                             'Bridge 3 Resistance (Ohms)','Moment (emu)',
                             'DC Moment Fixed Ctr (emu)',
                             'DC Moment Free Ctr (emu)',
                             'AC Moment (emu)',
                             'AC Phase (deg)',
                             'AC Susceptibility (emu/Oe)',
                             "AC X' (emu/Oe)",
                             "AC X'' (emu/Oe)",
                             "AC Drive (Oe)",
                             "AC Frequency (Hz)"]
        
        self.optionsMarker=['.','o','v','^','s','D']
        #self.optionsColor=['k','b','r','c','m','y','w']
        
        self.ADR_Xoptions=['PPMS Temperature (K)','ADR Temperature (K)','ADR Resistance Ch.3 (Ohms)']
                            
        
    def Create_Root(self,title,icon):
        #controls rool application window
        self.root=tk.Tk()
        #self.root.configure(bg='#525F88')
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
        self.LoadFrame=tk.LabelFrame(MasterTK,text='Load PPMS Data',padx=195)
        self.LoadFrame.grid(row=row,column=column,padx=10,pady=(0,15))
    
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
        
    def Create_EmptyPlot(self,MasterTK,row,column,rowspan_plot,columnspan_plot):
        #create plot and put on screen. Have it empty to start
        self.canvas,self.Fig,self.Plot,self.toolbarFrame=bt.Empty_Plot(MasterTK)
        #set plot to screen
        self.canvas.get_tk_widget().grid(row=row,column=column,rowspan=rowspan_plot,columnspan=columnspan_plot)
    
        
        self.toolbarFrame.grid(row=row+rowspan_plot,column=column,columnspan=columnspan_plot)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        self.Update_Bplot=tk.Button(MasterTK,text='Update Plot')
        Update_Loc=column+1
        self.Update_Bplot.grid(row=row+rowspan_plot,column=Update_Loc,sticky=tk.E)
    
    def Create_ADREmptyPlot(self,MasterTK,row,column,rowspan_plot,columnspan_plot):
        #create plot and put on screen. Have it empty to start
        self.canvas,self.Fig,self.Plot,self.toolbarFrame=bt.Empty_Plot(MasterTK)
        #set plot to screen
        self.canvas.get_tk_widget().grid(row=row,column=column,rowspan=rowspan_plot,columnspan=columnspan_plot)
    
        
        self.toolbarFrame.grid(row=row+rowspan_plot,column=column,columnspan=columnspan_plot)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        
        #add title to make plot clearer
        self.Plot.set_title('ADR Sample Bridge 1')
    
    def Create_ADREmptyPlot2(self,MasterTK,row,column,rowspan_plot,columnspan_plot):
        #create a second plot and put on screen. Have it empty to start
        self.canvas2,self.Fig2,self.Plot2,self.toolbarFrame2=bt.Empty_Plot(MasterTK)
        #set plot to screen
        self.canvas2.get_tk_widget().grid(row=row,column=column,rowspan=rowspan_plot,columnspan=columnspan_plot)
    
        
        self.toolbarFrame2.grid(row=row+rowspan_plot,column=column,columnspan=columnspan_plot)
        self.toolbar2 = NavigationToolbar2Tk(self.canvas2, self.toolbarFrame2)
        
        
        #add title to make plot clearer
        self.Plot2.set_title('ADR Sample Bridge 2')
    
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
        self.Ychoice.set('Bridge 1 Resistance (Ohms)')
        
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
        
    def Create_ChiSettingsFrame(self,MasterTK,row,column):
        self.SetFrame=tk.LabelFrame(MasterTK,text='Settings')
        self.SetFrame.grid(row=row,column=column)
        
        #1st direction: pick axes
        help1='Select your data transformation type'
        self.Direction1=tk.Label(self.SetFrame,text=help1)
        self.Direction1.grid(row=0,column=0,columnspan=3)
        
        #Chi selection
        self.Chi_Toggle=tk.StringVar()
        self.Chi_Toggle.set('M (emu)')
        
        self.RadioM=tk.Radiobutton(self.SetFrame,text='M (emu)',variable=self.Chi_Toggle, value='M (emu)')
        self.RadioM.grid(row=1,column=0)
        
        self.RadioMu=tk.Radiobutton(self.SetFrame,text='Mu (emu/mole)',variable=self.Chi_Toggle, value='Mu (emu/mole)')
        self.RadioMu.grid(row=1,column=1)
        
        self.RadioChi=tk.Radiobutton(self.SetFrame,text='Chi (emu/[mole Oe])',variable=self.Chi_Toggle, value='Chi (emu/[mole Oe])')
        self.RadioChi.grid(row=1,column=2)
        
        #Mass entry
        self.MassSample=tk.DoubleVar()
        self.MassSample.set(0)
        
        self.MolarSample=tk.DoubleVar()
        self.MolarSample.set(0)
        
        self.MassL=tk.Label(self.SetFrame,text='Mass (g)')
        self.MassE=tk.Entry(self.SetFrame,textvariable=self.MassSample)
        
        self.MassL.grid(row=2,column=0,pady=(10,0))
        self.MassE.grid(row=2,column=1,pady=(10,0))
        
        self.MolarL=tk.Label(self.SetFrame,text='Molar Mass (g)')
        self.MolarE=tk.Entry(self.SetFrame,textvariable=self.MolarSample)
        
        self.MolarL.grid(row=3,column=0,pady=(0,10))
        self.MolarE.grid(row=3,column=1,pady=(0,10))
        
        #x and y axis drop down menu selection
        self.Xchoice=tk.StringVar()
        self.Ychoice=tk.StringVar()
        
        #set each as the usualy starting ones
        self.Xchoice.set('Temperature (K)')
        self.Ychoice.set('DC Moment Fixed Ctr (emu)')
        
        #make menus
        self.QuickP_Xchoice_L=tk.Label(self.SetFrame,text='x axis')
        self.QuickP_Xchoice_L.grid(row=4,column=0)
        
        self.QuickP_Ychoice_L=tk.Label(self.SetFrame,text='y axis')
        self.QuickP_Ychoice_L.grid(row=5,column=0,pady=(0,5))
       
        self.QuickP_Xchoice_D=tk.OptionMenu(self.SetFrame, self.Xchoice, *self.dataNames)
        self.QuickP_Xchoice_D.grid(row=4,column=1)
        self.QuickP_Ychoice_D=tk.OptionMenu(self.SetFrame, self.Ychoice, *self.dataNames)
        self.QuickP_Ychoice_D.grid(row=5,column=1,pady=(0,5))
    
        #make update button for plot below settings settings
        self.Update_Bset=tk.Button(self.SetFrame,text='Update Plot')
        self.Update_Bset.grid(row=6,column=0,pady=(10,0))
        
        
    def Create_PlotSettingsFrame(self,MasterTK,row,column):
        self.PlotFrame=tk.LabelFrame(MasterTK,text='Plot Settings')
        self.PlotFrame.grid(row=row,column=column)
        #x and y axis drop down menu selection
        self.Xchoice=tk.StringVar()
        self.Ychoice=tk.StringVar()
    
        #set each as the usualy starting ones
        self.Xchoice.set('Temperature (K)')
        self.Ychoice.set('Bridge 1 Resistance (Ohms)')
    
        #make menus
        self.QuickP_Xchoice_L=tk.Label(self.PlotFrame,text='x axis')
        self.QuickP_Xchoice_L.grid(row=0,column=0)
        
        self.QuickP_Ychoice_L=tk.Label(self.PlotFrame,text='y axis')
        self.QuickP_Ychoice_L.grid(row=1,column=0,pady=(0,5))
        
        self.QuickP_Xchoice_D=tk.OptionMenu(self.PlotFrame, self.Xchoice, *self.dataNames)
        self.QuickP_Xchoice_D.grid(row=0,column=1)
        self.QuickP_Ychoice_D=tk.OptionMenu(self.PlotFrame, self.Ychoice, *self.dataNames)
        self.QuickP_Ychoice_D.grid(row=1,column=1,pady=(0,5))
        
        #update plot
        self.Update_Bsettings=tk.Button(self.PlotFrame,text='Update Plot')
        self.Update_Bsettings.grid(row=0,column=2,rowspan=2)
        
    def Create_ParseSettingsFrame(self,MasterTK,row,column):
        self.ParseFrame=tk.LabelFrame(MasterTK,text='Parse Data Settings')
        self.ParseFrame.grid(row=row,column=column)
    
        #create empty lists to store labels and methods lists
        self.Labels_ref=[]
        self.Methods_ref=[]
        self.DividerL_ref=[]
        self.DividerM_ref=[]
        self.Divider_names=[]
        self.Divider_Legend_widget=[]
        self.Divider_Legend_names=[]
    
        #keep track of rownumbers
        self.RowCount=tk.IntVar()
        self.RowCount.set(2)
        
        #explanation for settings
        self.Explain_L=tk.Label(self.ParseFrame,text='For each divider, select the data \nused to split and the method for splitting')
        self.Explain_L.grid(row=0,column=0,columnspan=3)
    
        #button to create a new list
        self.Add_Row_B=tk.Button(self.ParseFrame,text='Create New Divider')
        self.Add_Row_B.grid(row=1,column=0,columnspan=1)
        
        #buttton to remove item for list
        self.Remove_Row_B=tk.Button(self.ParseFrame,text='Remove Divider')
        self.Remove_Row_B.grid(row=1,column=1,columnspan=2)
        

    def Create_ADR1SampleFrame(self,MasterTK,row,column):
        #create frame
        self.ADR1Frame=tk.LabelFrame(MasterTK,text='Sample 1 settings')
        self.ADR1Frame.grid(row=row,column=column)
        
        #create variables
        self.X1=tk.StringVar() #name of x-axis for ADR
        self.X1.set('ADR Temperature (K)')
        
        #Create x-axis setting (the toggle)
        self.X1_L=tk.Label(self.ADR1Frame,text='x axis:')
        self.X1_L.grid(row=0,column=0)
        
        self.X1_D=tk.OptionMenu(self.ADR1Frame, self.X1, *self.ADR_Xoptions)
        self.X1_D.grid(row=0,column=1)
        
        #create update button
        self.Update1_B=tk.Button(self.ADR1Frame,text='Update')
        self.Update1_B.grid(row=1,column=0)
        
    def Create_ADR2SampleFrame(self,MasterTK,row,column):
        #create frame
        self.ADR2Frame=tk.LabelFrame(MasterTK,text='Sample 2 settings')
        self.ADR2Frame.grid(row=row,column=column)
        
        #create variables
        self.X2=tk.StringVar() #name of x-axis for ADR
        self.X2.set('ADR Temperature (K)')
        
        #Create x-axis setting (the toggle)
        self.X2_L=tk.Label(self.ADR2Frame,text='x axis:')
        self.X2_L.grid(row=0,column=0)
        
        self.X2_D=tk.OptionMenu(self.ADR2Frame, self.X1, *self.ADR_Xoptions)
        self.X2_D.grid(row=0,column=1)
        
        #create update button
        self.Update2_B=tk.Button(self.ADR2Frame,text='Update')
        self.Update2_B.grid(row=1,column=0)
        
            
        
    def generate_parse_section(self,MasterTK,labeltext):
        #creates parse widgets
        
        #Menu string choice for method of split
        Method=tk.StringVar() 
        #String choice for selecting a data column
        DataLabel=tk.StringVar()
        #string choice for legend
        Legend=tk.StringVar()
        Legend.set('Insert Data Name')
        
        #simple label telling user what label number you are on
        Divider_L=tk.Label(MasterTK,text=labeltext)
        #menu option widget for methods
        Divider_Method=tk.OptionMenu(MasterTK,Method,'Shift_Direction',
                           'Shift_Dynamic')
        #menu option widget for data columns
        Divider_Label=tk.OptionMenu(MasterTK,DataLabel,*self.dataNames)
        #label entry for user's legend
        Divider_Legend=tk.Entry(MasterTK,textvariable=Legend)
        
        return Method,DataLabel,Divider_L,Divider_Method,Divider_Label,Divider_Legend,Legend
        
    def add_parse_section(self,MasterTK):
        #creates Parse widgets and places them on the screen
        #stores new reference widgets for labels and methods into a list
        row=self.RowCount.get()
        
        #if it's the first row, create a starting label
        if row==2:
            Starter_Label=tk.StringVar()
            Starter_Label.set('Insert Data Name')
            
            First_Label=tk.Entry(MasterTK,textvariable=Starter_Label)
            First_Label.grid(row=row,column=3)
            self.Divider_Legend_widget.append(First_Label)
            self.Divider_Legend_names.append(Starter_Label)
            row=row+1
        
        Method,DataLabel,Divider_L1,Divider_Method,Divider_Label,Divider_Legend,Legend=self.generate_parse_section(MasterTK,'Divider '+str(row-2)+':  ')
        Divider_L1.grid(row=row,column=0)
        Divider_Label.grid(row=row,column=1)
        Divider_Method.grid(row=row,column=2)
        Divider_Legend.grid(row=row,column=3)
        
        #update lists of widgets
        print('adding parse info')
        self.Labels_ref.append(DataLabel)
        self.Methods_ref.append(Method)
        self.DividerL_ref.append(Divider_Label)
        self.DividerM_ref.append(Divider_Method)
        self.Divider_names.append(Divider_L1)
        self.Divider_Legend_widget.append(Divider_Legend)
        self.Divider_Legend_names.append(Legend)
        
        #update row number
        self.RowCount.set(row+1)
        
    def remove_parse_section(self,MasterTK):
        
        #update lists if not empty
        if self.RowCount.get()>4:
            row=self.RowCount.get()
            self.RowCount.set(row-1)
            
            self.DividerL_ref[-1].grid_forget()
            self.DividerM_ref[-1].grid_forget()
            self.Divider_names[-1].grid_forget()
            self.Divider_Legend_widget[-1].grid_forget()
        
        elif self.RowCount.get()==4:
            #special case, need to remove even initial first label as well
            row=self.RowCount.get()
            self.RowCount.set(row-2)
            
            self.DividerL_ref[-1].grid_forget()
            self.DividerM_ref[-1].grid_forget()
            self.Divider_names[-1].grid_forget()
            self.Divider_Legend_widget[-1].grid_forget()
            self.Divider_Legend_widget[-2].grid_forget()
            
            self.Divider_Legend_names.pop()
            self.Divider_Legend_widget.pop()
        
        
        #deletes last parse section row
        self.Labels_ref.pop()
        self.Methods_ref.pop()
        self.DividerL_ref.pop()
        self.DividerM_ref.pop()
        self.Divider_names.pop()
        self.Divider_Legend_names.pop()
        self.Divider_Legend_widget.pop()
        
    
    def Create_MultiPlotDirections(self,MasterTK,row,column):
        
        #create directions text for user of multiploter
        self.DirectionsL=tk.Label(MasterTK,text='directions for user')
        self.DirectionsL.grid(row=row,column=column)
        
    def Create_MultiPlotSettingsFrame(self,MasterTK,row,column):
        #keep track of number of datafile
        self.DataCount=tk.IntVar()
        self.DataCount.set(0)
        
        self.MultiFrame=tk.LabelFrame(MasterTK,text='Multi Plot Settings')
        self.MultiFrame.grid(row=row,column=column)
    
        #create empty lists to store labels and vars lists
        self.LoadB_ref=[]
        self.FileL_ref=[]
        self.MachineM_ref=[]
        self.PlotMarkerM_ref=[]
        self.PlotColorM_ref=[]
        self.LegendE_ref=[]
        
        self.FileVar_ref=[]
        self.MachineVar_ref=[]
        self.MarkerVar_ref=[]
        self.ColorVar_ref=[]
        self.LegendVar_ref=[]
        self.DataVar_ref=[]
    
        #keep track of rownumbers
        self.RowCount=tk.IntVar()
        self.RowCount.set(1)
        
        #button to create a new list
        self.Add_Row_B=tk.Button(self.MultiFrame,text='Add Data',command=lambda: self.add_load_section(self.MultiFrame))
        self.Add_Row_B.grid(row=0,column=0,columnspan=1)
        
        #buttton to remove item for list
        self.Remove_Row_B=tk.Button(self.MultiFrame,text='Remove Data',command=lambda: self.remove_load_section(self.MultiFrame))
        self.Remove_Row_B.grid(row=0,column=1,columnspan=2)
        
        #label each column with it's function
        self.Explain1=tk.Label(self.MultiFrame,text='Loaded Data').grid(row=1,column=1)
        self.Explain2=tk.Label(self.MultiFrame,text='Machine Type').grid(row=1,column=2)
        self.Explain3=tk.Label(self.MultiFrame,text='Plot Marker').grid(row=1,column=3)
        self.Explain4=tk.Label(self.MultiFrame,text='Plot Color').grid(row=1,column=4)
        self.Explain5=tk.Label(self.MultiFrame,text='Legend Name').grid(row=1,column=5)
        
        
        
    def generate_load_section(self,MasterTK,start_row):
        #creates needed load widgets for multi-plot functions
        FileVar=tk.StringVar()
        FileVar.set('')
        
        FileDisplayVar=tk.StringVar()
        FileDisplayVar.set('.....')
        
        MachineVar=tk.StringVar()
        MachineVar.set('9T-R')
        
        MarkerVar=tk.StringVar()
        MarkerVar.set('.')
        
        ColorVar=tk.StringVar()
        ColorVar.set('#0080ff') #blue by default
        
        LegendVar=tk.StringVar()
        LegendVar.set('Legend Name')
        
        DataVar=cl.DataPPMS(FileVar, MachineVar)
        
        LoadB=tk.Button(MasterTK, text='Load Data',command=lambda: bt.Button_LoadData(MasterTK, FileVar, FileDisplayVar, MachineVar, DataVar))
        LoadDisplayL=tk.Label(MasterTK,textvariable=FileDisplayVar,bg='white')
        LoadMachineM=tk.OptionMenu(MasterTK, MachineVar, *self.optionsMachine)
        
        PlotMarkerM=tk.OptionMenu(MasterTK, MarkerVar,*self.optionsMarker)
        PlotColorB=tk.Button(MasterTK, text='Color',bg=ColorVar.get(),command=lambda: bt.Button_ColorPicker(ColorVar,PlotColorB))
        
        LegendE=tk.Entry(MasterTK,textvariable=LegendVar)
        
        #place onto screen
        LoadB.grid(row=start_row,column=0)
        LoadDisplayL.grid(row=start_row,column=1)
        LoadMachineM.grid(row=start_row,column=2)
        PlotMarkerM.grid(row=start_row,column=3)
        PlotColorB.grid(row=start_row,column=4)
        LegendE.grid(row=start_row,column=5)
        
        
        #package widgets for use
        Vars=[FileVar,MachineVar,MarkerVar,ColorVar,LegendVar,DataVar]
        Widgets=[LoadB,LoadDisplayL,LoadMachineM,PlotMarkerM,PlotColorB,LegendE]
        
        return Vars,Widgets
        
        
        
    def add_load_section(self,MasterTK):
        
        #creates load widgets for multi-plot functions
        dataNum=self.DataCount.get()
        
        #create new section of widgets and variables
        Vars,Widgets=self.generate_load_section(MasterTK,dataNum+2)
        
        #update datacount
        self.DataCount.set(dataNum+1)
        
        #update lists
        self.LoadB_ref.append(Widgets[0])
        self.FileL_ref.append(Widgets[1])
        self.MachineM_ref.append(Widgets[2])
        self.PlotMarkerM_ref.append(Widgets[3])
        self.PlotColorM_ref.append(Widgets[4])
        self.LegendE_ref.append(Widgets[5])
        
        self.FileVar_ref.append(Vars[0])
        self.MachineVar_ref.append(Vars[1])
        self.MarkerVar_ref.append(Vars[2])
        self.ColorVar_ref.append(Vars[3])
        self.LegendVar_ref.append(Vars[4])
        self.DataVar_ref.append(Vars[5])
        
    def remove_load_section(self,MasterTK):
        
        #grab current data number
        dataNum=self.DataCount.get()
        
        if dataNum > 0:
            
            #update dataNum
            self.DataCount.set(dataNum-1)
            
            #remove current row from the screen
            self.LoadB_ref[-1].grid_forget()
            self.FileL_ref[-1].grid_forget()
            self.MachineM_ref[-1].grid_forget()
            self.PlotMarkerM_ref[-1].grid_forget()
            self.PlotColorM_ref[-1].grid_forget()
            self.LegendE_ref[-1].grid_forget()
            
            #remove current batch from the list
            self.LoadB_ref.pop()
            self.FileL_ref.pop()
            self.MachineM_ref.pop()
            self.PlotMarkerM_ref.pop()
            self.PlotColorM_ref.pop()
            self.LegendE_ref.pop()
        
            self.FileVar_ref.pop()
            self.MachineVar_ref.pop()
            self.MarkerVar_ref.pop()
            self.ColorVar_ref.pop()
            self.LegendVar_ref.pop()
            self.DataVar_ref.pop()
            
    
    def Create_ADRLoadFrame(self,MasterTK,row,column):
        #creates standard loadframe use for applications
        self.LoadFrame=tk.LabelFrame(MasterTK,text='Load ADR Data')
        self.LoadFrame.grid(row=row,column=column,padx=10,pady=self.ExFrameY,sticky=tk.W)
        #LoadFrame.grid_configure(ipadx=300)
        
        #Widgets and placement
        #file and machine selection for data
        self.Machine=tk.StringVar()
        self.Machine.set('9T-R')
    
        self.DataLoc=tk.StringVar()
        
        self.DataDisplay=tk.StringVar()
        self.DataDisplay.set('      No Data Loaded      ')
        
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
            
            
        
        
        
        
        
        
        
        

class AppBox():
    
    
    
    def __init__(self,MasterTK,title,icon,row,column):
        
        #General padding to have frames match
        self.JobFrame_Ysize=56
        #Padding if there is missing lines for the explaination text
        self.LinePadding=12
        #Padding for icons
        self.icon_spacingx=55
        self.icon_spacingy=55
        
        self.ExFrameY=5 #boarder space around export frame
        self.ExportPadding=50 #seperation of export buttons
        self.ExportBoarderX=20 #boarder space around export buttons
        self.ExportBoarderY=5 #boarder space around export buttons
        self.ExFrameY=5 #boarder space around export frame
        
        #Options for PPMS and MPMS systems
        self.optionsMachine=['9T-ACT','9T-R','14T-ACT','14T-R','Dynacool','MPMS3']
        self.dataNames=['Time Stamp (sec)',
                             'Temperature (K)',
                             'Magnetic Field (Oe)',
                             'Sample Position (deg)',
                             'Bridge 1 Resistance (Ohms)',
                             'Bridge 2 Resistance (Ohms)',
                             'Bridge 3 Resistance (Ohms)','Moment (emu)',
                             'DC Moment Fixed Ctr (emu)',
                             'DC Moment Free Ctr (emu)',
                             'AC Moment (emu)',
                             'AC Phase (deg)',
                             'AC Susceptibility (emu/Oe)',
                             "AC X' (emu/Oe)",
                             "AC X'' (emu/Oe)",
                             "AC Drive (Oe)",
                             "AC Frequency (Hz)"]
        
        
        self.title=title
        self.row=row
        self.column=column
        self.MasterTK=MasterTK
        self.icon=icon
        
    def Create_QuickPlot(self):
        #self.PlotFrame=tk.LabelFrame(self.MasterTK,text='Plot Frame',bg='white')
        self.PlotFrame=tk.LabelFrame(self.MasterTK)
        self.PlotFrame.grid(row=self.row,column=self.column,padx=10,pady=10)
    
        #plot icon
        Icon=Image.open(self.icon)
        IconPic=ImageTk.PhotoImage(Icon)
        self.QuickP_icon=tk.Label(self.PlotFrame,image=IconPic)
        self.QuickP_icon.image=IconPic
        self.QuickP_icon.grid(row=0,column=0,columnspan=2)
    
        #plot explanation
        self.QuickP_title=tk.Label(self.PlotFrame,text='Quick Plot',font=('Standard Symbols L',10))
        self.QuickP_explain=tk.Label(self.PlotFrame,text='Pick x and y axis from menu.')
        self.QuickP_title.grid(row=1,column=0,columnspan=2)
        self.QuickP_explain.grid(row=2,column=0,columnspan=2)
        
        #plot button
        self.QuickP_B=tk.Button(self.PlotFrame,text='Quick Plot')
        self.QuickP_B.grid(row=3,column=0,columnspan=2)
        
        #x and y axis drop down menu selection
        self.Xchoice=tk.StringVar()
        self.Ychoice=tk.StringVar()
        #set each as the usualy starting ones
        self.Xchoice.set('Temperature (K)')
        self.Ychoice.set('Bridge 1 Resistance (Ohms)')
        #make menus
        self.QuickP_Xchoice_L=tk.Label(self.PlotFrame,text='x axis')
        self.QuickP_Xchoice_L.grid(row=4,column=0)
    
        self.QuickP_Ychoice_L=tk.Label(self.PlotFrame,text='y axis')
        self.QuickP_Ychoice_L.grid(row=5,column=0,pady=(0,5))
        
        
        
        self.QuickP_Xchoice_D=tk.OptionMenu(self.PlotFrame, self.Xchoice, *self.dataNames)
        self.QuickP_Xchoice_D.grid(row=4,column=1)
        self.QuickP_Ychoice_D=tk.OptionMenu(self.PlotFrame, self.Ychoice, *self.dataNames)
        self.QuickP_Ychoice_D.grid(row=5,column=1,pady=(0,5))
        
        
    def Create_Export(self):
        self.ExportFrame=tk.LabelFrame(self.MasterTK)
        self.ExportFrame.grid(row=self.row,column=self.column,padx=10,pady=10)
    
        #explort icon and explanation
        Icon=Image.open(self.icon)
        IconPic=ImageTk.PhotoImage(Icon)
        self.Export_icon=tk.Label(self.ExportFrame,image=IconPic)
        self.Export_icon.image=IconPic
        self.Export_icon.grid(row=0,column=0,padx=self.icon_spacingx)
        
        self.Export_title=tk.Label(self.ExportFrame,text='Quick Export',font=('Standard Symbols L',10))
        self.Export_title.grid(row=1,column=0)
    
        self.Export_explain=tk.Label(self.ExportFrame,text='Export PPMS data\nto CSV.')
        self.Export_explain.grid(row=2,column=0,pady=(0,self.icon_spacingy))
    
        #Simple File Output button
        self.Export_file_B=tk.Button(self.ExportFrame,text='Quick Export')
        self.Export_file_B.grid(row=3,column=0)
        
        
    def Create_Launcher(self,AppText):
        
        self.AppFrame=tk.LabelFrame(self.MasterTK)
        self.AppFrame.grid(row=self.row,column=self.column,padx=10,pady=10)
    
        #explort icon and explanation
        #explort icon and explanation
        Icon=Image.open(self.icon)
        IconPic=ImageTk.PhotoImage(Icon)
        self.App_icon=tk.Label(self.AppFrame,image=IconPic)
        self.App_icon.image=IconPic
        self.App_icon.grid(row=0,column=0,padx=self.icon_spacingx)
        
        self.App_title=tk.Label(self.AppFrame,text=self.title,font=('Standard Symbols L',10))
        self.App_title.grid(row=1,column=0)
    
        self.App_explain=tk.Label(self.AppFrame,text=AppText)
        self.App_explain.grid(row=2,column=0,pady=(0,self.icon_spacingy-5))
        
    
        #Simple File Output button
        self.App_B=tk.Button(self.AppFrame,text=self.title)
        self.App_B.grid(row=3,column=0,pady=(0,5),padx=32)
        
        