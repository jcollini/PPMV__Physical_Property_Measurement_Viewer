# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 20:16:18 2020

@author: jccol
"""


from PIL import Image,ImageTk
import tkinter as tk
root=tk.Tk()

image = Image.open('Icon_Quick_Plot.png')
photo = ImageTk.PhotoImage(image)


label = tk.Label(image=photo)
label.image = photo # keep a reference!
label.grid(row=0,column=0)


tk.mainloop()