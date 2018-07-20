# Integration-Program
manually.py - Integrate area under curves from screengrabs
Manual Integration Program 1.0 7/16/18

## Instructions:

1) Take screen capture of chart.
2) In graphical editor (e.g. MS Paint), crop out everything but analytical program window.
3) Place integration marker with RED line.
4) Save as PNG file.
5) Open python or cmd and type:
```
>>> import manually
>>> manually.integrate()
```
6) Input file name and extension when prompted.
7) Input total area of chart when prompted.

## General Usage Notes:

+ Current version of software only compatible with black curve on white background with red integration marker. Watch future versions for better compatibility.

+ Input total area of chart in mV\*s units if using for CNS applications. Do this by multiplying the range of the x-axis by the range of the y-axis

+ Outputs units are in mV\*s. Convert to concentration by dividing most recent CCV area by area count as conversion factor.

+ For any other application, input custom units when prompted by setting custom = True

+ Set pixel option to true (px=True) to get area count in terms of pixels.

+ Setting audit = true saves the cropped graph and colors the area underneath the curve used for the calculation

## Installation:

+ Install Python3.7 on computer. 
+ Run in python or cmd terminal.

## Contact:

Name: Omar Ali
Email: Omarh90@gmail.com

## Copyright:
Copyright &copy; 2018 Omar Ali - All Rights Reserved
You may use, distribute, modify this code if attributed to original source and as subject to license agreement.
