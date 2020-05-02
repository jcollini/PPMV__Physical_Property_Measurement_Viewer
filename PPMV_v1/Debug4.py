import tkinter as tk

#Debug functions
def Radio_Click(MasterTK,RadioValueTK,Old_RadioTK):
    #Test function for radios. For Debug use
    Old_RadioTK.grid_forget()
    RadioTest=tk.Label(MasterTK,text=RadioValueTK)
    RadioTest.grid(row=5,column=0)
