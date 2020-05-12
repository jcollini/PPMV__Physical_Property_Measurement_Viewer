##Data Parser for PPMV program
import tkinter as tk

import PPMV_Jobs4 as ppmv
import PPMV_Classes4 as cl
import Button_Functions4 as bt

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler


def Parse_Section(MasterTK,labeltext):
    #creates parse widgets
    Method=tk.StringVar() #choice for menu
    #Method.set('Shift_Direction')
    
    DataLabel=tk.StringVar()
    #DataLabel.set('Temperature (K)')
    
    Divider_L=tk.Label(MasterTK,text=labeltext)
    
    Divider_Method=tk.OptionMenu(MasterTK,Method,'Shift_Direction',
                           'Shift_Dynamic')
    
    Divider_Label=tk.OptionMenu(MasterTK,DataLabel,'Temperature (K)',
                                   'Field (Oe)',
                                   'theta (deg)',
                                   'Bridge1_R (ohms)',
                                   'Bridge2_R (ohms)',
                                   'Bridge3_R (ohms)')
    
    return Method,DataLabel,Divider_L,Divider_Method,Divider_Label

def Add_Parse_Section(MasterTK,RowTK,DP_Label_ref,DP_Method_ref):
    #creates Parse widgets and places them on the screen
    #stores new reference widgets for labels and methods into a list
    row=RowTK.get()
    Method,DataLabel,Divider_L1,Divider_Method,Divider_Label=Parse_Section(MasterTK,'Divider '+str(row)+':  ')
    Divider_L1.grid(row=row,column=0)
    Divider_Label.grid(row=row,column=1)
    Divider_Method.grid(row=row,column=2)
    
    #update lists
    DP_Label_ref.append(DataLabel)
    DP_Method_ref.append(Method)
    
    #update row number
    RowTK.set(row+1)
    
def Button_UpdatePlotDP(canvas_PLT,Plot_PLT,Data_CL,DP_Label_ref,DP_Method_ref,XchoiceTK,YchoiceTK):
    #clear current plot
    Plot_PLT.clear()
    
    #use dividers, if avaliable
    if DP_Label_ref:
        #add divider code here
        testing=[]
    else:
        #otherwise, just plot the data as is
        data=Data_CL.data
        
        #grab needed data
        Xdata=data[XchoiceTK.get()]
        Xname=XchoiceTK.get()
        
        Ydata=data[YchoiceTK.get()]
        Yname=YchoiceTK.get()
        
        Plot_PLT.plot(Xdata,Ydata)
        Plot_PLT.set_xlabel(Xname)
        Plot_PLT.set_ylabel(Yname)
        
    #redraw canvas with ticks inside
    Plot_PLT.tick_params(direction='in')
    
    Plot_PLT.relim()
    Plot_PLT.autoscale()
    canvas_PLT.draw()
    
    
  

def App_DataParaser(DataLoc,MachineType):
    #general settings
    ExportPadding=50 #seperation of export buttons
    ExportBoarderX=20 #boarder space around export buttons
    ExportBoarderY=5 #boarder space around export buttons
    ExFrameY=5 #boarder space around export frame
   
    #controls the window for cooling and warming
    rootDP=tk.Toplevel()
    rootDP.title('PPMV Data Parser')
    rootDP.iconbitmap('QMC_Temp.ico')

####Header widget
    Header_L=tk.Label(rootDP,text='PPMV Data Parasing')
    Header_L.grid(row=0,column=0,pady=(0,10))
    
    #directions for user
    Explain_L=tk.Label(rootDP,text='For each divider, select the data \nused to split and the method for splitting')
    Explain_L.grid(row=2,column=0)
    
####Load Frame
    LoadFrame=tk.LabelFrame(rootDP,text='Check/Change Loaded Data')
    LoadFrame.grid(row=1,column=0,padx=10,pady=ExFrameY,sticky=tk.W)
    #LoadFrame.grid_configure(ipadx=300)
    
    #show load buttons and import load from the previous window
    #load data widgets
    Load_B=tk.Button(LoadFrame,text="Load data",command=lambda: bt.Button_LoadData__2(rootDP, 
                                                                                      Load_check_E,
                                                                                      Machine,
                                                                                      Data))
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
    
    #create empty data object and fill it with the pre-loaded data, if avaliable
    Data=cl.PPMSData()
    if Load_check_E.get():
        Data.load_data(DataLoc, MachineType)
   
    

####Plotting
    #create empty figure objects and put them on screen
    canvas,fig,axis,toolbarFrame=bt.Empty_Plot(rootDP)
    
    canvas.get_tk_widget().grid(row=2,column=1,columnspan=2,rowspan=2)
    
    toolbarFrame.grid(row=4,column=1,columnspan=2)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
    
####PlotFrame
    PlotFrame=tk.LabelFrame(rootDP,text='Plot Settings')
    PlotFrame.grid(row=1,column=1,columnspan=2)
    #x and y axis drop down menu selection
    Xchoice=tk.StringVar()
    Ychoice=tk.StringVar()
    
    #set each as the usualy starting ones
    Xchoice.set('Temperature (K)')
    Ychoice.set('Bridge1_R (ohms)')
    
    #make menus
    QuickP_Xchoice_L=tk.Label(PlotFrame,text='x axis')
    QuickP_Xchoice_L.grid(row=0,column=0)
    
    QuickP_Ychoice_L=tk.Label(PlotFrame,text='y axis')
    QuickP_Ychoice_L.grid(row=1,column=0,pady=(0,5))
   
    QuickP_Xchoice_D=tk.OptionMenu(PlotFrame, Xchoice, 'Temperature (K)','Field (Oe)')
    QuickP_Xchoice_D.grid(row=0,column=1)
    QuickP_Ychoice_D=tk.OptionMenu(PlotFrame, Ychoice, 'Bridge1_R (ohms)','Bridge2_R (ohms)','Bridge3_R (ohms)')
    QuickP_Ychoice_D.grid(row=1,column=1,pady=(0,5))
    
    #update plot
    Update_B=tk.Button(PlotFrame,text='Update Plot',command=lambda: Button_UpdatePlotDP(canvas, 
                                                                                        axis, 
                                                                                        Data, 
                                                                                        Labels_ref, 
                                                                                        Methods_ref, 
                                                                                        Xchoice, 
                                                                                        Ychoice))
    
    Update_B.grid(row=0,column=2,rowspan=2)
    
    
####Parsing Settings Frame
    ParseFrame=tk.LabelFrame(rootDP,text='Parse Data Settings')
    ParseFrame.grid(row=3,column=0)
    
    #create empty lists to store labels and methods lists
    Labels_ref=[]
    Methods_ref=[]
    
    #keep track of rownumbers
    RowCount=tk.IntVar()
    RowCount.set(1)
    
    #button to create a new list
    Add_Row_B=tk.Button(ParseFrame,text='Create New Divider',command=lambda: Add_Parse_Section(ParseFrame, 
                                                                                       RowCount, 
                                                                                       Labels_ref, 
                                                                                       Methods_ref))
    
    Add_Row_B.grid(row=0,column=0,columnspan=3)
    


    
    
    
    
    
    

