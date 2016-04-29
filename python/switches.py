# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from texplt import texSaveFig, texFigure

if __name__ == "__main__":
    
    data = pd.read_csv("../data/switches.txt", sep='\t', dtype=np.float64)
   
    fig = texFigure()
                     
    ctmp = plt.get_cmap('copper')
    colors = [ctmp(i) for i in np.linspace(0, 1, 4, endpoint=False)]    
    ic=iter(colors)                     
                     
    for i in range(2):
        ecdf = sm.distributions.ECDF(data.iloc[:,i])    
        x = np.linspace(data.iloc[:,i].min(), data.iloc[:,i].max(), len(data.iloc[:,i]))
        y = ecdf(x)
        plt.step(x, y, color=next(ic))                                       
                
    plt.xlim([0, 8])                
    plt.ylim([0, 1])                
                
    plt.xlabel("Number of switches per minute")
    plt.ylabel(r"$P(x<X)$")
    
    #plt.annotate(s=r'optimization', xy=(30,1.6), xytext=(15,2.2), arrowprops=dict(arrowstyle='->'))         
    
    plt.annotate(s='opt', xy=(3,0.9), xytext=(4,0.8), arrowprops=dict(arrowstyle='->'))     
    plt.annotate(s='measurement', xy=(0.6,0.5), xytext=(1.1,0.25), arrowprops=dict(arrowstyle='->'))     
    
    texSaveFig("../latex/figs/switches_py.pdf")    
    plt.close(fig)