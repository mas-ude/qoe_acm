# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from texplt import texSaveFig, texFigure
from plotting.maineffect import _main_effect, _main_effect_kmeans


if __name__ == "__main__":

    data = pd.read_csv("../data/static_opt_stall.csv")
    
    samples = [tuple(row[1]) for row in data[['pl_avg_assumed_quality_ql',
                                              'pl_norm_buf_events']].iterrows()]

    fig = texFigure()
                                              
    h = _main_effect_kmeans(samples, bins=40)

    plt.xlim([0, 3])
    plt.ylim([0, 1.2])

    plt.xlabel("Average playback quality")
    plt.ylabel(r"Buffering events ($min^-1$)")
    
    texSaveFig("../latex/figs/33qualityvstalling.pdf")    
    plt.close(fig)
    