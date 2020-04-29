# PPMV__Physical_Property_Measurement_Viewer
Python GUI tool for quickly accessing and quickly analyzing data from Physical Property Measurement Systems. [in development]

Author: John Collini

REQUIRES PYTHON 3
NEEDED LIBRARIES:
--numpy
--matplotlib
--tkinter
--pillow
--pandas
--scipy

To use: 

(Open folder PPMV_v1 folder

1.) run PPMV#.py (where # is the highest number you see) using a Python3 GUI or commandline.
	-->This brings up the PPMV GUI

2.) load an uneditted (*.dat) file you have using the upper left button
	-->This will open up many more options along the top. Your file path should show in a box below. Your file is now recognized by PPMV
	   
3.) Use the drop down to select which machine and puck was used. For instance, if I use an ACT puck in the 14T, I would pick 14T-ACT

4.) If you'd like to see an example plot of your data, use the quick plot option application ro the upper left. Select the desired x and y axis from the drop downs

5.) A pop up window will display a plot in matpotlib. Here you can save using the save button in the upper right corner, if you'd like. 
Otherwise close this pop up when done.

6.) If you'd like a simplifed output of your data with just [Temp, Field, theta, Bridge1R, Bridge2R, Bridge3R], hit the quick save button to save as a simple csv
	--> A standard dialog window will come up. Save just as you would any file

Future:

--Add functionality to each application button from the launcher
--Making the GUI look better	     
