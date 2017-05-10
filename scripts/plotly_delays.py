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

for i, workertype in enumerate(df['workertype'].unique()):
    results = df.loc[df['workertype'] == workertype]['delay']
    all_data.append({
        'y': results,
        'type': 'box',
        'name': workertype,
        'marker': {'color': c[i]},
    })
    # long delays here, let's have a graph we can see for the rest.
    if workertype == 'human-decision':
        continue
    some_data.append({
        'y': results,
        'type': 'box',
        'name': workertype,
        'marker': {'color': c[i]},
    })
    # trace = go.Box(name=workertype, y=results)
    # data.append(trace)


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

# url_1 = plotly.offline.plot(data, filename='scatter-for-dashboard', auto_open=False)
# plotly.offline.plot(data, filename='scatter-for-dashboard')
plotly.offline.plot(go.Figure(data=all_data, layout=layout), filename='task-delays.html')
plotly.offline.plot(go.Figure(data=some_data, layout=layout), filename='task-delays-filtered.html')
