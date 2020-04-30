import tkinter as tk
from tkinter import filedialog

import PPMV_Jobs3 as ppmv
import Cooling_Warming as cw
#Designer and Programer: John Collini
#Front end design for PPMV (Physical Property Measurement Viewer)
#Style is a LAUNCHER

    



#Needed Functions for buttons and selections
def Button_LoadData(FileTK,MasterTK):
    #button to grab datafile location
    #Start at desktop
    file_location='::{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}'
    MasterTK.filename=filedialog.askopenfilename(initialdir=file_location,title='Select a file',filetypes=(('PPMS files','*.dat'),('all files','*.*')))
    
    #update the entry with the new file. Clear it first
    FileTK.delete(0,tk.END)
    FileTK.insert(0,MasterTK.filename)
    
    #return new FileTK variable
    return FileTK
    
def Button_QuickPlot():
    #button for quick plot
    ppmv.Job_QuickPlot(Load_check_E.get(),Machine.get(),Xchoice.get(),Ychoice.get())
    
def Button_QuickSave():
    #Button to quickly save loaded file
    
    #grab loaded PPMS file dataframe
    PPMS_File=Load_check_E.get()
    MachineType=Machine.get()
    data=ppmv.Read_PPMS_File(PPMS_File,MachineType)
    
    #Grab the file location and name from the user
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv',filetypes=(('csv','*.csv'),('all files','*.*')))
                                    
    data.to_csv (export_file_path, index = False, header=True)
    
def Launch_CoolingWarming(DataLoc,MachineType):
    #launches Cooling and Warming application
    cw.App_CoolingWarming(DataLoc,MachineType)

if __name__=='__main__':

####General Settings
    #General padding to have frames match
    JobFrame_Ysize=56
    #Padding if there is missing lines for the explaination text
    LinePadding=12
    
    
####Root window characteristics
    root=tk.Tk()
    root.title('Physical Property Measurement Viewer (PPMV)')
    root.iconbitmap('QMC_Temp.ico')
    
    #Header widget
    Header_L=tk.Label(root,text='Physical Property Measurement Viewer (PPMV)')
    Header_L.grid(row=0,column=0,pady=(0,10))
    

    

####Load Frame
    LoadFrame=tk.LabelFrame(root,text='Load PPMS Data',padx=205)
    LoadFrame.grid(row=1,column=0,padx=10,sticky=tk.W)
    #LoadFrame.grid_configure(ipadx=300)
    
    #Widgets and placement
    #load data widgets
    Load_B=tk.Button(LoadFrame,text="Load data",command=lambda: Button_LoadData(Load_check_E,root))
    Load_B.grid(row=0,column=0)
    
    Load_check_L=tk.Label(LoadFrame,text='File:')
    Load_check_L.grid(row=0,column=1,padx=(20,0))
    
    Load_check_E=tk.Entry(LoadFrame)
    Load_check_E.grid(row=0,column=2)
    
    #machine selection for data
    Machine=tk.StringVar()
    Machine.set('9T-R')
    
    Load_machine_L=tk.Label(LoadFrame,text='PPMS and Puck Used:')
    Load_machine_L.grid(row=0,column=3,padx=(20,0))
    
    Load_machine_D=tk.OptionMenu(LoadFrame, Machine, '9T-ACT','9T-R','14T-ACT','14T-R','Dynacool')
    Load_machine_D.grid(row=0,column=4)

####Jobs Frame 
    JobsFrame=tk.LabelFrame(root,text='Jobs Frame')
    JobsFrame.grid(row=2,column=0,padx=10,pady=(0,10),sticky=tk.W)
    #JobsFrame.grid_configure(ipadx=85)
    
####quick plot frame and widges
    PlotFrame=tk.LabelFrame(JobsFrame,text='Plot Frame')
    PlotFrame.grid(row=0,column=0,padx=10,pady=10)
    
    #plot icon
    QuickP_icon=tk.Label(PlotFrame,text='***Plot Icon***')
    QuickP_icon.grid(row=0,column=0,columnspan=2)
    
    #plot explanation
    QuickP_explain=tk.Label(PlotFrame,text='Plot your loaded data.\nPick x and y axis from menu.')
    QuickP_explain.grid(row=1,column=0,columnspan=2)
    
    #plot button
    QuickP_B=tk.Button(PlotFrame,text='Quick Plot',command=Button_QuickPlot)
    QuickP_B.grid(row=2,column=0,columnspan=2)
    
    #x and y axis drop down menu selection
    Xchoice=tk.StringVar()
    Ychoice=tk.StringVar()
    #set each as the usualy starting ones
    Xchoice.set('Temperature (K)')
    Ychoice.set('Bridge1_R (ohms)')
    #make menus
    QuickP_Xchoice_L=tk.Label(PlotFrame,text='x axis')
    QuickP_Xchoice_L.grid(row=3,column=0)
    
    QuickP_Ychoice_L=tk.Label(PlotFrame,text='y axis')
    QuickP_Ychoice_L.grid(row=4,column=0,pady=(0,5))
   
    QuickP_Xchoice_D=tk.OptionMenu(PlotFrame, Xchoice, 'Temperature (K)','Field (Oe)','theta (deg)','Bridge1_R (ohms)','Bridge2_R (ohms)','Bridge3_R (ohms)')
    QuickP_Xchoice_D.grid(row=3,column=1)
    QuickP_Ychoice_D=tk.OptionMenu(PlotFrame, Ychoice, 'Temperature (K)','Field (Oe)','theta (deg)','Bridge1_R (ohms)','Bridge2_R (ohms)','Bridge3_R (ohms)')
    QuickP_Ychoice_D.grid(row=4,column=1,pady=(0,5))
    
####Export CSV Frame   
    ExportFrame=tk.LabelFrame(JobsFrame,text='Export Frame')
    ExportFrame.grid(row=0,column=1,padx=10,pady=10)
    
    #explort icon and explanation
    Export_icon=tk.Label(ExportFrame,text='***Export Icon***')
    Export_icon.grid(row=0,column=0)
    
    Export_explain=tk.Label(ExportFrame,text='Export PPMS data \nto CSV.')
    Export_explain.grid(row=1,column=0)
    
    #Simple File Output button
    Export_file_B=tk.Button(ExportFrame,text='Export (.dat) data \n to (.csv)',command=Button_QuickSave)
    Export_file_B.grid(row=2,column=0,pady=(JobFrame_Ysize,5),padx=45)
    
    
####Cooling and Warming Frame
    CWFrame=tk.LabelFrame(JobsFrame,text='Cooling and Warming')
    CWFrame.grid(row=0,column=2,padx=10,pady=10)
    
    #explort icon and explanation
    CW_icon=tk.Label(CWFrame,text='***CW Icon***')
    CW_icon.grid(row=0,column=0)
    
    CW_explain=tk.Label(CWFrame,text='Application for seperating \nand plotting cooling \nand warming curves')
    CW_explain.grid(row=1,column=0)
    
    #Simple File Output button
    CW_B=tk.Button(CWFrame,text='Cooling and Warming',command=lambda: Launch_CoolingWarming(Load_check_E.get(),Machine.get()))
    CW_B.grid(row=2,column=0,pady=(JobFrame_Ysize,5),padx=32)
    
####Magnetoresistance Frame
    MRFrame=tk.LabelFrame(JobsFrame,text='Magnetoresistance')
    MRFrame.grid(row=0,column=3,padx=10,pady=10)
    
    #explort icon and explanation
    MR_icon=tk.Label(MRFrame,text='***MR Icon***')
    MR_icon.grid(row=0,column=0)
    
    MR_explain=tk.Label(MRFrame,text='Application for seperating \n and plotting \nmagnetoresistance curves')
    MR_explain.grid(row=1,column=0)
    
    #Simple File Output button
    MR_B=tk.Button(MRFrame,text='Magnetoresistance')
    MR_B.grid(row=2,column=0,pady=(JobFrame_Ysize,5),padx=32)
    

####Advanced Plot Frame
    AdvPlotFrame=tk.LabelFrame(JobsFrame,text='Advanced Plotting')
    AdvPlotFrame.grid(row=1,column=0,padx=10,pady=10)
    
    #explort icon and explanation
    AdvPlot_icon=tk.Label(AdvPlotFrame,text='***Adv Plot Icon***')
    AdvPlot_icon.grid(row=0,column=0)
    
    AdvPlot_explain=tk.Label(AdvPlotFrame,text='Application showing advanced \nplot settings for data\n')
    AdvPlot_explain.grid(row=1,column=0)
    
    #Simple File Output button
    AdvPlot_B=tk.Button(AdvPlotFrame,text='Advanced Plot')
    AdvPlot_B.grid(row=2,column=0,pady=(JobFrame_Ysize,5),padx=32)
    

####Custom PPMS File Editor 
    CustomFrame=tk.LabelFrame(JobsFrame,text='Parse PPMS File')
    CustomFrame.grid(row=1,column=1,padx=10,pady=10)
    
    #explort icon and explanation
    Custom_icon=tk.Label(CustomFrame,text='***Parse Icon***')
    Custom_icon.grid(row=0,column=0)
    
    Custom_explain=tk.Label(CustomFrame,text='Application for editting \nand parsing PPMS data\n')
    Custom_explain.grid(row=1,column=0)
    
    #Simple File Output button
    Custom_B=tk.Button(CustomFrame,text='Parse Data')
    Custom_B.grid(row=2,column=0,pady=(JobFrame_Ysize,5),padx=70)
    

    


    
    
    
    
    
    
    
    
    
    
    
    
    
    #Run Window
    root.mainloop()