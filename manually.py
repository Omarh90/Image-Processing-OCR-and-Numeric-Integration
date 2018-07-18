import os
import math
import collections
import warnings
from PIL import Image

def integrate(px = False):

    #wd: C:\\Program Files\\Python37'
    #os.chdir("C:\Documents and Settings\Chemist\Desktop\Manual Integration Files")
    filename = input('Enter filename, including extension and directory:')
    chart_area = input('Enter total area of chart (in mV *s):')
    im = Image.open(filename)
    w, h = im.size
    pix_val = list(im.getdata())
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
    w2, h2 = graph.size
    pix_val2 = list(graph.getdata())
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

    if px == False:
        return "Peak area = " + str(round(area,2)) + " mV*sec"
    elif px == True:
        return "Peak area = " + str(area_px) + " pixels"
    else:
        return 0

    #TODO: Numeric pixel library
