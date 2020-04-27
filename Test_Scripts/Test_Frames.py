import tkinter as tk


def ShowFrame():
    F.pack()
    
def HideFrame():
    F.pack_forget()
    

#testing frame invisability
root=tk.Tk()

Hide=tk.Button(root,text='hide frame',command=HideFrame)
Hide.pack()

Show=tk.Button(root,text='show frame',command=ShowFrame)
Show.pack()

F=tk.LabelFrame(root,text='Dis a frame',padx=300)
F.pack()

F_label=tk.Label(F,text='inside frame')
F_label.pack()

F2_label=tk.Label(F,text='also inside frame')
F2_label.pack()


root.mainloop()