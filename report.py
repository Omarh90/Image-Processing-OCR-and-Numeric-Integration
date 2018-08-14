#Written by: Omar Ali <Omarh90@gmail.com>
import datetime
import os
import math
from decimal import Decimal
def generate(filename_dir, conc, corr_factor, wt, area_px, x_axis, y_axis,
    chart_area, chartarea_px, cal_audit, ret_time, user_ID):
            
    """
    Generates report for area under curve in command window,
    and saves in filename_calc folder as .txt file.
    ____________________________________________________________________________
    Parameters:

    * filename: Name (including directory) of png file with screen cap and added integration marker.

    * conc: Calculated sample concentration in mg/kg.

    * corr_factor: Instrument correction factor. Measured per analytical run.

    * wt: Sample weight in mg.

    * area_px: Area underneath curve in pixels.

    * x_axis: Ordered tuple of x-axis values on chart.

    * y_axis: Ordered tuple of y-axis values on chart.

    * chart_area Total area of graph in *mVsec (mV or V?.

    * chartarea_px = Total area of graph in pixels.

    * cal_audit: (list, len=6) exhaustive calibration information:
         coefficents, calibration range, calibration date, and calibration ID for report.

         * cal_audit[0] = (y,x,el) (float, float, str)
         * cal_audit[1] = (a,b,c,d,e) (float)
         * cal_audit[2] = (upper_range, lower_range, n (polynomial order)) (int)
         * cal_audit[3] = cal_date (str)
         * cal_audit[4] = cal_ID (str)
         * cal_audit[5] = errormessage (str)
    ____________________________________________________________________________
    Returns:

    * report: Prints tabulated data summary, displayed in command window and saves txt in filename_calc folder.
    
    """
    #Filename parsing.
    currentdate = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}'
    directory, filename = os.path.split(filename_dir)
    sample_ID = filename.split('.')[:-1][0]

    #Calibration data.
    el = cal_audit[0][2]
    analyte_abs = cal_audit[0][0]
    high_conc = cal_audit[2][0]
    low_conc = cal_audit[2][1]
    order = cal_audit[2][2]
    cal_ID = cal_audit[3][1]
    cal_error = cal_audit[4]

    #Calibration parameters and related report formatting
    x = cal_audit[0][1]
    coeff = ['%.6E' % Decimal(i) for i in cal_audit[1]]
    coeff2 = ['%.4E' % Decimal(abs(i)) for i in cal_audit[1]]
    coeff_spacing = [" "*math.ceil(i/abs(2*i)) for i in cal_audit[1]]
    plus, i = [], 0
    for i in cal_audit[1]:
        if i >= 0:
            plus.append('+')
        elif i < 0:
            plus.append('-')
    if plus[0] == '+':
        plus[0] = ['']

    #Formatting.
    if el == 'C':
        element = 'Carbon'
    elif el == 'N':
        element = 'Nitrogen'
    elif el == 'S':
        element = 'Sulfur'
    if not cal_error:
        errorindicator = ''
    else:
        errorindicator = '#'

    #Unit conversions.
    x_V = x
    x_mV = x*1000
    wt_kg = wt/1000000

    #Format smaller numbers for report.
    corr_factor = '{:.3f}'.format(corr_factor)
    x_V = '{:.3f}'.format(x_V)
    analyte_abs = '{:.4f}'.format(analyte_abs)
    conc = '{:.3f}'.format(conc)

    #Format larger numbers for report.
    x_mV = '{:,.0f}'.format(x_mV)
    chart_area = '{:,}'.format(chart_area)
    chartarea_px = '{:,.0f}'.format(chartarea_px)
    area_px = '{:,.0f}'.format(area_px)
    high_conc = '{:,}'.format(high_conc/1000)
    low_conc = '{:,}'.format(low_conc/1000)
    ret_time = '{:,.2f}'.format(ret_time)

    #Dictionary for report.
    sample_info = {'now': currentdate, 'file': filename, 'ID': sample_ID, 'u': user_ID, 'el1': el, 'el2': element, 'c_ID': cal_ID, \
        'cn': conc, 'wt1': wt, 'wt2': wt_kg, 'f': corr_factor, 'x1': area_px, 'x2': x_mV, 'x3': x_V, 'ax_x': x_axis, \
        'ax_y': y_axis, 'ar1': chart_area, 'ar2': chartarea_px, 'y': analyte_abs, 's': coeff_spacing, '+': plus, 'c_i': coeff, 'c2_i': coeff2, 'rt': ret_time, \
        'n': order, 'h': high_conc, 'l': low_conc, 'errmsg': cal_error, 'err': errorindicator}

    report1 = ' \
    \nManual Integration for {ID} \
    \nGenerated on {now} by {u}\
    \n________________________________________________________________________ \
    \nResults: \
    \n \
    \n\t	Total {el2} = {cn} mg {el1}/kg  {err} \
    \n	\
    \n\t	Area = {x2} mV*sec \
    \n\t	Retention time = {rt} sec \
    \n\t	Correction Factor = {f} \
    \n\t	Total mass {el2} in sample = {y} mg {el1} \
    \n\t	Sample weight = {wt1} mg '.format(**sample_info)

    if cal_error:
        report2 =' \
        \n\t      # Calculation Error  = {errmsg}'.format(**sample_info)
    else:
        report2 = '\n'

    report3 = ' \
    \n________________________________________________________________________ \
    \nCalibration: \
    \n \
    \nCNS instrument calibration equation for {el2} in '.format(**sample_info)

    if el == 'C':
        report4 = '"Insensitive" analysis mode. Coefficient ID: {c_ID}'.format(**sample_info)

    elif el == 'N' or el == 'S':
        report4 = 'sensitive analysis mode. Coefficient ID: {c_ID}'.format(**sample_info)

    if order == 4:
        report5 = ' \
            \n \
            \n\t         y = a + b*x + c*x^2 + d*x^3 + e*x^4, \
            \n \
            \n for  x < {h} and x > {l}, where x={x3} V*sec is the area count underneath the curve, \
            \n y is amount of {el2} in sample, y={y} mg {el1}, and: \
            \n \
            \n\t         a = {s[0]}{c_i[0]}, \
            \n\t         b = {s[1]}{c_i[1]}, \
            \n\t         c = {s[2]}{c_i[2]}, \
            \n\t         d = {s[3]}{c_i[3]}, \
            \n\t         e = {s[4]}{c_i[4]}'.format(**sample_info)
    elif order == 3:
        report5 = ' \
            \n \
            \n\t {y} mg {el1} = a + b*x + c*x^2 + d*x^3, \
            \n \
            \n for  x < {h} and x > {l},where x={x3} is the area count underneath the curve in V*sec, and: \
            \n\t         a = {s[0]}{c_i[0]}, \
            \n\t         b = {s[1]}{c_i[1]}, \
            \n\t         c = {s[2]}{c_i[2]}, \
            \n\t         d = {s[3]}{c_i[3]},'.format(**sample_info)

    report6 = ' \
    \n________________________________________________________________________ \
    \nCalculations: \
    \n \
    \n\t	{cn} mg {el1}/kg= {y} mg {el1} * {f}/{wt2} kg \
    \n\t	{x2} mV*sec = {ar1} mV*sec * {x1} pix/{ar2} pix \
    \n\t	{x3} V*sec = {x2} mV*sec/1000 \
    \n\t        {y} mg {el1} = {+[0]}{c2_i[0]} {+[1]} {c2_i[1]}*{x3} {+[2]} {c2_i[2]}*{x3}^2 \
    \n\t            {+[3]} {c2_i[3]}*{x3}^3 {+[4]} {c2_i[4]}*{x3}^4 \
    \n \
    \n________________________________________________________________________ \
    \nGraph Info: \
    \n \
    \n\t        File: {file} \
    \n\t	x-axis (sec) = {ax_x} \
    \n\t	y-axis (mV) = {ax_y} \
    \n\t        Total chart area = {ar1} mV*sec \
    \n'.format(**sample_info)

    report = report1 + report2 + report3 + report4 + report5 + report6
    return report;

