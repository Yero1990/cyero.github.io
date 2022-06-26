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

# group cafe configuration
#df_grouped = df.groupby(['target', 'kin\nstudy'])


fig = go.Figure()
'''
for i, group in df_grouped:

    # set name of the configuration (to be put in legend)
    iname = i[0].strip() + ', ' + i[1].strip()

    print(group)
    print(group['run_center'])
    
    #print('run:',group['run\nnumber'])
    #print('run:',group['run\nnumber'])
    #print('run:',df['run\nnumber'])
    
    # add figure trace for each configuration
    fig.add_trace(
        #print('counter'),
        # plot the bar chart
        go.Bar(x=group['run_center'], y=group['BCM4A\ncharge\n[mC]'], width=group['run_len_ms'],

               # set name of configuration
               name="%s" % (iname), 
               
               # set template for information the user want to appear while hovering over the data
               hovertemplate="run_number  :%s<br>"
                             #"start_of_run:%s<br>"
                             #"end_of_run  :%s<br>"
                             #"target      :%s<br>"
                             #"kin_study   :%s<br>"
                             "<extra></extra>" %               
               (
               group['run\nnumber'].to_string(index=False),
               # group['start_run'].to_string(index=False),
               # group['end_run'].to_string(index=False),
               # group['target'].to_string(index=False),
               # group['kin\nstudy'].to_string(index=False),                
               ),
              
        ),
        
    )


# add figure trace for each configuration

#fig.add_trace(
#    go.Bar(x=df['run_center'], y=df['BCM4A\ncharge\n[mC]'], width=df['run_len_ms'],name="trace")        
#)


#fig.update_layout(legend_title_text = "CaFe Configuration")
#fig.update_xaxes(title_text="Date")
#fig.update_yaxes(title_text="Charge [mC]")
#fig.show()

# slice the dataframe into (target, kin_study config)
h2_singles_df = df[(df['target'].str.contains('LH2')) & (df['kin\nstudy'].str.contains('heep_singles'))]
h2_coin_df = df[(df['target'].str.contains('LH2')) & (df['kin\nstudy'].str.contains('heep_coin'))]

d2_MF_df = df[(df['target'].str.contains('LD2')) & (df['kin\nstudy'].str.contains('MF'))]
d2_SRC_df = df[(df['target'].str.contains('LD2')) & (df['kin\nstudy'].str.contains('SRC'))]

Ca48_MF_df = df[(df['target'].str.contains('Ca48')) & (df['kin\nstudy'].str.contains('MF'))]
Ca48_SRC_df = df[(df['target'].str.contains('Ca48')) & (df['kin\nstudy'].str.contains('SRC'))]


# add figure trace for each configuration
fig.add_trace(go.Bar(x=h2_coin_df['run_center'], y=h2_coin_df['BCM4A\ncharge\n[mC]'], width=h2_coin_df['run_len_ms'],name="LH2, heep_coin"))
fig.add_trace(go.Bar(x=d2_MF_df['run_center'], y=d2_MF_df['BCM4A\ncharge\n[mC]'], width=d2_MF_df['run_len_ms'],name="LD2, MF"))
fig.add_trace(go.Bar(x=d2_SRC_df['run_center'], y=d2_SRC_df['BCM4A\ncharge\n[mC]'], width=d2_SRC_df['run_len_ms'],name="LD2, SRC"))        

fig.add_trace(go.Bar(x=Ca48_MF_df['run_center'], y=Ca48_MF_df['BCM4A\ncharge\n[mC]'], width=Ca48_MF_df['run_len_ms'],name="Ca48, MF"))
fig.add_trace(go.Bar(x=Ca48_SRC_df['run_center'], y=Ca48_SRC_df['BCM4A\ncharge\n[mC]'], width=Ca48_SRC_df['run_len_ms'],name="Ca48, SRC"))        



fig.update_layout(legend_title_text = "CaFe Configuration")
fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="Charge [mC]")
#fig.show()
'''

cafe_dict = {
    'target_names' : {
        'LH2',
        'LD2',
        'Ca48'
    },

    'kinematic_study' : {
        'heep_coin',
        'MF',
        'SRC'
    },

    'color' : {
        'LH2' : { 'heep_coin': 'rgba(169, 169, 169, 0.8)' },  

        'LD2' : { 'MF'       : 'rgba(220, 220, 220, 0.8)' ,  
                  'SRC'      : 'rgba(220, 220, 220, 0.8)'},  

        'Ca48' : { 'MF'       : 'rgba(255, 127, 14, 0.8)', 
                   'SRC'      : 'rgba(255, 127, 14, 0.8)'},  

    },
    
}

#target_names = ['LH2', 'LD2', 'C12', 'Ca48']
#kinematic_study = ['heep_singles', 'heep_coin', 'MF', 'SRC']

for targ in cafe_dict['target_names']:
    for kin in cafe_dict['kinematic_study']:

        # set color
        #bar_color = cafe_dict['color'][targ][kin]
        
        # selected dataframe
        df_select = df[(df['target'].str.contains(targ)) & (df['kin\nstudy'].str.contains(kin))]

        #print(df_select.shape[0])
        if(df_select.shape[0]<2):
            print('targ, kin -->', targ, kin)
            fig.add_trace(
                go.Bar(x=df_select['run_center'], y=df_select['BCM4A\ncharge\n[mC]'], width=df_select['run_len_ms'],
                       name="%s, %s" % (targ, kin), marker = {'color' : cafe_dict['color'][targ][kin]},
                       hovertext = "%s" % df_select['run\nnumber']  # or hoverinfo = "y"                   
                )
            )
        else:
            print(df_select.shape[0])
            
            for (index_label, row_series) in df_select.iterrows():

                # need single dataframe values to be type list for plotting
                print('Row Index label : ', index_label)
                x_list = []
                y_list = []
                w_list = []
                x_list.append(df_select['run_center'][index_label])
                y_list.append(df_select['BCM4A\ncharge\n[mC]'][index_label])
                w_list.append(df_select['run_len_ms'][index_label])
                print('list = ',x_list)

                fig.add_trace(
                    go.Bar(x=x_list, y=y_list, width=w_list,
                           name="%s, %s" % (targ, kin), marker = {'color' : cafe_dict['color'][targ][kin]},
                           hovertext = "%s" % df_select['run\nnumber'][index_label]  # or hoverinfo = "y"                   
                    )
                )
         
                

fig.update_layout(legend_title_text = "CaFe Configuration")
fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="Charge [mC]")
fig.show()
