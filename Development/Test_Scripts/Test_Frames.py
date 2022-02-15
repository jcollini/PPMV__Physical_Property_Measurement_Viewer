import tkinter as tk


def ShowFrame():
    F.grid(row=1,column=0)
    
def HideFrame():
    F.grid_forget()
    

#testing frame invisability
root=tk.Tk()

Hide=tk.Button(root,text='hide frame',command=HideFrame)
Hide.grid(row=0,column=0)

Show=tk.Button(root,text='show frame',command=ShowFrame)
Show.grid(row=0,column=1)

F=tk.LabelFrame(root,text='Dis a frame')
F.grid(row=1,column=0,columnspan=2)
F.grid_configure(ipadx=30)

F_label=tk.Label(F,text='inside frame')
F_label.grid(row=0,column=0)

F2_label=tk.Label(F,text='also inside frame')
F2_label.grid(row=0,column=1)


root.mainloop()