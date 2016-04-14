# -*- coding: utf-8 -*-

import pandas as pd

def clean_resulset(f, minruns=12, uptoshaping=312500):
    
    data = pd.read_csv(f)

    reqcount = sum(data['net_avg_shaping_rate'].unique()<=uptoshaping) * minruns

    #data.groupby(['yt_id', 'net_avg_shaping_rate']).count()['rnd_traffic']
    
    # If video has enough runs or not
    vids = data.groupby(['yt_id']).count()['rnd_traffic']>reqcount
    vids = list(vids[vids].reset_index()['yt_id'])
    
    data = data[data.loc[:,'yt_id'].isin(vids)]
    
    data.to_csv('traces/static_cleaned.csv')
