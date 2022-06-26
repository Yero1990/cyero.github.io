import pandas as pd
import plotly_express as px
from plotly.subplots import make_subplots
import datetime
import chart_studio
import chart_studio.plotly as charts
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np


# define the timestamps for the entire experiment
exp_start = datetime(2018,4,3).timestamp()
exp_end = datetime(2018,4,9).timestamp()

# convert csv to dataframe 
df = pd.read_csv("cafe-2022_runlist.csv") 

#group by target and kinematic_type, then do cumulative sum of charge
charge_csum = df.groupby(['target', 'kin\nstudy'])['BCM4A\ncharge\n[mC]'].cumsum()

run     = df['run\nnumber']
charge = df['BCM4A\ncharge\n[mC]']
target = df['target']
run_start = pd.to_datetime(df['start_run'])
run_end = pd.to_datetime(df['end_run'])
run_center = run_start + 0.5*(run_end-run_start)
run_len = (run_end-run_start)
run_len_ms = run_len.dt.total_seconds() * 1.e3 # run len in millisecond (required for width)

# add new columns to dataframe
df['run_center'] = run_center
df['run_len_ms'] = run_len_ms


#  APPROACH #1 : grouping dataframe manually based on (target, kin_study)
# way to splitting dataframe based on specific (target, kin_study) combo for plotting using the go.Bar() command
# d2_MF = df.loc[(df['target'].str.contains('LD2')) & (df['kin\nstudy'].str.contains('MF'))]
# d2_SRC = df.loc[(df['target'].str.contains('LD2')) & (df['kin\nstudy'].str.contains('SRC'))]


# APPROACH #2: loop over grouped variables (target, kin_study)
fig = go.Figure()
for i, group in df.groupby(['target', 'kin\nstudy']):

   
    #print(group['target'].to_string())
    fig.add_trace(go.Bar(x=group['run_center'], y=group['BCM4A\ncharge\n[mC]'], width=group['run_len_ms'], name="%s"%( group['target'].to_string(index=False)+group['kin\nstudy'].to_string(index=False)),
                         hovertemplate="start_of_run=%s<br>end_of_run=%s<br>target=%s<br><extra></extra>" %
                         (group['start_run'].to_string(index=False), group['end_run'].to_string(index=False), group['target'].to_string(index=False)) 
    ))
    showlegend=False
    
fig.update_layout(legend_title_text = "config")

fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="Charge [mC]")
fig.show()

#fig.add_traces(list(px.line(d2_MF, x=run_center, y=charge_csum, title='cumulative charge', color='target', line_dash='kin\nstudy', markers=True).select_traces()))
#fig.add_trace(go.Bar(x=run_center[], y=charge, width=run_len_ms) )  # width is in milliseconds
#fig.add_traces(list(px.bar(df, x=['start_run'], y='BCM4A\ncharge\n[mC]', color='target', pattern_shape="kin\nstudy").select_traces()))

#fig.show()


'''
run_len1 = 3600. 
run_len2 = 1500. 

#convert to datetime object to calculate center and end time
run1_start = datetime.strptime(run1_start, '%Y-%m-%d %H:%M:%S')
run1_end = run1_start + timedelta(seconds=run_len1)
run1_center = run1_start + 0.5*(run1_end - run1_start)

run2_start = datetime.strptime(run2_start, '%Y-%m-%d %H:%M:%S')
run2_end = run2_start + timedelta(seconds=run_len2)
run2_center = run2_start + 0.5*(run2_end - run2_start)

arr = [run1_center, run2_center]

#convert run length (width from sec to milliseconds, as this is the unit it takes)
run_len1 =  run_len1*1e3
run_len2 =  run_len2*1e3

fig = go.Figure()

fig.add_trace(go.Bar(x=[run1_center, run2_center], y=[10,8], width=[run_len1, run_len2]))  # width is in milliseconds




fig.show()

'''
