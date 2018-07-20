import os
import math
import collections
import warnings
from PIL import Image
import pdb

def integrate(px = False, crop = True, audit = False, custom = False):

    #wd: C:\\Program Files\\Python37
    #colors:

    
    
    if custom == True or audit == True:
        directory = input('Enter directory (folder) where file is located:')
        os.chdir(directory)
    else:
        os.chdir("C:\Documents and Settings\Chemist\Desktop\Manual Integration Files")
    filename = input('Enter filename, including extension and directory:')
    
    if custom == False:
        chart_area = input('Enter total area of chart (in mV *s):')
        peak_clr = 'black'
        background_clr = 'white'
        integrationmarker_clr = 'red'
    else:
        if crop == True:
            warnings.warn('please submit cropped graph with crop option set to False', Warning)
        chart_area = input('Enter total area of chart:')
        units = input('Enter units of chart area:')
        peak_clr
        background_clr
        integrationmarker_clr
            
        
    if audit == True:
        folder = directory + '\\' + filename[:-4] + '_calc'
        os.makedirs(folder,exist_ok = True)
        
    im = Image.open(filename)
    w, h = im.size
    pix_val = list(im.getdata())
    
    if crop == True:
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
            warnings.warn("Script failed to crop chart. Rerun program with only cropped region with crop setting as False.", Warning)
        w2, h2 = graph.size
        pix_val2 = list(graph.getdata())
        if audit == True:
            croppedfilename = folder + '\\' + filename[:-4] + '_crop.png'
            graph.save(croppedfilename)
    else:
        graph = im
        w2, h2 = w, h
        pix_val2 = pix_val
    peak = [i for i, x in enumerate(pix_val2) if (x[0] == x[1] & x[1] == x[2] & x[2] <= 20)]
    int_marker = [i for i, x in enumerate(pix_val2) if x[0] > 200 and x[1] <= 100 and x[2] <= 100]

    if len(int_marker) <= 10:
        warnings.warn("Integration marker not recognized. Results are artificially high.", Warning)
    peak_cols_clean = []
    clean_peak = []
    for x in peak:
        if x%w2 not in peak_cols_clean:
            clean_peak.append(x)
            peak_cols_clean.append(x%w2)
    area_px = sum([(x - y)/w2 for x in int_marker for y in clean_peak if y%w2 == x%w2])
    
    area_crop = (w2 + 1) * (h2 + 1)
    area_crop_mVs = float(chart_area)  #input product of length and width of graph in terms of seconds and mV
    area = area_px * area_crop_mVs/area_crop
    area_px = int(area_px)
    if audit == True:
        im_audit = graph
        x_min, x_max = min([x%w2 for x in int_marker]), max([x%w2 for x in int_marker])
        int_marker_sorted = sorted(int_marker, key = lambda int_marker: int(int_marker)%w2)
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
        croppedfilename = folder+ '\\' + filename[:-4] + '_integration.png'
        im_audit.save(croppedfilename)
    if float(area_px_audit) > float(area_px) * 1.01 or float(area_px_audit) < float(area_px) * 0.99:
        warnings.warn("Shaded area not representative of calculated area!", Warning)
        print('Area under curve = ' + str(area_px_audit) + 'pixels')
    if px == False:
        if custom == False:
            return "Peak area = " + str(round(area,2)) + " mV*sec"
        else:
            return "Peak area = " + str(round(area,2)) + units
    elif px == True:
        return "Peak area = " + str(area_px) + " pixels"
    else:
        return 0

    #TODO: Numeric pixel library
