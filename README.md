# Integration-Program
manually.py - Integrate area under curves from screengrabs

Manual Integration Program 2.0 8/14/18

## Instructions:

1) Press print screen button.
2) In graphic editor (e.g. MS Paint), crop out everything but analytical program window.
3) Place integration marker with RED line and save file in directory with permissions in which folder can be created.
5) In python:
```
>>> import manually
>>> manually.integrate()
```
6) Select file when prompted.
7) When prompted, input element, correction factor (between 0 and 1), sample weight (2.5 g default), and initials. 
7) Confirm integration and axis parse by images in filename_calc folder.

## General Usage Notes:

+ Current version of software only compatible with black curve on white background with red integration marker. Watch future versions for better compatibility.

+ Creates report from manual integration, including calibration parameters and calculations.

+ For any other application, input custom units of total area of graph (e.g. product of x- and y-axis range) when prompted by setting custom = True

+ Set pixel option to true (px=True) to get area count in terms of pixels.

+ Saves the cropped graph and colors the area underneath the curve used for the calculation. Run python as admin if permissions needed to save files to directory

## Installation:

+ Install Python3.7 on computer. 
+ Run in python or cmd terminal.
+ Test functionality by saving try_me1.png or try_me2.png in folder with permissions to create new directory and run through program.

## Contact:

Name: Omar Ali
Email: Omarh90@gmail.com

## Copyright:
Copyright &copy; 2018 Omar Ali - All Rights Reserved
You may use, distribute, modify this code if attributed to original source and as subject to license agreement.
