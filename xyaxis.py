#Written by: Omar Ali <Omarh90@gmail.com>
import os
import math
import collections
import warnings
from PIL import Image
import numpy as np
import pdb

"""
Reads x- and y-values on axes from screengrab of graph, returning tuple list in ascending order of x or y-values on axes. 
"""

def parse(y,w3,h3,total_pixels, axis_ls):

    if y:
        x = False
    else:
        x = True

    i, j = 0, 0
    digit = []
    digitchk1, digitchk2 = 1,1
    minus = False
    w_chr,h_chr = 5,8
    space = 3
    axis_numbers = []
    axis_numbers2 = []

    while i <= total_pixels:

        if axis_ls[i][0] == axis_ls[i][1] & axis_ls[i][0] == axis_ls[i][2] & axis_ls[i][0] < 50:

            if i + 8*w3 + 5 < total_pixels:

                  if axis_ls[i+w3][0] == axis_ls[i+ w3][1] & axis_ls[i+w3][0] == axis_ls[i+w3][2] & axis_ls[i+w3][0] < 50:

                      if axis_ls[i+w3-1][0] == axis_ls[i+ w3 -1][1] & axis_ls[i+w3-1][0] == axis_ls[i+w3-1][2] & axis_ls[i+w3 -1][0] < 50:

                          if (axis_ls[i+w3-2][0] == axis_ls[i+w3-2][1] & axis_ls[i+w3-2][0] == axis_ls[i+w3 -2][2] & axis_ls[i+w3-2][0] < 50) \
                          & (axis_ls[i+3*w3][0] == axis_ls[i+3*w3][1] & axis_ls[i+3*w3][0] == axis_ls[i+3*w3][2] & axis_ls[i+3*w3][0] < 50) \
                          & (axis_ls[i+4*w3][0] == axis_ls[i+4*w3][1] & axis_ls[i+4*w3][0] == axis_ls[i+4*w3][2] & axis_ls[i+4*w3][0] < 50) \
                          & (axis_ls[i+5*w3][0] == axis_ls[i+5*w3][1] & axis_ls[i+5*w3][0] == axis_ls[i+5*w3][2] & axis_ls[i+5*w3][0] < 50) \
                          & (axis_ls[i+6*w3][0] == axis_ls[i+6*w3][1] & axis_ls[i+6*w3][0] == axis_ls[i+6*w3][2] & axis_ls[i+6*w3][0] < 50) \
                          & (axis_ls[i+7*w3][0] == axis_ls[i+7*w3][1] & axis_ls[i+7*w3][0] == axis_ls[i+7*w3][2] & axis_ls[i+7*w3][0] < 50) \
                          & (axis_ls[i+8*w3][0] == axis_ls[i+8*w3][1] & axis_ls[i+8*w3][0] == axis_ls[i+8*w3][2] & axis_ls[i+8*w3][0] < 50) \
                          & (axis_ls[i+8*w3-2][0] == axis_ls[i+8*w3-2][1] & axis_ls[i+8*w3-2][0] == axis_ls[i+8*w3-2][2] & axis_ls[i+8*w3-2][0] < 50) \
                          & (axis_ls[i+8*w3-1][0] == axis_ls[i+8*w3-1][1] & axis_ls[i+8*w3-1][0] == axis_ls[i+8*w3-1][2] & axis_ls[i+8*w3-1][0] < 50) \
                          & (axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][1] & axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][2] & axis_ls[i+8*w3+1][0] < 50) \
                          & (axis_ls[i+8*w3+2][0] == axis_ls[i+8*w3+2][1] & axis_ls[i+8*w3+2][0] == axis_ls[i+8*w3+2][2] & axis_ls[i+8*w3+2][0] < 50):

                            #1
                            digit = 1
                            digitchk1 *= -1
                            i += 3
                            
                          if (axis_ls[i+2*w3][0] == axis_ls[i+2*w3][1] & axis_ls[i+2*w3][0] == axis_ls[i+2*w3][2] & axis_ls[i+2*w3][0] < 50) \
                          & (axis_ls[i+2*w3-1][0] == axis_ls[i+2*w3-1][1] & axis_ls[i+2*w3-1][0] == axis_ls[i+2*w3-1][2] & axis_ls[i+2*w3-1][0] < 50) \
                          & (axis_ls[i+3*w3][0] == axis_ls[i+3*w3][1] & axis_ls[i+3*w3][0] == axis_ls[i+3*w3][2] & axis_ls[i+3*w3][0] < 50) \
                          & (axis_ls[i+3*w3-2][0] == axis_ls[i+3*w3-2][1] & axis_ls[i+3*w3-2][0] == axis_ls[i+3*w3-2][2] & axis_ls[i+3*w3-2][0] < 50) \
                          & (axis_ls[i+4*w3][0] == axis_ls[i+4*w3][1] & axis_ls[i+4*w3][0] == axis_ls[i+4*w3][2] & axis_ls[i+4*w3][0] < 50) \
                          & (axis_ls[i+4*w3-2][0] == axis_ls[i+4*w3-2][1] & axis_ls[i+4*w3-2][0] == axis_ls[i+4*w3-2][2] & axis_ls[i+4*w3-2][0] < 50) \
                          & (axis_ls[i+5*w3][0] == axis_ls[i+5*w3][1] & axis_ls[i+5*w3][0] == axis_ls[i+5*w3][2] & axis_ls[i+5*w3][0] < 50) \
                          & (axis_ls[i+5*w3-3][0] == axis_ls[i+5*w3-3][1] & axis_ls[i+5*w3-3][0] == axis_ls[i+5*w3-3][2] & axis_ls[i+5*w3-3][0] < 50) \
                          & (axis_ls[i+6*w3][0] == axis_ls[i+6*w3][1] & axis_ls[i+6*w3][0] == axis_ls[i+6*w3][2] & axis_ls[i+6*w3][0] < 50) \
                          & (axis_ls[i+6*w3-3][0] == axis_ls[i+6*w3-3][1] & axis_ls[i+6*w3-3][0] == axis_ls[i+6*w3-3][2] & axis_ls[i+6*w3-3][0] < 50) \
                          & (axis_ls[i+6*w3-2][0] == axis_ls[i+6*w3-2][1] & axis_ls[i+6*w3-2][0] == axis_ls[i+6*w3-2][2] & axis_ls[i+6*w3-2][0] < 50) \
                          & (axis_ls[i+6*w3-1][0] == axis_ls[i+6*w3-1][1] & axis_ls[i+6*w3-1][0] == axis_ls[i+6*w3-1][2] & axis_ls[i+6*w3-1][0] < 50) \
                          & (axis_ls[i+6*w3+1][0] == axis_ls[i+6*w3+1][1] & axis_ls[i+6*w3+1][0] == axis_ls[i+6*w3+1][2] & axis_ls[i+6*w3+1][0] < 50) \
                          & (axis_ls[i+7*w3][0] == axis_ls[i+7*w3][1] & axis_ls[i+7*w3][0] == axis_ls[i+7*w3][2] & axis_ls[i+7*w3][0] < 50) \
                          & (axis_ls[i+8*w3][0] == axis_ls[i+8*w3][1] & axis_ls[i+8*w3][0] == axis_ls[i+8*w3][2] & axis_ls[i+8*w3][0] < 50) \
                          & (axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][1] & axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][2] & axis_ls[i+8*w3+1][0] < 50) \
                          & (axis_ls[i+8*w3-1][0] == axis_ls[i+8*w3-1][1] & axis_ls[i+8*w3-1][0] == axis_ls[i+8*w3-1][2] & axis_ls[i+8*w3-1][0] < 50):
                                   #4
                            digit = 4
                            digitchk1 *= -1
                            i += 2

                  if axis_ls[i+1][0] == axis_ls[i+1][1] & axis_ls[i+1][0] == axis_ls[i+1][2] & axis_ls[i+1][0] < 50:
                      
                      if (axis_ls[i+w3-1][0] == axis_ls[i+w3-1][1] & axis_ls[i+w3-1][0] == axis_ls[i+w3-1][2] & axis_ls[i+w3-1][0] < 50) \
                      & (axis_ls[i+2*w3-2][0] == axis_ls[i+2*w3-2][1] & axis_ls[i+2*w3-2][0] == axis_ls[i+2*w3-2][2] & axis_ls[i+2*w3-2][0] < 50) \
                      & (axis_ls[i+3*w3-2][0] == axis_ls[i+3*w3-2][1] & axis_ls[i+3*w3-2][0] == axis_ls[i+3*w3-2][2] & axis_ls[i+3*w3-2][0] < 50) \
                      & (axis_ls[i+4*w3-2][0] == axis_ls[i+4*w3-2][1] & axis_ls[i+4*w3-2][0] == axis_ls[i+4*w3-2][2] & axis_ls[i+4*w3-2][0] < 50) \
                      & (axis_ls[i+4*w3-1][0] == axis_ls[i+4*w3-1][1] & axis_ls[i+4*w3-1][0] == axis_ls[i+4*w3-1][2] & axis_ls[i+4*w3-1][0] < 50) \
                      & (axis_ls[i+4*w3][0] == axis_ls[i+4*w3][1] & axis_ls[i+4*w3][0] == axis_ls[i+4*w3][2] & axis_ls[i+4*w3][0] < 50) \
                      & (axis_ls[i+4*w3+1][0] == axis_ls[i+4*w3+1][1] & axis_ls[i+4*w3+1][0] == axis_ls[i+4*w3+1][2] & axis_ls[i+4*w3+1][0] < 50) \
                      & (axis_ls[i+5*w3-2][0] == axis_ls[i+5*w3-2][1] & axis_ls[i+5*w3-2][0] == axis_ls[i+5*w3-2][2] & axis_ls[i+5*w3-2][0] < 50) \
                      & (axis_ls[i+5*w3+2][0] == axis_ls[i+5*w3+2][1] & axis_ls[i+5*w3+2][0] == axis_ls[i+5*w3+2][2] & axis_ls[i+5*w3+2][0] < 50) \
                      & (axis_ls[i+6*w3-2][0] == axis_ls[i+6*w3-2][1] & axis_ls[i+6*w3-2][0] == axis_ls[i+6*w3-2][2] & axis_ls[i+6*w3-2][0] < 50) \
                      & (axis_ls[i+6*w3+2][0] == axis_ls[i+6*w3+2][1] & axis_ls[i+6*w3+2][0] == axis_ls[i+6*w3+2][2] & axis_ls[i+6*w3+2][0] < 50) \
                      & (axis_ls[i+7*w3-2][0] == axis_ls[i+7*w3-2][1] & axis_ls[i+7*w3-2][0] == axis_ls[i+7*w3-2][2] & axis_ls[i+7*w3-2][0] < 50) \
                      & (axis_ls[i+7*w3+2][0] == axis_ls[i+7*w3+2][1] & axis_ls[i+7*w3+2][0] == axis_ls[i+7*w3+2][2] & axis_ls[i+7*w3+2][0] < 50) \
                      & (axis_ls[i+8*w3-1][0] == axis_ls[i+8*w3-1][1] & axis_ls[i+8*w3-1][0] == axis_ls[i+8*w3-1][2] & axis_ls[i+8*w3-1][0] < 50) \
                      & (axis_ls[i+8*w3][0] == axis_ls[i+8*w3][1] & axis_ls[i+8*w3][0] == axis_ls[i+8*w3][2] & axis_ls[i+8*w3][0] < 50) \
                      & (axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][1] & axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][2] & axis_ls[i+8*w3+1][0] < 50):
                          #6
                          digit = 6
                          digitchk1 *= -1
                          i += 3

                      if axis_ls[i+2][0] == axis_ls[i+2][1] & axis_ls[i+2][0] == axis_ls[i+2][2] & axis_ls[i+2][0] < 50:

                          if (axis_ls[i+3][0] == axis_ls[i+3][1] & axis_ls[i+3][0] == axis_ls[i+3][2] & axis_ls[i+3][0] < 50) \
                          & (axis_ls[i+4][0] == axis_ls[i+4][1] & axis_ls[i+4][0] == axis_ls[i+4][2] & axis_ls[i+4][0] < 50) \
                          & (axis_ls[i+w3][0] == axis_ls[i+w3][1] & axis_ls[i+w3][0] == axis_ls[i+w3][2] & axis_ls[i+w3][0] < 50):

                               if (axis_ls[i+w3+4][0] == axis_ls[i+w3+4][1] & axis_ls[i+w3+4][0] == axis_ls[i+w3+4][2] & axis_ls[i+w3+4][0] < 50) \
                               & (axis_ls[i+2*w3+4][0] == axis_ls[i+2*w3+4][1] & axis_ls[i+2*w3+4][0] == axis_ls[i+2*w3+4][2] & axis_ls[i+2*w3+4][0] < 50) \
                               & (axis_ls[i+3*w3+3][0] == axis_ls[i+3*w3+3][1] & axis_ls[i+3*w3+3][0] == axis_ls[i+3*w3+3][2] & axis_ls[i+3*w3+3][0] < 50) \
                               & (axis_ls[i+4*w3+3][0] == axis_ls[i+4*w3+3][1] & axis_ls[i+4*w3+3][0] == axis_ls[i+4*w3+3][2] & axis_ls[i+4*w3+3][0] < 50) \
                               & (axis_ls[i+5*w3+2][0] == axis_ls[i+5*w3+2][1] & axis_ls[i+5*w3+2][0] == axis_ls[i+5*w3+2][2] & axis_ls[i+5*w3+2][0] < 50) \
                               & (axis_ls[i+6*w3+2][0] == axis_ls[i+6*w3+2][1] & axis_ls[i+6*w3+2][0] == axis_ls[i+6*w3+2][2] & axis_ls[i+6*w3+2][0] < 50) \
                               & (axis_ls[i+7*w3+1][0] == axis_ls[i+7*w3+1][1] & axis_ls[i+7*w3+1][0] == axis_ls[i+7*w3+1][2] & axis_ls[i+7*w3+1][0] < 50) \
                               & (axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][1] & axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][2] & axis_ls[i+8*w3+1][0] < 50):
                                   #7
                                   digit = 7
                                   digitchk1 *= -1
                                   i += 5

                               if (axis_ls[i+2*w3][0] == axis_ls[i+2*w3][1] & axis_ls[i+2*w3][0] == axis_ls[i+2*w3][2] & axis_ls[i+2*w3][0] < 50) \
                               & (axis_ls[i+3*w3][0] == axis_ls[i+3*w3][1] & axis_ls[i+3*w3][0] == axis_ls[i+3*w3][2] & axis_ls[i+3*w3][0] < 50) \
                               & (axis_ls[i+4*w3][0] == axis_ls[i+4*w3][1] & axis_ls[i+4*w3][0] == axis_ls[i+4*w3][2] & axis_ls[i+4*w3][0] < 50) \
                               & (axis_ls[i+4*w3][0] == axis_ls[i+4*w3][1] & axis_ls[i+4*w3][0] == axis_ls[i+4*w3][2] & axis_ls[i+4*w3][0] < 50) \
                               & (axis_ls[i+4*w3+1][0] == axis_ls[i+4*w3+1][1] & axis_ls[i+4*w3+1][0] == axis_ls[i+4*w3+1][2] & axis_ls[i+4*w3+1][0] < 50) \
                               & (axis_ls[i+4*w3+2][0] == axis_ls[i+4*w3+2][1] & axis_ls[i+4*w3+2][0] == axis_ls[i+4*w3+2][2] & axis_ls[i+4*w3+2][0] < 50) \
                               & (axis_ls[i+5*w3+4][0] == axis_ls[i+5*w3+4][1] & axis_ls[i+5*w3+4][0] == axis_ls[i+5*w3+4][2] & axis_ls[i+5*w3+4][0] < 50) \
                               & (axis_ls[i+6*w3+4][0] == axis_ls[i+6*w3+4][1] & axis_ls[i+6*w3+4][0] == axis_ls[i+6*w3+4][2] & axis_ls[i+6*w3+4][0] < 50) \
                               & (axis_ls[i+7*w3+4][0] == axis_ls[i+7*w3+4][1] & axis_ls[i+7*w3+4][0] == axis_ls[i+7*w3+4][2] & axis_ls[i+7*w3+4][0] < 50) \
                               & (axis_ls[i+7*w3][0] == axis_ls[i+7*w3][1] & axis_ls[i+7*w3][0] == axis_ls[i+7*w3][2] & axis_ls[i+7*w3][0] < 50) \
                               & (axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][1] & axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][2] & axis_ls[i+8*w3+1][0] < 50) \
                               & (axis_ls[i+8*w3+2][0] == axis_ls[i+8*w3+2][1] & axis_ls[i+8*w3+2][0] == axis_ls[i+8*w3+2][2] & axis_ls[i+8*w3+2][0] < 50) \
                               & (axis_ls[i+8*w3+3][0] == axis_ls[i+8*w3+3][1] & axis_ls[i+8*w3+3][0] == axis_ls[i+8*w3+3][2] & axis_ls[i+8*w3+3][0] < 50):
                                   #5
                                   digit = 5
                                   digitchk1 *= -1
                                   i += 5

                    #2,3,0,8,9
                          if (axis_ls[i+w3-1][0] == axis_ls[i+w3-1][1] & axis_ls[i+w3-1][0] == axis_ls[i+w3-1][2] & axis_ls[i+w3-1][0] < 50) \
                          & (axis_ls[i+w3+3][0] == axis_ls[i+w3+3][1] & axis_ls[i+w3+3][0] == axis_ls[i+w3+3][2] & axis_ls[i+w3+3][0] < 50):

                              if (axis_ls[i+2*w3-1][0] == axis_ls[i+2*w3-1][1] & axis_ls[i+2*w3-1][0] == axis_ls[i+2*w3-1][2] & axis_ls[i+2*w3-1][0] < 50) \
                              &(axis_ls[i+2*w3+3][0] == axis_ls[i+2*w3+3][1] & axis_ls[i+2*w3+3][0] == axis_ls[i+2*w3+3][2] & axis_ls[i+2*w3+3][0] < 50):

                                  if (axis_ls[i+3*w3-1][0] == axis_ls[i+3*w3-1][1] & axis_ls[i+3*w3-1][0] == axis_ls[i+3*w3-1][2] & axis_ls[i+3*w3-1][0] < 50) \
                                  & (axis_ls[i+3*w3+3][0] == axis_ls[i+3*w3+3][1] & axis_ls[i+3*w3+3][0] == axis_ls[i+3*w3+3][2] & axis_ls[i+3*w3+3][0] < 50):

                                      if (axis_ls[i+4*w3-1][0] == axis_ls[i+4*w3-1][1] & axis_ls[i+4*w3-1][0] == axis_ls[i+4*w3-1][2] & axis_ls[i+4*w3-1][0] < 50) \
                                      & (axis_ls[i+4*w3+3][0] == axis_ls[i+4*w3+3][1] & axis_ls[i+4*w3+3][0] == axis_ls[i+4*w3+3][2] & axis_ls[i+4*w3+3][0] < 50) \
                                      & (axis_ls[i+5*w3-1][0] == axis_ls[i+5*w3-1][1] & axis_ls[i+5*w3-1][0] == axis_ls[i+5*w3-1][2] & axis_ls[i+5*w3-1][0] < 50) \
                                      & (axis_ls[i+5*w3+3][0] == axis_ls[i+5*w3+3][1] & axis_ls[i+5*w3+3][0] == axis_ls[i+5*w3+3][2] & axis_ls[i+5*w3+3][0] < 50) \
                                      & (axis_ls[i+6*w3-1][0] == axis_ls[i+6*w3-1][1] & axis_ls[i+6*w3-1][0] == axis_ls[i+6*w3-1][2] & axis_ls[i+6*w3-1][0] < 50) \
                                      & (axis_ls[i+6*w3+3][0] == axis_ls[i+6*w3+3][1] & axis_ls[i+6*w3+3][0] == axis_ls[i+6*w3+3][2] & axis_ls[i+6*w3+3][0] < 50) \
                                      & (axis_ls[i+7*w3-1][0] == axis_ls[i+7*w3-1][1] & axis_ls[i+7*w3-1][0] == axis_ls[i+7*w3-1][2] & axis_ls[i+7*w3-1][0] < 50) \
                                      & (axis_ls[i+7*w3+3][0] == axis_ls[i+7*w3+3][1] & axis_ls[i+7*w3+3][0] == axis_ls[i+7*w3+3][2] & axis_ls[i+7*w3+3][0] < 50) \
                                      & (axis_ls[i+8*w3][0] == axis_ls[i+8*w3][1] & axis_ls[i+8*w3][0] == axis_ls[i+8*w3][2] & axis_ls[i+8*w3][0] < 50) \
                                      & (axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][1] & axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][2] & axis_ls[i+8*w3+1][0] < 50) \
                                      & (axis_ls[i+8*w3+2][0] == axis_ls[i+8*w3+2][1] & axis_ls[i+8*w3+2][0] == axis_ls[i+8*w3+2][2] & axis_ls[i+8*w3+2][0] < 50):
                                          #0
                                          digit = 0
                                          digitchk1 *= -1
                                          i += 4
                                          
                                      if (axis_ls[i+4*w3][0] == axis_ls[i+4*w3][1] & axis_ls[i+4*w3][0] == axis_ls[i+4*w3][2] & axis_ls[i+4*w3][0] < 50) \
                                      & (axis_ls[i+4*w3+1][0] == axis_ls[i+4*w3+1][1] & axis_ls[i+4*w3+1][0] == axis_ls[i+4*w3+1][2] & axis_ls[i+4*w3+1][0] < 50) \
                                      & (axis_ls[i+4*w3+2][0] == axis_ls[i+4*w3+2][1] & axis_ls[i+4*w3+2][0] == axis_ls[i+4*w3+2][2] & axis_ls[i+4*w3+2][0] < 50) \
                                      & (axis_ls[i+5*w3+3][0] == axis_ls[i+5*w3+3][1] & axis_ls[i+5*w3+3][0] == axis_ls[i+5*w3+3][2] & axis_ls[i+5*w3+3][0] < 50) \
                                      & (axis_ls[i+6*w3+3][0] == axis_ls[i+6*w3+3][1] & axis_ls[i+6*w3+3][0] == axis_ls[i+6*w3+3][2] & axis_ls[i+6*w3+3][0] < 50) \
                                      & (axis_ls[i+7*w3+2][0] == axis_ls[i+7*w3+2][1] & axis_ls[i+7*w3+2][0] == axis_ls[i+7*w3+2][2] & axis_ls[i+7*w3+2][0] < 50) \
                                      & (axis_ls[i+8*w3][0] == axis_ls[i+8*w3][1] & axis_ls[i+8*w3][0] == axis_ls[i+8*w3][2] & axis_ls[i+8*w3][0] < 50) \
                                      & (axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][1] & axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][2] & axis_ls[i+8*w3+1][0] < 50):
                                          #9
                                          digit = 9
                                          digitchk1 *= -1
                                          i += 4
                                          
                                      if (axis_ls[i+5*w3-1][0] == axis_ls[i+5*w3-1][1] & axis_ls[i+5*w3-1][0] == axis_ls[i+5*w3-1][2] & axis_ls[i+5*w3-1][0] < 50) \
                                      & (axis_ls[i+5*w3+3][0] == axis_ls[i+5*w3+3][1] & axis_ls[i+5*w3+3][0] == axis_ls[i+5*w3+3][2] & axis_ls[i+5*w3+3][0] < 50) \
                                      & (axis_ls[i+6*w3-1][0] == axis_ls[i+6*w3-1][1] & axis_ls[i+6*w3-1][0] == axis_ls[i+6*w3-1][2] & axis_ls[i+6*w3-1][0] < 50) \
                                      & (axis_ls[i+6*w3+3][0] == axis_ls[i+6*w3+3][1] & axis_ls[i+6*w3+3][0] == axis_ls[i+6*w3+3][2] & axis_ls[i+6*w3+3][0] < 50) \
                                      & (axis_ls[i+7*w3-1][0] == axis_ls[i+7*w3-1][1] & axis_ls[i+7*w3-1][0] == axis_ls[i+7*w3-1][2] & axis_ls[i+7*w3-1][0] < 50) \
                                      & (axis_ls[i+7*w3+3][0] == axis_ls[i+7*w3+3][1] & axis_ls[i+7*w3+3][0] == axis_ls[i+7*w3+3][2] & axis_ls[i+7*w3+3][0] < 50) \
                                      & (axis_ls[i+8*w3][0] == axis_ls[i+8*w3][1] & axis_ls[i+8*w3][0] == axis_ls[i+8*w3][2] & axis_ls[i+8*w3][0] < 50) \
                                      & (axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][1] & axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][2] & axis_ls[i+8*w3+1][0] < 50) \
                                      & (axis_ls[i+8*w3+2][0] == axis_ls[i+8*w3+2][1] & axis_ls[i+8*w3+2][0] == axis_ls[i+8*w3+2][2] & axis_ls[i+8*w3+2][0] < 50):
                                          #8
                                          digit = 8
                                          digitchk1 *= -1
                                          i += 4

                              if (axis_ls[i+2*w3+3][0] == axis_ls[i+2*w3+3][1] & axis_ls[i+2*w3+3][0] == axis_ls[i+2*w3+3][2] & axis_ls[i+2*w3+3][0] < 50) \
                              & (axis_ls[i+3*w3+3][0] == axis_ls[i+3*w3+3][1] & axis_ls[i+3*w3+3][0] == axis_ls[i+3*w3+3][2] & axis_ls[i+3*w3+3][0] < 50) \
                              & (axis_ls[i+4*w3+1][0] == axis_ls[i+4*w3+1][1] & axis_ls[i+4*w3+1][0] == axis_ls[i+4*w3+1][2] & axis_ls[i+4*w3+1][0] < 50) \
                              & (axis_ls[i+4*w3+2][0] == axis_ls[i+4*w3+2][1] & axis_ls[i+4*w3+2][0] == axis_ls[i+4*w3+2][2] & axis_ls[i+4*w3+2][0] < 50) \
                              & (axis_ls[i+5*w3+3][0] == axis_ls[i+5*w3+3][1] & axis_ls[i+5*w3+3][0] == axis_ls[i+5*w3+3][2] & axis_ls[i+5*w3+3][0] < 50) \
                              & (axis_ls[i+6*w3+3][0] == axis_ls[i+6*w3+3][1] & axis_ls[i+6*w3+3][0] == axis_ls[i+6*w3+3][2] & axis_ls[i+6*w3+3][0] < 50) \
                              & (axis_ls[i+7*w3+3][0] == axis_ls[i+7*w3+3][1] & axis_ls[i+7*w3+3][0] == axis_ls[i+7*w3+3][2] & axis_ls[i+7*w3+3][0] < 50) \
                              & (axis_ls[i+7*w3-1][0] == axis_ls[i+7*w3-1][1] & axis_ls[i+7*w3-1][0] == axis_ls[i+7*w3-1][2] & axis_ls[i+7*w3-1][0] < 50) \
                              & (axis_ls[i+8*w3][0] == axis_ls[i+8*w3][1] & axis_ls[i+8*w3][0] == axis_ls[i+8*w3][2] & axis_ls[i+8*w3][0] < 50) \
                              & (axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][1] & axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][2] & axis_ls[i+8*w3+1][0] < 50) \
                              & (axis_ls[i+8*w3+2][0] == axis_ls[i+8*w3+2][1] & axis_ls[i+8*w3+2][0] == axis_ls[i+8*w3+2][2] & axis_ls[i+8*w3+2][0] < 50):

                                  #3
                                  digit = 3
                                  digitchk1 *= -1
                                  i += 4

                              if (axis_ls[i+2*w3+3][0] == axis_ls[i+2*w3+3][1] & axis_ls[i+2*w3+3][0] == axis_ls[i+2*w3+3][2] & axis_ls[i+2*w3+3][0] < 50) \
                              & (axis_ls[i+3*w3+3][0] == axis_ls[i+3*w3+3][1] & axis_ls[i+3*w3+3][0] == axis_ls[i+3*w3+3][2] & axis_ls[i+3*w3+3][0] < 50) \
                              & (axis_ls[i+4*w3+2][0] == axis_ls[i+4*w3+2][1] & axis_ls[i+4*w3+2][0] == axis_ls[i+4*w3+2][2] & axis_ls[i+4*w3+2][0] < 50) \
                              & (axis_ls[i+5*w3+1][0] == axis_ls[i+5*w3+1][1] & axis_ls[i+5*w3+1][0] == axis_ls[i+5*w3+1][2] & axis_ls[i+5*w3+1][0] < 50) \
                              & (axis_ls[i+6*w3][0] == axis_ls[i+6*w3][1] & axis_ls[i+6*w3][0] == axis_ls[i+6*w3][2] & axis_ls[i+6*w3][0] < 50) \
                              & (axis_ls[i+7*w3-1][0] == axis_ls[i+7*w3-1][1] & axis_ls[i+7*w3-1][0] == axis_ls[i+7*w3-1][2] & axis_ls[i+7*w3-1][0] < 50) \
                              & (axis_ls[i+8*w3-1][0] == axis_ls[i+8*w3-1][1] & axis_ls[i+8*w3-1][0] == axis_ls[i+8*w3-1][2] & axis_ls[i+8*w3-1][0] < 50) \
                              & (axis_ls[i+8*w3][0] == axis_ls[i+8*w3][1] & axis_ls[i+8*w3][0] == axis_ls[i+8*w3][2] & axis_ls[i+8*w3][0] < 50) \
                              & (axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][1] & axis_ls[i+8*w3+1][0] == axis_ls[i+8*w3+1][2] & axis_ls[i+8*w3+1][0] < 50) \
                              & (axis_ls[i+8*w3+2][0] == axis_ls[i+8*w3+2][1] & axis_ls[i+8*w3+2][0] == axis_ls[i+8*w3+2][2] & axis_ls[i+8*w3+2][0] < 50) \
                              & (axis_ls[i+8*w3+3][0] == axis_ls[i+8*w3+3][1] & axis_ls[i+8*w3+3][0] == axis_ls[i+8*w3+3][2] & axis_ls[i+8*w3+3][0] < 50):
                                  #2
                                  digit = 2
                                  digitchk1 *= -1
                                  i += 4

        if digitchk1 == -1*digitchk2:
            if i + 5*w3-8 < total_pixels:
                digitchk2 =  digitchk1
                if len(axis_numbers) == j:
                    axis_numbers.append(digit)

                    if ((axis_ls[i-10][0] >= 50 or axis_ls[i-10][1] >= 50 or axis_ls[i-10][2] >= 50) \
                    or ((axis_ls[i-10][1] > axis_ls[i-10][0] + 5 or axis_ls[i-10][1] < axis_ls[i-10][0] - 5) \
                    or (axis_ls[i-10][2] > axis_ls[i-10][0] + 5 or axis_ls[i-10][2] < axis_ls[i-10][0] - 5))) \
                    or ((axis_ls[i-9][0] >= 50 or axis_ls[i-9][1] >= 50 or axis_ls[i-9][2] >= 50) \
                    or ((axis_ls[i-9][1] > axis_ls[i-9][0] + 5 or axis_ls[i-9][1] < axis_ls[i-9][0] - 5) \
                    or (axis_ls[i-9][2] > axis_ls[i-9][0] + 5 or axis_ls[i-9][2] < axis_ls[i-9][0] - 5))) \
                    or ((axis_ls[i-8][0] >= 50 or axis_ls[i-8][1] >= 50 or axis_ls[i-8][2] >= 50) \
                    or ((axis_ls[i-8][1] > axis_ls[i-8][0] + 5 or axis_ls[i-8][1] < axis_ls[i-8][0] - 5) \
                    or (axis_ls[i-8][2] > axis_ls[i-8][0] + 5 or axis_ls[i-8][2] < axis_ls[i-8][0] - 5))) \
                    or ((axis_ls[i-7][0] >= 50 or axis_ls[i-7][1] >= 50 or axis_ls[i-7][2] >= 50) \
                    or ((axis_ls[i-7][1] > axis_ls[i-7][0] + 5 or axis_ls[i-7][1] < axis_ls[i-7][0] - 5) \
                    or (axis_ls[i-7][2] > axis_ls[i-7][0] + 5 or axis_ls[i-7][2] < axis_ls[i-7][0] - 5))):
                        
                        #check for minus sign

                        if (axis_ls[i+5*w3-8][0] == axis_ls[i+5*w3-8][1] & axis_ls[i+5*w3-8][0] == axis_ls[i+5*w3-8][2] & axis_ls[i+5*w3-8][0] < 50) \
                        &(axis_ls[i+5*w3-9][0] == axis_ls[i+5*w3-9][1] & axis_ls[i+5*w3-9][0] == axis_ls[i+5*w3-9][2] & axis_ls[i+5*w3-9][0] < 50) \
                        & (axis_ls[i+5*w3-10][0] == axis_ls[i+5*w3-10][1] & axis_ls[i+5*w3-10][0] == axis_ls[i+5*w3-10][2] & axis_ls[i+5*w3-10][0] < 50) \
                        & (axis_ls[i+5*w3-11][0] == axis_ls[i+5*w3-11][1] & axis_ls[i+5*w3-11][0] == axis_ls[i+5*w3-11][2] & axis_ls[i+5*w3-11][0] < 50) \
                        & (axis_ls[i+5*w3-12][0] == axis_ls[i+5*w3-12][1] & axis_ls[i+5*w3-12][0] == axis_ls[i+5*w3-12][2] & axis_ls[i+5*w3-12][0] < 50) \
                        & (axis_ls[i+5*w3-13][0] == axis_ls[i+5*w3-13][1] & axis_ls[i+5*w3-13][0] == axis_ls[i+5*w3-13][2] & axis_ls[i+5*w3-13][0] < 50) \
                        & (axis_ls[i+5*w3-14][0] == axis_ls[i+5*w3-14][1] & axis_ls[i+5*w3-14][0] == axis_ls[i+5*w3-14][2] & axis_ls[i+5*w3-14][0] < 50):
                            #-
                            minus = True       

                else:
                    axis_numbers[j] = axis_numbers[j]*10 + digit

                if (math.floor((i+3)/w3) > math.floor(i/w3)) \
                | ((axis_ls[i+4][0] >= 50 or axis_ls[i+4][1] >= 50 or axis_ls[i+4][2] >= 50) \
                or ((axis_ls[i+4][1] > axis_ls[i+4][0] + 5 or axis_ls[i+4][1] < axis_ls[i+4][0] - 5) \
                or (axis_ls[i+4][2] > axis_ls[i+4][0] + 5 or axis_ls[i+4][2] < axis_ls[i+4][0] - 5))) \
                & ((axis_ls[i+5][0] >= 50 or axis_ls[i+5][1] >= 50 or axis_ls[i+5][2] >= 50) \
                or ((axis_ls[i+5][1] > axis_ls[i+5][0] + 5 or axis_ls[i+5][1] < axis_ls[i+5][0] - 5) \
                or (axis_ls[i+5][2] > axis_ls[i+5][0] + 5 or axis_ls[i+5][2] < axis_ls[i+5][0] - 5))) \
                & ((axis_ls[i+6][0] >= 50 or axis_ls[i+6][1] >= 50 or axis_ls[i+6][2] >= 50) \
                or ((axis_ls[i+6][1] > axis_ls[i+6][0] + 5 or axis_ls[i+6][1] < axis_ls[i+6][0] - 5) \
                or (axis_ls[i+6][2] > axis_ls[i+6][0] + 5 or axis_ls[i+6][2] < axis_ls[i+6][0] - 5))) \
                & ((axis_ls[i+7][0] >= 50 or axis_ls[i+7][1] >= 50 or axis_ls[i+7][2] >= 50) \
                or ((axis_ls[i+7][1] > axis_ls[i+7][0] + 5 or axis_ls[i+7][1] < axis_ls[i+7][0] - 5) \
                or (axis_ls[i+7][2] > axis_ls[i+7][0] + 5 or axis_ls[i+7][2] < axis_ls[i+7][0] - 5))) \
                & ((axis_ls[i+8][0] >= 50 or axis_ls[i+8][1] >= 50 or axis_ls[i+8][2] >= 50) \
                or ((axis_ls[i+8][1] > axis_ls[i+8][0] + 5 or axis_ls[i+8][1] < axis_ls[i+8][0] - 5) \
                or (axis_ls[i+8][2] > axis_ls[i+8][0] + 5 or axis_ls[i+8][2] < axis_ls[i+8][0] - 5))):
                    
                    axis_numbers[j] = axis_numbers[j]*(-1)**minus
                    if y:
                        i = math.floor((i+ 8*w3)/w3)*w3
                    elif x:
                        if (math.floor((i+3)/w3) > math.floor(i/w3)) and axis_numbers:
                            i = total_pixels        
                    digit = []
                    j+=1
                   
        i+=1

    return axis_numbers;
