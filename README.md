# Integration-Program
Calculate area underneath curve from a screengrab with integrate_alpha.py.

Integration Program 1.0 9/4/18

## Instructions:

1) Press print screen button.
2) In graphic editor (e.g. MS Paint), crop out everything but analytical program window and save as png file.
3) Double-click on 'integrate_alpha', or in python:
```
>>> import integrate_alpha
```
4) Right-click and drag across peak to place integration marker.
5) To save, select File > Save from dropdown, and input sample ID and user initials when prompted.
6) Sample report will autogenerate.

## General Usage Notes:

+ Current version of software only compatible with black curve on white background with red integration marker. Watch future versions for better compatibility.

+ Creates report from manual integration, including calibration parameters and calculations.

+ For any other application, input custom units of total area of graph (e.g. product of x- and y-axis range) when prompted by setting custom = True (Watch future versions for this feature to be enabled.)

+ Saves the cropped graph and colors the area underneath the curve used for the calculation. Run python as admin if permissions needed to save files to directory

## Installation:

+ Install Python3.7.
+ Install the following Python modules: tkinter, shutil, pdb, os, Image, math, collections, warnings, numpy, datetime, decimal
+ Save integrate_alpha.py and auxiliary program files into directory with file-save permissions.
+ Run integrate_alpha.py in python or cmd terminal, or just doubleclick on integrate_alpha.py
+ Test functionality by loading try_me1.png or try_me2.png in folder with permissions to create new directory and run through program, and saving in same folder.
+ Note: has not yet been test on Linux or Mac OS.

## Contact:

Name: Omar Ali
Email: Omarh90@gmail.com

## Copyright:
Copyright &copy; 2018 Omar Ali - All Rights Reserved
You may use, distribute, modify this code if attributed to original source and as subject to license agreement.
