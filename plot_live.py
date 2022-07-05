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

    simc_parm_file_path = '../cafe_online_replay/UTILS_CAFE/inp/set_basic_simc_param.inp'
    simc_parm_file = open(simc_parm_file_path)

    val = 0
    
    for line in simc_parm_file:
        if (line[0]=="#"): continue;

        if string in line:
            val = float((line.split("=")[1]).strip())
    return val


        


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

# add simc columns of 1) total counts goal, 2) luminosity goal, 3) norm-luminosity goal: grouped based on (target, kin_study), 

# create new columns to hold CaFe statistigal goals determined from SIMC simulations
#df['simc_counts_goal'] = np.nan
#df['simc_lumi_goal'] = np.nan
#df['simc_lumiNorm_goal'] = np.nan

#df.loc[(df['target'].str.contains('LH2') & df['kin\nstudy'].str.contains('heep_coin')), 'simc_counts_goal']   = 500.
#df.loc[(df['target'].str.contains('LH2') & df['kin\nstudy'].str.contains('heep_coin')), 'simc_lumi_goal']     = 500.
#df.loc[(df['target'].str.contains('LH2') & df['kin\nstudy'].str.contains('heep_coin')), 'simc_lumiNorm_goal'] = 500.

    
# calculate cumulative quantities
charge_csum = df.groupby(['target', 'kin\nstudy'])['BCM4A\ncharge\n[mC]'].cumsum() 
df['cumulative_charge'] = charge_csum 

luminosity_csum = df.groupby(['target', 'kin\nstudy'])['integrated\nluminosity\n[fb^-1]'].cumsum()
df['cumulative_luminosity'] = luminosity_csum

lumiNorm_csum = df.groupby(['target', 'kin\nstudy'])['lumiNorm_counts[fb]'].cumsum()
df['cumulative_lumiNorm'] = lumiNorm_csum

# create a new column in the dataframe which will be the addition of columns: heep_singles, heep_coin, MF_real, SRC_real into a single column
# NOTE: the columns can be added safely (will not actually mix different kinematics), e.g., no change of mixing heep_coin with MF_real counts, as one of these will be NaN and the other will NOT.
df['real_counts'] = df.fillna(0)['heep_singles\ncounts'] + df.fillna(0)['heep_coin\ncounts'] + df.fillna(0)['MF_real\ncounts'] + df.fillna(0)['SRC_real\ncounts']
df['real_rates'] = df.fillna(0)['heep_singles\nrates [Hz]'] + df.fillna(0)['heep_coin\nrates [Hz]'] + df.fillna(0)['MF_real\nrates [Hz]'] + df.fillna(0)['SRC_real\nrates [Hz]']

#calculate total counts
counts_csum = df.groupby(['target', 'kin\nstudy'])['real_counts'].cumsum() 
df['cumulative_counts'] = counts_csum

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
                 # rgb(188, 189, 34)  lime
                 # rgb(23, 190, 207)  blue
                 # rgb(255, 127, 14)  orange
                 # rgb(44, 160, 44)   green
                 # rgb(148, 103, 189) purple
                 # rgb(214, 39, 40)   red
                 'LH2' : { 'heep_singles': 'rgba(127, 127, 127, 0.8)',   # gray
                           'heep_coin'   : 'rgba(255, 255, 0,   0.8)'},  # yellow  
                 
                 'LD2' : { 'MF'       : 'rgba(0,255,255, 0.8)' ,          # cyan
                           'SRC'      : 'rgba(0,255,255, 0.8)'},
                 
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

hover_template = ""

fig2 = px.scatter(df_cafe, x="run_center", y="counts_per_mC", color="target", facet_col="kin\nstudy", hover_name="run\nnumber")
fig2.update_layout( title={'text':'Charge Normalized Counts', 'x':0.5},  font=dict(size=14), yaxis_title="Counts / mC")
fig2.update_yaxes(matches=None)
fig2.update_xaxes(matches=None)
fig2.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
fig2.update_traces(mode="markers+lines")
#fig2.update_xaxes(tickangle=0)
#fig2.update_layout(hovermode="x")


fig3 = px.scatter(df_cafe, x="run_center", y="real_rates", color="target", facet_col="kin\nstudy", hover_name="run\nnumber")
fig3.update_layout( title={'text':'Real Count Rates', 'x':0.5},  font=dict(size=14), yaxis_title="Count Rate [Hz]")
fig3.update_yaxes(matches=None)
fig3.update_xaxes(matches=None)
fig3.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
fig3.update_traces(mode="markers+lines")
#fig3.update_layout(hovermode="x unified")


fig4 = px.scatter(df_cafe, x="run_center", y="beam_eff", color="target", facet_col="kin\nstudy", hover_name="run\nnumber")
fig4.update_layout( title={'text':'Beam Efficiency', 'x':0.5},  font=dict(size=14), yaxis_title="efficiency")
fig4.update_yaxes(matches=None)
fig4.update_xaxes(matches=None)
fig4.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
fig4.update_traces(mode="markers+lines")
#fig4.update_layout(hovermode="x unified")

'''
fig5 = px.scatter(df_cafe, x="run_center", y="T1\nscaler_rates\n[kHz]", color="target", facet_col="kin\nstudy", hover_name="run\nnumber")
fig5.add_trace(px.scatter(df_cafe, x="run_center", y="T2\nscaler_rates\n[kHz]", color="target", facet_col="kin\nstudy", hover_name="run\nnumber"))

fig5.update_layout( title={'text':'Scaler pre-Trigger Rates', 'x':0.5},  font=dict(size=14), yaxis_title="Scaler Rates [kHz]")
fig5.update_yaxes(matches=None)
fig5.update_xaxes(matches=None)
fig5.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
fig5.update_traces(mode="markers+lines")
'''

fig6 = px.scatter(df_cafe, x="run_center", y="cumulative_luminosity", color="target", facet_col="kin\nstudy", hover_name="run\nnumber")
fig6.update_layout( title={'text':'Integrated Luminosity', 'x':0.5},  font=dict(size=14), yaxis_title="Integrated Luminosity [1/fb]")
fig6.update_yaxes(matches=None)
fig6.update_xaxes(matches=None)
fig6.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
fig6.update_traces(mode="markers+lines")

fig7 = px.scatter(df_cafe, x="run_center", y="cumulative_lumiNorm", color="target", facet_col="kin\nstudy", hover_name="run\nnumber")
fig7.update_layout( title={'text':'Luminosity-Normalized Counts', 'x':0.5},  font=dict(size=14), yaxis_title="Counts / Int. Luminosity [fb]")
fig7.update_yaxes(matches=None)
fig7.update_xaxes(matches=None)
fig7.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
fig7.update_traces(mode="markers+lines")

fig8 = px.scatter(df_cafe, x="run_center", y="cumulative_counts", color="target", facet_col="kin\nstudy", hover_name="run\nnumber")
fig8.add_traces(list(px.scatter(df_cafe, x="run_center", y="simc_counts_goal", color="target",facet_col="kin\nstudy" ).select_traces()))

for idx, row in df_cafe['target'].iteritems():

    # Set the (x,y) location of the SIMC reference lines for both MF (left subplot) and SRC (right subplot)
    '''
    y_simc_MF        = (df_cafe.loc[(df_cafe['kin\nstudy'].str.contains('MF') & df_cafe['target'].str.contains(row))])['simc_counts_goal'].median()
    x_min_simc_MF    = (df_cafe.loc[(df_cafe['kin\nstudy'].str.contains('MF') & df_cafe['target'].str.contains(row))])['start_run'].min()
    x_max_simc_MF    = (df_cafe.loc[(df_cafe['kin\nstudy'].str.contains('MF') & df_cafe['target'].str.contains(row))])['end_run'].max()
    x_median_simc_MF = (df_cafe.loc[(df_cafe['kin\nstudy'].str.contains('MF') & df_cafe['target'].str.contains(row))])['run_center'].median()

    fig8.add_shape(type="line", xref="x", yref="y",
                   x0=x_min_simc_MF,
                   y0=y_simc_MF,
                   x1=x_max_simc_MF,
                   y1=y_simc_MF,
                   line_width=2,
                   line_dash="dash", line_color="red", row=1,col=1)
    ''' 
    y_simc           = (df_cafe.loc[(df_cafe['kin\nstudy'].str.contains('SRC') & df_cafe['target'].str.contains(row))])['simc_counts_goal'].median()
    x_min_simc       = (df_cafe.loc[(df_cafe['kin\nstudy'].str.contains('SRC') & df_cafe['target'].str.contains(row))])['start_run'].min()
    x_max_simc       = (df_cafe.loc[(df_cafe['kin\nstudy'].str.contains('SRC') & df_cafe['target'].str.contains(row))])['end_run'].max()
    x_median_simc    = (df_cafe.loc[(df_cafe['kin\nstudy'].str.contains('SRC') & df_cafe['target'].str.contains(row))])['run_center'].median()

    fig8.add_shape(type="line", xref="x", yref="y",
                x0=x_min_simc,
                y0=y_simc,
                x1=x_max_simc,
                y1=y_simc,
                line_width=2,
                line_dash="dash", line_color="red", row=1,col=2)

    '''
    # add annotation text with an arrow
    fig8.add_annotation(
        x=x_median_simc_MF,
        y=y_simc_MF,
        xref='x1',  # this represents subplot 2
        yref='y1', 
        text=f'%s stats goal:<br> %.1f counts '%(row.strip(), y_simc_MF),
        yanchor='bottom',
        showarrow=False,
        arrowhead=1,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=-20,
        ay=-30,
        font=dict(size=11, color="black", family="Courier New, monospace"),
        align="left",
        )
    '''




    '''
    # add annotation text with an arrow
    fig8.add_annotation(
        x=x_median_simc,
        y=y_simc,
        xref='x2',  # this represents subplot 2
        yref='y2', 
        text=f'%s stats goal:<br> %.1f counts '%(row.strip(), y_simc),
        yanchor='bottom',
        showarrow=False,
        arrowhead=1,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=-20,
        ay=-30,
        font=dict(size=11, color="black", family="Courier New, monospace"),
        align="left",
        )
    '''





#fig8.add_traces(list(px.line(df_cafe, x="run_center", y="simc_counts_goal", line_dash="target",  facet_col="kin\nstudy", name="trace").select_traces()))
fig8.update_layout( title={'text':'Total A(e,e\'p) Counts', 'x':0.5},  font=dict(size=14), yaxis_title="Total Counts")
fig8.update_yaxes(matches=None)
fig8.update_xaxes(matches=None)
fig8.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
fig8.update_traces(mode="markers+lines")

with open('index.html', 'w') as f:
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig2.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig3.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig4.to_html(full_html=False, include_plotlyjs='cdn'))
    #f.write(fig5.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig6.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig7.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig8.to_html(full_html=False, include_plotlyjs='cdn'))
