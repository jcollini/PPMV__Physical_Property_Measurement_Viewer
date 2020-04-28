import tkinter as tk

##test disable widgets

root=tk.Tk()

b1=tk.Button(root,text='switching on and off',state=tk.DISABLED).pack()
b2=tk.Button(root,text='click me').pack()


root.mainloop()