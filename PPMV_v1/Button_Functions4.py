import tkinter as tk


from tkinter import filedialog

import PPMV_Jobs4 as ppmv


#Modual for button functions in PPMV

def Button_LoadData(MasterTK,Load_EntryTK):
    #button to grab datafile location
    #
    #--MasterTK is Tk window locaion of buttton
    #--Load_EntryTK is Tk variable for load path
    #
    #Start at desktop
    file_location='::{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}'
    MasterTK.filename=filedialog.askopenfilename(initialdir=file_location,title='Select a file',filetypes=(('PPMS files','*.dat'),('all files','*.*')))
    
    #update the entry with the new file. Clear it first
    Load_EntryTK.delete(0,tk.END)
    Load_EntryTK.insert(0,MasterTK.filename)
    
    
    
def Button_QuickPlot(Load_EntryTK,MachineTK,XchoiceTK,YchoiceTK):
    #button for quick plot
    #
    #--Load_EntryTK is Tk variable for load path
    #--MachineTK is Tk variable for machine type
    #--XchoiceTK and YchoiceTK are Tk variables for names of x and y axis of a dataset
    ppmv.Job_QuickPlot(Load_EntryTK.get(),MachineTK.get(),XchoiceTK.get(),YchoiceTK.get())
    
def Button_QuickSave_CSV(Load_EntryTK,MachineTK):
    #Button to quickly save loaded file
    #
    #--Load_EntryTK is Tk variable for load path
    #--MachineTK is Tk variable for machine type
    #
    #grab loaded PPMS file dataframe
    PPMS_File=Load_EntryTK.get()
    MachineType=MachineTK.get()
    data=ppmv.Read_PPMS_File(PPMS_File,MachineType)
    
    #Grab the file location and name from the user
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv',filetypes=(('csv','*.csv'),('all files','*.*')))
                                    
    data.to_csv (export_file_path, index = False, header=True)
    



def Button_UpdatePlot(MasterTK,Fig_PLT,Load_EntryTK,MachineTK,XchoiceTK,YchoiceTK,CW_Toggle):
    #clear original figure
    Fig_PLT.clear()
    
    #create subplot to plot inside of cleared figure
    Plot_PLT=Fig_PLT.add_subplot(1,1,1)
    
    #Load data
    data=ppmv.Read_PPMS_File(Load_EntryTK.get(),MachineTK.get())
    
    #Grab wanted axis anmes and data, convert to numpy
    Xdata=data[XchoiceTK.get()]
    Xname=XchoiceTK.get()
        
    Ydata=data[YchoiceTK.get()]
    Yname=YchoiceTK.get()
    
    #Plot data depending on toggle
    if CW_Toggle:
        #Split data
        X1,Y1,X2,Y2=ppmv.Job_CW_Split_Data(Xdata, Ydata)
        #overwrite original fig and plot with new split data
        FIG_PLT,PlotPLT=ppmv.Job_CWPlot(X1,Y1,X2,Y2)
        Plot_PLT.set_xlabel(Xname)
        Plot_PLT.set_ylabel(Yname)
    else:
        #overwrite original fig and plot with unsplit data
        FIG_PLT,PlotPLT=ppmv.Job_CWPlot(X1,Y1,X2,Y2)
        Plot_PLT.set_xlabel(Xname)
        Plot_PLT.set_ylabel(Yname)
        
    
    
    
        
    
def Button_SaveFig(Load_EntryTK,MachineTK,XchoiceTK,YchoiceTK,CW_Toggle):
    #Button to quickly save loaded file
    
    #Reamke current figure with the user settings
    #Load data
    data=ppmv.Read_PPMS_File(Load_EntryTK.get(),MachineTK.get())
    
    #Grab wanted axis anmes and data, convert to numpy
    Xdata=data[XchoiceTK.get()]
    Xname=XchoiceTK.get()
        
    Ydata=data[YchoiceTK.get()]
    Yname=XchoiceTK.get()
    
    #Plot data depending on toggle
    if CW_Toggle:
        #Split data
        X1,Y1,X2,Y2=ppmv.Job_CW_Split_Data(Xdata, Ydata)
        #plot all data
        fig,CWPlot=ppmv.Job_CWPlot(X1,Y1,X2,Y2)
        CWPlot.set_xlabel(Xname)
        CWPlot.set_ylabel(Yname)
    else:
        #Plot just the original data
        fig,CWPlot=ppmv.Job_CWPlot(Xdata,Ydata)
        CWPlot.set_xlabel(Xname)
        CWPlot.set_ylabel(Yname)
    
    #Grab the file location and name from the user
    export_file_path = filedialog.asksaveasfilename(defaultextension='.png',filetypes=(('png','*.png'),('all files','*.*')))
                                    
    fig.savefig(export_file_path)
    

def Button_ExportCW_CSVs():
    #example stuff
    tk.Label()
    
