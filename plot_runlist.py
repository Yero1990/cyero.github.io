import pandas as pd
import plotly_express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime
import chart_studio
import chart_studio.plotly as charts
from datetime import datetime, timedelta

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

#In [1]: start_of_run = '2022-06-18 13:13:41'

#In [2]: start_of_run
#Out[2]: '2022-06-18 13:13:41'

#In [3]: from datetime import datetime, timedelta

#In [4]: start_of_run_fmt = datetime.strptime(start_of_run, '%Y-%m-%d %H:%M:%S')

#In [5]: start_of_run_fmt
#Out[5]: datetime.datetime(2022, 6, 18, 13, 13, 41)

#In [6]: start_of_run_fmt + timedelta(seconds=3600)
#Out[6]: datetime.datetime(2022, 6, 18, 14, 13, 41)

#In [7]: end_of_run_fmt = start_of_run_fmt + timedelta(seconds=3600)

#In [8]: start_of_run_fmt
#Out[8]: datetime.datetime(2022, 6, 18, 13, 13, 41)

#In [9]: end_of_run_fmt
#Out[9]: datetime.datetime(2022, 6, 18, 14, 13, 41)

# calculate mid-point of the run (to put correct tick in center)
#In [27]: time_stamp_fmt + 0.5*(end_time - time_stamp_fmt)
#Out[27]: datetime.datetime(2022, 6, 20, 7, 43, 41)

#------------------------
