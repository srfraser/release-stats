import plotly.graph_objs as go
import plotly

import pandas as pd
import numpy as np


df = pd.read_csv('rundata1.csv')
# convert from strings, through default timedelta, to seconds
df['duration'] = pd.to_timedelta(df['duration']).astype('timedelta64[s]')
df['delay'] = pd.to_timedelta(df['delay']).astype('timedelta64[s]')

all_data = list()
some_data = list()

count = len(df['workertype'].unique())
c = ['hsl(' + str(h) + ',50%' + ',50%)' for h in np.linspace(0, 360, count)]

#for i, workertype in enumerate(df['workertype'].unique()):
#    results = df.loc[df['workertype'] == workertype]['duration']
#    bins = [0, 1000, 2000, 4000, 30000]
#    group_names = ['Quick', 'Errr', 'Slow', 'Anomalous']
#    df['categories'] = pd.cut(results, bins, labels=group_names)
all_data.append(go.Bar(
        #y=df.loc[df['workertype'] == workertype].groupby('categories')['categories'].count(),
        #x=group_names,
        y=df.groupby('duration')['duration'].count(),
        x=df['duration'].unique(),
        # name=workertype,
        marker={'color': c[0]},
))


layout = {'xaxis':
          {
              'showgrid': False,
              'zeroline': False,
              'tickangle': 60,
              'showticklabels': True,
          },
          'yaxis':
          {
              'zeroline': False,
              'gridcolor': 'white',
              'nticks': 20,
          },
          'paper_bgcolor': 'rgb(233,233,233)',
          'plot_bgcolor': 'rgb(233,233,233)',
          }

plotly.offline.plot(go.Figure(data=all_data, layout=layout),
                    filename='task-duration-distribution.html')
