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
import xyaxis
import calibration
import report

def integrate(im_dir="", px=False, crop=True, audit=True, custom=False, subtract=False, gui=False,
              colorint=False, save='', gui_info=[]):

    """
    Integrates area underneath curve, by taking sum of the vertical difference
    between each point of the peak and the integration marker.

    ____________________________________________________________________________
    Parameters:

    * im_dir: (str) indicates file extension for image file when GUI option used.
    
    * px: (bool) indicates whether or not to return area in units of pixels.

    * crop: (bool) indicates whether or not to auto-crop screen grab.
      Only works for graphs with black borders.

    * audit: (bool) creates text report and graphical files for each step of the program.

    * custom: (bool) for more general applications aside from CNS analysis. Not yet implimented.

    * subtract: (bool) indicates whether or not to count peak below integration marker as
      negative area (subtact = True) or not count it (subtact = False).

    * gui: (bool) for graphical user interface.

    * gui_info: (list) exhaustive list of parameters from GUI program.
                  * rt_coord list len =2 of (int 2-tuple): start and endpoints of real time integration line.
                  * filename of picture (str)
                  * calibration input (list): correction factor (float), sample weight in mg (float), element (chr)
                  * userID: Initials
                  * sample_ID: user input of sample


    * colors (list): TBD
   
    *save

    *colorint
    
    """

    #TODO:
    #      change int-marker color from red!
    #      custom feature: colors
    #      GUI
    
    errormsg = ""
    if gui == False:
        root=tk.Tk()
        filename_dir = askopenfilename()
        root.destroy()
    else:
        filename_dir = gui_info[1]
    
    if custom == False and gui == False:
        el = input('Enter element for single peak (C/N/S):').strip()[0].capitalize()
        corr_factor = float(input('Enter correction factor (0 < f <= 1):'))
        wt = float(input('Enter sample weight, mg (default 2500 mg):'))
        user_ID = input('Enter initials:').upper()
        peak_clr = 'black'
        background_clr = 'white'
        integrationmarker_clr = 'red'

    elif gui == True:
        try:      
            corr_factor = gui_info[2][0]
            wt = gui_info[2][1]
            el = gui_info[2][2]
            user_ID =gui_info[2][3]
            if save == True:
                sample_ID= gui_info[2][4]
            else:
                sample_ID=''
        except:
            errormsg = errormsg + "Input errors!"
            return None
        
    else:
        if crop == True:
            warnings.warn('Please submit cropped graph with crop option set to \'False\'.', Warning)
        chart_area = input('Enter total area of chart:')
        units = input('Enter units of chart area:')

    im = Image.open(filename_dir)
    w, h = im.size
    pix_val = list(im.getdata())

    if audit == True:
        #Makes file_calc folder in same directory as image file.
        
            directory, filename = os.path.split(filename_dir)
            filename_noext = filename.split('.')[:-1][0]
            ext = filename.split('.')[-1:][0]
            filename_audit = filename.split('.')[:-1][0] + '_calc'
            filedir_audit = os.path.join(directory, filename_audit)
            os.makedirs(filedir_audit, exist_ok = True)
            filename_dirext = os.path.join(filedir_audit, filename_noext + '.png')
        
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
        graph = im.crop((left_border+1, top_border+1, right_border-1, bottom_border-1))
        if not graph:
            warnings.warn('Script failed to crop chart. Rerun program on only cropped region with crop setting as False.', Warning)
            errormsg = errormsg + "Script failed to crop chart. Rerun program on only cropped region with crop setting as False."
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
        x_axis = xyaxis.parse(False, w_x, h_x, x_totalpx, x_axis_val)
        y_axis = xyaxis.parse(True, w_y, h_y, y_totalpx, y_axis_val)

        #Calulates area of entire graph.
        chart_area = int(-1*(np.mean(np.diff(x_axis))*(len(x_axis)-1))*np.mean(np.diff(y_axis))*(len(y_axis)-1))
        
        if audit == True:
            #Saves each cropped image from source graphic to calc folder.
            croppedfilename = os.path.join(filedir_audit, filename_noext + '_crop.png')
            graph.save(croppedfilename)
            xaxisfilename = os.path.join(filedir_audit, filename_noext + '_xaxis.png')
            xaxis_image.save(xaxisfilename)
            yaxisfilename = os.path.join(filedir_audit, filename_noext + '_yaxis.png')
            yaxis_image.save(yaxisfilename)

    else:
        #No cropping necessary.
        graph = im
        w2, h2 = w, h
        pix_val2 = pix_val

    #Finds peak and integration marker from cropped graph.
    peak = [i for i, x in enumerate(pix_val2) if (x[0] == x[1] & x[1] == x[2] & x[2] <= 20)]      #Redefine for different color peak.
    if gui == False:
        int_marker = [i for i, x in enumerate(pix_val2) if x[0] > 200 and x[1] <= 100 and x[2] <= 100]#Redefine from red integration marker.
    else:
        x1, y1, x2, y2 = gui_info[0][0][0], gui_info[0][0][1], gui_info[0][1][0], gui_info[0][1][1]
        x1 -= left_border
        x2 -= left_border
        y1 -= top_border
        y2 -= top_border
        if x1 < x2:
            x_val = range(x1, x2)
        elif x2 < x1:
            x_val = range(x2, x1)
        else:
            errormsg = errormsg + "Error! zero length int marker!"
        int_slope = (y2 - y1)/(x2 - x1)
        int_intercept = y1 - int_slope*x1
        y_val = [x*int_slope + int_intercept for x in x_val]
        y_val = [int(round(x,0)) for x in y_val]
        int_xypairs = list(zip(x_val,y_val))
        int_markerzip = [p for p in int_xypairs if (p[0] < w2 and p[0] > 0) and (p[1] < h2 and p[1] > 0)]
        int_marker = list(map(lambda p: p[1]*w2 + p[0],int_markerzip))

    if len(int_marker) <= 10:
        warnings.warn('Integration marker not recognized. Results may be artificially high.', Warning)
        errormsg = errormsg + 'Integration marker not recognized.     Results may be artificially high.'

    #Cleans up integration marker (makes one to one).
    int_cols_clean = []
    int_marker_clean1 = []
    for x in int_marker:
        if x%w2 not in int_cols_clean:
            int_marker_clean1.append(x)
            int_cols_clean.append(x%w2)

    #Cleans up peak (makes one to one).
    peak_cols_clean = []
    clean_peak = []
    for x in peak:
        if x%w2 not in peak_cols_clean:
            clean_peak.append(x)
            peak_cols_clean.append(x%w2)

    #Finds area under curve, in pixels.
    if subtract == True:
        area_px = sum([(x - y)/w2 for x in int_marker_clean1 for y in clean_peak if y%w2 == x%w2])
    else:
        area_px = sum([(x - y)/w2 for x in int_marker_clean1 for y in clean_peak if y%w2 == x%w2 and x >= y])
        
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
        intcolor_audit = (255,0,0)
        intcolor_save = (255,0,0)
        subt_areacoloraudit = (255- areacolor_audit[0], 255- areacolor_audit[1], 255- areacolor_audit[2])
        subt_areacoloraudit = (200, 0, 0)
        area_px_audit = 0
        x_fill_audit, y_fill_audit = [], []

        #Cleans up integration marker for graphics.
        x_min, x_max = min([p[0] for p in int_markerzip]), max([p[0] for p in int_markerzip])
        int_marker_sorted = sorted(int_marker_clean1, key = lambda x: int(x)%w2)
        int_marker_y = [math.floor(y/w2) for y in int_marker_sorted]
        integration_values = [(x - y)/w2 for x in int_marker_sorted for y in clean_peak if y%w2 == x%w2]

        #Coordinate transformation for peak to x, y values.
        xmin_pk, xmax_pk = min([x%w2 for x in clean_peak]), max([x%w2 for x in clean_peak])
        cleanpeak_x = [x%w2 for x in clean_peak]
        cleanpeak_y = [math.floor(y/w2) for y in clean_peak]
        intmarker_x = [x%w2 for x in int_marker_clean1]
        intmarker_y = [math.floor(y/w2) for y in int_marker_clean1]
        xyint = list(zip(intmarker_x,intmarker_y))
        xypeak_1 = list(zip(cleanpeak_x, cleanpeak_y))
        
        #Transforms integration marker coordinates from (x,y) to absolute.
        xyint = list(zip(intmarker_x,intmarker_y))#clean int marker?
        xypeak_unsorted = list(zip(cleanpeak_x, cleanpeak_y))
        xyint = sorted(xyint, key = lambda p: p[0])
        xypeak =sorted(xypeak_unsorted, key = lambda p: p[0])

        #Removes negative integration values for subtract = False (e.g. integration marker above peak).
        if subtract == False:
            int_marker_clean = [p[0] + p[1]*w2 for p in xyint for q in xypeak if p[0] == q[0] and p[0] > q[1]]
        else:
            int_marker_clean = [p[0] + p[1]*w2 for p in xyint for q in xypeak if p[0] == q[0]] # and p[0] > q[1]]
        intmarker_x = [x%w2 for x in int_marker_clean]
        intmarker_y = [math.floor(y/w2) for y in int_marker_clean]
        intmarker_x1 = [x%w2 for x in int_marker_clean1]
        intmarker_y1 = [math.floor(y/w2) for y in int_marker_clean1]
        
        #Shades in peak area.
        for x in range(0, len(integration_values)):
            for y in range(0, abs(int(integration_values[x]))):
                if int(integration_values[x]) >= 0:
                    x_fill_audit.append(x)
                    y_fill_audit.append(y)
                    org_color = im_audit.getpixel((x+x_min,-y+int_marker_y[x]-1))
                    int_color = int((areacolor_audit[0] + org_color[0])/2), \
                        int((areacolor_audit[1] + org_color[1])/2), \
                        int((areacolor_audit[2] + org_color[2])/2)
                    im_audit.putpixel((x+x_min,-y+int_marker_y[x]-1), int_color)
                    area_px_audit += 1
                elif subtract == True and int(integration_values[x]) < 0:
                    x_fill_audit.append(x)
                    y_fill_audit.append(y)
                    org_color = im_audit.getpixel((x+x_min,y+int_marker_y[x]))
                    subt_color = int((subt_areacoloraudit[0] + org_color[0])/2), \
                        int((subt_areacoloraudit[1] + org_color[1])/2), \
                        int((subt_areacoloraudit[2] + org_color[2])/2)
                    im_audit.putpixel((x+x_min,y+int_marker_y[x]), subt_color)
                    area_px_audit -= 1

        #Colors in peak line.
        for x in range(0, len(clean_peak)):
            if cleanpeak_x[x] > x_min and cleanpeak_x[x] < x_max:
                if subtract == False:
                    point = [p for p in xyint if p[0] == cleanpeak_x[x]]
                    if point and point[0][1] > xypeak_unsorted[x][1]:
                        im_audit.putpixel((cleanpeak_x[x],cleanpeak_y[x]), peakcolor_audit)
                        im_audit.putpixel((cleanpeak_x[x],cleanpeak_y[x]+1), peakcolor_audit)
                else:
                    im_audit.putpixel((cleanpeak_x[x],cleanpeak_y[x]), peakcolor_audit)
                    im_audit.putpixel((cleanpeak_x[x],cleanpeak_y[x]+1), peakcolor_audit)
            
        #Colors in integration marker.
        if colorint == True and not save:
            for x in range(0,len(int_marker_clean1)): #clean vclean1
                im_audit.putpixel((intmarker_x1[x], intmarker_y1[x]), intcolor_audit)
                im_audit.putpixel((intmarker_x1[x], intmarker_y1[x]+1), intcolor_audit)
            int_fill_coordinates = list(zip(x_fill_audit,y_fill_audit))
        elif save:
            im_save = im_audit.copy()
            for x in range(0,len(int_marker_clean1)): #clean vclean1
                im_save.putpixel((intmarker_x1[x], intmarker_y1[x]), intcolor_save)
                im_save.putpixel((intmarker_x1[x], intmarker_y1[x]+1), intcolor_save)
            int_fill_coordinates = list(zip(x_fill_audit,y_fill_audit))
            
        #Finds retention time of peak in terms of seconds.
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

        #Pastes filled in chart onto original image.
        offset_chart = (left_border + 1, top_border +1)
        im.paste(im_audit, offset_chart)
        integrationfilename = os.path.join(filedir_audit, filename_noext + '_integration.png')
        im.save(integrationfilename)

        #Saves image with integration marker. Used for GUI save function.
        if save:
            im.paste(im_save, offset_chart)
            integrationfilename_save = os.path.join(filedir_audit, filename_noext + '_m.' + ext)
            im.save(integrationfilename_save)

        #Opens image for user.
        if gui == False:
            imresults = Image.open(integrationfilename)
            imresults.show()

    #Confirms that colored in area is equal to measured area.
    if (float(area_px_audit) > float(area_px) * 1.01 or float(area_px_audit) < float(area_px) * 0.99) and subtract==False \
     or (abs((float(area_px_audit) - float(area_px))/np.mean((area_px_audit,area_px))) > 0.01 and subtract==True):
        warnings.warn('Shaded area not representative of calculated area!***', Warning)
        errormsg = errormsg + '***shaded area not representative         of calculated area***'
        print('Shaded area under curve = ' + str(area_px_audit) + 'pixels')
        print('Area under curve = ' + str(area_px) + 'pixels')

    if px == False:
        if custom == False:
            #Gives sample concentration in mg/kg.
            if el == 'C':
                #'Insensitive' mode calibration.
                cal_audit = calibration.curve(area, el, False, True)
                if gui == False:
                    print("cal_audit, C:",cal_audit)
            elif el == 'N' or el == 'S':
                #Sensitive mode calibration.
                cal_audit = calibration.curve(area, el, True, True)
                if gui == False:
                    print("cal_audit, N, S:",cal_audit)
            else:
                errormsg = errormsg + 'Element not recognized. Please input /"C/", /"N/", or /"S/"'

            #Calls report function to display report, and saves in sample_calc folder.
            y = cal_audit[0][0]
            conc = 1000000*corr_factor*y/wt
            return_area = "Peak area = " + str(round(area,2)) + " mV*sec"
            return_conc = "Concentration = " + str(round(conc,3)) + " mg " + el + "/kg"
            oneline_results = ', '.join((return_area, return_conc, errormsg))
            results = [return_conc, return_area, el, ret_time, errormsg]
            
            if audit==True:
                #Saves and prints report in command window.
                finalreport = report.generate(filename, conc, corr_factor, wt, area_px, x_axis, y_axis,
                    chart_area, chartarea_px, cal_audit, ret_time, user_ID, sample_ID)
                reportfile_name = os.path.join(filedir_audit, filename_noext + '_report.txt')
                report_file = open(reportfile_name,'w+')
                report_file.write(finalreport)
                report_file.close()
                if gui==False:
                    print(oneline_results)
                    return None;
                else:
                    #return results to gui
                    if save:
                        integrationfilename = integrationfilename_save
                    gui_return = [results, integrationfilename, xyint, errormsg]
                    return gui_return
            else:
                return oneline_results

        else:
            return "Peak area = " + str(round(area,2)) + units
    elif px == True:
        return "Peak area = " + str(area_px) + " pixels"
    else:
        return 0;
