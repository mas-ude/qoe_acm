# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from texplt import texSaveFig, texFigure

if __name__ == "__main__":
    
    data = pd.read_csv("../data/qualitygain.txt", sep='\t', dtype=np.float64)
   
    fig = texFigure()
                     
    ctmp = plt.get_cmap('copper')
    colors = [ctmp(i) for i in np.linspace(0, 1, 4, endpoint=False)]    
    ic=iter(colors)                     
                     
    for i in range(3):
        ecdf = sm.distributions.ECDF(data.iloc[:,i])    
        x = np.linspace(data.iloc[:,i].min(), data.iloc[:,i].max(), 1000)
        y = ecdf(x)
        plt.step(x, y, color=next(ic))                                       
                
    plt.xlim([0, 3])                
    plt.ylim([0, 1])                
                
    plt.xlabel("Potential gain in quality")
    plt.ylabel(r"$P(x<X)$")
    
    #plt.annotate(s=r'optimization', xy=(30,1.6), xytext=(15,2.2), arrowprops=dict(arrowstyle='->'))         
    
    plt.annotate(s='heuristic', xy=(1.9,0.8), xytext=(2,0.7), arrowprops=dict(arrowstyle='->'))     
    plt.annotate(s='optimization, no stalling', xy=(1.5,0.6), xytext=(1.5,0.5), arrowprops=dict(arrowstyle='->'))     
    plt.annotate(s='optimization, stalling', xy=(0.9,0.3), xytext=(1,0.25), arrowprops=dict(arrowstyle='->'))     
    
    texSaveFig("../latex/figs/qualitygain_py.pdf")    
    plt.close(fig)