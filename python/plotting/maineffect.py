# -*- coding: utf-8 -*-
import matplotlib.pylab as plt
import scipy.stats
import math
import numpy as np
import pandas as pd
import sklearn.cluster
from collections import defaultdict


def _main_effect(data, line=True, bins = 0, **kwargs):
    """
    Plot a factor plot with 95% confidence interval.
    
    Parameters:
        values: A list of (x,y) values.
    """    

    if not bins is 0:
        data = pd.DataFrame(data, columns=['X', 'Y']).sort('X')
        data = [tuple(row[1]) for row in data.iterrows()]
        data_split = np.array_split(data, bins)    
        data = [(np.median(i[:,0]), x[1]) for i in data_split for x in i]    
    
    by_x = defaultdict(list)
    for x, value in data:
        by_x[x].append(value)

    rows = []  
    
    for x, values in by_x.items():

        n, min_max, mean, var, skew, kurt = scipy.stats.describe(values)
        std = math.sqrt(var)

        intv = scipy.stats.t.interval(0.95,len(values)-1,loc=mean,scale=std/math.sqrt(len(values)))
        
        mean = np.mean(values)
        yerr = ((intv[1] - intv[0]) / 2)
        
        rows.append((x, mean, yerr))

    ar = np.array(rows)

    ar = ar[ar[:,0].argsort()]

    return plt.errorbar(ar[:,0], ar[:,1], yerr=ar[:,2], fmt = '' if line else 'None', **kwargs)


def _main_effect_kmeans(data, bins = 20,  **kwargs):
    
    data = pd.DataFrame(data, columns=['X', 'Y']).sort('X')
    
    X = np.swapaxes(np.array([data.X]), 0, 1)
    Y = np.swapaxes(np.array([data.Y]), 0, 1)
    
    kmeans = sklearn.cluster.KMeans(n_clusters = bins)
    
    kmeans_fit = kmeans.fit_predict(X)
    
    clustered = []    
    counts = {i: 0 for i in range(bins)}
    
    for cluster, value in zip(kmeans_fit, Y):
        clustered.append((kmeans.cluster_centers_[cluster][0], value[0]))
        counts[cluster] += 1
        
    countlst = []
    for cluster, count in counts.items():
        countlst.append((kmeans.cluster_centers_[cluster][0], count))
        
    pdcount = pd.DataFrame(countlst, columns=["cluster","count"])
    pdcount.sort('cluster', inplace=True)        
        
    return _main_effect(clustered, **kwargs), pdcount
    