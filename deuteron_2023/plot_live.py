import pandas as pd
import plotly_express as px
from plotly.subplots import make_subplots
import datetime
import sys
import chart_studio
import chart_studio.plotly as charts
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import pandas as pandasForSortingCSV
import chart_studio.tools as tls

#user argument (deep or heep)
kin_study = sys.argv[1]


# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)


# define the timestamps for the entire experiment
exp_start = datetime(2023,2,24).timestamp()
exp_end = datetime(2023,3,20).timestamp()

#-------------------------------------------------------
# Get deuteron SIMC stats goals (for plotting as reference)
#-------------------------------------------------------



# convert csv to dataframe 
df = pandasForSortingCSV.read_csv("./deut-2023_runlist.csv", comment='#') 

# sort data frame based on 1st column (run number)
df.sort_values(df.columns[0], 
                    axis=0,
                    inplace=True)

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

#beam-on-target cumulative sum
beam_csum = df.groupby(['target', 'kin_study', 'setting'])['beam_on_target'].cumsum()
df['cumulative_time'] = beam_csum / 3600. # convert from sec to hours


# ---- calculate percent completion of data-----
 
# calculate percent of charge completed
df['charge_perct_completed'] = df['cumulative_charge'] / df['simc_charge_goal'] * 100.

# calculate percent of counts completed
df['counts_perct_completed'] = df['cumulative_counts'] / df['simc_counts_goal'] * 100.

# calculate percentage of beam-on-target hours completed for each setting
#df['beam_perc_completed'] = df['cumulative_time'] / 

#--------------------------------------------------

# calculate counts/mC
df['counts_per_mC'] =  df['real_counts'] / charge
df['counts_per_mC_err'] =  df['real_counts'] / (np.sqrt( df['real_counts'] ) * charge ) * 0.001
print('count_per_mC_err = ', df['counts_per_mC_err'])

# calculate beam efficiency
df['beam_eff'] = df['beam_on_target'] /df['run_len']




# re-define dataframe for special tasks
if kin_study=="heep":
    title='h(e,e\'p) delta scan'
    my_df = df[ df["kin_study"].str.contains("heep") ]

elif kin_study=="deep":
    title='d(e,e\'p) '
    my_df = df[ df["kin_study"].str.contains("deep") ]
    
elif kin_study=="lumi":
    title='d(e,e\'p) luminosity scan'
    my_df = df[ df["kin_study"].str.contains("lumi") ]
    
else:
    print('\n Please enter one of the following arguments: heep, deep, lumi\n'
          'e,g, ipython plot_line.py heep \n')

    exit()


#convert rates to counts per hour
my_df["real_rate"] = my_df["real_rate"] * 3600. # convert to counts / hour
my_df['beam_on_target'] = my_df['beam_on_target'] / 3600. # convert sec. to hours


#---------------------------------------
#
#  Make Plots  
#
#---------------------------------------


if not my_df.empty:
    print('Deuteron DataFrame is NOT empty!')

    print(my_df)
    hover_template = ""

    
    
    fig2 = px.scatter(my_df, x="run_center", y="counts_per_mC", error_y="counts_per_mC_err", color="setting", facet_col="kin_study", hover_name="run")
    fig2.update_layout( title={'text':'Charge Normalized Counts', 'x':0.5},  font=dict(size=14), yaxis_title="Counts / mC")
    fig2.update_yaxes(matches=None)
    fig2.update_xaxes(matches=None)
    fig2.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig2.update_traces( marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines" )
    #fig2.update_xaxes(tickangle=0)
    #fig2.update_layout(hovermode="x")

    
    fig3 = px.scatter(my_df, x="run_center", y="real_rate", color="setting", hover_name="run",  facet_col="kin_study", hover_data={       'real_rate':':%.2f',
                                                                                                                                           'run_start':(':%s', my_df['start_run'].astype("string")),
                                                                                                                                          'run_end':(':%s', my_df['end_run'].astype("string")),
                                                                                                                                          'beam_current [uA] (this run)':(':%.2f', my_df['BCM4A_current'])})
    fig3.update_layout( title={'text':'Real Count Rates', 'x':0.5},  font=dict(size=14), yaxis_title="Count Rate [per hour]")
    fig3.update_yaxes(matches=None)
    fig3.update_xaxes(matches=None)
    fig3.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig3.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines")
    #fig3.update_layout(hovermode="x unified")
    
    
    fig4 = px.scatter(my_df, x="run_center", y="beam_eff", color="setting", hover_name="run")
    fig4.update_layout( title={'text':'Beam Efficiency', 'x':0.5},  font=dict(size=14), yaxis_title="efficiency")
    fig4.update_yaxes(matches=None)
    fig4.update_xaxes(matches=None)
    fig4.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig4.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines")
    #fig4.update_layout(hovermode="x unified")
    
    

    # working version
    fig5 = px.scatter(my_df, x="run_center", y="cumulative_charge", color="setting", hover_name="run", facet_col="kin_study", hover_data={
        'run_start':(':%s', my_df['start_run'].astype("string")),
        'run_end':(':%s', my_df['end_run'].astype("string")),
        'charge (this run) [mC]':(':.3f', my_df['BCM4A_charge']),
        'cumulative_charge [mC]':(':.2f', my_df['cumulative_charge']),
        'statistical_goal [mC]':(':.3f', my_df['simc_charge_goal']),
        'percentage_completed [%]':(':.2f', my_df['charge_perct_completed'])})
    
    fig5.update_layout( title={'text':'Accumulated Charge', 'x':0.5},  font=dict(size=14), yaxis_title="BCM4A Charge [mC]")
    fig5.update_yaxes(matches=None)
    fig5.update_xaxes(matches=None)
    fig5.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig5.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines")
    

    
    
    

    fig8 = px.scatter(my_df, x="run_center", y="cumulative_counts", color="setting",  hover_name="run", facet_col="kin_study", hover_data={               'cumulative_counts':':.2f',
                                                                                                                                                           'run_start':(':%s', my_df['start_run'].astype("string")),
                                                                                                                                                        'run_end':(':%s', my_df['end_run'].astype("string")),
                                                                                                                                                          'counts (this run)':(':i', my_df['real_counts']),
                                                                                                                                                          'count rate [per hour] (this run)':(':%.2f', my_df['real_rate']),
                                                                                                                                                          'beam_current [uA] (this run)':(':%.2f', my_df['BCM4A_current']),
                                                                                                                                                         'statistical_goal':(':i', my_df['simc_counts_goal']),
                                                                                                                                                           'percentage_completed [%]':(':.2f', my_df['counts_perct_completed']),
                                                                                                                                           })
    
    fig8.update_layout( title={'text':'Total A(e,e\'p) Counts', 'x':0.5},  font=dict(size=14), yaxis_title="Total Counts")
    fig8.update_yaxes(matches=None)
    fig8.update_xaxes(matches=None)
    fig8.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig8.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines")

    

    fig8.update_layout(legend_title_text = "Kinematic Configuration", title={'text':title+' scan Run Summary (Feb 24 - Mar 30, 2023) <br> Total  A(e,e\'p) Counts', 'x':0.5, 'y':0.98},  font=dict(size=12), yaxis_title="Total Counts")




    
    fig9 = px.scatter(my_df, x="run_center", y="cumulative_time", color="setting",  hover_name="run", facet_col="kin_study", hover_data={               'cumulative_time':':.3f',
                                                                                                                                                        'run_start':(':%s', my_df['start_run'].astype("string")),
                                                                                                                                                        'run_end':(':%s', my_df['end_run'].astype("string")),
                                                                                                                                                          'beam_on_time [hrs] (this run)':(':.2f', my_df['beam_on_target']),
                                                                                                                                                          'count rate [per hr] (this run)':(':%.2f', my_df['real_rate']),
                                                                                                                                                          'beam_current [uA] (this run)':(':%.2f', my_df['BCM4A_current']),
                                                                                                                                                         'statistical_goal':(':i', my_df['simc_counts_goal']),
                                                                                                                                                           'percentage_completed [%]':(':.2f', my_df['counts_perct_completed']),
                                                                                                                                           })
    
    fig9.update_layout( title={'text':'Total Beam-on-Target Time', 'x':0.5},  font=dict(size=14), yaxis_title="Total Time [hrs]")
    fig9.update_yaxes(matches=None)
    fig9.update_xaxes(matches=None)
    fig9.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig9.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines")



    fig9 = px.scatter(my_df, x="run_center", y="cumulative_time", color="setting",  hover_name="run", facet_col="kin_study", hover_data={               'cumulative_time':':.3f',
                                                                                                                                                        'run_start':(':%s', my_df['start_run'].astype("string")),
                                                                                                                                                        'run_end':(':%s', my_df['end_run'].astype("string")),
                                                                                                                                                          'beam_on_time [hrs] (this run)':(':.2f', my_df['beam_on_target']),
                                                                                                                                                          'count rate [per hr] (this run)':(':%.2f', my_df['real_rate']),
                                                                                                                                                          'beam_current [uA] (this run)':(':%.2f', my_df['BCM4A_current']),
                                                                                                                                                         'statistical_goal':(':i', my_df['simc_counts_goal']),
                                                                                                                                                           'percentage_completed [%]':(':.2f', my_df['counts_perct_completed']),
                                                                                                                                           })
    
    fig9.update_layout( title={'text':'Total Beam-on-Target Time', 'x':0.5},  font=dict(size=14), yaxis_title="Total Time [hrs]")
    fig9.update_yaxes(matches=None)
    fig9.update_xaxes(matches=None)
    fig9.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig9.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines")



    fig10 = px.scatter(my_df, x="run_center", y="T6_tLT", color="setting",  hover_name="run", facet_col="kin_study", hover_data={                       'T6_tLT':':.3f',
                                                                                                                                                        'beam_current [uA]':(':.3f', my_df['BCM4A_current']),
                                                                                                                                                        'run_start':(':%s', my_df['start_run'].astype("string")),
                                                                                                                                                        'run_end':(':%s', my_df['end_run'].astype("string")),
                                                                                                                                                    
                                                                                                                                 })
    
    fig10a = px.scatter(my_df, x="run_center", y="HMS_TrkEff", color="setting",  hover_name="run", facet_col="kin_study", hover_data={                  'HMS_TrkEff':':.3f',
                                                                                                                                                        'beam_current [uA]':(':.3f', my_df['BCM4A_current']),
                                                                                                                                                        'run_start':(':%s', my_df['start_run'].astype("string")),
                                                                                                                                                        'run_end':(':%s', my_df['end_run'].astype("string")),
                                                                                                                                                    
                                                                                                                                      })
    
    fig10.add_trace(fig10a.data[0])
    fig10.add_trace(fig10a.data[1])
    fig10.add_trace(fig10a.data[2])
    fig10.update_layout(showlegend=False)


    fig10b = px.scatter(my_df, x="run_center", y="SHMS_TrkEff", color="setting",  hover_name="run", facet_col="kin_study", hover_data={                  'SHMS_TrkEff':':.3f',
                                                                                                                                                         'beam_current [uA]':(':.3f', my_df['BCM4A_current']),
                                                                                                                                                        'run_start':(':%s', my_df['start_run'].astype("string")),
                                                                                                                                                        'run_end':(':%s', my_df['end_run'].astype("string")),
                                                                                                                                                    
                                                                                                                                 })
    fig10b.update_layout(showlegend=False)
    fig10.add_trace(fig10b.data[0])
    fig10.add_trace(fig10b.data[1])
    fig10.add_trace(fig10b.data[2])
    
        
    fig10.update_layout( title={'text':'Efficiencies', 'x':0.5},  font=dict(size=14), yaxis_title="Efficiency")
    fig10.update_yaxes(matches=None)
    fig10.update_xaxes(matches=None)
    fig10.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig10.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines")

path_to_index=kin_study+'/index.html'

# Write to .html
with open(path_to_index, 'w') as f:
    #f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

    if not my_df.empty:
        print('not empty')
        f.write(fig8.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig5.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig9.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig3.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig4.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig10.to_html(full_html=False, include_plotlyjs='cdn'))

    else:
        print('empty')


