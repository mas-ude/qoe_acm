
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.isotonic import IsotonicRegression
from scipy import interpolate
from texplt import texSaveFig, texFigure

regressions = {}
interp = {}

def do_regressions(data, method = IsotonicRegression):

    for name, group in data.groupby('yt_id'):
      
        reg = method() 
        x, y = group['net_played_bytes'], group['pl_avg_assumed_quality_ql']
        
        reg.fit_transform(x, y)
        regressions[name] = reg
    
    return regressions


def do_interp(data):
    
    itags = [160, 133, 134, 134]
    
    for name, group in data.groupby('yt_id'):
        
        itags_br = [group['br_avg_i%d' % t].unique()[0] for t in itags]
        
        interp[name] = interpolate.interp1d(itags_br, range(len(itags)), bounds_error=False)

        
    for name, group in data.groupby('yt_id'):
         data.loc[:, 'interp_ql'] = data.apply(lambda row: interp[row['yt_id']](row['net_played_bytes'] * 8 * 1000 * 1000 / row['vid_length']), axis=1)
            
        
        
        pass
    
    
    pass
    


def do_plot_paper(yt_id, data, regs, savef):
    
    #fig = texFigure(fig_width=3, fig_height=3, font_scale=155)
    fig = texFigure()    
    
    data = data[data['yt_id'] == yt_id]        
    
    x, y = data['net_played_bytes'], data['pl_avg_assumed_quality_ql']
    y_= regressions[yt_id].predict(x)

    plt.xlabel("Played Bytes (MB)")
    plt.ylabel(r"Average Quality Level")

    plt.annotate(s=r'\phi', xy=(30,1.6), xytext=(15,2.2), arrowprops=dict(arrowstyle='->'))     

    ctmp = plt.get_cmap('copper')
    colors = [ctmp(i) for i in np.linspace(0, 1, 4, endpoint=False)]    
    ic=iter(colors)    
    
    plt.plot(x, y, ".", color=colors[3], markersize=6, alpha=0.5)
    plt.plot(x, y_, '.-', color=colors[1], markersize=6)
    
    plt.xlim([0,75])
    #plt.xticks([15, 30, 45, 60])

    texSaveFig(savef)    
    plt.close(fig)


def plot_regressions(data, regs):
    
    i = 0
    for name, group in data.groupby('yt_id'):
     
        do_plot_paper(name, data, regs, os.path.join(studypath, "32_%s.pdf" % name))     
        
        i+=1
        #if i == 3:
        #    break


def predict(dl_bytes, yt_id):
    return regressions[yt_id].predict([dl_bytes])[0]


if __name__ == "__main__":

    data = pd.read_csv("../data/static_opt_stall.csv")

    data['net_played_bytes'] = data['net_played_bytes'] / 1000 / 1000
    data.sort('net_played_bytes', inplace=True)

    regressions = do_regressions(data)

    #plot_regressions(data, regressions)

    #selection = ['_pjBVUyq530', 'Jy8fAyXTij4', '7JIiOgJWlcs', 'CRZbG73SX3s', 'vbLLqaa9ksw']
    selection = ['_pjBVUyq530', 'vbLLqaa9ksw']
    
    for s in selection:
        do_plot_paper(s, data, regressions, "../latex/figs/32_%s.pdf" % s)
    
    data.loc[:, 'predicted_ql'] = data.apply(lambda row: regressions[row['yt_id']].predict([row['net_played_bytes']])[0], axis=1)
    