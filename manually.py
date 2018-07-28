import os
import math
import collections
import warnings
from PIL import Image
import pdb
import numpy as np
from tkinter.filedialog import askopenfilename

def integrate(px = False, crop = True, audit = True, custom = False):
    #pdb.set_trace()
    #TODO: define colors
    #      make popup for convenience
    #      output text file of results
    #      close tkinter
    #      calibration
    #      clean up integration marker
    #      highlight clean int marker and peak marker in audit file

    import axis
    filename = askopenfilename()
    #tkinter.destroy()
    
    if custom == False:
        peak_clr = 'black'
        background_clr = 'white'
        integrationmarker_clr = 'red'
    else:
        if crop == True:
            warnings.warn('please submit cropped graph with crop option set to False', Warning)
        chart_area = input('Enter total area of chart:')
        units = input('Enter units of chart area:')
        #print('Indicate the colors used for your chart from the following selection: red, orange, yellow, green, blue, purple, black, white, brown')
        #peak_clr = lower(input('Enter color of curve:'))
        #background_clr = lower(input('Enter color of chart background:'))
        #integrationmarker_clr = lower(input('Enter color of integration marker:'))

    im = Image.open(filename)
    w, h = im.size
    pix_val = list(im.getdata())

    if audit == True:
        folder = filename[:-4] + '_calc'
        os.makedirs(folder,exist_ok = True)
        k = len(filename) - len(filename.split('/')[-1])
        filename_audit = filename[:k] + filename.split('/')[-1][:-4] + '_calc' + '/' + filename.split('/')[-1]
        im.save(filename_audit)
        
    if crop == True:
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
            warnings.warn("Script failed to crop chart. Rerun program on only cropped region with crop setting as False.", Warning)
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

        x_axis = axis.parse(False, w_x, h_x, x_totalpx, x_axis_val)
        print("x axis: " + str(x_axis))
        y_axis = axis.parse(True, w_y, h_y, y_totalpx, y_axis_val)
        print("y axis: " + str(y_axis))
        
        chart_area = int(-1*(np.mean(np.diff(x_axis))*(len(x_axis)-1))*np.mean(np.diff(y_axis))*(len(y_axis)-1))
        
        if audit == True:

            k = len(filename) - len(filename.split('/')[-1])
            croppedfilename = filename[:k] + filename.split('/')[-1][:-4] + '_calc' + '/' + filename.split('/')[-1][:-4] + '_crop.png'
            graph.save(croppedfilename)
            xaxisfilename = filename[:k] + filename.split('/')[-1][:-4] + '_calc' + '/' + filename.split('/')[-1][:-4] + '_xaxis.png'
            xaxis_image.save(xaxisfilename)
            yaxisfilename = filename[:k] + filename.split('/')[-1][:-4] + '_calc' + '/' + filename.split('/')[-1][:-4] + '_yaxis.png'
            yaxis_image.save(yaxisfilename)
    else:
        graph = im
        w2, h2 = w, h
        pix_val2 = pix_val
    peak = [i for i, x in enumerate(pix_val2) if (x[0] == x[1] & x[1] == x[2] & x[2] <= 20)]
    int_marker = [i for i, x in enumerate(pix_val2) if x[0] > 200 and x[1] <= 100 and x[2] <= 100]

    if len(int_marker) <= 10:
        warnings.warn("Integration marker not recognized. Results are artificially high.", Warning)

    int_cols_clean = []
    int_marker_clean = []
    for x in int_marker:
        if x%w2 not in int_cols_clean:
            int_marker_clean.append(x)
            int_cols_clean.append(x%w2)
        
    peak_cols_clean = []
    clean_peak = []
    for x in peak:
        if x%w2 not in peak_cols_clean:
            clean_peak.append(x)
            peak_cols_clean.append(x%w2)
    area_px = sum([(x - y)/w2 for x in int_marker_clean for y in clean_peak if y%w2 == x%w2])
    
    area_crop = (w2 + 1) * (h2 + 1)
    area_crop_mVs = float(chart_area)
    area = area_px * area_crop_mVs/area_crop
    area_px = int(area_px)
    if audit == True:
        im_audit = graph
        x_min, x_max = min([x%w2 for x in int_marker_clean]), max([x%w2 for x in int_marker_clean])
        int_marker_sorted = sorted(int_marker_clean, key = lambda int_marker_clean: int(int_marker_clean)%w2)
        int_marker_y = [math.floor(y/w2) for y in int_marker_sorted]
        integration_values = [(x - y)/w2 for x in int_marker_sorted for y in clean_peak if y%w2 == x%w2]
        areacolor_audit = (5,80,100)
        peakcolor_audit = (10,10,255)
        area_px_audit = 0
        x_fill_audit, y_fill_audit = [], []
        for x in range(0, len(integration_values)-1):
            for y in range(0, int(integration_values[x])):
                x_fill_audit.append(x)
                y_fill_audit.append(y)
                im_audit.putpixel((x+x_min+1,-y+int_marker_y[x]-1),areacolor_audit)
                area_px_audit += 1
        int_fill_coordinates = list(zip(x_fill_audit,y_fill_audit))
        integrationfilename = filename[:k] + filename.split('/')[-1][:-4] + '_calc' + '/' + filename.split('/')[-1][:-4] + '_integration.png'
        im_audit.save(integrationfilename)

    if float(area_px_audit) > float(area_px) * 1.01 or float(area_px_audit) < float(area_px) * 0.99:
        warnings.warn("Shaded area not representative of calculated area!", Warning)
        print('Shaded area under curve = ' + str(area_px_audit) + 'pixels')
        print('Area under curve = ' + str(area_px) + 'pixels')
        
    if px == False:
        if custom == False:
            return "Peak area = " + str(round(area,2)) + " mV*sec"
        else:
            return "Peak area = " + str(round(area,2)) + units
    elif px == True:
        return "Peak area = " + str(area_px) + " pixels"
    else:
        return 0

