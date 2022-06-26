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
df['run_center'] = run_center   # time corresponding to middle of run
df['run_len_ms'] = run_len_ms   # time corresponding to run length

print(df.loc[1]['start_run'])
# group cafe configuration
df_grouped = df.groupby(['target', 'kin\nstudy'])


fig = go.Figure()
for i, group in df_grouped:

    # set name of the configuration (to be put in legend)
    iname = i[0].strip() + ', ' + i[1].strip()

    #print(type(group['run_center']))
    
    #print('run:',group['run\nnumber'])
    #print('run:',group['run\nnumber'])
    #print('run:',df['run\nnumber'])
    
    # add figure trace for each configuration
    fig.add_trace(

        # plot the bar chart
        go.Bar(x=group['run_center'], y=group['BCM4A\ncharge\n[mC]'], width=group['run_len_ms'],

               # set name of configuration
               name="%s" % (iname), 
               
               # set template for information the user want to appear while hovering over the data
               hovertemplate="run_number  :%s<br>"
                             "start_of_run:%s<br>"
                             "end_of_run  :%s<br>"
                             "target      :%s<br>"
                             "kin_study   :%s<br>"
                             "<extra></extra>" %               
               (group['run\nnumber'].to_string(index=False),
                group['start_run'].to_string(index=False),
                group['end_run'].to_string(index=False),
                group['target'].to_string(index=False),
                group['kin\nstudy'].to_string(index=False),
                
               ),
               

              
        )
    )

fig.update_layout(legend_title_text = "CaFe Configuration")
fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="Charge [mC]")
#fig.show()
