# Integration-Program
Integrate Software Charts.py
Manual Integration Program 1.0 7/16/18

INSTRUCTIONS:

1) Take screen capture of chart.
2) In graphical editor (e.g. MS Paint), crop out everything but analytical program window.
3) Place integration marker with RED line.
4) Save as PNG file.
5) Open python or cmd and type:
   import manually
   manually.integrate()
6) Input file name (as png) and extension when prompted.
7) Input area of chart when prompted.

GENERAL USAGE NOTES:

+ Input total area of chart in mV\*s units. Do this by multiplying the range of the x-axis by the range of the y-axis

+ Outputs units are in mV\*s. Convert to concentration by dividing most recent CCV area by area count as conversion factor.

+ Set pixel option to true (px=True) to get area count in terms of pixels.

INSTALLATION:

+ Install Python3.7 on computer. Run in python or cmd terminal.

CONTACT:

Name: Omar Ali
Contact: Omarh90@gmail.com

Copyright (C) 2018 Omar Ali - All Rights Reserved
You may use, distribute, modify this code if attributed to original source and as subject to license agreement.
