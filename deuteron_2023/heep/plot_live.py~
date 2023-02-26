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
exp_start = datetime(2023,2,20).timestamp()
exp_end = datetime(2023,3,20).timestamp()

#-------------------------------------------------------
# Get CaFe deuteron SIMC stats goals (for plotting as reference)
#-------------------------------------------------------
'''
def get_simc_ref(string=''):

    simc_parm_file_path = '../../cafe_online_replay/UTILS_CAFE/inp/set_basic_simc_param.inp'
    simc_parm_file = open(simc_parm_file_path)

    val = 0
    
    for line in simc_parm_file:
        if (line[0]=="#"): continue;

        if string in line:
            val = float((line.split("=")[1]).strip())
    return val
'''



# convert csv to dataframe 
#df = pd.read_csv("../../cafe_online_replay/UTILS_CAFE/runlist/cafe-2022_runlist.csv") 
df = pd.read_csv("./deut-2023_runlist.csv", comment='#') 

run     = df['run']
charge = df['BCM4A_charge'] # [mC]
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

# add simc columns of 1) total counts goal, 2) luminosity goal, 3) norm-luminosity goal: grouped based on (target, kin_study), 


# calculate cumulative quantities
charge_csum = df.groupby(['target', 'kin_study', 'setting'])['BCM4A_charge'].cumsum() 

df['cumulative_charge'] = charge_csum 

print(df['cumulative_charge'])

#calculate total counts cumulative 
counts_csum = df.groupby(['target', 'kin_study', 'setting'])['real_counts'].cumsum() 
df['cumulative_counts'] = counts_csum


# ---- calculate percent completion of data-----
 
# calculate percent of charge completed
df['charge_perct_completed'] = df['cumulative_charge'] / df['simc_charge_goal'] * 100.

# calculate percent of counts completed
df['counts_perct_completed'] = df['cumulative_counts'] / df['simc_counts_goal'] * 100.


#--------------------------------------------------

# calculate counts/mC
df['counts_per_mC'] =  df['real_counts'] / charge
df['counts_per_mC_err'] =  df['real_counts'] / (np.sqrt( df['real_counts'] ) * charge ) * 0.001
print('count_per_mC_err = ', df['counts_per_mC_err'])

# calculate beam efficiency
df['beam_eff'] = df['beam_on_target'] /df['run_len']


# re-define dataframe for special tasks

# 1) filter out (use only) deuteron (for tracking quantities over entire run period) : heep will only be tracked in the Run Summary plot
#df_deut = df[df["kin\nstudy"].str.contains("deep")]
df_deut = df


target_dict = {'target_names' : {'dummy', 'LH2', 'LD2'},
               
               'kinematic_study' : {
                   'dummy': {'heep_singles', 'heep_coin', 'deep'},
                   'LH2' : {'heep_singles', 'heep_coin'},
                   'LD2' : {'deep'},
                   
               },
               
               'setting' : {
                   'dummy' : {'NA'},
                   'LH2' : {'delta_scan_-8','delta_scan_-4', 'delta_scan_0', 'delta_scan_+4', 'delta_scan_+8', 'delta_scan_+12'},
                   'LD2' : {'120', '580', '800', '900'} 
               },
             
               'color' : {
                 
                 # rgb(31, 119, 180) muted blue
                 # rgb(227, 119, 194) pink
                 # rgb(188, 189, 34)  lime
                 # rgb(23, 190, 207)  blue
                 # rgb(255, 127, 14)  orange
                 # rgb(44, 160, 44)   green
                 # rgb(148, 103, 189) purple
                 # rgb(214, 39, 40)   red
                 
                 'dummy' : {

                     'heep_singles'      : {
                         
                         'NA' : 'rgba(255,248,220, 0.8)' ,          # cornsilk
                     },

                     'heep_coin'          : {
                         'NA' : 'rgba(255,248,220, 0.8)' ,
                     },
                     
                    'deep'              : {
                        'NA' : 'rgba(255,248,220, 0.8)',
                    },
                 },

                 'LH2' : {

                     'heep_singles'    : {

                     'delta_scan_-4' : 'rgba(127, 127, 127, 0.8)',   # gray
                     'delta_scan_+4' : 'rgba(127+5, 127+5, 127+5, 0.8)',   # gray+5

                     },
                           
                           
                     'heep_coin'   : {

                    'delta_scan_-4' :  'rgba(148, 103, 189,   0.8)',  # purple
                    'delta_scan_+4' :  'rgba(31, 119, 180,   0.8)',  # muted blue
                         
                     },
                 },
                     
                 'LD2' : {


                     'deep'       : {
                         
                           '120' :'rgba(227, 119, 194, 0.8)' ,          # pink
                           '580' :'rgba(188, 189, 34, 0.8)' ,          # lime
                           '800' :'rgba(255, 127, 14, 0.8)' ,          # orange
                           '900' :'rgba(148, 103, 189, 0.8)' ,          # purple
                     
                        },
                  },
                
               }
               
            }



'''
fig = go.Figure()
for targ in target_dict['target_names']:  
    for kin in target_dict['kinematic_study'][targ]:
        for iset in target_dict['setting'][targ]:
        
            #print('targ,kin,iset ---> ', targ,',',kin,',',iset)
            # set color, pattern and line style
            bar_color   = target_dict['color'][targ][kin][iset]
            
            #print(bar_color)
            
            # define selected dataframe @ selected  (targ,kin)
            df_select = df[(df['target'].str.contains(targ)) & (df['kin\nstudy'].str.contains(kin)) & (df['setting']==iset)]

            mycustomdata = np.stack((df_select['cumulative_counts'], df_select['counts_perct_completed'], df_select['charge_perct_completed'],  df_select['target'],
                                     df_select['kin\nstudy'], df_select['setting']), axis=-1)


            print('targ,kin,setting, cumulative_counts ---> ', targ,',',kin,',',iset,',',df_select['cumulative_counts'])
       
            #print(df_select.shape[0])
            #if(df_select.shape[0]>0 and df_select.shape[0]<5):

    

                #print('setting----->',df_select['setting'])

            # add bar chart
            
            fig.add_trace(

                    
                go.Bar(x=df_select['run_center'], y=df_select['BCM4A\ncharge\n[mC]'], width=df_select['run_len_ms'],
                       name="%s, %s, %s" % (targ, kin, iset), marker = {'color' : bar_color}, 

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
                    print('kin -->', kin)
                    if kin!='heep_singles':
                        if kin!='optics':
                            fig.add_trace(
                                go.Scatter(x=df_select['run_center'], y=df_select['cumulative_charge'], mode='markers+lines', customdata = mycustomdata, marker=dict(color=bar_color), showlegend=False,
                                           hovertemplate = '<br>%{customdata[3]:%s}, %{customdata[4]:%s}'+
                                           '<br>total_charge: %{y:.3f} [mC]' +
                                           '<br>charge_percent_completed: %{customdata[2]:.3f}'+
                                           '<br>total_counts: %{customdata[0]:.1f}'+
                                           '<br>counts_percent_completed: %{customdata[1]:.3f}'
                                           '<extra></extra>',
                                           ),
                            )
                            
                            
                            fig.add_trace(
                                go.Bar(x=x_list, y=y_list, width=w_list,
                                       name="%s, %s, %s" % (targ, kin, iset), legendgroup='%s_%s_%s' % (targ, kin, iset), marker = {'color' : bar_color},
                                       
                                       
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


fig.update_layout(legend_title_text = "Deuteron Configuration", title={'text':'Online Deuteron Run Summary (Feb - March 2022)', 'x':0.5},  font=dict(size=14))
fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="Charge [mC]")

#fig.update_layout(hovermode="x unified")


'''
            
#---------------------------------------
#
#  Make Plots  MF, SRC related quantities with time
#
#---------------------------------------


if not df_deut.empty:
    print('Deuteron DataFrame is NOT empty!')

    print(df_deut)
    hover_template = ""

    
    
    fig2 = px.scatter(df_deut, x="run_center", y="counts_per_mC", error_y="counts_per_mC_err", color="setting", facet_col="kin_study", hover_name="run")
    fig2.update_layout( title={'text':'Charge Normalized Counts', 'x':0.5},  font=dict(size=14), yaxis_title="Counts / mC")
    fig2.update_yaxes(matches=None)
    fig2.update_xaxes(matches=None)
    fig2.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig2.update_traces( marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines" )
    #fig2.update_xaxes(tickangle=0)
    #fig2.update_layout(hovermode="x")

    
    fig3 = px.scatter(df_deut, x="run_center", y="real_rate", color="setting", hover_name="run",  facet_col="kin_study", hover_data={       'real_rate':':%.2f',
                                                                                                                                                     'beam_current [uA] (this run)':(':%.2f', df_deut['BCM4A_current'])})
    fig3.update_layout( title={'text':'Real Count Rates', 'x':0.5},  font=dict(size=14), yaxis_title="Count Rate [Hz]")
    fig3.update_yaxes(matches=None)
    fig3.update_xaxes(matches=None)
    fig3.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig3.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines")
    #fig3.update_layout(hovermode="x unified")
    
    
    fig4 = px.scatter(df_deut, x="run_center", y="beam_eff", color="setting", hover_name="run")
    fig4.update_layout( title={'text':'Beam Efficiency', 'x':0.5},  font=dict(size=14), yaxis_title="efficiency")
    fig4.update_yaxes(matches=None)
    fig4.update_xaxes(matches=None)
    fig4.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig4.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines")
    #fig4.update_layout(hovermode="x unified")
    
    

    # working version
    fig5 = px.scatter(df_deut, x="run_center", y="cumulative_charge", color="setting", hover_name="run", facet_col="kin_study", hover_data={'charge (this run) [mC]':(':.3f', df_deut['BCM4A_charge']),
                                                                                                                             'cumulative_charge [mC]':(':.2f', df_deut['cumulative_charge']),
                                                                                                                             'statistical_goal [mC]':(':.3f', df_deut['simc_charge_goal']),
                                                                                                                             'percentage_completed [%]':(':.2f', df_deut['charge_perct_completed'])})
    fig5.update_layout( title={'text':'Accumulated Charge', 'x':0.5},  font=dict(size=14), yaxis_title="BCM4A Charge [mC]")
    fig5.update_yaxes(matches=None)
    fig5.update_xaxes(matches=None)
    fig5.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig5.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines")
    

    
    
    

    fig8 = px.scatter(df_deut, x="run_center", y="cumulative_counts", color="setting",  hover_name="run", facet_col="kin_study", hover_data={ 'cumulative_counts':':.2f',
                                                                                                                                                    'counts (this run)':(':i', df_deut['real_counts']),
                                                                                                                                                     'count rate [Hz] (this run)':(':%.2f', df_deut['real_rate']),
                                                                                                                                                     'beam_current [uA] (this run)':(':%.2f', df_deut['BCM4A_current']),
                                                                                                                                                    'statistical_goal':(':i', df_deut['simc_counts_goal']),
                                                                                                                                                     'percentage_completed [%]':(':.2f', df_deut['counts_perct_completed'])})
    
    fig8.update_layout( title={'text':'Total A(e,e\'p) Counts', 'x':0.5},  font=dict(size=14), yaxis_title="Total Counts")
    fig8.update_yaxes(matches=None)
    fig8.update_xaxes(matches=None)
    fig8.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig8.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines")

    

fig8.update_layout(legend_title_text = "Kinematic Configuration", title={'text':'d(e,e\'p) Run Summary (Feb 24 - Mar 30, 2023) <br> Total  A(e,e\'p) Counts', 'x':0.5, 'y':0.98},  font=dict(size=12), yaxis_title="Total Counts")


# Write to .html
with open('index.html', 'w') as f:
    #f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

    if not df_deut.empty:
        print('not empty')
        f.write(fig8.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig3.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig4.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig5.to_html(full_html=False, include_plotlyjs='cdn'))
        #f.write(fig6.to_html(full_html=False, include_plotlyjs='cdn'))
        #f.write(fig7.to_html(full_html=False, include_plotlyjs='cdn'))
    else:
        print('empty')
