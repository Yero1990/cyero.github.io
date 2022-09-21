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

#-------------------------------------------------------
# Get CaFe SIMC stats goals (for plotting as reference)
#-------------------------------------------------------

def get_simc_ref(string=''):

    simc_parm_file_path = '../../cafe_online_replay/UTILS_CAFE/inp/set_basic_simc_param.inp'
    simc_parm_file = open(simc_parm_file_path)

    val = 0
    
    for line in simc_parm_file:
        if (line[0]=="#"): continue;

        if string in line:
            val = float((line.split("=")[1]).strip())
    return val




# convert csv to dataframe 
#df = pd.read_csv("../../cafe_online_replay/UTILS_CAFE/runlist/cafe-2022_runlist.csv") 
df = pd.read_csv("./cafe-2022_runlist.csv") 

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

# add simc columns of 1) total counts goal, 2) luminosity goal, 3) norm-luminosity goal: grouped based on (target, kin_study), 


# calculate cumulative quantities
charge_csum = df.groupby(['target', 'kin\nstudy'])['BCM4A\ncharge\n[mC]'].cumsum() 

df['cumulative_charge'] = charge_csum 

print(df['cumulative_charge'])

# convert dtype object to float (for some unknown reason, for this column, when np.nan is used, the dtype changes from float to object, so Im changing back)
df['integrated\nluminosity\n[fb^-1]'] = pd.to_numeric(df['integrated\nluminosity\n[fb^-1]'], errors='coerce')
luminosity_csum = df.groupby(['target', 'kin\nstudy'])['integrated\nluminosity\n[fb^-1]'].cumsum()
df['cumulative_luminosity'] = luminosity_csum

df['lumiNorm_counts[fb]'] = pd.to_numeric(df['lumiNorm_counts[fb]'], errors='coerce')
lumiNorm_csum = df.groupby(['target', 'kin\nstudy'])['lumiNorm_counts[fb]'].cumsum()
df['cumulative_lumiNorm'] = lumiNorm_csum


# create a new column in the dataframe which will be the addition of columns: heep_singles, heep_coin, MF_real, SRC_real into a single column
# NOTE: the columns can be added safely (will not actually mix different kinematics), e.g., no chance of mixing heep_coin with MF_real counts, etc. as one of these will be NaN and the other will NOT.
df['real_counts'] = df.fillna(0)['heep_singles\ncounts'] + df.fillna(0)['heep_coin\ncounts'] + df.fillna(0)['MF_real\ncounts'] + df.fillna(0)['SRC_real\ncounts']
df['real_rates'] = df.fillna(0)['heep_singles\nrates [Hz]'] + df.fillna(0)['heep_coin\nrates [Hz]'] + df.fillna(0)['MF_real\nrates [Hz]'] + df.fillna(0)['SRC_real\nrates [Hz]']

#calculate total counts cumulative 
counts_csum = df.groupby(['target', 'kin\nstudy'])['real_counts'].cumsum() 
df['cumulative_counts'] = counts_csum


# ---- calculate percent completion of data-----
 
# calculate percent of charge completed
df['charge_perct_completed'] = df['cumulative_charge'] / df['simc_charge_goal\n[mC]'] * 100.

# calculate percent of integrated luminosity completed
df['lumi_perct_completed'] = df['cumulative_luminosity'] / df['simc_integrated\nluminosity\n[fb^-1]'] * 100.

# calculate percent of integrated luminosity normalized by total counts completed
df['lumiNorm_perct_completed'] = df['cumulative_lumiNorm'] / df['simc_lumiNorm_counts[fb]'] * 100.

# calculate percent of counts completed
df['counts_perct_completed'] = df['cumulative_counts'] / df['simc_counts_goal'] * 100.


#--------------------------------------------------

# calculate counts/mC
df['counts_per_mC'] =  df['real_counts'] / charge

# calculate beam efficiency
df['beam_eff'] = df['beam_on_target\n[sec]'] /df['run_len']



# re-define dataframe for special tasks

# 1) filter out (use only) MF and SRC (for tracking quantities over entire run period) : heep will only be tracked in the Run Summary plot
df_cafe = df[df["kin\nstudy"].str.contains("MF") | df["kin\nstudy"].str.contains("SRC")]



cafe_dict = {'target_names' : {'dummy', 'LH2', 'LD2', 'Be9', 'B10', 'B11', 'C12_optics', 'C12', 'Ca40', 'Ca48', 'Ti48', 'Fe54'},
             
             'kinematic_study' : {
                 'dummy': {'MF', 'SRC'},
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
                 # rgb(188, 189, 34)  lime
                 # rgb(23, 190, 207)  blue
                 # rgb(255, 127, 14)  orange
                 # rgb(44, 160, 44)   green
                 # rgb(148, 103, 189) purple
                 # rgb(214, 39, 40)   red
                 
                 'dummy' : {'MF'      : 'rgba(255,248,220, 0.8)' ,          # cornsilk
                           'SRC'      : 'rgba(255,248,220, 0.8)'},

                 'LH2' : { 'heep_singles': 'rgba(127, 127, 127, 0.8)',   # gray
                           'heep_coin'   : 'rgba(155, 135, 12,   0.8)'},  # yellow  
                 
                 'LD2' : { 'MF'       : 'rgba(48,128,20, 0.8)' ,          # sapgreen
                           'SRC'      : 'rgba(48,128,20, 0.8)'},
                 
                 'Be9' : { 'MF'       : 'rgba(255,140,0, 0.8)',     # dark orange   
                           'SRC'      : 'rgba(255,140,0, 0.8)'},
                 
                 'B10' : { 'MF'       : 'rgba(255,0,255, 0.8)',     # magenta   
                           'SRC'      : 'rgba(255,0,255, 0.8)'},
                 
                 'B11' : { 'MF'       : 'rgba(148,0,211, 0.8)',   # dark violet 
                           'SRC'      : 'rgba(148,0,211, 0.8)'},
                
                 'C12_optics' : { 'optics'       : 'rgba(230,230,250, 0.8)'},  # lavender
                 
                 'C12' : { 'MF'       : 'rgba(0,191,255, 0.8)',    # deep sky blue   
                           'SRC'      : 'rgba(0,191,255, 0.8)'},
                 
                 
                 'Ca40' : { 'MF'       : 'rgba(255,0,0, 0.8)',    # red   
                            'SRC'      : 'rgba(255,0,0, 0.8)'},
                 
                 
                 'Ca48' : { 'MF'       : 'rgba(0,0,255, 0.8)',    # blue   
                            'SRC'      : 'rgba(0,0,255, 0.8)'},
                 
                 'Ti48' : { 'MF'       : 'rgba(210,105,30, 0.8)',  # chocolae   
                            'SRC'      : 'rgba(210,105,30, 0.8)'},
                 
                 'Fe54' : { 'MF'       : 'rgba(0,255,0, 0.8)',    # green (lime)  
                            'SRC'      : 'rgba(0,255,0, 0.8)'},        
             },
             
             'pattern' : {
                 'dummy' : {'MF'       : '' ,  
                           'SRC'      : '/'},
                 
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
                 'dummy' : { 'MF'       : 'solid' ,  
                            'SRC'      : 'dash'},
                 
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
                print('kin -->', kin)
                if kin!='heep_singles':
                    if kin!='optics':
                        fig.add_trace(
                            go.Scatter(x=df_select['run_center'], y=df_select['cumulative_charge'], mode='markers+lines', marker=dict(color=bar_color), line=dict(dash=line_style), showlegend=False,
                                       hovertemplate = 'total_charge: %{y:.3f} [mC]  <extra></extra>'
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
                                         "Beam E [ GeV ]  : %.4f <br>"
                                         "SHMS P [GeV/c]  : %.3f <br>"
                                         "SHMS Angle [deg]: %.3f <br>"
                                         "HMS P [GeV/c]  : %.3f <br>"
                                         "HMS Angle [deg]: %.3f <br>"
                                         "run_length [sec] :%s<br>"
                                         "beam_time  [sec] :%s<br>"                                       
                                         "beam_current [uA] :%s<br>"
                                         "beam_charge  [mC] :%s<br>"
                                         "T1 pre-scale factor: %i <br>"
                                         "T1 scalers:  %.1f kHz    <br>"
                                         "T1 accepted: %.1f kHz    <br>"
                                         "T2 pre-scale factor: %i <br>"
                                         "T2 scalers:  %.1f kHz    <br>"
                                         "T2 accepted: %.1f kHz    <br>"
                                         "T3 pre-scale factor: %i <br>"
                                         "T3 scalers:  %.1f kHz    <br>"
                                         "T3 accepted: %.1f kHz    <br>"
                                         "T5 pre-scale factor: %i <br>"
                                         "T5 scalers:  %.1f kHz    <br>"
                                         "T5 accepted: %.1f kHz    <br>"
                                         "T5_tLT:      %.3f:      <br>"
                                         "HMS (e-) trk eff: %.3f <br>"
                                         "SHMS (e-) trk eff: %.3f <br>"
                                         "<extra></extra>" %
                           (
                               df_select['run\nnumber'][index_label],
                               df_select['target'][index_label],
                               df_select['kin\nstudy'][index_label],
                               df_select['start_run'][index_label],
                               df_select['end_run'][index_label],
                               df_select['beam\nenergy\n[GeV]'][index_label],
                               df_select['SHMS_P\n[GeV/c]'][index_label],
                               df_select['SHMS_Angle\n[deg]'][index_label],
                               df_select['HMS_P\n[GeV/c]'][index_label],
                               df_select['HMS_Angle\n[deg]'][index_label],
                               df_select['run_len'][index_label],
                               df_select['beam_on_target\n[sec]'][index_label],                
                               df_select['BCM4A\ncurrent\n[uA]'][index_label],
                               df_select['BCM4A\ncharge\n[mC]'][index_label],
                               df_select['PS1'][index_label],
                               df_select['T1\nscaler_rates\n[kHz]'][index_label],
                               df_select['T1\naccp_rates\n[kHz]'][index_label],
                               df_select['PS2'][index_label],
                               df_select['T2\nscaler_rates\n[kHz]'][index_label],
                               df_select['T2\naccp_rates\n[kHz]'][index_label],
                               df_select['PS3'][index_label],
                               df_select['T3\nscaler_rates\n[kHz]'][index_label],
                               df_select['T3\naccp_rates\n[kHz]'][index_label],                               
                               df_select['PS5'][index_label],
                               df_select['T5\nscaler_rates\n[kHz]'][index_label],
                               df_select['T5\naccp_rates\n[kHz]'][index_label],
                               df_select['T5_tLT'][index_label],
                               df_select['HMS\nTrkEff'][index_label],
                               df_select['SHMS\nTrkEff'][index_label],
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


fig.update_layout(legend_title_text = "CaFe Configuration", title={'text':'CaFe Run Summary (September 2022)', 'x':0.5},  font=dict(size=14))
fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="Charge [mC]")

#fig.update_layout(hovermode="x unified")



#---------------------------------------
#
#  Make Plots  MF, SRC related quantities with time
#
#---------------------------------------

if not df_cafe.empty:
    print('CaFe DataFrame is NOT empty!')
    
    hover_template = ""

    fig2 = px.scatter(df_cafe, x="run_center", y="counts_per_mC", color="target", facet_col="kin\nstudy", hover_name="run\nnumber")
    fig2.update_layout( title={'text':'Charge Normalized Counts', 'x':0.5},  font=dict(size=14), yaxis_title="Counts / mC")
    fig2.update_yaxes(matches=None)
    fig2.update_xaxes(matches=None)
    fig2.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig2.update_traces( marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines" )
    #fig2.update_xaxes(tickangle=0)
    #fig2.update_layout(hovermode="x")


    fig3 = px.scatter(df_cafe, x="run_center", y="real_rates", color="target", facet_col="kin\nstudy", hover_name="run\nnumber",  hover_data={       'real_rates':':%.2f',
                                                                                                                                                     'beam_current [uA] (this run)':(':%.2f', df_cafe['BCM4A\ncurrent\n[uA]'])})
    fig3.update_layout( title={'text':'Real Count Rates', 'x':0.5},  font=dict(size=14), yaxis_title="Count Rate [Hz]")
    fig3.update_yaxes(matches=None)
    fig3.update_xaxes(matches=None)
    fig3.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig3.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines")
    #fig3.update_layout(hovermode="x unified")
    
    
    fig4 = px.scatter(df_cafe, x="run_center", y="beam_eff", color="target", facet_col="kin\nstudy", hover_name="run\nnumber")
    fig4.update_layout( title={'text':'Beam Efficiency', 'x':0.5},  font=dict(size=14), yaxis_title="efficiency")
    fig4.update_yaxes(matches=None)
    fig4.update_xaxes(matches=None)
    fig4.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig4.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines")
    #fig4.update_layout(hovermode="x unified")
    
    
    fig5 = px.scatter(df_cafe, x="run_center", y="cumulative_charge", color="target", facet_col="kin\nstudy", hover_name="run\nnumber", hover_data={'cumulative_charge [mC]':(':.2f', df_cafe['cumulative_charge']),
                                                                                                                                                    'statistical_goal [mC]':(':.3f', df_cafe['simc_charge_goal\n[mC]']),
                                                                                                                                                    'percentage_completed [%]':(':.2f', df_cafe['charge_perct_completed'])})
    fig5.update_layout( title={'text':'Accumulated Charge', 'x':0.5},  font=dict(size=14), yaxis_title="BCM4A Charge [mC]")
    fig5.update_yaxes(matches=None)
    fig5.update_xaxes(matches=None)
    fig5.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig5.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines")
    
    
    fig6 = px.scatter(df_cafe, x="run_center", y="cumulative_luminosity", color="target", facet_col="kin\nstudy", hover_name="run\nnumber", hover_data={'cumulative_luminosity [1/fb]':(':.3f', df_cafe['cumulative_luminosity']),
                                                                                                                                                        'statistical_goal [1/fb]':(':.3f', df_cafe['integrated\nluminosity\n[fb^-1]']),
                                                                                                                                                        'percentage_completed [%]':(':.2f', df_cafe['lumi_perct_completed'])})
    fig6.update_layout( title={'text':'Integrated Luminosity', 'x':0.5},  font=dict(size=14), yaxis_title="Integrated_Luminosity [1/fb]")
    fig6.update_yaxes(matches=None)
    fig6.update_xaxes(matches=None)
    fig6.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig6.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines")

    
    fig7 = px.scatter(df_cafe, x="run_center", y="cumulative_lumiNorm", color="target", facet_col="kin\nstudy", hover_name="run\nnumber", hover_data={'cumulative_counts_per_luminosity [fb]':(':.3f', df_cafe['cumulative_lumiNorm']),
                                                                                                                                                      'statistical_goal [fb]':(':.3f', df_cafe['simc_lumiNorm_counts[fb]']),
                                                                                                                                                      'percentage_completed [%]':(':.2f', df_cafe['lumiNorm_perct_completed'])})

    fig7.update_layout( title={'text':'Luminosity-Normalized Counts', 'x':0.5},  font=dict(size=14), yaxis_title="(Counts / Integrated_Luminosity) [fb]")
    fig7.update_yaxes(matches=None)
    fig7.update_xaxes(matches=None)
    fig7.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig7.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines")
    

    fig8 = px.scatter(df_cafe, x="run_center", y="cumulative_counts", color="target", facet_col="kin\nstudy", hover_name="run\nnumber", hover_data={ 'cumulative_counts':':.2f',
                                                                                                                                                    'counts (this run)':(':i', df_cafe['real_counts']),
                                                                                                                                                     'count rate [Hz] (this run)':(':%.2f', df_cafe['real_rates']),
                                                                                                                                                     'beam_current [uA] (this run)':(':%.2f', df_cafe['BCM4A\ncurrent\n[uA]']),
                                                                                                                                                    'statistical_goal':(':i', df_cafe['simc_counts_goal']),
                                                                                                                                                     'percentage_completed [%]':(':.2f', df_cafe['counts_perct_completed'])})
    
    fig8.update_layout( title={'text':'Total A(e,e\'p) Counts', 'x':0.5},  font=dict(size=14), yaxis_title="Total Counts")
    fig8.update_yaxes(matches=None)
    fig8.update_xaxes(matches=None)
    fig8.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig8.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')), mode="markers+lines")


with open('index.html', 'w') as f:
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

    if not df_cafe.empty:
        f.write(fig2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig3.to_html(full_html=False, include_plotlyjs='cdn'))
        #f.write(fig4.to_html(full_html=False, include_plotlyjs='cdn'))
        #f.write(fig5.to_html(full_html=False, include_plotlyjs='cdn'))
        #f.write(fig6.to_html(full_html=False, include_plotlyjs='cdn'))
        #f.write(fig7.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig8.to_html(full_html=False, include_plotlyjs='cdn'))



