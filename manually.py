#Written by: Omar Ali <Omarh90@gmail.com>

import os
import math
import collections
import warnings
from PIL import Image
import pdb
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename
import axis
import calibration
import report

def integrate(px = False, crop = True, audit = True, custom = False):

    """
    Integrates area underneath curve, by taking sum of the vertical difference
    between each point of the peak and the integration marker.

    ____________________________________________________________________________
    Parameters: (all bool)
    
    * px: indicates whether or not to return area in units of pixels.

    * crop: indicates whether or not to auto-crop screen grab.
      Only works for graphs with black borders.

    * audit: creates text report and graphical files for each step of the program.

    * custom: for more general applications aside from CNS analysis. Not yet implimented.
    """

    #TODO:
    #      custom feature: colors
    #      GUI
    
    errormsg = ''
    root=tk.Tk()
    filename_dir = askopenfilename()
    root.destroy()
    
    #For CNS instrument graph parse.
    if custom == False:
        #User input sample parameters.
        el = input('Enter element for single peak (C/N/S):').strip()[0].capitalize()
        corr_factor = float(input('Enter correction factor (0 < f <= 1):'))
        wt = float(input('Enter sample weight, mg (default 2500 mg):'))
        user_ID = input('Enter initials:').upper()
        peak_clr = 'black'
        background_clr = 'white'
        integrationmarker_clr = 'red'
    else:
        if crop == True:
            warnings.warn('Please submit cropped graph with crop option set to \'False\'.', Warning)
        chart_area = input('Enter total area of chart:')
        units = input('Enter units of chart area:')

    #Saves image, stores dimensions, and stores pixel colors.
    print("file: " + filename_dir)
    im = Image.open(filename_dir)
    w, h = im.size
    pix_val = list(im.getdata())

    if audit == True:
        #Makes file_calc folder in same directory as image file.
        directory, filename = os.path.split(filename_dir)
        filename_nodir = filename.split('.')[:-1][0]
        filename_audit = filename.split('.')[:-1][0] + '_calc'
        filedir_audit = os.path.join(directory, filename_audit)
        os.makedirs(filedir_audit, exist_ok = True)
        filename_dirext = os.path.join(filedir_audit, filename_nodir + '.png')
        im.save(filename_dirext)
        
    if crop == True:
        #Finds black borders around graph, and crops area inside.
        w_yaxis = 70
        h_xaxis = 15
        black_pixels = [i for i, x in enumerate(pix_val) if x[0] == x[1] & x[0] == x[2] & x[0] < 10]
        blackpixels_rows = [math.floor(x/w) for x in black_pixels]
        blkpixel_rowfreq = collections.Counter(blackpixels_rows)
        hz_borders = sorted(blkpixel_rowfreq.most_common(2))
        top_border, bottom_border = hz_borders[0][0], hz_borders[1][0]
        blackpixels_cols = [x%w for x in black_pixels]
        blkpixel_colfreq = collections.Counter(blackpixels_cols)
        vt_borders = sorted(blkpixel_colfreq.most_common(2))
        left_border, right_border = vt_borders[0][0], vt_borders[1][0]
        graph = im.crop((left_border + 1, top_border + 1, right_border -1, bottom_border - 1))
        if not graph:
            warnings.warn('Script failed to crop chart. Rerun program on only cropped region with crop setting as False.', Warning)
        w2, h2 = graph.size
        pix_val2 = list(graph.getdata())
        yaxis_image = im.crop((right_border + 1, top_border - 4, right_border + w_yaxis, bottom_border + 7))
        xaxis_image = im.crop((left_border - 13, bottom_border +7, right_border + 50, bottom_border + 7 + h_xaxis))
        w_y, h_y = yaxis_image.size
        w_x, h_x = xaxis_image.size
        x_axis_val = list(xaxis_image.getdata())
        y_axis_val = list(yaxis_image.getdata())
        x_totalpx = len(x_axis_val)-1
        y_totalpx = len(y_axis_val)-1

        #Reads x and y axis.
        x_axis = axis.parse(False, w_x, h_x, x_totalpx, x_axis_val)
        y_axis = axis.parse(True, w_y, h_y, y_totalpx, y_axis_val)

        #Calulates area of entire graph.
        chart_area = int(-1*(np.mean(np.diff(x_axis))*(len(x_axis)-1))*np.mean(np.diff(y_axis))*(len(y_axis)-1))
        
        if audit == True:
            #Saves each cropped image from source graphic to calc folder.
            croppedfilename = os.path.join(filedir_audit, filename_nodir + '_crop.png')
            graph.save(croppedfilename)
            xaxisfilename = os.path.join(filedir_audit, filename_nodir + '_xaxis.png')
            xaxis_image.save(xaxisfilename)
            yaxisfilename = os.path.join(filedir_audit, filename_nodir + '_yaxis.png')
            yaxis_image.save(yaxisfilename)

    else:
        #No cropping necessary.
        graph = im
        w2, h2 = w, h
        pix_val2 = pix_val

    #Finds peak and integration marker from cropped graph.
    peak = [i for i, x in enumerate(pix_val2) if (x[0] == x[1] & x[1] == x[2] & x[2] <= 20)]
    int_marker = [i for i, x in enumerate(pix_val2) if x[0] > 200 and x[1] <= 100 and x[2] <= 100]

    #Checks if integration marker list is empty, or close to it.
    if len(int_marker) <= 10:
        warnings.warn('Integration marker not recognized. Results are artificially high.', Warning)

    #Cleans up integration marker (makes one to one).
    int_cols_clean = []
    int_marker_clean = []
    for x in int_marker:
        if x%w2 not in int_cols_clean:
            int_marker_clean.append(x)
            int_cols_clean.append(x%w2)

    #Cleans up peak (makes one to one).
    peak_cols_clean = []
    clean_peak = []
    for x in peak:
        if x%w2 not in peak_cols_clean:
            clean_peak.append(x)
            peak_cols_clean.append(x%w2)

    #Finds area under curve, in pixels.
    area_px = sum([(x - y)/w2 for x in int_marker_clean for y in clean_peak if y%w2 == x%w2])

    #Converts units from pixels based on ratio of area under curve to total area on chart.
    chartarea_px = (w2 + 1)*(h2 + 1)
    area_crop_mVs = float(chart_area)
    area = area_px * area_crop_mVs/chartarea_px
    area_px = int(area_px)
    if audit == True:
        im_audit = graph

        #Defines colors used to fill in graph.
        areacolor_audit = (179,228,255)
        peakcolor_audit = (0,45,65)
        intcolor_audit = (240,0,0)
        area_px_audit = 0
        x_fill_audit, y_fill_audit = [], []

        #Cleans up integration marker for graphics.
        x_min, x_max = min([x%w2 for x in int_marker_clean]), max([x%w2 for x in int_marker_clean])
        int_marker_sorted = sorted(int_marker_clean, key = lambda int_marker_clean: int(int_marker_clean)%w2)
        int_marker_y = [math.floor(y/w2) for y in int_marker_sorted]
        integration_values = [(x - y)/w2 for x in int_marker_sorted for y in clean_peak if y%w2 == x%w2]
              
        #Shades in peak area.
        for x in range(0, len(integration_values)-1):
            for y in range(0, int(integration_values[x])):
                x_fill_audit.append(x)
                y_fill_audit.append(y)
                im_audit.putpixel((x+x_min,-y+int_marker_y[x]-1), areacolor_audit)
                area_px_audit += 1

        #Coordinate transformation for peak to x, y values.
        xmin_pk, xmax_pk = min([x%w2 for x in clean_peak]), max([x%w2 for x in clean_peak])
        cleanpeak_x = [x%w2 for x in clean_peak]
        cleanpeak_y = [math.floor(y/w2) for y in clean_peak]

        #Finds retention time of peak in seconds.
        rt_px0 = clean_peak[0]%w2
        rt_px, i = [clean_peak[0]], 0
        while i <=len(clean_peak):
            if clean_peak[i+1] == clean_peak[i]+1:
                rt_px.append(clean_peak[i+1])
            else:
                i = len(clean_peak)
            i+=1
        rettime_px = [x%w2 for x in rt_px]
        ret_time = x_axis[0] +(x_axis[-1] - x_axis[0])*np.mean(rettime_px)/w2

        #Colors in peak
        for x in range(0, len(clean_peak)):
            im_audit.putpixel((cleanpeak_x[x],cleanpeak_y[x]), peakcolor_audit)
            im_audit.putpixel((cleanpeak_x[x],cleanpeak_y[x]+1), peakcolor_audit)
            
        #Colors in integration marker.
        for x in range(0,len(int_marker_clean)):
            im_audit.putpixel((x + x_min, -y+int_marker_y[x]-1), intcolor_audit)
            im_audit.putpixel((x + x_min, -y+int_marker_y[x]), intcolor_audit)
        int_fill_coordinates = list(zip(x_fill_audit,y_fill_audit))

        #Pastes filled in chart onto original image.
        offset_chart = (left_border + 1, top_border +1)
        im.paste(im_audit, offset_chart)
        integrationfilename = os.path.join(filedir_audit, filename_nodir + '_integration.png')
        im.save(integrationfilename)
        imresults = Image.open(integrationfilename)
        imresults.show()

    #Confirms that colored in area is equal to measured area.
    if float(area_px_audit) > float(area_px) * 1.01 or float(area_px_audit) < float(area_px) * 0.99:
        warnings.warn('Shaded area not representative of calculated area!', Warning)
        print('Shaded area under curve = ' + str(area_px_audit) + 'pixels')
        print('Area under curve = ' + str(area_px) + 'pixels')

    if px == False:
        if custom == False:
            #Gives sample concentration in mg/kg.
            if el == 'C':
                #'Insensitive' mode calibration.
                cal_audit = calibration.curve(area, el, False, True)
            elif el == 'N' or el == 'S':
                #Sensitive mode calibration.
                cal_audit = calibration.curve(area, el, True, True)
            else:
                errormsg = 'Element not recognized. Please input /"C/", /"N/", or /"S/"'

            #Calls report function to display report, and saves in sample_calc folder.
            y = cal_audit[0][0]
            conc = 1000000*corr_factor*y/wt
            if audit==True:
                #Saves and prints report in command window.
                finalreport = report.generate(filename, conc, corr_factor, wt, area_px, x_axis, y_axis,
                    chart_area, chartarea_px, cal_audit, ret_time, user_ID)
                reportfile_name = os.path.join(filedir_audit, filename_nodir + '_report.txt')
                report_file = open(reportfile_name,'w+')
                report_file.write(finalreport)
                report_file.close()
                print(finalreport)               
                return None;
            else:
                return_area = "Peak area = " + str(round(area,2)) + " mV*sec"
                return_conc = "Concentration = " + str(round(conc,3)) + " mg " + el + "/kg" + errormsg
                return ', '.join((return_area, return_conc));

        else:
            return "Peak area = " + str(round(area,2)) + units
    elif px == True:
        return "Peak area = " + str(area_px) + " pixels"
    else:
        return 0;
