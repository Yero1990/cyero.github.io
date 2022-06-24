import pandas as pd
import plotly_express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime
import chart_studio
import chart_studio.plotly as charts


#The initialization step places a special .plotly/.credentials file in your home directory. ( i think only done once)
#chart_studio.tools.set_credentials_file(username='cyero', api_key='JCKnODSC8EtxOT1GdtND')






# using now() to get current time
current_time = datetime.datetime.now()
print(current_time)

# making dataframe 
df = pd.read_csv("test.csv") 

#group by target and kinematic_type, then do cumulative sum of charge
print(df.groupby(['target', 'kin_type'])['charge'].cumsum())
charge_csum = df.groupby(['target', 'kin_type'])['charge'].cumsum()

#fig = go.Figure()
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_traces(list(px.line(df, x='run', y=charge_csum, title='cumulative charge', color='target', line_dash='kin_type', markers=True).select_traces()))
fig.add_traces(list(px.bar(df, x='run', y='charge', color='target', pattern_shape="kin_type").select_traces()))
fig.update_yaxes(title_text="charge [mC]", secondary_y=False)

fig.update_layout(hovermode='x unified')
#fig.update_xaxes(tickmode='linear', ticklabelmode="period")
fig.update_layout(bargap=0)

#fig.add_trace(px.bar(df, x='run', y='charge', color='target', pattern_shape="kin_type").data[1])
#fig.update_layout(xaxis={'visible': False, 'showticklabels': False})
#fig.show()

# create .html interactive plot 
fig.write_html("index.html")

# copy it to my github pages


#charts.plot(fig, filename = 'basic-line', auto_open=True)




#------------------------
#how to convert string time_stamp to python formatted timestamp to plot
#from datetime import datetime, timedelta

#time_stamp= 'Sat Jun 18 13:13:41 2022'

#In [12]: time_stamp_fmt = datetime.strptime(time_stamp, '%a %b %d %H:%M:%S %Y') make sure to put the correct format of the string

#In [13]: time_stamp_fmt
#Out[13]: datetime.datetime(2022, 6, 18, 13, 13, 41)

#time_stamp_fmt.timestamp() --> this gives an absolute time number in seconds.

# to add delta time (e.g., run length in seconds) to get the end_time, do:
#end_time = time_stamp_fmt + timedelta(seconds=3600)  # if a run lasted 1 hour

#In [24]: time_stamp_fmt
#Out[24]: datetime.datetime(2022, 6, 18, 13, 13, 41)

#In [25]: end_time
#Out[25]: datetime.datetime(2022, 6, 22, 2, 13, 41)

# calculate time width of the run (sec)
#In [26]: end_time.timestamp() - time_stamp_fmt.timestamp()
#Out[26]: 306000.0

# calculate mid-point of the run (to put correct tick in center)
#In [27]: time_stamp_fmt + 0.5*(end_time - time_stamp_fmt)
#Out[27]: datetime.datetime(2022, 6, 20, 7, 43, 41)

#------------------------
