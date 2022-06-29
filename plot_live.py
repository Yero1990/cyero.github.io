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
charge = df['BCM4A\ncharge\n[mC]'] # convert to micro-coulomb for visualization purpose
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


# create a new column in the dataframe which will be the addition of columns: heep_singles, heep_coin, MF_real, SRC_real into a single column
# NOTE: the columns can be added safely (will not actually mix different kinematics), e.g., no change of mixing heep_coin with MF_real counts, as one of these will be NaN and the other will NOT.
df['real_counts'] = df.fillna(0)['heep_singles\ncounts'] + df.fillna(0)['heep_coin\ncounts'] + df.fillna(0)['MF_real\ncounts'] + df.fillna(0)['SRC_real\ncounts']
df['real_rates'] = df.fillna(0)['heep_singles\nrates [Hz]'] + df.fillna(0)['heep_coin\nrates [Hz]'] + df.fillna(0)['MF_real\nrates [Hz]'] + df.fillna(0)['SRC_real\nrates [Hz]']

# calculate counts/mC
df['counts_per_mC'] =  df['real_counts'] / charge

# calculate beam efficiency
df['beam_eff'] = df['beam_on_target\n[sec]'] /df['run_len']



# re-define dataframe for special tasks

# 1) filter out (use only) MF and SRC (for tracking quantities over entire run period) : heep will only be tracked in the Run Summary plot
df_cafe = df[df["kin\nstudy"].str.contains("MF") | df["kin\nstudy"].str.contains("SRC")]



cafe_dict = {'target_names' : {'LH2', 'LD2', 'Be9', 'B10', 'B11', 'C12_optics', 'C12', 'Ca40', 'Ca48', 'Ti48', 'Fe54'},
             
             'kinematic_study' : {
                 'LH2' : {'heep_singles', 'heep_coin'},
                 'LD2' : {'MF', 'SRC'},
                 'Be9' : {'MF', 'SRC'},
                 'B10' : {'MF', 'SRC'},
                 'B11' : {'MF', 'SRC'},
                 'C12_optics' : {'optics'},
                 'C12' : {'MF', 'SRC'},
                 'Ca40': {'MF', 'SRC'},
                 'Ca48': {'MF', 'SRC'},
                 'Ti48': {'MF', 'SRC'},
                 'Fe54': {'MF', 'SRC'},    
             },
             
             'color' : {
                 
                 # rgb(31, 119, 180) muted blue
                 # rgb(227, 119, 194) pink
                 # rgb(127, 127, 127) gray
                 # rgb(188, 189, 34)  lime
                 # rgb(23, 190, 207)  blue
                 # rgb(255, 127, 14)  orange
                 # rgb(44, 160, 44)   green
                 # rgb(148, 103, 189) purple
                 # rgb(214, 39, 40)   red
                 'LH2' : { 'heep_singles': 'rgba(127, 127, 127, 0.8)',
                           'heep_coin': 'rgba(227, 119, 194, 0.8)'},  
                 
                 'LD2' : { 'MF'       : 'rgba(148, 103, 189, 0.8)' ,   
                           'SRC'      : 'rgba(214, 39, 40, 0.8)'},
                 
                 'Be9' : { 'MF'       : 'rgba(148, 103, 189, 0.8)',   
                           'SRC'      : 'rgba(148, 103, 189, 0.8)'},
                 
                 'B10' : { 'MF'       : 'rgba(148, 103, 189, 0.8)',   
                           'SRC'      : 'rgba(148, 103, 189, 0.8)'},
                 
                 'B11' : { 'MF'       : 'rgba(148, 103, 189, 0.8)',   
                           'SRC'      : 'rgba(148, 103, 189, 0.8)'},
                
                 'C12_optics' : { 'optics'       : 'rgba(148, 103, 189, 0.8)'},
                 
                 'C12' : { 'MF'       : 'rgba(148, 103, 189, 0.8)',   
                           'SRC'      : 'rgba(148, 103, 189, 0.8)'},
                 
                 
                 'Ca40' : { 'MF'       : 'rgba(148, 103, 189, 0.8)',   
                            'SRC'      : 'rgba(148, 103, 189, 0.8)'},
                 
                 
                 'Ca48' : { 'MF'       : 'rgba(148, 103, 189, 0.8)',   
                            'SRC'      : 'rgba(148, 103, 189, 0.8)'},
                 
                 'Ti48' : { 'MF'       : 'rgba(148, 103, 189, 0.8)',   
                            'SRC'      : 'rgba(148, 103, 189, 0.8)'},
                 
                 'Fe54' : { 'MF'       : 'rgba(148, 103, 189, 0.8)',   
                            'SRC'      : 'rgba(148, 103, 189, 0.8)'},        
             },
             
             'pattern' : {
                 'LH2' : { 'heep_singles': '',
                           'heep_coin': ''},  
                 
                 'LD2' : { 'MF'       : '' ,  
                           'SRC'      : '/'},
                 
                 'Be9' : { 'MF'       : '' ,  
                           'SRC'      : '/'},
                 
                 'B10' : { 'MF'       : '' ,  
                           'SRC'      : '/'},
                 
                 'B11' : { 'MF'       : '' ,  
                           'SRC'      : '/'},
                 
                 'C12_optics' : { 'optics': '.'},
                 
                 'C12' : { 'MF'       : '' ,  
                           'SRC'      : '/'},
                 
                 'Ca40' : { 'MF'       : '' ,  
                            'SRC'      : '/'},
                 
                 'Ca48' : { 'MF'       : '' ,  
                            'SRC'      : '/'},
                 
                 'Ti48' : { 'MF'       : '' ,  
                            'SRC'      : '/'},  
                 
                 
                 'Fe54' : { 'MF'       : '', 
                            'SRC'      : '/'},  
                 
             },
             
             'linestyle' : {
                 'LH2' : { 'heep_singles': 'solid',
                           'heep_coin': 'dash'},  
                 
                 'LD2' : { 'MF'       : 'solid' ,  
                           'SRC'      : 'dash'},  

   
                 'Be9' : { 'MF'       : 'solid', 
                            'SRC'      : 'dash'},

                    
                 'B10' : { 'MF'       : 'solid', 
                            'SRC'      : 'dash'},

                    
                 'B11' : { 'MF'       : 'solid', 
                            'SRC'      : 'dash'},

                    
                 'C12_optics' : { 'optics'       : 'solid'},

                    
                 'C12' : { 'MF'       : 'solid', 
                            'SRC'      : 'dash'},

                    
                 'Ca40' : { 'MF'       : 'solid', 
                            'SRC'      : 'dash'},

                    
                 'Ca48' : { 'MF'       : 'solid', 
                            'SRC'      : 'dash'},

                    
                 'Ca48' : { 'MF'       : 'solid', 
                            'SRC'      : 'dash'},

                    
                 'Ti48' : { 'MF'       : 'solid', 
                            'SRC'      : 'dash'},

                    
                 'Fe54' : { 'MF'       : 'solid', 
                            'SRC'      : 'dash'},
                 
             },
}



fig = go.Figure()
for targ in cafe_dict['target_names']:
    for kin in cafe_dict['kinematic_study'][targ]:

        print('targ,kin ---> ', targ,',',kin)
        # set color, pattern and line style
        bar_color   = cafe_dict['color'][targ][kin]
        bar_pattern = cafe_dict['pattern'][targ][kin]
        line_style  = cafe_dict['linestyle'][targ][kin]
        
        #print(bar_color)
        
        # define selected dataframe @ selected  (targ,kin)
        df_select = df[(df['target'].str.contains(targ)) & (df['kin\nstudy'].str.contains(kin))]


        #print(df_select.shape[0])
        if(df_select.shape[0]>0 and df_select.shape[0]<2):
            
            # add bar chart
            fig.add_trace(
                
                go.Bar(x=df_select['run_center'], y=df_select['BCM4A\ncharge\n[mC]'], width=df_select['run_len_ms'],
                       name="%s, %s" % (targ, kin), marker = {'color' : bar_color}, marker_pattern_shape=bar_pattern, 

                       #hovertext = "%s" % df_select['run\nnumber']
                           hovertemplate="run_number    :%s<br>"
                                         "target        :%s<br>"
                                         "kin_study     :%s<br>"
                                         "start_of_run  :%s<br>"
                                         "end_of_run    :%s<br>"
                                         "run_length [sec] :%s<br>"
                                         "beam_time  [sec] :%s<br>"
                                         "beam_current [uA] :%s<br>"
                                         "beam_charge  [mC] :%s<br>"
                                         "<extra></extra>" %
                       (
                           df_select['run\nnumber'].to_string(index=False),
                           df_select['target'].to_string(index=False),
                           df_select['kin\nstudy'].to_string(index=False),
                           df_select['start_run'].to_string(index=False),
                           df_select['end_run'].to_string(index=False),
                           df_select['run_len'].to_string(index=False),
                           df_select['beam_on_target\n[sec]'].to_string(index=False),                          
                           df_select['BCM4A\ncurrent\n[uA]'].to_string(index=False),
                           df_select['BCM4A\ncharge\n[mC]'].to_string(index=False),
                           
                       )
                       
                ), #end go.Bar
                

            
            ) # end add_trace


        else:

            cnt = 0 # counter
            for (index_label, row_series) in df_select.iterrows():

                # need single dataframe values to be type list for plotting
                x_list = []
                y_list = []
                w_list = []
                x_list.append(df_select['run_center'][index_label])
                y_list.append(df_select['BCM4A\ncharge\n[mC]'][index_label])
                w_list.append(df_select['run_len_ms'][index_label])
                
                if cnt==0:
                    showlegend_flag = True
                else:
                    showlegend_flag = False

                # we dont want to keep track of accumulated charge for hydrogen elastics as these will be maybe 1-2 runs ONLY
                if(targ!='LH2'):
                    fig.add_trace(
                        go.Scatter(x=df_select['run_center'], y=df_select['cumulative_charge'], mode='markers+lines', marker=dict(color=bar_color), line=dict(dash=line_style), showlegend=False,
                                   hovertemplate = 'total_charge: %{y:.3f} [mC]<extra></extra>'
                                   ),
                    )
                
                fig.add_trace(
                    go.Bar(x=x_list, y=y_list, width=w_list,
                           name="%s, %s" % (targ, kin), legendgroup='%s_%s' % (targ, kin), marker = {'color' : bar_color}, marker_pattern_shape=bar_pattern,


                           #hovertext = "%s" % df_select['run\nnumber'][index_label],
                           hovertemplate="run_number    :%s<br>"
                                         "target        :%s<br>"
                                         "kin_study     :%s<br>"
                                         "start_of_run  :%s<br>"
                                         "end_of_run    :%s<br>"
                                         "run_length [sec] :%s<br>"
                                         "beam_time  [sec] :%s<br>"                                       
                                         "beam_current [uA] :%s<br>"
                                         "beam_charge  [mC] :%s<br>"
                                         "<extra></extra>" %
                           (
                               df_select['run\nnumber'][index_label],
                               df_select['target'][index_label],
                               df_select['kin\nstudy'][index_label],
                               df_select['start_run'][index_label],
                               df_select['end_run'][index_label],
                               df_select['run_len'][index_label],
                               df_select['beam_on_target\n[sec]'][index_label],                
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

#last_x = df.groupby(['target', 'kin\nstudy']).last()['run_center']
#last_y = df.groupby(['target', 'kin\nstudy']).last()['cumulative_charge']


#cnt=0
#for idx, val in last_y.items():
#    print('last_x.shape: ',last_x.shape)
#    print('last_y.shape: ',last_y.shape)
#    fig.add_annotation(x=last_x[cnt], y=last_y[cnt] + last_y[cnt]*0.15, xref="x", yref="y",
#                       text=f"<b>total_charge: %s  mC</b>" %last_y[cnt], showarrow=False,
#                       font=dict(
#                           family="Arial, sans-serif",
#                           color='black',
#                           size=12),
#                       bgcolor="white"
#    )
#    cnt=cnt+1


fig.update_layout(legend_title_text = "CaFe Configuration", title={'text':'CaFe Run Summary', 'x':0.5},  font=dict(size=14))
fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="Charge [mC]")
#fig.update_layout(hovermode="x unified")



#---------------------------------------
#
#  Make Plots  MF, SRC related quantities with time
#
#---------------------------------------

fig2 = px.scatter(df_cafe, x="run_center", y="counts_per_mC", color="target", facet_col="kin\nstudy")

fig2.update_layout( title={'text':'Charge Normalized Counts', 'x':0.5},  font=dict(size=14), yaxis_title="Counts / mC")
# do not use the same y scale
fig2.update_yaxes(matches=None)
fig2.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
fig2.update_traces(mode="markers+lines", hovertemplate=None)
fig2.update_layout(hovermode="x unified")


fig3 = px.scatter(df_cafe, x="run_center", y="real_rates", color="target", facet_col="kin\nstudy")
fig3.update_layout( title={'text':'Real Count Rates', 'x':0.5},  font=dict(size=14), yaxis_title="Count Rate [Hz]")
fig3.update_yaxes(matches=None)
fig3.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
fig3.update_traces(mode="markers+lines", hovertemplate=None)
fig3.update_layout(hovermode="x unified")


fig4 = px.scatter(df_cafe, x="run_center", y="beam_eff", color="target", facet_col="kin\nstudy")
fig4.update_layout( title={'text':'Beam Efficiency', 'x':0.5},  font=dict(size=14), yaxis_title="efficiency")
fig4.update_yaxes(matches=None)
fig4.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
fig4.update_traces(mode="markers+lines", hovertemplate=None)
fig4.update_layout(hovermode="x unified")


with open('index.html', 'w') as f:
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig2.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig3.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig4.to_html(full_html=False, include_plotlyjs='cdn'))
