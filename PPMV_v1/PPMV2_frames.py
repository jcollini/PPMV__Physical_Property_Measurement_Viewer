import tkinter as tk
import matplotlib.pyplot as plt
import PPMV_Jobs2 as ppmv
from tkinter import filedialog
#Designer and Programer: John Collini
#Front end design for PPMV (Physical Property Measurement Viewer)

##specifically test lots of frames for design
    



#Needed Functions for buttons and selections
def Button_LoadData():
    #needed global variables
    #global Load_check_E
    #button to grab datafile location
    #Start at desktop
    file_location='::{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}'
    root.filename=filedialog.askopenfilename(initialdir=file_location,title='Select a file',filetypes=(('PPMS files','*.dat'),('all files','*.*')))
    
    #update the entry with the new file. Clear it first
    Load_check_E.delete(0,tk.END)
    Load_check_E.insert(0,root.filename)
    
    #place widgets back on th screen after loading data
    Load_check_L.grid(row=2,column=0)
    Load_check_E.grid(row=2,column=1,sticky=tk.W)
    Load_machine_L.grid(row=3,column=0,sticky=tk.E)
    Load_machine_D.grid(row=3,column=1,sticky=tk.W)

    QuickP_B.grid(row=1,column=2,columnspan=2)
    QuickP_Xchoice_L.grid(row=2,column=2)
    QuickP_Xchoice_D.grid(row=2,column=3,sticky=tk.W)
    QuickP_Ychoice_L.grid(row=3,column=2)
    QuickP_Ychoice_D.grid(row=3,column=3,sticky=tk.W)

    Simple_file_B.grid(row=1,column=4,sticky=tk.W)
    
    #place Jobs frame back on screen
    JobsFrame.grid(row=4,column=1,columnspan=4)

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

if __name__=='__main__':
  
    root=tk.Tk()
    
    #Root window characteristics
    
    root.title('PPMV')
    root.iconbitmap('QMC_Temp.ico')
    
    #Create buttons, labels, and other widgets
    #Header widget
    Header_L=tk.Label(root,text='Physical Property Measurement Viewer (PPMV)')
    #load data widgets
    Load_B=tk.Button(root,text="Load PPMS data\n(*.dat)",command=Button_LoadData)
    
    Load_check_L=tk.Label(root,text='File:')
    Load_check_E=tk.Entry(root)
    
    #machine selection for data
    Machine=tk.StringVar()
    Machine.set('9T-R')
    Load_machine_L=tk.Label(root,text='PPMS and Puck Used:')
    Load_machine_D=tk.OptionMenu(root, Machine, '9T-ACT','9T-R','14T-ACT','14T-R','Dynacool')
    
    #quick plot widgets
    #plot button
    QuickP_B=tk.Button(root,text='Quick Plot',command=Button_QuickPlot)
    
    #x and y axis drop down menu selection
    Xchoice=tk.StringVar()
    Ychoice=tk.StringVar()
    #set each as the usualy starting ones
    Xchoice.set('Temperature (K)')
    Ychoice.set('Bridge1_R (ohms)')
    #make menus
    QuickP_Xchoice_L=tk.Label(root,text='x axis')
    QuickP_Ychoice_L=tk.Label(root,text='y axis')
    QuickP_Xchoice_D=tk.OptionMenu(root, Xchoice, 'Temperature (K)','Field (Oe)','theta (deg)','Bridge1_R (ohms)','Bridge2_R (ohms)','Bridge3_R (ohms)')
    QuickP_Ychoice_D=tk.OptionMenu(root, Ychoice, 'Temperature (K)','Field (Oe)','theta (deg)','Bridge1_R (ohms)','Bridge2_R (ohms)','Bridge3_R (ohms)')
    
    #Simple File Output button
    Simple_file_B=tk.Button(root,text='Create Simple\nOutput',command=Button_QuickSave)
    
    
    #Put buttons on grid
    Header_L.grid(row=0,column=0,columnspan=5)
    
    Load_B.grid(row=1,column=0,columnspan=2)
    Load_check_L.grid(row=2,column=0)
    Load_check_E.grid(row=2,column=1)
    Load_machine_L.grid(row=3,column=0)
    Load_machine_D.grid(row=3,column=1)
    
    QuickP_B.grid(row=1,column=2,columnspan=2)
    QuickP_Xchoice_L.grid(row=2,column=2)
    QuickP_Xchoice_D.grid(row=2,column=3)
    QuickP_Ychoice_L.grid(row=3,column=2)
    QuickP_Ychoice_D.grid(row=3,column=3)
    
    Simple_file_B.grid(row=1,column=4)
    
    #start with buttons except loading and title invisable
    Load_check_L.grid_forget()
    Load_check_E.grid_forget()
    Load_machine_L.grid_forget()
    Load_machine_D.grid_forget()
    
    QuickP_B.grid_forget()
    QuickP_Xchoice_L.grid_forget()
    QuickP_Xchoice_D.grid_forget()
    QuickP_Ychoice_L.grid_forget()
    QuickP_Ychoice_D.grid_forget()
    
    Simple_file_B.grid_forget()
    
    ####Additional Jobs Frame
    JobsFrame=tk.LabelFrame(root,text='PPMS Analysis Tools',padx=300)
    JobsFrame.grid(row=4,column=1,columnspan=4)
    
    Job1=tk.Button(JobsFrame,text='Multi-Plot').grid(row=0,column=0)
    Job2=tk.Button(JobsFrame,text='Magnetoresistance').grid(row=0,column=1)
    Job3=tk.Button(JobsFrame,text='Hall Analysis').grid(row=0,column=2)
    Job3=tk.Button(JobsFrame,text='Cooling and Warming Curves').grid(row=0,column=3)
    
    #start with jobs frame invisable until loading data
    JobsFrame.grid_forget()
    
    #####Frame for selected Job
    #creates to drop in options for complex jobs the user selects
    #WSFrame stands for Workspace Frame
    WSFrame=tk.LabelFrame(root,text='***Fill in with job name***',padx=200)
    WSFrame.grid(row=1,column=5)
    
    WS_test=tk.Label(WSFrame,text='test job space').pack()
    
    
    
    
    
    #Run Window
    root.mainloop()