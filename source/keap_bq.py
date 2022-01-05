from google.oauth2 import service_account
from google.cloud.bigquery_connection_v1.services.connection_service import (ConnectionServiceAsyncClient)
from google.cloud import bigquery
from os.path import join
from datetime import datetime, timedelta
import pandas as pd
from plotly.colors import n_colors
from plotly.offline import plot
import plotly.express as px
from plotly.graph_objs import *
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt

json_path = 'C:\\Users\\User\\Downloads\\infusionsoft-mobile-23c7cc475efc.json'
project_id = 'infusionsoft-mobile'
table = 'infusionsoft-mobile.analytics_151450590.events_'
params = 'firebase_event_origin', 'edition'
#event_name = 'AdWatched'

def main(start , end, start_cur, end_cur, start_day = '20210929', end_date = '20211031'):
    
  #dataframe = query_data(json_path, project_id, table, params, 1)
  #dataframe.to_csv('bq_keap_new.csv', mode = 'a', header = None) 
  
  print('ok')
  cols_list = ['event_date','user_pseudo_id', 'event_timestamp', 'event_name', 'city','country', 'version', 'key', 'string_value', 'operating_system', 'category']
  df = pd.read_csv('bq_keap_new.csv', usecols=cols_list)
  #df['version'] = df['version'].apply(lambda x: int(re.sub(r"\.|\-\w+", "", str(x))))
  print(df.columns)
  print(df['event_date'].max())

  
  print('######')
  figs_bq = []
  #fig_range = graphRangeRetention(start_day, end_date, df)
  #figs_bq.append(fig_range)
  
  #Dates just for ret tables
  start_day = '20211004'
  end_date = '20211114'
  
  ran = getDayDiff(start_day, end_date)
  weeks = ran // 7
  print(weeks)
  colors = n_colors('rgb(239, 243, 255)', 'rgb(49, 130, 189)', 11, colortype='rgb')
  
  
  #tem = df[(df['event_name'] == 'ArtOpen') & (df['key'] == 'coloringId')]['string_value'].unique()
  #print(tem)

  '''
  heads = ['Mon19', 'Tue20', 'Wed21', 'Thur22', 'Fri23', 'Sat24', 'Sun25', 'Mon26', 'Tue27', 'Wed28', 'Thu29', 'Fri30', 'Sat31', 'Sund1']
  rolls = pd.DataFrame(columns = heads)
  limit = 0
  end_of_comp = 20210802 
  lista = [20210719,20210720,20210721,20210722, 20210723, 20210724, 20210725, 20210726,20210727,20210728,20210729, 20210730, 20210731, 20210801]
  
  for day in lista:
    roll, item = getRollingRetention(day, end_of_comp, df, 'JeffSrsic.skullWater')
    cols = rolls.columns[limit:]
    print(day)
    if item != 0:
      print(roll)
      print(item)
      rolls.loc['Day {} ({})'.format(limit, item), cols] = roll 
    else:  
      rolls.loc['Day {} ({})'.format(limit, item), cols] = [0] * (len(lista)-limit)
    limit += 1

  print(rolls)
  rolls.fillna(0, inplace = True)
  vals = [np.round(rolls[i].values * 100, 0) for i in heads]
  heads.insert(0,'')
  vals.insert(0,rolls.index)

  #conditional coloring to all table values
  fills = [np.array(colors)[np.round((rolls[col]* 10).astype('int').values, 0)] for col in rolls.columns]

  fills.insert(0, 'rgb(245, 245, 245)')
  #init fig table
  fig_roll = go.Figure(go.Table(header=dict(values= heads), cells=dict(values=vals,fill_color= fills)))
  fig_roll.update_layout(title_text = "Rolling Retention based on JeffSrsic.skullWater Art Unique Users (in %s)", height = 375)
  figs_bq.append(fig_roll)

  
  heads = ['Thu22','Fri23','Sat24', 'Sund25']
  rolls = pd.DataFrame(columns = heads)
  limit = 0
  end_of_comp = 20210426 

  for day in [20210422, 20210423, 20210424,20210425]:
    roll, item = getRollingRetention(day, end_of_comp, df, 'PhilipHolt.smallIsland')
    cols = rolls.columns[limit:]
    print(day)
    if item != 0:
      print(roll)
      print(item)
      rolls.loc['Day {} ({})'.format(limit, item), cols] = roll 
    else:  
      rolls.loc['Day {} ({})'.format(limit, item), cols] = [0] * (3-limit)
  
    limit += 1

  print(rolls)
  rolls.fillna(0, inplace = True)
  vals = [np.round(rolls[i].values * 100, 0) for i in heads]
  heads.insert(0,'')
  vals.insert(0,rolls.index)

  #conditional coloring to all table values
  fills = [np.array(colors)[np.round((rolls[col]* 10).astype('int').values, 0)] for col in rolls.columns]

  fills.insert(0, 'rgb(245, 245, 245)')
  #init fig table
  fig_roll = go.Figure(go.Table(header=dict(values= heads),
                cells=dict(values=vals,
                fill_color= fills)))
  fig_roll.update_layout(title_text = "Rolling Retention based on PhilipHolt.smallIsland Art Unique Users (in %s)", height = 375)
  figs_bq.append(fig_roll)
  
  
  #'LangoOlivera.Hanna', 'MattBeckerich.roses','TimHendricks.eagle','ClaudiaDeSabe.WomanFace', 'RG.zootsuit','JeffSrsic.Jaguar','ChrisGarver.coiledSnake', 'FlorencioRojas.dancingFrogs'
  tables = ['ChrisNunez.infiniteDragon']
  #tables = [('20201201', '20210101'),('20210101', '20210215')]

  ##PLOT Ret tables
  for tab in tables:
    print(tab)
    columns_df = ['week_' + str(i) for i in range(weeks)]
    df_table = event_based(start_day, end_date, columns_df, weeks, df, event_name = 'ArtOpen', param = tab)
    heads = [i for i in columns_df]
    heads.insert(0,'')
    vals = [np.round(df_table[i].values * 100, 0) for i in columns_df]
    vals.insert(0,df_table.index)
    #conditional coloring to values of retention table
    fills = [np.array(colors)[np.round((df_table[col]* 10).astype('int').values, 0)] for col in df_table.columns]
    fills.insert(0, 'rgb(245, 245, 245)')
    #init fig table
    fig = go.Figure(go.Table(header=dict(values= heads),
                cells=dict(values=vals,
                fill_color= fills)))
    fig.update_layout(title_text = "Retention based on users who opened Art {} (in %s)".format(tab), height = 375)
    figs_bq.append(fig)

  with open('CC_June_Ret.html', 'w') as f:
    for file in figs_bq:
      f.write(file.to_html(full_html=False, include_plotlyjs='cdn'))
  
#Look at proxy metric
#table of rolling
  
  #(start_day, end_date)
  #weeks = ran // 7

  tables = [0,1,2,3]

  for tab in tables:
    print(tab)
    columns_df = ['week_' + str(i) for i in range(weeks + 1)]
    df_table, totals = ret_proxy_habit(start_day, end_date, columns_df, weeks, df, event_name = ["notification_open"], num = tab, platform = 'None')
    heads = [i for i in columns_df]
    heads.insert(0,'')
    vals = [np.round(df_table[i].values *100 , 0) for i in columns_df] 
    vals.insert(0,df_table.index)
    #conditional coloring to values of retention table
    fills = [np.array(colors)[np.round((df_table[col]* 10).astype('int').values, 0)] for col in df_table.columns]
    fills.insert(0, 'rgb(245, 245, 245)')
    #init fig table
    totals = totals.set_index('event_name')
    counts = [sum(totals.loc[i,:]) / len(totals.columns) for i in totals.index]
    totals['counts'] = np.round(counts, 0)
    totals.reset_index(inplace = True)
    totals = totals.sort_values('counts', ascending= False).head(12)
    trace = go.Table(header=dict(values= heads),cells=dict(values=vals,fill_color= fills), domain=dict(x=[0, .5],y=[0, 1]))
    trace1 = go.Pie(values=totals.counts.values, labels=totals.event_name.values, hole=.3, name = 'Top', domain=dict(x=[0.52, 0.77],y=[0, 1]), title_text = 'Events', textposition='inside', textinfo='percent', hoverinfo="label+value")
    trace2 = go.Table(header=dict(values= ['Event', 'Total']),cells=dict(values=[totals.event_name.values, totals.counts.values]), domain=dict(x=[0.75, 1],y=[0, 1]))
    fig = go.Figure(data = [trace,trace1, trace2])
    fig.update_layout(title_text = "Retention based on users who notification_open {} or more days in one week (%)".format(tab), height = 450)
    figs_bq.append(fig)
    print('add')
  
  for tab in tables:
    print(tab)
    columns_df = ['week_' + str(i) for i in range(weeks + 1)]
    df_table, totals = ret_proxy_habit(start_day, end_date, columns_df, weeks, df, event_name = ["finish_task"], num = tab, platform = 'None')
    heads = [i for i in columns_df]
    heads.insert(0,'')
    vals = [np.round(df_table[i].values *100 , 0) for i in columns_df] 
    vals.insert(0,df_table.index)
    #conditional coloring to values of retention table
    fills = [np.array(colors)[np.round((df_table[col]* 10).astype('int').values, 0)] for col in df_table.columns]
    fills.insert(0, 'rgb(245, 245, 245)')
    #init fig table
    totals = totals.set_index('event_name')
    counts = [sum(totals.loc[i,:]) / len(totals.columns) for i in totals.index]
    totals['counts'] = np.round(counts, 0)
    totals.reset_index(inplace = True)
    totals = totals.sort_values('counts', ascending= False).head(12)
    trace = go.Table(header=dict(values= heads),cells=dict(values=vals,fill_color= fills), domain=dict(x=[0, .5],y=[0, 1]))
    trace1 = go.Pie(values=totals.counts.values, labels=totals.event_name.values, hole=.3, name = 'Top', domain=dict(x=[0.52, 0.77],y=[0, 1]), title_text = 'Events', textposition='inside', textinfo='percent', hoverinfo="label+value")
    trace2 = go.Table(header=dict(values= ['Event', 'Total']),cells=dict(values=[totals.event_name.values, totals.counts.values]), domain=dict(x=[0.75, 1],y=[0, 1]))
    fig = go.Figure(data = [trace,trace1, trace2])
    fig.update_layout(title_text = "Retention based on users who finish_task {} or more days in one week (%)".format(tab), height = 450)
    figs_bq.append(fig)
    print('send')
  

  for tab in tables:
    print(tab)
    columns_df = ['week_' + str(i) for i in range(weeks + 1)]
    df_table, totals = ret_proxy_habit(start_day, end_date, columns_df, weeks, df, event_name = ["add_contact"], num = tab, platform = "None")
    heads = [i for i in columns_df]
    heads.insert(0,'')
    vals = [np.round(df_table[i].values *100 , 0) for i in columns_df] 
    vals.insert(0,df_table.index)
    #conditional coloring to values of retention table
    fills = [np.array(colors)[np.round((df_table[col]* 10).astype('int').values, 0)] for col in df_table.columns]
    fills.insert(0, 'rgb(245, 245, 245)')
    #init fig table
    totals = totals.set_index('event_name')
    counts = [sum(totals.loc[i,:]) / len(totals.columns) for i in totals.index]
    totals['counts'] = np.round(counts, 0)
    totals.reset_index(inplace = True)
    totals = totals.sort_values('counts', ascending= False).head(12)
    trace = go.Table(header=dict(values= heads),cells=dict(values=vals,fill_color= fills), domain=dict(x=[0, .5],y=[0, 1]))
    trace1 = go.Pie(values=totals.counts.values, labels=totals.event_name.values, hole=.3, name = 'Top', domain=dict(x=[0.52, 0.77],y=[0, 1]), title_text = 'Events', textposition='inside', textinfo='percent', hoverinfo="label+value")
    trace2 = go.Table(header=dict(values= ['Event', 'Total']),cells=dict(values=[totals.event_name.values, totals.counts.values]), domain=dict(x=[0.75, 1],y=[0, 1]))
    fig = go.Figure(data = [trace,trace1, trace2])
    fig.update_layout(title_text = "Retention based on users who did add_contact {} or more days in one week (%)".format(tab), height = 450)
    figs_bq.append(fig)
    print('outbound')
  
  for tab in tables:
    print(tab)
    columns_df = ['week_' + str(i) for i in range(weeks + 1)]
    df_table, totals = ret_proxy_habit(start_day, end_date, columns_df, weeks, df, event_name = ["add_contact"], num = tab, platform = 'iOS')
    heads = [i for i in columns_df]
    heads.insert(0,'')
    vals = [np.round(df_table[i].values *100 , 0) for i in columns_df] 
    vals.insert(0,df_table.index)
    #conditional coloring to values of retention table
    fills = [np.array(colors)[np.round((df_table[col]* 10).astype('int').values, 0)] for col in df_table.columns]
    fills.insert(0, 'rgb(245, 245, 245)')
    #init fig table
    totals = totals.set_index('event_name')
    counts = [sum(totals.loc[i,:]) / len(totals.columns) for i in totals.index]
    totals['counts'] = np.round(counts, 0)
    totals.reset_index(inplace = True)
    totals = totals.sort_values('counts', ascending= False).head(12)
    trace = go.Table(header=dict(values= heads),cells=dict(values=vals,fill_color= fills), domain=dict(x=[0, .5],y=[0, 1]))
    trace1 = go.Pie(values=totals.counts.values, labels=totals.event_name.values, hole=.3, name = 'Top', domain=dict(x=[0.52, 0.77],y=[0, 1]), title_text = 'Events', textposition='inside', textinfo='percent', hoverinfo="label+value")
    trace2 = go.Table(header=dict(values= ['Event', 'Total']),cells=dict(values=[totals.event_name.values, totals.counts.values]), domain=dict(x=[0.75, 1],y=[0, 1]))
    fig = go.Figure(data = [trace,trace1, trace2])
    fig.update_layout(title_text = "iOS Retention based on users who did add_contact {} or more days in one week (%)".format(tab), height = 450)
    figs_bq.append(fig)
    print('ios')
  
  for tab in tables:
    print(tab)
    columns_df = ['week_' + str(i) for i in range(weeks + 1)]
    df_table, totals = ret_proxy_habit(start_day, end_date, columns_df, weeks, df, event_name = ["add_contact"], num = tab, platform = 'Android')
    heads = [i for i in columns_df]
    heads.insert(0,'')
    vals = [np.round(df_table[i].values *100 , 0) for i in columns_df] 
    vals.insert(0,df_table.index)
    #conditional coloring to values of retention table
    fills = [np.array(colors)[np.round((df_table[col]* 10).astype('int').values, 0)] for col in df_table.columns]
    fills.insert(0, 'rgb(245, 245, 245)')
    #init fig table
    totals = totals.set_index('event_name')
    counts = [sum(totals.loc[i,:]) / len(totals.columns) for i in totals.index]
    totals['counts'] = np.round(counts, 0)
    totals.reset_index(inplace = True)
    totals = totals.sort_values('counts', ascending= False).head(12)
    trace = go.Table(header=dict(values= heads),cells=dict(values=vals,fill_color= fills), domain=dict(x=[0, .5],y=[0, 1]))
    trace1 = go.Pie(values=totals.counts.values, labels=totals.event_name.values, hole=.3, name = 'Top', domain=dict(x=[0.52, 0.77],y=[0, 1]), title_text = 'Events', textposition='inside', textinfo='percent', hoverinfo="label+value")
    trace2 = go.Table(header=dict(values= ['Event', 'Total']),cells=dict(values=[totals.event_name.values, totals.counts.values]), domain=dict(x=[0.75, 1],y=[0, 1]))
    fig = go.Figure(data = [trace,trace1, trace2])
    fig.update_layout(title_text = "Android Retention based on users who did add_contact {} or more days in one week (%)".format(tab), height = 450)
    figs_bq.append(fig)
    print('android')

  print('slice')

  
  
  ## For Pulse Data
  
  df['event_timestamp'] = timestamp_reg(df)
  df_all = df.copy()

  pulse = df_all[df_all['event_name'] == 'first_open']
  pulse['values'] = 1
  pulse_general = pulse.groupby('event_date').sum().reset_index().sort_values('event_date')
  pulse_general['type'] = 'installs'
  pulse_country = pulse.groupby(['event_date', 'country']).sum().reset_index().sort_values('event_date')
  pulse_country['type'] = 'installs'
  pulse_os = pulse.groupby(['event_date', 'operating_system']).sum().reset_index().sort_values('event_date')
  pulse_os['type'] = 'installs'
  pulse_cat = pulse.groupby(['event_date', 'category']).sum().reset_index().sort_values('event_date')
  pulse_cat['type'] = 'installs'

  drops = df_all[df_all['event_name'] == 'app_remove']
  drops['values'] = 1

  drops_general = drops.groupby('event_date').sum().reset_index().sort_values('event_date')
  drops_general['type'] = 'app removes'
  drops_country = drops.groupby(['event_date', 'country']).sum().reset_index().sort_values('event_date')
  drops_country['type'] = 'app removes'
  drops_os = drops.groupby(['event_date', 'operating_system']).sum().reset_index().sort_values('event_date')
  drops_os['type'] = 'app removes'
  drops_cat = drops.groupby(['event_date', 'category']).sum().reset_index().sort_values('event_date')
  drops_cat['type'] = 'app removes'
  graph_country = pd.concat([pulse_country, drops_country], axis = 0).reset_index(drop = True)
  graph_country['event_date'] = pd.to_datetime(graph_country['event_date'], format = '%Y%m%d')
  graph_country.fillna(int(0), inplace = True)
  graph_country.to_csv('country.csv')
  graph_top = graph_country.groupby('country').sum().reset_index().sort_values('values', ascending = False)
  top_countries = graph_top['country'].values[:4]
  idx = [i for i in graph_country.index if graph_country.loc[i, 'country'] in top_countries]
  graph_top = graph_country[graph_country.index.isin(idx)]
  graph_device = pd.concat([pulse_os, drops_os], axis = 0).reset_index(drop = True)
  graph_device['event_date'] = pd.to_datetime(graph_device['event_date'], format = '%Y%m%d')
  graph_cat = pd.concat([pulse_cat, drops_cat], axis = 0).reset_index(drop = True)
  graph_cat['event_date'] = pd.to_datetime(graph_cat['event_date'], format = '%Y%m%d')
  pulse_graph = pd.merge(pulse_general, drops_general, on = 'event_date', how = 'left')
  pulse_graph['event_date'] = pd.to_datetime(pulse_graph['event_date'], format="%Y%m%d")
  pulse_graph.fillna(int(0), inplace = True)
  pulse_graph.to_csv('pulse.csv')
  pulse_graph['event_date'] = pd.to_datetime(pulse_graph['event_date'], format='%Y%m%d')
  pulse_fig = make_subplots(specs=[[{"secondary_y": True}]])
  pulse_fig.add_trace(go.Scatter(x=pulse_graph['event_date'], y=pulse_graph['values_x'], name = 'Installs', marker_color = '#AB63FA'))
  pulse_fig.add_trace(go.Scatter(x=pulse_graph['event_date'], y=pulse_graph['values_y'], name = 'App removes', marker_color = 'rgb(204,204,204)'), secondary_y = True)
  pulse_fig.update_layout(title_text = "Daily Pulse")
  pulse_fig.update_yaxes(title_text="Users Installs", secondary_y=False)
  pulse_fig.update_yaxes(title_text="Users App Removes", secondary_y=True)
  pulse_fig.update_xaxes(title_text="Day")
  figs_bq.append(pulse_fig)
  country_fig = px.line(graph_top, x="event_date", y="values", color="type", facet_col = "country", facet_col_wrap= 1)
  country_fig.update_layout(title_text = 'Pulse Performance per country')
  country_fig.update_traces(mode='markers+lines')
  country_fig.update_xaxes(matches='x')
  country_fig.update_yaxes(matches=None)
  figs_bq.append(country_fig)
  dict_device = {'iOS': 'iOS', 'IOS': 'iOS', 'ANDROID': 'Android', 'Android': 'Android'}
  graph_device['operating_system'] = graph_device['operating_system'].map(dict_device)
  device_fig = px.line(graph_device, x="event_date", y="values", color="type", facet_col = "operating_system", facet_col_wrap= 1)
  device_fig.update_layout(title_text = 'Pulse Performance per OS')
  device_fig.update_traces(mode='markers+lines')
  device_fig.update_xaxes(matches='x')
  device_fig.update_yaxes(matches=None)
  figs_bq.append(device_fig)
  cat_fig = px.line(graph_cat, x="event_date", y="values", color="type", facet_col = "category", facet_col_wrap= 1)
  cat_fig.update_layout(title_text = 'Pulse Performance per Device Category')
  cat_fig.update_traces(mode='markers+lines')
  cat_fig.update_xaxes(matches='x')
  cat_fig.update_yaxes(matches=None)
  figs_bq.append(cat_fig)
  '''

  print('normal')
  #('20210621','20210704', '20210705', '20210718')
  
  df_pre = slice_dfby_date(df, start, end)
  
  df_cur = slice_dfby_date(df, start_cur, end_cur)
  print(df_cur['event_name'].unique())
  print(df_cur.head(50))

  
  events_df_pre = reduce_dups(df_pre)
  events_df_cur = reduce_dups(df_cur)
  print(events_df_cur['event_name'].unique())
  print(len(events_df_cur))
  events_df = reduce_dups(df_cur)
  #events_df_pre['event_timestamp'] = timestamp_reg(events_df_pre)
  #events_df_cur['event_timestamp'] = timestamp_reg(events_df_cur)
  totale = len(events_df_cur)


  print(events_df_cur.head(10))

  max, min = date_r(events_df_cur)


  ##PLOT PIE EVENTS
  
  ##EVENTS (used with reduce_dups)
  events_sel = events_df_cur.groupby('event_name').count().reset_index().sort_values('user_pseudo_id', ascending = False)
  print(events_sel)
  events_sel_pre = events_df_pre.groupby('event_name').count().reset_index().sort_values('user_pseudo_id', ascending = False).reset_index(drop = True)
  events_sel_pre['pos'] = events_sel_pre.index
  events_sel_pre = events_sel_pre[['event_name','user_pseudo_id', 'pos']]
  merged = pd.merge(events_sel, events_sel_pre, on = 'event_name', how = 'left')
  merged['change'] = ((merged['user_pseudo_id_x'] - merged['user_pseudo_id_y']) / (merged['user_pseudo_id_x'] + merged['user_pseudo_id_y']) * 100)
  merged = merged[['event_name','change', 'pos']]
  events_sel = pd.merge(events_sel, merged, on = 'event_name', how = 'left')
  es = list(events_sel.head(10)['event_name'].values)
  idx = [i for i in events_sel.index if events_sel.loc[i,'event_name'] in es]
  events_pie = events_sel.loc[idx,:]
  #pie_events = px.pie(events_pie, names = 'event_name', values = 'user_pseudo_id', hover_name= 'event_name', labels= ['event', 'ocassions'], hole = .3, title = 'Events Breakdown From {} to {} (Total events {})'.format(min, max, totale) )
  
  trace = go.Table(header=dict(values=['Event','Counter', 'Change % (15 days)', 'Prev place']),
              cells=dict(values=[events_sel.event_name.values, events_sel.user_pseudo_id.values, np.round(events_sel.change, 2), events_sel.pos]), domain=dict(x=[0.52, 1],y=[0, 1]))   
  trace0 = go.Pie(values=events_pie.user_pseudo_id, labels=events_pie.event_name, hole=.4, name = 'Events', domain=dict(x=[0.1, 0.5],y=[0, 1]), title_text = 'Top 10 Events', textposition='inside', textinfo='percent', hoverinfo="label+value")   
  fig_dough = go.Figure(data = [trace, trace0])
  fig_dough.update_layout(title_text='Events Breakdown From {} to {} (Total events {})'.format(min, max, totale))
#fig_dough.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
  fig_dough.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
  figs_bq.append(fig_dough)

  #Mobile Only (use without reduce_dups)
  idx = df_cur.duplicated(['event_date','event_name','event_timestamp', 'user_pseudo_id'], keep = False)
  print(params[-1])
  idx = [ i for i in df_cur[idx].index if df_cur.loc[i, 'key'] == params[-1]]
  temp_cur = df_cur[df_cur.index.isin(idx)]
  print(temp_cur)
  events_dough_cur = temp_cur[(temp_cur['string_value'] == 'Keap Mobile Edition') | (temp_cur['string_value'] == 'Keap Mobile Free Trial Edition')]
  print(events_dough_cur)
  idx = df_pre.duplicated(['event_date','event_name','event_timestamp', 'user_pseudo_id'], keep = False)
  idx = [ i for i in df_pre[idx].index if df_pre.loc[i, 'key'] == params[-1]]
  temp_pre = df_pre[df_pre.index.isin(idx)]
  events_dough_pre = temp_pre[(temp_pre['string_value'] == 'Keap Mobile Edition') | (temp_pre['string_value'] == 'Keap Mobile Free Trial Edition')] #ArtOpen, AdWatched
  totale = len(events_dough_cur)
  events_sel = events_dough_cur.groupby('event_name').count().reset_index().sort_values('user_pseudo_id', ascending = False)
  events_sel_pre = events_dough_pre.groupby('event_name').count().reset_index().sort_values('user_pseudo_id', ascending = False).reset_index(drop = True)
  events_sel_pre['pos'] = events_sel_pre.index
  events_sel_pre = events_sel_pre[['event_name','user_pseudo_id', 'pos']]
  merged = pd.merge(events_sel, events_sel_pre, on = 'event_name', how = 'left')
  merged['change'] = ((merged['user_pseudo_id_x'] - merged['user_pseudo_id_y']) / merged['user_pseudo_id_y']) * 100
  merged = merged[['event_name','change', 'pos']]
  events_sel = pd.merge(events_sel, merged, on = 'event_name', how = 'left')
  es = list(events_sel.head(15)['event_name'].values)
  idx = [i for i in events_sel.index if events_sel.loc[i,'event_name'] in es]
  events_pie = events_sel.loc[idx,:]
  
  trace = go.Table(header=dict(values=['Event','Counter', 'Change % (15 days)', 'Prev pos']),
              cells=dict(values=[events_sel.event_name.values, events_sel.user_pseudo_id.values,  np.round(events_sel.change, 2), events_sel.pos]), domain=dict(x=[0.52, 1],y=[0, 1]))      
  trace0 = go.Pie(values=events_pie.user_pseudo_id, labels=events_pie.event_name, hole=.4, name = 'Events', domain=dict(x=[0.1, 0.5],y=[0, 1]), title_text = 'Top 15 Events (Based on mobile only)', textposition='inside', textinfo='percent', hoverinfo="label+value")   
  fig_dough_opens_mobile = go.Figure(data = [trace, trace0])
  fig_dough_opens_mobile.update_layout(title_text='Mobile events breakdown Breakdown From {} to {} (Total Mobile events {})'.format(min, max, totale))
  #fig_dough.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
  fig_dough_opens_mobile.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
  figs_bq.append(fig_dough_opens_mobile)
  
  #idx = df_cur.duplicated(['event_date','event_timestamp', 'user_pseudo_id'], keep = False)
  #print(len(idx))

  #From location
  #idx = [ i for i in df_cur.index if df_cur.loc[i, 'key'] == params_cc[-5]]
  #temp = df_cur[df_cur.index.isin(idx)]
  #events_dough_cur = temp[temp['event_name'] == 'ArtOpen'] #ArtOpen, AdWatched
  #idx = df_pre.duplicated(['event_date','event_timestamp', 'user_pseudo_id'], keep = False)
  #idx = [ i for i in df_pre[idx].index if df_pre.loc[i, 'key'] == params_cc[-5]]
  #temp = df_pre[df_pre.index.isin(idx)]
  
  #events_dough_pre = temp[temp['event_name'] == 'ArtOpen'] #ArtOpen, AdWatched
  
  #totale = len(events_dough_cur)
  #events_sel = events_dough_cur.groupby('string_value').count().reset_index().sort_values('user_pseudo_id', ascending = False)
  #print(events_sel)
  #events_sel_pre = events_dough_pre.groupby('string_value').count().reset_index().sort_values('user_pseudo_id', ascending = False).reset_index(drop = True)
  #events_sel_pre['pos'] = events_sel_pre.index
  #events_sel_pre = events_sel_pre[['string_value','user_pseudo_id', 'pos']]
  #merged = pd.merge(events_sel, events_sel_pre, on = 'string_value', how = 'left')
  #merged['change'] = ((merged['user_pseudo_id_x'] - merged['user_pseudo_id_y']) / (merged['user_pseudo_id_x'] + merged['user_pseudo_id_y']) * 100)
  #merged = merged[['string_value','change', 'pos']]
  #events_sel = pd.merge(events_sel, merged, on = 'string_value', how = 'left')

  #es = list(events_sel.head(15)['string_value'].values)
  #idx = [i for i in events_sel.index if events_sel.loc[i,'string_value'] in es]
  #events_pie = events_sel.loc[idx,:]
  
  #trace = go.Table(header=dict(values=['Art','Counter', 'Change % (15 days)', 'Prev Pos']),
  #            cells=dict(values=[events_sel.string_value.values, events_sel.user_pseudo_id.values, np.round(events_sel.change, 2), events_sel.pos]), domain=dict(x=[0.52, 1],y=[0, 1]))
            
    
  #trace0 = go.Pie(values=events_pie.user_pseudo_id, labels=events_pie.string_value, hole=.4, name = 'Events', domain=dict(x=[0.1, 0.5],y=[0, 1]), title_text = 'Top 10 Arts (Based on ArtOpens)', textposition='inside', textinfo='percent', hoverinfo="label+value")
  #fig_dough_from = go.Figure(data = [trace0]) #trace, 
  #fig_dough_from.update_layout(title_text='ArtOpen Breakdown Location From {} to {} (Total ArtOpen {})'.format(min, max, totale))
#fig_dough.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
  #fig_dough_from.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
  #figs_bq.append(fig_dough_from)

  #ArtOpens
  #idx = [ i for i in df_cur.index if df_cur.loc[i, 'key'] == params_cc[-6]]
  #temp = df_cur[df_cur.index.isin(idx)]
  #events_dough_cur = temp[temp['event_name'] == 'ArtOpen'] #ArtOpen, AdWatched
#idx = df_pre.duplicated(['event_date','event_timestamp', 'user_pseudo_id'], keep = False)
  #idx = [ i for i in df_pre.index if df_pre.loc[i, 'key'] == params_cc[-6]]
  #temp = df_pre[df_pre.index.isin(idx)]
  
  #events_dough_pre = temp[temp['event_name'] == 'ArtOpen'] #ArtOpen, AdWatched
  #totale = len(events_dough_cur)
  #events_sel = events_dough_cur.groupby('string_value').count().reset_index().sort_values('user_pseudo_id', ascending = False)
  #print(events_sel)
  #events_sel_pre = events_dough_pre.groupby('string_value').count().reset_index().sort_values('user_pseudo_id', ascending = False).reset_index(drop = True)
  #events_sel_pre['pos'] = events_sel_pre.index
  #events_sel_pre = events_sel_pre[['string_value','user_pseudo_id', 'pos']]
  #merged = pd.merge(events_sel, events_sel_pre, on = 'string_value', how = 'left')
  #merged['change'] = ((merged['user_pseudo_id_x'] - merged['user_pseudo_id_y']) / (merged['user_pseudo_id_x'] + merged['user_pseudo_id_y']) * 100)
  #merged = merged[['string_value','change', 'pos']]
  #events_sel = pd.merge(events_sel, merged, on = 'string_value', how = 'left')

  #es = list(events_sel.head(15)['string_value'].values)
  #idx = [i for i in events_sel.index if events_sel.loc[i,'string_value'] in es]
  #events_pie = events_sel.loc[idx,:]
  #trace = go.Table(header=dict(values=['Art','Counter', 'Change % (15 days)', 'Prev Pos']),
  #            cells=dict(values=[events_sel.string_value.values, events_sel.user_pseudo_id.values, np.round(events_sel.change, 2), events_sel.pos]), domain=dict(x=[0.52, 1],y=[0, 1]))
  #trace0 = go.Pie(values=events_pie.user_pseudo_id, labels=events_pie.string_value, hole=.4, name = 'Events', domain=dict(x=[0.1, 0.5],y=[0, 1]), title_text = 'Top 10 Arts (Based on ArtOpens)', textposition='inside', textinfo='percent', hoverinfo="label+value")
  #fig_dough_opens = go.Figure(data = [trace0, trace]) #trace, 
  #fig_dough_opens.update_layout(title_text='ArtOpen Breakdown From {} to {} (Total ArtOpen {})'.format(min, max, totale))
#fig_dough.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
  #fig_dough_opens.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
  #figs_bq.append(fig_dough_opens)
  

  ##PLOT FIRST OPENS (city wise)
  fo = events_df[events_df.event_name == 'first_open']
  regs = fo.groupby('city').count().reset_index().sort_values('user_pseudo_id', ascending = False).head(7)['city'].values
  idx = [i for i in fo.index if fo.loc[i, 'city'] not in regs or fo.loc[i, 'city'] == '(not set)' ]
  fo.loc[idx, 'city'] = 'Other'
  fo.loc[idx, 'Other'] = "True"
  fo.loc[~fo.index.isin(idx), 'Other'] = 'False'
  fo_fig = fo.groupby(['event_date', 'city', 'Other']).count().reset_index().sort_values('event_date', ascending = True)
  fo_fig['event_date'] = pd.to_datetime(fo_fig['event_date'].astype('str'), format='%Y%m%d')
  fo_fig.sort_values('event_date', inplace = True)
  fo_fig = fo_fig[fo_fig['event_date'] >= pd.to_datetime('2020-12-24',format='%Y-%m-%d' )]
  fo_fig['event_date'] = fo_fig['event_date'].apply(lambda x: x.strftime('%b-%d'))
  
  first_opens = px.bar(fo_fig, x = 'event_date', y = 'user_pseudo_id', color = 'city', facet_row= 'Other', barmode = 'stack', title = 'First Opens per day')
  figs_bq.append(first_opens)

  ##PLOT Sessions (city wise)
  fo = events_df[events_df.event_name == 'session_start']
  regs = fo.groupby('city').count().reset_index().sort_values('user_pseudo_id', ascending = False)['city'].values
  print(regs)
  regs = fo.groupby('city').count().reset_index().sort_values('user_pseudo_id', ascending = False).head(7)['city'].values
  idx = [i for i in fo.index if fo.loc[i, 'city'] not in regs or fo.loc[i, 'city'] == '(not set)' ]
  fo.loc[idx, 'city'] = 'Other'
  fo.loc[idx, 'Other'] = "True"
  fo.loc[~fo.index.isin(idx), 'Other'] = 'False'
  fo_fig = fo.groupby(['event_date', 'city', 'Other']).count().reset_index().sort_values('event_date', ascending = True)
  fo_fig['event_date'] = pd.to_datetime(fo_fig['event_date'].astype('str'), format='%Y%m%d')
  fo_fig.sort_values('event_date', inplace = True)
  fo_fig = fo_fig[fo_fig['event_date'] >= pd.to_datetime('2020-12-24',format='%Y-%m-%d' )]
  fo_fig['event_date'] = fo_fig['event_date'].apply(lambda x: x.strftime('%b-%d'))
  
  sess_opens = px.bar(fo_fig, x = 'event_date', y = 'user_pseudo_id', color = 'city', barmode = 'stack', facet_row= 'Other', title = 'Sessions start per day')
  figs_bq.append(sess_opens)

  regs = events_df.groupby('city').count().reset_index().sort_values('user_pseudo_id', ascending = False).head(7)['city'].values

  states_facet = events_df.groupby(['event_name', 'city']).count().reset_index()
  idx = [i for i in states_facet.index if states_facet.loc[i, 'city'] in regs and states_facet.loc[i, 'city'] != '(not set)']
  states_facet = states_facet.loc[idx,:]

  es = list(events_df.groupby('event_name').count().reset_index().sort_values('user_pseudo_id', ascending = False).head(7)['event_name'].values)
  es.extend(['app_remove','notification_open', "AdWatched"])
  idx = [i for i in states_facet.index if states_facet.loc[i,'event_name'] in es]
  states_facet = states_facet.loc[idx,:]
  country_events = px.bar(states_facet, x = 'user_pseudo_id', y = 'event_name', facet_col= 'city', facet_col_wrap=2, title= 'Events per state (top 5 states)', orientation='h')
  country_events.update_yaxes(matches= 'y', showticklabels=True, title_text='Event', col = 1 )
  country_events.update_xaxes(matches= None, showticklabels=True, title_text='')
  
  figs_bq.append(country_events)
  
  
  
  #path = 'C:\\Users\\User\\Documents\\Python Scripts'
  

  with open('Keap_Normal.html', 'w') as f:
    for file in figs_bq:
      f.write(file.to_html(full_html=False, include_plotlyjs='cdn'))
  
  return figs_bq
  
  

# Retruns the number of days between dates in the df

def date_r(df):
  max_d = df['event_date'].max()
  min_d = df['event_date'].min()
  max_d = pd.to_datetime(str(max_d), format = '%Y%m%d').strftime(format = '%Y-%m-%d')
  min_d = pd.to_datetime(str(min_d), format = '%Y%m%d').strftime(format = '%Y-%m-%d')
  return max_d, min_d

def timestamp_reg(df):
  df['event_timestamp'] = df['event_timestamp']/1000000
  time = datetime.strptime('1970-01-01', '%Y-%m-%d')
  df['event_timestamp'] = df['event_timestamp'].apply(lambda x: time + timedelta(seconds = x))
  return df["event_timestamp"]

def getDayDiff(startDate, endDate):
  d1 = datetime.strptime(str(startDate), "%Y%m%d")
  d2 = datetime.strptime(str(endDate), "%Y%m%d")
  return (d2 - d1).days

## besides building the retention we remove duplicates based on the event we look for
def ret_proxy_habit(start_day,end_date, columns_df, weeks, df, event_name, num = 3, platform = 'None'):
  one_week_micros = 3600*24*7 
  for i in event_name:
    if i not in df['event_name'].unique():
      print('event_name not supported')
      return
  day0 = datetime.strptime(start_day, "%Y%m%d")
  dayend = datetime.strptime(end_date, "%Y%m%d")
  retention = df[df['event_name'] == 'session_start']
  #Calls the function to change the the timestamp series to a datetime series
  retention["event_timestamp"] = timestamp_reg(retention)
  idx = [i for i in retention.index if retention.loc[i, 'event_timestamp'] >= day0 and retention.loc[i, 'event_timestamp'] <= dayend]
  retention = retention.loc[idx, :] 
  rows = pd.DataFrame(columns = columns_df)
  limit = weeks + 1
  totals = []
  #biweeks = weeks // 2 
  for week in range(0,weeks + 1):
    start = (day0) + timedelta(seconds = (one_week_micros) * week) #/ len(week0_users)
    end_0 = start + timedelta(seconds = (one_week_micros))  
    fo_users = df[(df['event_date'] >= int(start.strftime(format = '%Y%m%d'))) & (df['event_date'] < int(end_0.strftime(format = '%Y%m%d'))) ]
    if platform == 'None':
      fo_users = fo_users[fo_users['event_name'] == 'free_trial_start']['user_pseudo_id'].unique()
    elif platform == 'iOS':
      fo_users = fo_users[(fo_users['event_name'] == 'free_trial_start') & (fo_users['operating_system'] == platform)]['user_pseudo_id'].unique()
    elif platform == 'Android':
      fo_users = fo_users[(fo_users['event_name'] == 'free_trial_start') & (fo_users['operating_system'] == platform)]['user_pseudo_id'].unique()

    if num > 0:
      idx = [i for i in df.index if df.loc[i,'event_name'] in event_name and df.loc[i,'user_pseudo_id'] in fo_users]
      temp = df.loc[idx]
      temp['values'] = 1
      week_df = temp[(temp['event_date'] >= int(start.strftime(format = '%Y%m%d'))) & (temp['event_date'] < int(end_0.strftime(format = '%Y%m%d'))) ]
      count_df = week_df.groupby(['event_date','user_pseudo_id']).count().reset_index()
      count_df['values'] = 1
      count_df = count_df.groupby(['user_pseudo_id']).sum().reset_index()
      week0_users = count_df[count_df['values'] >= num]['user_pseudo_id'].unique()
    else:
      idx = [i for i in df.index if df.loc[i,'user_pseudo_id'] in fo_users]
      temp = df.loc[idx]
      temp['values'] = 1
      week_df = temp[(temp['event_date'] >= int(start.strftime(format = '%Y%m%d'))) & (temp['event_date'] < int(end_0.strftime(format = '%Y%m%d'))) ]
      week0_users = week_df.groupby('user_pseudo_id').count().reset_index()['user_pseudo_id'].unique()

    #print(len(users))
    #idx = [i for i in temp.index if temp.loc[i, 'user_pseudo_id'] in users]
    #temp_check = temp.loc[idx, :]
    #week0_df = temp_check[(temp_check['event_date'] >= int(start.strftime(format = '%Y%m%d'))) & (temp_check['event_date'] < int(end_0.strftime(format = '%Y%m%d'))) ]
    #week0_users = week0_df['user_pseudo_id'].unique()
    print(len(week0_users))
    if len(week0_users) != 0:
      to_df = [len([i for i in retention[(retention.event_date >= int((start + timedelta(seconds = one_week_micros * j)).strftime(format = '%Y%m%d'))) & (retention.event_date < int((start + timedelta(seconds = one_week_micros * (j +1))).strftime(format = '%Y%m%d')))]['user_pseudo_id'].unique() if i in week0_users]) / len(week0_users) for j in range(0,limit)] #
      cols = rows.columns[:limit]
      print(cols)
      rows.loc['Mon' + start.strftime(format="%d") + '-' + (end_0 - timedelta(days =1)).strftime(format = "%d") + " (" + str(len(week0_users))+ ")", cols] = to_df
      print(rows)
    else:
      cols = rows.columns[:limit]
      rows.loc['Mon' + start.strftime(format="%b-%d") + '-' + (end_0 - timedelta(days =1)).strftime(format = "%d") + " (0)", cols] = [0] * (limit)
      print(rows)
    ##Distribution of events of week0 users (average per week)
    counts_df = df[(df['event_date'] >= int(start.strftime(format = '%Y%m%d'))) & (df['event_date'] < int(end_0.strftime(format = '%Y%m%d')))]
    idx = [i for i in counts_df.index if counts_df.loc[i, 'user_pseudo_id'] in week0_users]
    counts_df = counts_df.loc[idx, :]
    idx = counts_df.duplicated(['event_date','event_name','event_timestamp', 'user_pseudo_id'], keep = 'first')
    counts_df = counts_df[~idx]
    idx = [ i for i in counts_df.index if counts_df.loc[i, 'key'] == params[-1]]
    counts_df = counts_df[counts_df.index.isin(idx)]
    counts_df = counts_df[(counts_df['string_value'] == 'Keap Mobile Edition') | (counts_df['string_value'] == 'Keap Mobile Free Trial Edition')]
    print(counts_df)
    if week == 0:
      totals = counts_df.groupby('event_name').count().reset_index()[['event_name', 'user_pseudo_id']]
    if week > 0:
      new = counts_df.groupby('event_name').count().reset_index()[['event_name', 'user_pseudo_id']]
      totals = pd.merge(totals, new, how = 'left', left_on = 'event_name', right_on = 'event_name')   
    limit = limit - 1
  rows.fillna(0, inplace = True)
  print(rows)
  return rows, totals

def ret_proxy(start_day,end_date, columns_df, weeks, df, event_name, num = 3):
  one_week_micros = 3600*24*7 
  for i in event_name:
    if i not in df['event_name'].unique():
      print('event_name not supported')
      return
  day0 = datetime.strptime(start_day, "%Y%m%d")
  dayend = datetime.strptime(end_date, "%Y%m%d")
  fo_users = df[(df['event_date'] >= int(day0.strftime(format = '%Y%m%d'))) & (df['event_date'] < int(dayend.strftime(format = '%Y%m%d'))) ]
  fo_users = fo_users[fo_users['event_name'] == 'first_open']['user_pseudo_id'].unique()
  idx = [i for i in df.index if df.loc[i,'event_name'] in event_name and df.loc[i,'user_pseudo_id'] in fo_users]
  temp = df.loc[idx]
  temp['values'] = 1
  retention = df[df['event_name'] == 'session_start']
  #Calls the function to change the the timestamp series to a datetime series
  retention["event_timestamp"] = timestamp_reg(retention)
  idx = [i for i in retention.index if retention.loc[i, 'event_timestamp'] >= day0 and retention.loc[i, 'event_timestamp'] <= dayend]
  retention = retention.loc[idx, :] 
  rows = pd.DataFrame(columns = columns_df)
  limit = weeks
  totals = []
  biweeks = weeks // 2 
  for week in range(0,weeks):
    start = (day0) + timedelta(seconds = (one_week_micros) * week) #/ len(week0_users)
    end_0 = start + timedelta(seconds = (one_week_micros))  
    week_df = temp[(temp['event_date'] >= int(start.strftime(format = '%Y%m%d'))) & (temp['event_date'] < int(end_0.strftime(format = '%Y%m%d'))) ]
    count_df = week_df.groupby('user_pseudo_id').sum().reset_index()
    users = count_df[count_df['values'] >= num]['user_pseudo_id'].unique()
    print(len(users))
    idx = [i for i in temp.index if temp.loc[i, 'user_pseudo_id'] in users]
    temp_check = temp.loc[idx, :]
    week0_df = temp_check[(temp_check['event_date'] >= int(start.strftime(format = '%Y%m%d'))) & (temp_check['event_date'] < int(end_0.strftime(format = '%Y%m%d'))) ]
    week0_users = week0_df['user_pseudo_id'].unique()
    print(len(week0_users))
    if len(week0_users) != 0:
      to_df = [len([i for i in retention[(retention.event_date >= int((start + timedelta(seconds = one_week_micros * j)).strftime(format = '%Y%m%d'))) & (retention.event_date < int((start + timedelta(seconds = one_week_micros * (j +1))).strftime(format = '%Y%m%d')))]['user_pseudo_id'].unique() if i in week0_users]) / len(week0_users) for j in range(0,limit)] #
      cols = rows.columns[:limit]
      rows.loc['Thu' + start.strftime(format="%d") + '-' + end_0.strftime(format = "%d") + " (" + str(len(week0_users))+ ")", cols] = to_df
      print(rows)
    else:
      cols = rows.columns[:limit]
      rows.loc['Thu' + start.strftime(format="%b-%d")+ " (0)", cols] = [0] * limit
      print(rows)
    counts_df = df[(df['event_date'] >= int(start.strftime(format = '%Y%m%d'))) & (df['event_date'] < int(end_0.strftime(format = '%Y%m%d')))]
    idx = [i for i in counts_df.index if counts_df.loc[i, 'user_pseudo_id'] in week0_users]
    counts_df = counts_df.loc[idx]
    idx = counts_df.duplicated(['event_date','event_name','event_timestamp', 'user_pseudo_id'], keep = False)
    idx = [ i for i in counts_df[idx].index if counts_df.loc[i, 'key'] == params[-1]]
    counts_df = counts_df[counts_df.index.isin(idx)]
    counts_df = counts_df[(counts_df['string_value'] == 'Keap Mobile Edition') | (counts_df['string_value'] == 'Keap Mobile Free Trial Edition')]
    if week == 0:
      totals = counts_df.groupby('event_name').count().reset_index()[['event_name', 'user_pseudo_id']]
    if week > 0:
      new = counts_df.groupby('event_name').count().reset_index()[['event_name', 'user_pseudo_id']]
      totals = pd.merge(totals, new, how = 'left', left_on = 'event_name', right_on = 'event_name')   
    limit = weeks - 1
  rows.fillna(0, inplace = True)
  print(rows)
  return rows, totals

def event_based(start_day,end_date, columns_df, weeks, df, event_name = 'first_open', param = None, version = None, limit = None):
  one_week_micros = 3600*24*7 
  if event_name not in df['event_name'].unique():
    print('event_name not supported')
    return
  day0 = datetime.strptime(start_day, "%Y%m%d")
  dayend = datetime.strptime(end_date, "%Y%m%d")
  day1 = (day0 + timedelta(days = 1)).strftime(format = '%Y%m%d')
  temp = df[df['event_name'] == event_name]
  if event_name == 'ArtOpen':
    temp = temp[(temp['key'] == 'coloringId') & (temp['string_value'] == param)]
  else:
    temp = reduce_dups(temp)
  if version:
    temp = temp[(temp['version'] >= int(version)) & (temp['version'] < int(limit))]
  retention = df[df['event_name'] == 'session_start']
  #Calls the function to change the the timestamp series to a datetime series
  retention["event_timestamp"] = timestamp_reg(retention)
  idx = [i for i in retention.index if retention.loc[i, 'event_timestamp'] >= day0 and retention.loc[i, 'event_timestamp'] <= dayend]
  retention = retention.loc[idx, :]
  rows = pd.DataFrame(columns = columns_df)
  print(rows)
  print(retention)
  limit = weeks
  totals = []
  for week in range(0,weeks):
    start = (day0 + timedelta(days = 1)) + timedelta(seconds = one_week_micros * week) 
    end_0 = start + timedelta(seconds = one_week_micros)   
    week0_users = temp[(temp['event_date'] >= int(start.strftime(format = '%Y%m%d'))) & (temp['event_date'] < int(end_0.strftime(format = '%Y%m%d'))) ]['user_pseudo_id'].unique()
    if len(week0_users) != 0:
      to_df = [len([i for i in retention[(retention.event_date >= int((start + timedelta(seconds = one_week_micros * j)).strftime(format = '%Y%m%d'))) & (retention.event_date < int((start + timedelta(seconds = one_week_micros * (j +1))).strftime(format = '%Y%m%d')))]['user_pseudo_id'].unique() if i in week0_users]) / len(week0_users) for j in range(0,limit)]
      cols = rows.columns[:limit]
      rows.loc['Mon' + start.strftime(format="%b-%d") + " (" + str(len(week0_users))+ ")", cols] = to_df
    else:
      cols = rows.columns[:limit]
      rows.loc['Mon' + start.strftime(format="%b-%d")+ " (0)", cols] = [0] * limit
    totals.append(week0_users)    
    limit = weeks - 1
  rows.fillna(0, inplace = True)
  print(rows)
  return rows

def getClassicRetention(startDate, endDate, df):
    grpd_ename = df.groupby('event_name')
    fo_list = grpd_ename.get_group('first_open')
    fo_list_start = fo_list[fo_list['event_date'] == startDate]
    # uniqID_fo_start is a list of unique user ids
    uniqID_fo_start = fo_list_start['user_pseudo_id'].unique()
    # get range of days
    retRange = getDayDiff(startDate, endDate)
    ss_list_day = grpd_ename.get_group('session_start')
    # a list with # of returning users each day, should be of length retRange
    returningUsers = []
    # get datetime, so we can add days in the for loop
    tm = datetime.strptime(str(startDate), "%Y%m%d")
    for day in range(retRange):
        # get active users, check with uniqID_fo_start, get ratio, store in table
        new_date = tm + timedelta(days = day)
        new_date = int(new_date.strftime('%Y%m%d'))
        activeUsersDay = ss_list_day[ss_list_day['event_date'] == new_date]
        returningUsers.append(countSimilarities(uniqID_fo_start,activeUsersDay['user_pseudo_id'].unique()))
    # Retention is ratio of returning users and new users on day 0
    retentionList = [x/fo_list_start['user_pseudo_id'].nunique() for x in returningUsers]
    # can now use list to plot graph, etc
    return retentionList

def getRollingRetention(startDate,endDate,df, art):
    grpd_ename = df.groupby('event_name')
    fo_list = grpd_ename.get_group('ArtOpen')
    fo_list = fo_list[(fo_list['key'] == 'coloringId') & (fo_list['string_value'] == art)]
    print('oweek')
    fo_list_start = fo_list[fo_list['event_date'] == startDate]
    print(fo_list_start)
    # uniqID_fo_start is a list of unique user ids
    uniqID_fo_start = fo_list_start['user_pseudo_id'].unique()
    print(uniqID_fo_start)
    ss_list_day = grpd_ename.get_group('session_start')
    # a list with # of returning users each day, should be of length retRange
    retRange = getDayDiff(startDate, endDate)
    tm = datetime.strptime(str(startDate), "%Y%m%d")
    retention = []
    for day in range(retRange):
        new_date = tm + timedelta(days = day)
        #new_date = int(new_date.strftime('%Y%m%d'))
        days_left = retRange - day
        retList = []
        print(days_left)
        for d in range(days_left):
            nd = new_date + timedelta(days = d)
            nd = int(nd.strftime('%Y%m%d'))
            activeUsersDay = ss_list_day[ss_list_day['event_date'] == nd]
            retList.extend(activeUsersDay['user_pseudo_id'].unique())
        day_ret = countSimilarities(uniqID_fo_start,retList)
        retention.append(day_ret)
    #print(retention)
    if fo_list_start['user_pseudo_id'].nunique() != 0:
      retentionList = [x/fo_list_start['user_pseudo_id'].nunique() for x in retention]
      print(retentionList)
      return retentionList, fo_list_start['user_pseudo_id'].nunique()
    else:
      return None, 0
    
    # can now use list to plot graph, etc
    
# Range Retention is based on new users over some time range, and then compared to
    # returning users in the following time ranges
    # endDate is the end of the time period
    # rangeType is the time period length, i.e week, month as strings

def getRangeRetentionWeek(startDate, endDate, df):
    grpd_ename = df.groupby('event_name')
    fo_list = grpd_ename.get_group('first_open')
    ss_list_day = grpd_ename.get_group('session_start')
    retRange = getDayDiff(startDate, endDate)
    retention = [1]
    fo_count = 0
    if (retRange//7 == 0):
        print('select more than a week')
    else:    
        week0_fo = []
        tm = datetime.strptime(str(startDate), "%Y%m%d")
        for day in range(6):
            date = tm + timedelta(days = day)
            date = int(date.strftime("%Y%m%d"))
            today = fo_list[fo_list['event_date'] == date]
            week0_fo.extend(today['user_pseudo_id'].unique())
        fo_count = len(week0_fo)
        if fo_count != 0:
          for week in range(retRange//7):
            # do something for each week
            week_range_start = tm + timedelta(days = (7*(1+week)))
            mlist = []
            for day in range(6):
                # check for session start unique users that week
                # if the user id matches something in week0_fo, count the user
                # this count/len(set(week0_fo)) is weekly retention
                today = week_range_start + timedelta(days=day)
                today = int(today.strftime('%Y%m%d'))
                activeUsers = ss_list_day[ss_list_day['event_date'] == today]
                mlist.extend(activeUsers['user_pseudo_id'].unique())
            ret = countSimilarities(week0_fo, mlist)
            retention.append(ret/fo_count)
        else:
          retention = [0]*(retRange//6) 
        #retention = [x/fo_count for x in retention]
    return retention, fo_count

def countSimilarities(l1, l2):
    x = 0
    for item in l1:
        if item in l2:
            x = x + 1
    return x

def graphRangeRetention(startDate, endDate,df):
  numWeeks = getDayDiff(startDate, endDate) // 6
  masterRetention = []
  y_axis = []
  for weekRange in range(numWeeks):
    cohortStartDate = datetime.strptime(str(startDate), "%Y%m%d") + timedelta(days=weekRange*7)
    cohortStartDate = int(datetime.strftime(cohortStartDate, "%Y%m%d"))
    
    cohortRetention, cohortCount = getRangeRetentionWeek(cohortStartDate,endDate,df)
    y_axis.append(str(cohortStartDate) + '\r \n {} users'.format(cohortCount))
    masterRetention.append(cohortRetention)
  x_axis = []
  headerVals = ['Cohort']
  for week in range(numWeeks):
    x_axis.append("Week " + str(week))
    headerVals.append("Week " + str(week))
  masterRetention = pd.DataFrame(masterRetention, columns = x_axis)
  masterRetention.insert(loc=0,column='Cohort',value=y_axis)
  masterRetention.fillna(0, inplace=True)
  masterRetention.set_index('Cohort')
  print(masterRetention)
  
  vals = masterRetention.to_numpy().transpose()
  vals[1:,:] = np.round((vals[1:,:]*100).astype(np.double),1)

  fig = go.Figure(go.Table(header=dict(values=headerVals),
                cells=dict(values=vals)))

  fig.update_layout(title_text= 'Last 30 days retention')
  
  return fig


def top_e(df, start_date, end_date):

  day0 = datetime.strptime(start_date, "%Y%m%d")
  dayend = datetime.strptime(end_date, "%Y%m%d")

  df_e = df.copy()
  df_e["event_timestamp"] = timestamp_reg(df_e)
  
  idx = [i for i in df_e.index if df_e.loc[i, 'event_timestamp'] >= day0 and df_e.loc[i, 'event_timestamp'] <= dayend]
  df_e= df_e.loc[idx, :]

  counting = df_e.groupby("event_name").count().reset_name().sort_values("event_timestamp", ascending = False)

  tab_e = go.Figure(data = [go.Table(header=dict(values=['Event_name','Count', 'Count (unique)']),
              cells=dict(values=[counting.event_name.values, counting.event_timestamp.values, counting.event_timestamp.values]))])
  tab_e.update_layout(title_text = "Top events on app")
    
  return tab_e

def top_params(df, start_date, end_date, event, key):
  day0 = datetime.strptime(start_date, "%Y%m%d")
  dayend = datetime.strptime(end_date, "%Y%m%d")
  df_e = df.copy()
  df_e["event_timestamp"] = timestamp_reg(df_e)
  idx = [i for i in df_e.index if df_e.loc[i, 'event_timestamp'] >= day0 and df_e.loc[i, 'event_timestamp'] <= dayend]
  df_e= df_e.loc[idx, :]
  df_e = df_e[(df_e["key"] == key) & (df_e["event_name"] == event)]
  counting = df_e.groupby("string_value").count().reset_index().sort_values("event_timestamp", ascending = False)
  tab_e = go.Figure(data = [go.Table(header=dict(values=['Param','Count', 'Count (unique)']),
              cells=dict(values=[counting.string_value.values, counting.event_timestamp.values, counting.event_timestamp.values]))])
  tab_e.update_layout(title_text = "Top events on app")
  return tab_e

def reduce_dups(df):
  idx = df.duplicated(['event_date','event_name','event_timestamp', 'user_pseudo_id'], keep = False)
  idx_ = [ i for i in df[idx].index if df.loc[i, 'key'] == 'firebase_event_origin']
  #idx_clean = [ i for i in df[idx].index if df.loc[i, 'key'] == 'firebase_event_origin']
  temp = pd.concat([df[df.index.isin(idx_)] , df[~idx]], axis = 0)
  return temp

def reduce_purchases(df):
  print(df.columns)
  idx = df.duplicated(['event_timestamp', 'string_value'], keep = False)
  print(len(idx))
  temp_df = df[idx]
  temp_df['max_timestamp'] = temp_df['event_timestamp'].apply(lambda x: max(temp_df[temp_df['event_timestamp'] == x]['event_timestamp'].values))
  idx_ = [i for i in temp_df.index if temp_df.loc[i, 'event_timestamp'] == temp_df.loc[i, 'max_timestamp']]
  purchases_df = temp_df.loc[idx_, :]
  purchases_df.drop('max_timestamp', axis = 1, inplace = True)
  total_idx = [i for i in df.index if i not in temp_df.index]
  total_df = pd.concat([df.loc[total_idx, :], purchases_df], axis = 0)
  print(total_df.columns)
  return total_df

def query_data(json_path, project_id, table, params, day_ago):
  credentials = service_account.Credentials.from_service_account_file(json_path)
  scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/bigquery'])
  ConnectionServiceAsyncClient(credentials = scoped_credentials)
  bqclient = bigquery.Client(credentials=scoped_credentials, project = project_id)
  date = (datetime.now() - timedelta(days= day_ago))
  string_date = date.strftime('%Y%m%d')
  FROM = table + string_date
  query_string = '''SELECT event_date, event_timestamp, event_name, params.key, params.value.string_value, user_pseudo_id, device.category, device.operating_system, geo.continent, geo.country, geo.city, app_info.version, app_info.install_source, traffic_source.medium, traffic_source.source FROM `{}`, UNNEST(event_params) as params WHERE params.key IN {}'''.format(FROM, params)
  dataframe = (bqclient.query(query_string).result().to_dataframe())
  print(dataframe.head())
  return dataframe

def slice_dfby_date(df, start, end):
  idx = [i for i in df.index if df.loc[i, 'event_date'].astype('float') >= float(start) and df.loc[i, 'event_date'].astype('float') <= float(end)]
  df = df.loc[idx, :]
  return df




def event_digest(df, event_base, groups):
  temp = df[df['event_name'] == event_base]
  tocon = pd.DataFrame(dict(event_timestamp= temp.event_timestamp.unique()))
  for g in groups:
    idx = [i for i in temp.index if temp.loc[i, 'key'] == g]
    temp_main = temp.loc[idx, :]
    tocon = pd.merge(tocon, temp_main, on = 'event_timestamp', how = 'right')
  print(tocon.head())
  tocon['values'] = int(1)
  fig = px.sunburst(tocon, path=['string_value_x', 'string_value_y'], values='values')
  return fig, tocon
  

def event_track(df, result_events):
  #df_base = df[df['event_name'] == 'OnIPBundlePurchasePopupOpened']
  #unique_bun = df_base['user_pseudo_id'].unique()
  numbers = []
  for e in result_events:
    temp_e = df[df['event_name'] == e]
    temp_e.drop_duplicates(subset=['event_timestamp'], inplace= True)
    #temp_e.to_csv('{}.csv'.format(e))
    #idx = temp_e.duplicated(['event_timestamp'], keep = 'first')
    #temp_e = temp_e[~idx]
    uni = temp_e.event_timestamp.unique()
    #u = [i for i in uni if i in unique_bun]
    if len(uni) > 0:
      n = len(uni)
    else:
      n = 0
    numbers.append(n)
  data = pd.DataFrame(dict(number= numbers,stage=result_events))
  fig = px.funnel(data, x='number', y='stage')
  return fig

def event_digest_df(df, df_main, event_base, groups):
  temp = df_main[df_main['event_name'] == event_base]
  dfs = []
  for g in groups:
    temp_g = temp[temp['key'] == g]
    #temp_g = temp_g.drop_duplicates(subset = ['event_timestamp', 'string_value'])
    #temp_df['max_timestamp'] = temp_df['event_timestamp'].apply(lambda x: max(temp_df[temp_df['event_timestamp'] == x]['event_timestamp'].values))
    #idx_ = [i for i in temp_df.index if temp_df.loc[i, 'event_timestamp'] == temp_df.loc[i, 'max_timestamp']]
    #g_df = temp_df.loc[idx_, :]
    #g_df.drop('max_timestamp', axis = 1, inplace = True)
    #total_idx = [i for i in temp_g.index if i not in temp_df.index]
    #total_df = pd.concat([temp_g.loc[total_idx, :], g_df], axis = 0)
    dfs.append(temp_g)
  #stretched = pd.merge(dfs[0], dfs[1], on = 'event_timestamp', how = 'left')
  #stretched.to_csv('stretched.csv')
  tocon = df.copy()
  tocon_one = tocon[tocon['event_name'] == "OnIPBundlePurchased"]
  tocon_half1 = pd.merge(tocon_one, dfs[1], on = ['event_date', 'user_pseudo_id', 'string_value', 'country', 'city'],  how = 'left')
  tocon_half1.to_csv('hi1.csv')
  tocon_half1.drop_duplicates(subset=['event_timestamp_x'], inplace= True)
  tocon_half1.to_csv('hi2.csv')
  tocon_half1['string_value_y'] = tocon_half1['string_value']
  tocon_half1.rename(columns = {'string_value': 'string_value_x'}, inplace = True)
  tocon_two = tocon[tocon['event_name'] == "PlusPurchased"]
  tocon_half2 = pd.merge(tocon_two, dfs[1], on = ['event_date', 'user_pseudo_id', 'country', 'city'],  how = 'left')
  tocon_half2.to_csv('hi3.csv')
  tocon_half2.drop_duplicates(subset=['event_timestamp_x'], inplace= True)
  tocon_half2.to_csv('hi4.csv')
  tocon = pd.concat([tocon_half1, tocon_half2], axis = 0)
  tocon.to_csv('hi5.csv')
  tocon = pd.merge(tocon, dfs[0], left_on = ['event_timestamp_y', 'country', 'city'], right_on = ['event_timestamp', 'country', 'city'],  how = 'left')
  tocon.to_csv('hi6.csv')
  tocon['values'] = int(1)
  tocon.drop_duplicates(subset=['event_timestamp_x'], inplace= True)
  tocon.to_csv('all_done.csv')
  return tocon

def track_purchases(df, event):
  temp_e = df[df['event_name'] == event]
  temp_e = temp_e.drop_duplicates(subset = ['event_timestamp'])
  #temp = pd.merge(temp, temp_e, on = ['user_pseudo_id', 'event_timestamp'], how = 'right')
  #temp.rename(columns = {'key_x': 'key'}, inplace = True)
  temp_e['values'] = int(1)
  return temp_e

if __name__ == '__main__':
  main('20211014','20211029', '20211030', '20211114')