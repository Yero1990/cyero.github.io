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


run     = df['run\nnumber']
charge = df['BCM4A\ncharge\n[mC]']
target = df['target']
run_start = pd.to_datetime(df['start_run'])
run_end = pd.to_datetime(df['end_run'])
run_center = run_start + 0.5*(run_end-run_start)
run_len = (run_end-run_start)                   # run length 
run_len_ms = run_len.dt.total_seconds() * 1.e3 # run length  in millisecond (required for width)

# add new columns to dataframe
df['run_center'] = run_center   # time corresponding to middle of run
df['run_len'] = run_len.dt.total_seconds()   # run length in sec
df['run_len_ms'] = run_len_ms   # time corresponding to run length


# calculate cumulative quantities
charge_csum = df.groupby(['target', 'kin\nstudy'])['BCM4A\ncharge\n[mC]'].cumsum()
df['cumulative_charge'] = charge_csum


cafe_dict = {
    'target_names' : {
        'LH2',
        'LD2',
        'Ca48'
    },

    'kinematic_study' : {
        'LH2' : {'heep_singles', 'heep_coin'},
        'LD2' : {'MF', 'SRC'},
        'Ca48': {'MF', 'SRC'},
        
    },

    'color' : {

        # rgb(227, 119, 194) pink
        # rgb(127, 127, 127) gray
        # rgb(188, 189, 34)  lime
        # rgb(23, 190, 207)  blue
        # rgb(255, 127, 14)  orange
        # rgb(44, 160, 44)   green
        # rgb(148, 103, 189) purple
        # rgb(214, 39, 40)   red
        'LH2' : { 'heep_singles': 'rgba(227, 119, 194, 0.5)',
                  'heep_coin': 'rgba(227, 119, 194, 0.5)'},  

        'LD2' : { 'MF'       : 'rgba(44, 160, 44, 0.5)' ,   
                  'SRC'      : 'rgba(44, 160, 44, 0.5)'},  

        'Ca48' : { 'MF'       : 'rgba(148, 103, 189, 0.5)',   
                   'SRC'      : 'rgba(148, 103, 189, 0.5)'},  

    },

    'pattern' : {
        'LH2' : { 'heep_singles': '',
                  'heep_coin': ''},  

        'LD2' : { 'MF'       : '' ,  
                  'SRC'      : '.'},  

        'Ca48' : { 'MF'       : '', 
                   'SRC'      : '.'},  

    },

    'linestyle' : {
        'LH2' : { 'heep_singles': 'solid',
                  'heep_coin': 'dash'},  
        
        'LD2' : { 'MF'       : 'solid' ,  
                  'SRC'      : 'dash'},  
        
        'Ca48' : { 'MF'       : 'solid', 
                   'SRC'      : 'dash'},  

    },
    

}



fig = go.Figure()

for targ in cafe_dict['target_names']:
    for kin in cafe_dict['kinematic_study'][targ]:

        #print('targ, kin:', targ, kin)
        # set color, pattern and line style
        bar_color   = cafe_dict['color'][targ][kin]
        bar_pattern = cafe_dict['pattern'][targ][kin]
        line_style  = cafe_dict['linestyle'][targ][kin]
        
        #print(bar_color)
        
        # selected dataframe @ selected  (targ,kin)
        df_select = df[(df['target'].str.contains(targ)) & (df['kin\nstudy'].str.contains(kin))]


        #print(df_select.shape[0])
        if(df_select.shape[0]>0 and df_select.shape[0]<2):

            #fig.add_trace(
            #go.Scatter(y=df_select['BCM4A\ncharge\n[mC]'])
            #)
            
            print('targ, kin : ', targ,',',kin)
            print('x: ', df_select['run_center'])
            print('y: ', df_select['BCM4A\ncharge\n[mC]'])

            # add cumulative charge line
            fig.add_trace(
                go.Scatter( x=df_select['run_center'], y=df_select['cumulative_charge'], mode='markers+lines', marker=dict(color=bar_color),line=dict(dash=line_style) )
            )
            
            # add bar chart
            fig.add_trace(
                
                go.Bar(x=df_select['run_center'], y=df_select['BCM4A\ncharge\n[mC]'], width=df_select['run_len_ms'],
                       name="%s, %s" % (targ, kin), marker = {'color' : bar_color}, marker_pattern_shape=bar_pattern,

                       #hovertext = "%s" % df_select['run\nnumber']
                           hovertemplate="run_number    :%s<br>"
                                         "start_of_run  :%s<br>"
                                         "end_of_run    :%s<br>"
                                         "run_length [sec] :%s<br>"
                                         "beam_time  [sec] :%s<br>"
                                         "target        :%s<br>"
                                         "kin_study     :%s<br>"
                                         "BCM4A current [uA] :%s<br>"
                                         "BCM4A charge  [mC] :%s<br>"
                                         "<extra></extra>" %
                       (
                           df_select['run\nnumber'].to_string(index=False),
                           df_select['start_run'].to_string(index=False),
                           df_select['end_run'].to_string(index=False),
                           df_select['run_len'].to_string(index=False),
                           df_select['beam_on_target\n[sec]'].to_string(index=False),
                           df_select['target'].to_string(index=False),
                           df_select['kin\nstudy'].to_string(index=False),
                           df_select['BCM4A\ncurrent\n[uA]'].to_string(index=False),
                           df_select['BCM4A\ncharge\n[mC]'].to_string(index=False),
                           
                       )
                       
                ), #end go.Bar
     
                

            
            ) # end add_trace




        else:
            #print(df_select.shape[0])
            cnt = 0 # counter
            for (index_label, row_series) in df_select.iterrows():

                # need single dataframe values to be type list for plotting
                #print('Row Index label : ', index_label)
                x_list = []
                y_list = []
                w_list = []
                x_list.append(df_select['run_center'][index_label])
                y_list.append(df_select['BCM4A\ncharge\n[mC]'][index_label])
                w_list.append(df_select['run_len_ms'][index_label])
                #print('list = ',x_list)
                
                if cnt==0:
                    showlegend_flag = True
                else:
                    showlegend_flag = False

                # add cumulative charge line
                fig.add_trace(
                    go.Scatter(name="%s, %s charge" % (targ, kin), x=df_select['run_center'], y=df_select['cumulative_charge'], mode='markers+lines', marker=dict(color=bar_color), line=dict(dash=line_style) )
                )
                
                fig.add_trace(
                    go.Bar(x=x_list, y=y_list, width=w_list,
                           name="%s, %s" % (targ, kin), legendgroup='%s_%s' % (targ, kin), marker = {'color' : bar_color}, marker_pattern_shape=bar_pattern,


                           #hovertext = "%s" % df_select['run\nnumber'][index_label],
                           hovertemplate="run_number    :%s<br>"
                                         "start_of_run  :%s<br>"
                                         "end_of_run    :%s<br>"
                                         "run_length [sec] :%s<br>"
                                         "beam_time  [sec] :%s<br>"
                                         "target        :%s<br>"
                                         "kin_study     :%s<br>"
                                         "BCM4A current [uA] :%s<br>"
                                         "BCM4A charge  [mC] :%s<br>"
                                         "<extra></extra>" %
                           (
                               df_select['run\nnumber'][index_label],
                               df_select['start_run'][index_label],
                               df_select['end_run'][index_label],
                               df_select['run_len'][index_label],
                               df_select['beam_on_target\n[sec]'][index_label],
                               df_select['target'][index_label],
                               df_select['kin\nstudy'][index_label],
                               df_select['BCM4A\ncurrent\n[uA]'][index_label],
                               df_select['BCM4A\ncharge\n[mC]'][index_label],


                           ),

                           showlegend=showlegend_flag                  
                    ), #print('(targ, kin):',targ,',',kin,'-->',bar_color)

                ) # end fig.add_trace
                
                cnt = cnt+1 #counter

                



                
#-------------------------------------------------------------
#
# Add annotation for total charge
# at the end of each line trace
#
#-------------------------------------------------------------

last_x = df.groupby(['target', 'kin\nstudy']).last()['run_center']
last_y = df.groupby(['target', 'kin\nstudy']).last()['cumulative_charge']


cnt=0
for idx, val in last_y.items():  
    fig.add_annotation(x=last_x[cnt], y=last_y[cnt], xref="x", yref="y",
                       text=f"<b>total_charge: %s  mC</b>" %last_y[cnt], showarrow=False,
                       font=dict(
                           family="Arial, sans-serif",
                           color='black',
                           size=16),
                       bgcolor="yellow"
    )
    cnt=cnt+1

#-------------------------------------------------------------


fig.update_layout(legend_title_text = "CaFe Configuration")
fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="Charge [mC]")

# create .html interactive plot 
fig.write_html("index.html")

fig.show()

