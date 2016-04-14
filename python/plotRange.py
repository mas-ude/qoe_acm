# -*- coding: utf-8 -*-
"""
Created on Thu Feb  5 14:06:11 2015

@author: sieber
"""

import csv
from texplt import texFigure, texSaveFig
from pylab import *
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

pdir='figures/'

#%% Read data

ranges = {}
mins = []

file = 'traces/range_1004_170227.csv'

with open(file, 'r') as csvfile:
    
    reader = csv.reader(csvfile)
    
    for row in reader:
        ranges[row[0]] = [float(x) for x in row[1:]]
        
        mins.append(min(ranges[row[0]][0::4]))

min_ts = min(mins) - 5

#%% Plot figure

fig = texFigure()
ax1 = fig.add_subplot(111)

style = {'160': {'label': '144p', 'color': 'green', 'linestyle': '-', 'marker': '^', 'markersize': 3},
         '133': {'label': '240p', 'color': 'red'  , 'linestyle': '-.', 'marker': 'o', 'markersize': 3},
         '134': {'label': '360p', 'color': 'blue' , 'linestyle': ':', 'marker': '*', 'markersize': 3},
         '135': {'label': '480p', 'color': 'grey' , 'linestyle': '--', 'marker': 'D', 'markersize': 3}}
          
hpatches = []
i=0
order = ['160', '133', '134', '135']

# Go through quality levels
for q in order:
 
    hpatches.append(mlines.Line2D([], 
                                  [], 
                                  **style[q]))
  
    # Select the timestamps
    for ts in list(range(0, len(ranges[q]), 4)):
    
        timestamp = ranges[q][ts] - min_ts
        length = ranges[q][ts+1]
        start = ranges[q][ts+2]
        end = ranges[q][ts+3]

        print("%s, %d: %.2f to %.2f (length: %.2f) " % (q, timestamp, start, end, length))
        
        plot([start+0.5, end], 
             [timestamp, timestamp], 
             **style[q])

    i += 1     
    
    X = [[30, 45], [45,58], [58,74.5], [74.5,89.5]]
    Y = [[21.7]*2, [42.7]*2, [61.5]*2,[73]*2]
    
    for idx,x in enumerate(X):
        ax1.fill_between(x, 
                         [0]*len(x),
                         Y[idx],
                         alpha=0.04,
                         facecolor='r',
                         linewidth=0.0)
                         
plt.plot([0,100], 
         [0,100], 
         color='g',
         alpha=0.15)

plt.annotate(s='$\kappa = 1$', xy=(80,82), xytext=(61,92), arrowprops=dict(arrowstyle='->'))     

ylim(0, 100)    
ylabel('Time of Request (s)')    
xlabel('Requested Video Interval (s)')
legend(handles=hpatches, loc='upper left')
   
texSaveFig(pdir + 'eg_request_schedule.pdf')
plt.close()
