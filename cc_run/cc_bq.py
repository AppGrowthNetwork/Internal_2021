from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
from google.cloud.bigquery_connection_v1.services.connection_service import (
    ConnectionServiceAsyncClient,
)
from google.cloud import bigquery
from google.cloud import bigquery_storage

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


def main():
  '''
  credentials = service_account.Credentials.from_service_account_file(
    'C:\\Users\\User\\Downloads\\color-collab-52972200-b7373ea11e68.json')

  scoped_credentials = credentials.with_scopes(
    ['https://www.googleapis.com/auth/bigquery'])


  ConnectionServiceAsyncClient(credentials = scoped_credentials)

  bqclient = bigquery.Client(credentials=scoped_credentials, project = 'color-collab-52972200')

  date = (datetime.now() - timedelta(days= 1))
  string_date = date.strftime('%Y%m%d')

  FROM = 'color-collab-52972200.analytics_230376997.events_' + string_date
  
  query_string = 
  SELECT  
  event_date, event_timestamp, event_name, params.key, params.value.string_value, user_pseudo_id, device.category, device.operating_system, geo.continent, geo.country, geo.city, app_info.version, app_info.install_source, traffic_source.medium, traffic_source.source
  FROM `{}`, UNNEST(event_params) as params
  WHERE params.key IN ('firebase_event_origin', 'firebase_screen_class', 'coloringId')
  .format(FROM)
  
  dataframe = (
  bqclient.query(query_string)
  .result()
  .to_dataframe()
  )
  print(dataframe.head())
  '''

  #dataframe.to_csv('C:\\Users\\User\\Documents\\Python Scripts\\bq_cc.csv', mode = 'a', header = None)
    

  cols_list = ['event_date','user_pseudo_id', 'event_timestamp', 'event_name', 'version', 'key', 'string_value' ]
  df = pd.read_csv('C:\\Users\\User\\Documents\\Python Scripts\\bq_cc.csv', usecols=cols_list)
  print(df['event_date'].max())
  df['version'] = df['version'].apply(lambda x: re.sub(r"[.]\-\w+$", "", x))
  print(df['version'].unique())
  
  '''
  start_day = 20201228
  end_date = 20210125

  figs_bq = []
  #fig_range = graphRangeRetention(start_day, end_date, df)
  #figs_bq.append(fig_range)

  start_day = '20201130'
  end_date = '20210121'

  ran = getDayDiff(start_day, end_date)
  weeks = ran // 7

  #tem = df[(df['event_name'] == 'ArtOpen') & (df['key'] == 'coloringId')]['string_value'].unique()
  #print(tem)

  
  arts = ['TwigSparks.snailSkull', 'LangoOlivera.Hanna', 'MattBeckerich.roses','TimHendricks.eagle','ClaudiaDeSabe.WomanFace', 'RG.zootsuit','JeffSrsic.Jaguar','ChrisGarver.coiledSnake', 'FlorencioRojas.dancingFrogs']
  
  colors = n_colors('rgb(239, 243, 255)', 'rgb(49, 130, 189)', 11, colortype='rgb')
  for art in arts:
    print(art)
    columns_df = ['week_' + str(i) for i in range(0,weeks)]
    df_table = event_based(start_day, end_date, columns_df, weeks, df, event_name = 'ArtOpen', param = art)
    heads = [i for i in columns_df]
    heads.insert(0,'')
    vals = [np.round(df_table[i].values * 100, 0) for i in columns_df]
    vals.insert(0,df_table.index)
    fills = [np.array(colors)[np.round((df_table[col]* 10).astype('int').values, 0)] for col in df_table.columns]
    fills.insert(0, 'rgb(245, 245, 245)')
    fig = go.Figure(go.Table(header=dict(values= heads),
                cells=dict(values=vals,
                fill_color= fills)))
    fig.update_layout(title_text = "Retention based on users who opened {}".format(art), height = 375)
    figs_bq.append(fig)


  #path = 'C:\\Users\\User\\Documents\\Python Scripts'

  #with open(join(path, 'CC.html'), 'w') as f:
    #for file in figs_bq:
      #f.write(file.to_html(full_html=False, include_plotlyjs='cdn'))

 
  return figs_bq
  '''

# Retruns the number of days between dates

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

def event_based(start_day,end_date, columns_df, weeks, df, event_name = 'first_open', param = None):
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
    idx = temp.duplicated(['event_date','event_timestamp', 'user_pseudo_id'], keep = False)
    idx = [ i for i in temp[idx].index if temp.loc[i, 'key'] == 'firebase_event_origin']
    temp = temp[temp.index.isin(idx)]

  

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
    week0_users = temp[temp['event_date'] == int(start.strftime(format = '%Y%m%d'))]['user_pseudo_id'].unique()
    if len(week0_users) != 0:
      to_df = [len([i for i in retention[(retention.event_date >= int((start + timedelta(seconds = one_week_micros * j)).strftime(format = '%Y%m%d'))) & (retention.event_date < int((start + timedelta(seconds = one_week_micros * (j +1))).strftime(format = '%Y%m%d')))]['user_pseudo_id'].unique() if i in week0_users]) / len(week0_users) for j in range(0,limit)]
      cols = rows.columns[:limit]
      rows.loc[start.strftime(format="%Y-%m-%d") + " (" + str(len(week0_users))+ ")", cols] = to_df
    else:
      cols = rows.columns[:limit]
      rows.loc[start.strftime(format="%Y-%m-%d")+ " (0)", cols] = [0] * limit
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

# Range Retention is based on new users over some time range, and then compared to
    # returning users in the following time ranges
    # endDate is the end of the time period
    # rangeType is the time period length, i.e week, month as strings

def getRangeRetentionWeek(startDate, endDate, df):
    grpd_ename = df.groupby('event_name')
    fo_list = grpd_ename.get_group('first_open')
    ss_list_day = grpd_ename.get_group('session_start')
    retRange = getDayDiff(startDate, endDate)
    retention = []
    
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
          for week in range(retRange//6):
            # do something for each week
            week_range_start = tm + timedelta(days = (6*(1+week)))
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
          retention.append(0)
        #retention = [x/fo_count for x in retention]
    
    return retention

def getRollingRetention(startDate,endDate,df):
    grpd_ename = df.groupby('event_name')
    fo_list = grpd_ename.get_group('first_open')
    fo_list_start = fo_list[fo_list['event_date'] == startDate]
    # uniqID_fo_start is a list of unique user ids
    uniqID_fo_start = fo_list_start['user_pseudo_id'].unique()

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
        for d in range(days_left):
            nd = new_date + timedelta(days = d)
            nd = int(nd.strftime('%Y%m%d'))
            activeUsersDay = ss_list_day[ss_list_day['event_date'] == nd]
            retList.extend(activeUsersDay['user_pseudo_id'].unique())
        day_ret = countSimilarities(uniqID_fo_start,retList)
        retention.append(day_ret)
    #print(retention)
    retentionList = [x/fo_list_start['user_pseudo_id'].nunique() for x in retention]
    # can now use list to plot graph, etc
    return retentionList

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
  for weekRange in range(numWeeks-1):
    cohortStartDate = datetime.strptime(str(startDate), "%Y%m%d") + timedelta(days=weekRange*7)
    cohortStartDate = int(datetime.strftime(cohortStartDate, "%Y%m%d"))
    y_axis.append(cohortStartDate)
    cohortRetention = getRangeRetentionWeek(cohortStartDate,endDate,df)
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
  vals[1:,:] = np.round(vals[1:,:]*100,1)

  fig = go.Figure(go.Table(header=dict(values=headerVals),
                cells=dict(values=vals)))

  fig.update_layout(title_text= 'Last 30 days retention', height = 375)
  
  #fig = ff.create_table(masterRetention)
  #path = 'C:\\Users\\Aleksei Feklisov\\Desktop\\AGN Appollo\\agn_cc'

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

if __name__ == '__main__':
  main()