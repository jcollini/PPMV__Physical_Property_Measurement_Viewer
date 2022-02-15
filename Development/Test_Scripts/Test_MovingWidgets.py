import tkinter as tk

#testing positions of labels
root=tk.Tk()

title=tk.Label(root,text='this is title')
title.grid(row=0,column=0,columnspan=3,sticky=tk.W)


OptionsL=tk.Label(root,text='pick something').grid(row=1,column=0)

g=tk.StringVar()
g.set('option1')
Options=tk.OptionMenu(root, g, 'option1', 'options2').grid(row=1,column=1)

Anotha1=tk.Button(root,text='This anotha\n button').grid(row=1,column=2)

root.mainloop()
