
from collections import defaultdict
from dateutil import parser
import datetime

import plotly.graph_objs as go
import plotly

import pandas as pd
import numpy as np


def bin_by_day(dt):
    return parser.parse(dt).strftime("%Y/%m/%d")

df = pd.read_csv('rundata1.csv')
# convert from strings, through default timedelta, to seconds
df['duration'] = pd.to_timedelta(df['duration']).astype('timedelta64[s]')
df['delay'] = pd.to_timedelta(df['delay']).astype('timedelta64[s]')

all_data = defaultdict(list)


df['bin'] = df['scheduled_time'].apply(bin_by_day)
# print(df['bin'])

count = len(df['bin'].unique())
c = ['hsl(' + str(h) + ',50%' + ',50%)' for h in np.linspace(0, 360, count)]


for workertype in df['workertype'].unique():
    print(workertype)
    byworker = df.loc[df['workertype'] == workertype]
    for i, bucket in enumerate(sorted(df['bin'].unique())):
        print(bucket)

        results = byworker.loc[byworker['bin'] == bucket]['delay']
        print(list(results)[:10])
        all_data[workertype].append({
            'y': results,
            # 'x': bucket,
            'type': 'box',
            'name': bucket,
            'marker': {'color': c[i]},
        })


layout = {'xaxis':
          {
              'showgrid': False,
              'zeroline': False,
              'tickangle': 60,
              'showticklabels': True,
              'autotick': True,
              'autorange': True,
          },
          'yaxis':
          {
              'zeroline': False,
              'gridcolor': 'white',
              'nticks': 20,
              # 'type': 'log',
          },
          'paper_bgcolor': 'rgb(233,233,233)',
          #'plot_bgcolor': 'rgb(233,233,233)',
          'plot_bgcolor': 'rgb(255,255,255)',
          }

# url_1 = plotly.offline.plot(data, filename='scatter-for-dashboard', auto_open=False)
# plotly.offline.plot(data, filename='scatter-for-dashboard')
for workertype in all_data:
    print("Ticks: {}".format(
        df.loc[df['workertype'] == workertype]['bin'].unique()))
    # layout['xaxis']['ticks'] = df.loc[df['workertype'] == workertype]['bin'].unique()

    plotly.offline.plot(go.Figure(data=all_data[workertype], layout=layout),
                        filename='task-delays-by-date-{}.html'.format(workertype), 
                        auto_open=False)
