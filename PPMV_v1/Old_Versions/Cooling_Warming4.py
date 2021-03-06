##Cooling and Warming Application for PPMV
import tkinter as tk

import PPMV_Jobs4 as ppmv
import Button_Functions4 as bt

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler





def App_CoolingWarming(DataLoc,MachineType):
    #general settings
    ExportPadding=50 #seperation of export buttons
    ExportBoarderX=20 #boarder space around export buttons
    ExportBoarderY=5 #boarder space around export buttons
    ExFrameY=5 #boarder space around export frame
   
    #controls the window for cooling and warming
    rootCW=tk.Toplevel()
    rootCW.title('PPMV Cooling and Warming')
    rootCW.iconbitmap('QMC_Temp.ico')
    #rootCW.grab_set() #places this window as a priority for events
    #rootCW.focus_displayof()
  

    
####Header widget
    Header_L=tk.Label(rootCW,text='PPMV Cooling and Warming')
    Header_L.grid(row=0,column=0,pady=(0,10))
    
####Load Frame
    LoadFrame=tk.LabelFrame(rootCW,text='Check/Change Loaded Data')
    LoadFrame.grid(row=1,column=0,padx=10,pady=ExFrameY,sticky=tk.W)
    #LoadFrame.grid_configure(ipadx=300)
    
    #show load buttons and import load from the previous window
    #load data widgets
    Load_B=tk.Button(LoadFrame,text="Load data",command=lambda: bt.Button_LoadData(rootCW, Load_check_E))
    Load_B.grid(row=0,column=0)
    
    Load_check_L=tk.Label(LoadFrame,text='File:')
    Load_check_L.grid(row=0,column=1,padx=(20,0))
    
    #Already loaded entry from launcher. Simply place on screen. Load info from launcher
    Load_check_E=tk.Entry(LoadFrame)
    Load_check_E.insert(0,DataLoc)
    Load_check_E.grid(row=0,column=2)
    
    Machine=tk.StringVar()
    Machine.set(MachineType)
    
    Load_machine_L=tk.Label(LoadFrame,text='PPMS and Puck Used:')
    Load_machine_L.grid(row=0,column=3,padx=(20,0))
    
    Load_machine_D=tk.OptionMenu(LoadFrame, Machine, '9T-ACT','9T-R','14T-ACT','14T-R','Dynacool')
    Load_machine_D.grid(row=0,column=4)
    
    
####Plotting
    #create plot and put on screen. Have it empty to start
    canvas,fig,CWPlot,toolbarFrame=bt.Empty_Plot(rootCW)
    #set plot to screen
    canvas.get_tk_widget().grid(row=2,column=1,columnspan=2)
    
    
    toolbarFrame.grid(row=3,column=1,columnspan=2)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
    
####Save/Export frame
    ExportFrame=tk.LabelFrame(rootCW,text='Save/Export')
    ExportFrame.grid(row=1,column=1,columnspan=2,pady=ExFrameY)    
    #create save button for plot
    SaveFig_B=tk.Button(ExportFrame,text='Save Figure',command=lambda: bt.Button_SaveFig(fig))
    SaveFig_B.grid(row=0,column=0,padx=(ExportBoarderX,ExportPadding),pady=ExportBoarderY)
    
    #create export CVS button
    Export_B=tk.Button(ExportFrame,text='Save Seperate CSVs',command=lambda: bt.Button_ExportCW_CSVs(rootCW, 
                                                                                                     Load_check_E, 
                                                                                                     Machine, 
                                                                                                     Xchoice, 
                                                                                                     Ychoice, 
                                                                                                     CW_Toggle))
    Export_B.grid(row=0,column=1,padx=(ExportPadding,ExportBoarderX),pady=ExportBoarderY)
    
    
   
    
    
    
####Cooling and Warming Settings Frame
    SetFrame=tk.LabelFrame(rootCW,text='Settings')
    SetFrame.grid(row=2,column=0)
    
    #1st direction: pick axes
    help1='Seperate your data into Cooling and Warming curves\nChoose your x and y axis to split up'
    Direction1=tk.Label(SetFrame,text=help1)
    Direction1.grid(row=0,column=0,columnspan=2)
    
    #x and y axis drop down menu selection
    Xchoice=tk.StringVar()
    Ychoice=tk.StringVar()
    
    #set each as the usualy starting ones
    Xchoice.set('Temperature (K)')
    Ychoice.set('Bridge1_R (ohms)')
    
    #make menus
    QuickP_Xchoice_L=tk.Label(SetFrame,text='x axis')
    QuickP_Xchoice_L.grid(row=1,column=0)
    
    QuickP_Ychoice_L=tk.Label(SetFrame,text='y axis')
    QuickP_Ychoice_L.grid(row=2,column=0,pady=(0,5))
   
    QuickP_Xchoice_D=tk.OptionMenu(SetFrame, Xchoice, 'Temperature (K)','Field (Oe)')
    QuickP_Xchoice_D.grid(row=1,column=1)
    QuickP_Ychoice_D=tk.OptionMenu(SetFrame, Ychoice, 'Bridge1_R (ohms)','Bridge2_R (ohms)','Bridge3_R (ohms)')
    QuickP_Ychoice_D.grid(row=2,column=1,pady=(0,5))
    
    #Cooling and Warming radio buttons toggle
    Radio_L=tk.Label(SetFrame,text='Cooling/Warming toggle')
    Radio_L.grid(row=3,column=0,rowspan=2)
    
    #test label
    CW_Toggle=tk.BooleanVar()
    CW_Toggle.set(False)
    

    RadioOff=tk.Radiobutton(SetFrame,text='off',variable=CW_Toggle, value=False)
    RadioOff.grid(row=3,column=1,sticky=tk.W)
    
    RadioOn=tk.Radiobutton(SetFrame,text='on',variable=CW_Toggle, value=True)
    RadioOn.grid(row=4,column=1,sticky=tk.W)
    
    
    
    
    
####Update Buttons
    #make update button for plot below settings settings
    Update_Bset=tk.Button(SetFrame,text='Update Plot',command=lambda:bt.Button_UpdatePlotCW(rootCW, 
                                                                                          canvas,
                                                                                          CWPlot,
                                                                                          Load_check_E, 
                                                                                          Machine, 
                                                                                          Xchoice, 
                                                                                          Ychoice, 
                                                                                          CW_Toggle))
    Update_Bset.grid(row=5,column=0) 
    
    #make update button for plot
    Update_B=tk.Button(rootCW,text='Update Plot',command=lambda:bt.Button_UpdatePlotCW(rootCW, 
                                                                                     canvas,
                                                                                     CWPlot, 
                                                                                     Load_check_E, 
                                                                                     Machine, 
                                                                                     Xchoice, 
                                                                                     Ychoice, 
                                                                                     CW_Toggle))
    Update_B.grid(row=3,column=2,sticky=tk.E)

    
    
    
    
    
    
    
    
        
    
    
