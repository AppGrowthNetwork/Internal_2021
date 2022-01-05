from googleads import adwords, oauth2
from appsflyer import AppsFlyer
from os.path import join
import pandas as pd
import io
from datetime import datetime, timedelta
import numpy as np
import json

import locale
import sys
import _locale

#from gspread_pandas import Spread, Client

from plotly.offline import plot
import plotly.express as px
from plotly.graph_objs import *
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import n_colors



_locale._getdefaultlocale = (lambda *args: ['en_US', 'UTF-8'])


def main():

    # We call our main delivery-boy function to do all the work


    #start_date_ = '2014-10-16'
    #end_date_ = (datetime.now() - timedelta(days= 43))
    
    start_date = '2021-08-01'
    end_date = (datetime.now() - timedelta(days= 1))

    client_id = '422898392645-kq6mc00a3h0c857qdp8jsre7pi9gjntv.apps.googleusercontent.com'
    client_secret = 'AH28CNr8Lnuuhw-irN6smI_O'
    refresh_token = '1//05OSJ-n2oByWCCgYIARAAGAUSNwF-L9IrnDBgcEpKTk5U3zem54PO2KUWWYSsgF2NBEBF33qM-lg118tPaHrKrKSSsWdcHx3B0-Q'
    developer_token = 'PJY5mhXidEqXfbuCZES9PQ'
    client_customer_id = '418-216-1384'

    ##client_id = '668318876553-b0m41upl4j68o1pjo4jvh5jhblvl0uke.apps.googleusercontent.com'
    #client_secret = 'f42IXqeThqdO3t83xfndjKOz'
    #refresh_token = '1//05vvY0sNML_G8CgYIARAAGAUSNwF-L9IrnPCJtIH7ZxPbkEEvAdU03C_KNp3-Qd0_yA-X2zZE9f7RnXdmfSzAEKaN8G9clIp--F8'
    #developer_token = 'PJY5mhXidEqXfbuCZES9PQ'
    #client_customer_id = '493-170-1935'


    #app_id = "id902026228"
    #api_token = "94c1018e-ab1a-4eb2-95b4-b46dc0c5de89"

    #start_DATE_ = '2020-10-18'
    #end_DATE_ = (datetime.now() - timedelta(days= 21)).strftime("%Y-%m-%d")

    

    #df_af_asa = get_geo_by_date_report(app_id, api_token, start_DATE_, end_DATE_)
    #df_af_asa = df_af_asa[df_af_asa['Media Source (pid)'] == 'googleadwords_int']
    #print(df_af_asa['Campaign (c)'].unique())

    #api_id = "com.ugroupmedia.pnp14"
    
    #df_af_g = get_geo_by_date_report(api_id, api_token, start_date_, end_DATE_)
    #df_af_g = df_af_g[df_af_g['Media Source (pid)'] == 'googleadwords_int']
    
    #print(df_af_g.columns)
    #df_date = df_af_g.groupby(['Date', 'Campaign (c)', 'Country']).sum().reset_index()
    #df_level = df_date[['Date','Campaign (c)','af_subscribe (Sales in CAD)', 'Country']]

    figs_gads = []
    #df1 = get_age(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date, end_date)
    #print(df1.head())
    #print(df1.columns)

    #df1 = df1[df1['Campaign state'] == 'enabled']
    #df1 = df1.groupby(['Age Range', 'Campaign']).sum().reset_index()

    scala = ['#0508b8', '#1910d8', '#3c19f0', '#6b1cfb', '#981cfd', '#bf1cfd', '#dd2bfd', '#f246fe', '#fc67fd', '#fe88fc', '#fea5fd', '#febefe', '#fec3fe',
            '#440154', '#482878', '#3e4989', '#31688e', '#26828e', '#1f9e89', '#35b779', '#6ece58', '#b5de2b', '#fde725','#0508b8', '#1910d8']
    j = 0

    #demo = make_subplots(rows = 1, cols =2, subplot_titles=('Age Range', 'Distribution of Revenue by Age'))
    #demo.add_trace(go.Bar(x = df1.Impressions, y = df1['Age Range'], orientation = 'h', name='Impressions'), 1,1)
    #demo.add_trace(go.Bar(x = df1.Clicks, y = df1['Age Range'], orientation = 'h', name='Clicks'),1,1)
    #demo.add_trace(go.Bar(x = df1.Conversions, y = df1['Age Range'], orientation = 'h', name='Conversions'),1,1)
    
    
   
    #for i in df1['Campaign'].unique():
    #    demo.add_trace(go.Scatter(y = df1[df1['Campaign'] == i]['Total conv. value'], x = df1[df1['Campaign'] == i]['Age Range'], marker_color = scala[j], name = i ),1,2)
    #    j+= 1
    #demo.update_layout(barmode = 'stack', title_text = 'Demographics')
    #figs_gads.append(demo)

    #df_ = get_placement(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date_, end_date_)
    #df_ = df_[df_['Campaign state'] == 'enabled']
    #df_ = df_.groupby(['Day', 'Campaign','Network']).sum().reset_index()
    
    #print(df_)

    #df_yt = get_placement_yt(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date_, end_date_)
    #print(df_yt)
    #df_yt = df_yt[df_yt['Campaign state'] == 'enabled']
    #df_yt = df_yt.groupby(['Day', 'Campaign','Network']).sum().reset_index()
    #print(df_yt)

    #joined = pd.concat([df_yt, df_], axis = 0)
    #yt_plot = joined.groupby(['Day', 'Campaign']).sum().reset_index()
    #print(joined)



    #yt = make_subplots(rows = 1, cols = 2, subplot_titles = ('Conversions per campaign', 'Revenue','Distribution per Network'), specs= [[{}, {"type": "domain"}]])
    #color_map = ['#EECA3B','green','orange','red']
    #j=0
    #for i in yt_plot.Campaign.unique():
       # yt.add_trace(go.Bar(x = yt_plot[yt_plot['Campaign'] == i]['Day'], y =yt_plot[yt_plot['Campaign'] == i]['Clicks'], name = i, marker_color = color_map[j]), 1,1)
       # j+=1
    #yt.add_trace(go.Scatter(x = yt_plot['Day'], y = yt_plot['Total conv. value'], name = 'Revenue'), 1,1)
    #yt.add_trace(go.Pie(values=joined['Total conv. value'], labels = joined['Network'], marker_colors=['lightcyan','royalblue']),row=1, col=2)
    #yt.update_layout(barmode = 'stack', title_text="Display Network & YT Videos Performance")


    df = get_campaign_performance_report(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date, end_date)
    #df_19 = get_campaign_performance_report(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date, end_date)
    channels = get_ad_performance(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date, end_date)
    #df_b = get_budget_report(client_id, client_secret, refresh_token, developer_token, client_customer_id, end_date_, end_date_)

    print(df.columns)
    #and df.loc[i, 'Campaign serving status'] == 'eligible'
    #Pick uac campaigns
    #index_uac = [i for i in df.index if 'NB' not in df.loc[i,'Campaign'] and 'BRANDED' not in df.loc[i,'Campaign'] and 'UAC' in df.loc[i,'Campaign'] ]
    #uac_campaigns = df.iloc[index_uac,:]

    #index_uac = [i for i in df_19.index if 'NB' not in df_19.loc[i,'Campaign'] and 'BRANDED' not in df_19.loc[i,'Campaign'] and 'UAC' in df_19.loc[i,'Campaign'] ]
    #uac_campaigns_19 = df_19.iloc[index_uac,:]
    
    #Pick nb campaigns
    #index_nb = [i for i in df.index if 'BRANDED' not in df.loc[i,'Campaign'] and 'UAC' not in df.loc[i,'Campaign'] and 'S - NB' in df.loc[i,'Campaign']]
    #nb_campaigns = df.iloc[index_nb,:]

    #index_nb = [i for i in df_19.index if 'BRANDED' not in df_19.loc[i,'Campaign'] and 'UAC' not in df_19.loc[i,'Campaign'] and 'S - NB' in df_19.loc[i,'Campaign'] ]
    #nb_campaigns_19 = df_19.iloc[index_nb,:]

    #Pick branded campaigns
    #index_b = [i for i in df.index if 'UAC' not in df.loc[i,'Campaign'] and 'NB' not in df.loc[i,'Campaign'] and 'BRANDED' in df.loc[i,'Campaign']  ]
    #b_campaigns = df.iloc[index_b,:]

    #index_b = [i for i in df_19.index if 'UAC' not in df_19.loc[i,'Campaign'] and 'NB' not in df_19.loc[i,'Campaign'] and 'BRANDED' in df_19.loc[i,'Campaign'] ]
    #b_campaigns_19 = df_19.iloc[index_b,:]


    #uac_campaigns['type'] = 'UAC'
    #nb_campaigns['type'] = 'Non-Branded'
    #b_campaigns['type'] = 'Branded'

    ##uac_campaigns_19['type'] = 'UAC'
    #nb_campaigns_19['type'] = 'Non-Branded'
    #b_campaigns_19['type'] = 'Branded'

    #unified = pd.concat([uac_campaigns, nb_campaigns, b_campaigns], axis = 0)
    temp = df.copy()
    print(temp.head())

    ### Filtering by end_date
    #uac_campaigns_day = uac_campaigns[uac_campaigns['Day'] == end_date_.strftime('%Y-%m-%d')]

    #nb_campaigns_day = nb_campaigns[nb_campaigns['Day'] == end_date_.strftime('%Y-%m-%d')]

    #b_campaigns_day = b_campaigns[b_campaigns['Day'] == end_date_.strftime('%Y-%m-%d')]

    #df_level['type'] = 'Adwords'

    #for i in df_level.index:
        #if 'UAC' in df_level.loc[i, 'Campaign (c)'] and 'NB' not in df_level.loc[i, 'Campaign (c)'] and 'BRANDED' not in df_level.loc[i, 'Campaign (c)']:
           # df_level.loc[i, 'type'] = 'UAC'
        #if 'NB' in df_level.loc[i, 'Campaign (c)'] and 'UAC' not in df_level.loc[i, 'Campaign (c)'] and 'BRANDED' not in df_level.loc[i, 'Campaign (c)']:
           # df_level.loc[i, 'type'] = 'Non-Branded'
        #if 'BRANDED' in df_level.loc[i, 'Campaign (c)'] and 'NB' not in df_level.loc[i, 'Campaign (c)'] and 'UAC' not in df_level.loc[i, 'Campaign (c)']:
          #  df_level.loc[i, 'type'] = 'Branded'
    
    #df_level = df_level[df_level['type'] != 'Adwords']        
    
    #plot_rev = pd.merge(temp.groupby(['Day','type']).sum().reset_index(),df_level.groupby(['Date', 'type']).sum().reset_index(), how = 'left', left_on =['Day', 'type'], right_on = ['Date', 'type'])
    #plot_rev = temp.groupby(['Day','type']).sum().reset_index()
    plot_rev = temp.groupby('Day').sum().reset_index()

    plot_rev['Day'] = pd.to_datetime(plot_rev['Day'], format ='%Y-%m-%d')
    #for i in range(len(plot_rev)):
        #if (plot_rev.loc[i,'Day'] < pd.to_datetime('2020-11-29', format='%Y-%m-%d')):  
            #plot_rev.loc[i,'Total conv. value'] = plot_rev.loc[i,'Total conv. value'] + plot_rev.loc[i,'af_subscribe (Sales in CAD)']
    plot_rev['Cost'] = plot_rev['Cost'] / 1000000
    plot_rev['ROAS'] = plot_rev['Total conv. value'] / plot_rev['Cost']
    #plot_rev[['Day','type','Conversions','Cost','Total conv. value', 'ROAS']].to_csv('upload_Adwords.csv')
    plot_rev['Day'] = plot_rev['Day'].apply(lambda x: x.strftime('%Y-%m-%d'))
    #subs_day = df_level[df_level['Date'] == end_date_.strftime('%Y-%m-%d')]

    #+ subs_day[subs_day['type'] == 'UAC']['af_subscribe (Sales in CAD)'].sum())
    ## Budget sheet (just end date totals)
    #if len(uac_campaigns_day.columns) > 0:
        #uac_totals = pd.DataFrame({'Date': end_date_.strftime('%Y-%m-%d'), 'Network': 'Google UAC', 'Installs': uac_campaigns_day['Conversions'].sum() , 'Cost': uac_campaigns_day['Cost'].sum(), 'Revenue' : uac_campaigns_day['Total conv. value'].sum()}, index = range(0,1))
    #else:
        #uac_totals = pd.DataFrame({'Date': end_date_.strftime('%Y-%m-%d'), 'Network': 'Google UAC', 'Installs': 0, 'Cost': 0, 'Revenue': 0}, index = range(0,1))
    #if len(nb_campaigns_day.columns) > 0:
        #nb_totals = pd.DataFrame({'Date': end_date_.strftime('%Y-%m-%d'), 'Network': 'Google Search (Non-Branded)', 'Installs': nb_campaigns_day['Conversions'].sum() , 'Cost': nb_campaigns_day['Cost'].sum(), 'Revenue' : nb_campaigns_day['Total conv. value'].sum()}, index = range(0,1))
    #else:
        #nb_totals = pd.DataFrame({'Date': end_date_.strftime('%Y-%m-%d'), 'Network': 'Google Search (Non-Branded)', 'Installs': 0, 'Cost': 0, 'Revenue': 0}, index = range(0,1))
    #if len(b_campaigns_day.columns) > 0:
        #branded_totals = pd.DataFrame({'Date': end_date_.strftime('%Y-%m-%d'), 'Network': 'Google Search (Branded)', 'Installs': b_campaigns_day['Conversions'].sum() , 'Cost': b_campaigns_day['Cost'].sum(), 'Revenue' : b_campaigns_day['Total conv. value'].sum()}, index = range(0,1))
    #else:
        #branded_totals = pd.DataFrame({'Date': end_date_.strftime('%Y-%m-%d'), 'Network': 'Google Search (Branded)', 'Installs': 0, 'Cost': 0, 'Revenue': 0}, index = range(0,1))

    

    #upload = pd.concat([uac_totals,branded_totals, nb_totals], axis =0)
    #upload['Cost'] = upload['Cost'] / 1000000
    #upload['ROAS'] = upload['Revenue'] / upload['Cost']
    #print(upload)
    #sheet_name = 'Daily_overview'
    #drive_g(upload, sheet_name)

    #unified_19 = pd.concat([uac_campaigns_19, nb_campaigns_19, b_campaigns_19], axis = 0)    
    #unified_19 = df_19.copy()

    #unified_19['Day'] = pd.to_datetime(unified_19['Day'], format ='%Y-%m-%d')
    #for i in range(len(unified_19)):
        #if (unified_19.loc[i,'Day'] < pd.to_datetime('2020-11-29', format='%Y-%m-%d')):  
            #unified_19.loc[i,'Total conv. value'] = unified_19.loc[i,'Total conv. value'] + unified_19.loc[i,'af_subscribe (Sales in CAD)']
    #unified_19['Cost'] = unified_19['Cost'] / 1000000
    #unified_19['ROAS'] = unified_19['Total conv. value'] / unified_19['Cost']
    #unified_19[['Day','type','Conversions','Cost','Total conv. value', 'ROAS']].to_csv('upload_Adwords.csv')
    #unified_19['Day'] = unified_19['Day'].apply(lambda x: x.strftime('%Y-%m-%d'))

    

    #uac_plot_19 = unified_19.groupby('Day').sum().reset_index()
    #uac_plot_19['avgCPC'] = uac_plot_19['Cost'] / uac_plot_19['Conversions']
    #uac_plot_19['TTR'] = uac_plot_19['Clicks'] / uac_plot_19['Impressions']
    #uac_plot_19['convRate'] = uac_plot_19['Conversions'] / uac_plot_19['Clicks']
    #uac_plot_19['ROAS'] = uac_plot_19['Total conv. value'] / uac_plot_19['Cost']


    uac_plot = plot_rev.groupby('Day').sum().reset_index()
    uac_plot['avgCPC'] = uac_plot['Cost'] / uac_plot['Conversions']
    uac_plot['TTR'] = uac_plot['Clicks'] / uac_plot['Impressions']
    uac_plot['convRate'] = uac_plot['Conversions'] / uac_plot['Clicks']
    uac_plot['ROAS'] = uac_plot['Total conv. value'] / uac_plot['Cost']
    #print(uac_plot)

    #uac_plot_uni = pd.concat([uac_plot_19, uac_plot])
    #uac_plot_uni['Year'] = uac_plot_uni['Day'].apply(lambda x: str(x)[:4])
    #uac_plot_uni['Day'] = pd.to_datetime(uac_plot_uni['Day'], format='%Y-%m-%d')
    #uac_plot_uni = uac_plot_uni.groupby(['Day','Year']).sum().reset_index().sort_values('Day', ascending = True)
    #uac_plot_uni['Day'] = uac_plot_uni['Day'].apply(lambda x: x.strftime('%b-%d'))
    


    df_geo = get_geo_performance(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date, end_date)
    end_date = (datetime.now() - timedelta(days= 406))
    #print(df_geo.columns)
    #df_geo_19 = get_geo_performance(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date, end_date)
    #df_geo = df_geo[df_geo['Campaign state'] == 'enabled']
    #locations = list(df_geo[df_geo['Location'] != ' --']['Location'].unique())
    #print(locations)
    #locations_19 = list(df_geo_19[df_geo_19['Location'] != ' --']['Location'].unique())
    #print(locations_19)
    #loc_details = get_location(client_id, client_secret, refresh_token, developer_token, client_customer_id, locations)
    #loc_details_19 = get_location(client_id, client_secret, refresh_token, developer_token, client_customer_id, locations_19)
    #dict_loc = {}
    #dict_loc_19 = {}
    #for location in loc_details:
    #    dict_loc[str(location['location']['id'])] = location['location']['locationName']
    #for location in loc_details_19:
    #    dict_loc_19[str(location['location']['id'])] = location['location']['locationName']

    df_geo['Cost'] = df_geo['Cost'] / 1000000
    #df_geo['locationName'] = df_geo['Location'].map(dict_loc) 
    df_geo['ROAS'] = df_geo['Total conv. value'].astype('float') / df_geo['Cost'].astype('float')
    df_geo['ARPU'] = df_geo['Total conv. value'].astype('float') / df_geo['Conversions'].astype('float')
    #df_geo['locationName'] = df_geo['locationName'].fillna('Other')

    #df_geo_19['Cost'] = df_geo_19['Cost'] / 1000000
    #df_geo_19['locationName'] = df_geo_19['Location'].map(dict_loc_19) 
    #df_geo_19['ROAS'] = df_geo_19['Total conv. value'].astype('float') / df_geo_19['Cost'].astype('float')
    #df_geo_19['ARPU'] = df_geo_19['Total conv. value'].astype('float') / df_geo_19['Conversions'].astype('float')
    #df_geo_19['locationName'] = df_geo_19['locationName'].fillna('Other')

    
    ### Per campaign/country

    #uac
    #indx = [i for i in df_geo.index if 'UAC' in df_geo.loc[i, 'Campaign'] and 'NB' not in df_geo.loc[i, 'Campaign'] and 'BRANDED' not in df_geo.loc[i, 'Campaign']]
    #df_geo_camp_uac = df_geo.loc[indx, :]

    #indx = [i for i in df_geo_19.index if 'UAC' in df_geo_19.loc[i, 'Campaign'] and 'NB' not in df_geo_19.loc[i, 'Campaign'] and 'BRANDED' not in df_geo_19.loc[i, 'Campaign']]
    #df_geo_camp_uac_19 = df_geo_19.loc[indx,:]

    #nb
    #indx = [i for i in df_geo.index if 'NB' in df_geo.loc[i, 'Campaign'] and 'UAC' not in df_geo.loc[i, 'Campaign'] and 'BRANDED' not in df_geo.loc[i, 'Campaign']]
    #df_geo_camp_nb = df_geo.loc[indx, :]

    #indx = [i for i in df_geo_19.index if 'NB' in df_geo_19.loc[i, 'Campaign'] and 'UAC' not in df_geo_19.loc[i, 'Campaign'] and 'BRANDED' not in df_geo_19.loc[i, 'Campaign']]
    #df_geo_camp_nb_19 = df_geo_19.loc[indx,:]

    #b
    #indx = [i for i in df_geo.index if 'BRANDED' in df_geo.loc[i, 'Campaign'] and 'NB' not in df_geo.loc[i, 'Campaign'] and 'UAC' not in df_geo.loc[i, 'Campaign']]
    #df_geo_camp_b = df_geo.loc[indx, :]
    
    #indx = [i for i in df_geo_19.index if 'BRANDED' in df_geo_19.loc[i, 'Campaign'] and 'NB' not in df_geo_19.loc[i, 'Campaign'] and 'UAC' not in df_geo_19.loc[i, 'Campaign']]
    #df_geo_camp_b_19 = df_geo_19.loc[indx,:]

    #uac merged campaigns 20 and 19
    #df_geo_camp_uac['type'] = 'UAC'
    #df_geo_camp_nb['type'] = 'Non-Branded'
    #df_geo_camp_b['type'] = 'Branded'
    #df_geo_camp_uac_19['type'] = 'UAC'
    #df_geo_camp_nb_19['type'] = 'Non-Branded'
    #df_geo_camp_b_19['type'] = 'Branded'

    #geo_camp_uni = pd.concat([df_geo_camp_uac, df_geo_camp_nb, df_geo_camp_b], axis = 0)
    geo_camp_uni = df_geo.copy()
    #geo_camp_uni_19 = pd.concat([df_geo_camp_uac_19, df_geo_camp_nb_19, df_geo_camp_b_19], axis = 0)
    #geo_camp_uni_19 = df_geo_19.copy()

    #print(geo_camp_uni['locationName'].unique())
    dic_country = {'AU' :'Australia', 'CA': 'Canada', 'UK': 'United Kingdom', 'IT': 'Italy', 'FR': 'France', 'US': 'United States',
                    'AR': 'Argentina', 'MX': 'Mexico', 'BE':'Belgium', 'ES':'Spain', 'ZA':'South Africa', 'NZ': 'New Zealand', 'CH':'Switzerland', 'IE':'Ireland'}
    #df_level['Country'] = df_level['Country'].map(dic_country)
    #df_subs = df_level.groupby(['Date','type', 'Country']).sum().reset_index()

    geo_report_ = geo_camp_uni.groupby(['Day']).sum().reset_index()
    #geo_report_ = geo_camp_uni.groupby(['Day', 'locationName']).sum().reset_index()

    #geo_report19 = geo_camp_uni_19.groupby(['Day', 'locationName']).sum().reset_index()
    
    geo_report = geo_report_.copy()
    #pd.merge(geo_report, df_subs, how = 'left', left_on= ['Day', 'type', 'locationName'], right_on= ['Date', 'type', 'Country'])
    #geo_report['Total conv. value'] = geo_report['Total conv. value'].astype('float') + geo_report['af_subscribe (Sales in CAD)'].astype('float')

    #geo_camp_total = pd.concat([geo_report, geo_report19], axis = 0)
    geo_camp_total = geo_report.copy()
    #geo_camp_total['Year'] = geo_camp_total['Day'].apply(lambda x: str(x)[:4])
    geo_camp_total['Day'] = pd.to_datetime(geo_camp_total['Day'], format='%Y-%m-%d')

   
    #geo_camp_fig = geo_camp_total.copy()


    #geo_camp_total = geo_report[geo_report['locationName'] != 'Other']
    
    geo_camp_total = geo_camp_total.groupby(['Day']).sum().reset_index().sort_values('Day', ascending = True)
    #geo_camp_total = geo_camp_total.groupby(['Day', 'locationName', 'Year']).sum().reset_index().sort_values('Day', ascending = True)
    geo_camp_total['Day'] = geo_camp_total['Day'].apply(lambda x: x.strftime('%b-%d'))
    
    

    
    fig = make_subplots( rows=1, cols=2, column_widths=[0.5, 0.5], specs=[[{'secondary_y':True}, {'secondary_y':True}]],
                    subplot_titles=("Daily Adwords Conversions vs. CPC", "Daily Adwords Revenue KPIs" ))

    # Add traces

    fig.add_trace(go.Scatter(x=uac_plot.Day, y=uac_plot['Cost'],
                    mode='lines+markers',
                    name='Cost', marker_color = '#109618'), row =1 , col = 2)
    fig.add_trace(go.Scatter(x=uac_plot.Day, y=uac_plot.avgCPC, name = 'CPC', marker_color = '#EF553B'), secondary_y = True, row=1, col=1)
    fig.add_trace(go.Bar(x=plot_rev.groupby('Day').sum().index, y=plot_rev.groupby('Day').sum()['Total conv. value'], marker_color = '#FEAF16', name = 'Conv. Value'),  row=1, col=2)

    fig.add_trace(go.Scatter(x=uac_plot['Day'], y=uac_plot['Total conv. value'] / uac_plot['Cost'],
                    mode='lines+markers',
                    name='Daily ROAS', marker_color = '#511CFB'), secondary_y = True, row =1 , col = 2)

    #fig.add_trace(go.Bar(x=uac_plot.Day, y=plot_rev.groupby(['Day','type']).sum()['Conversions'].loc[slice(None), 'UAC'],
     #               name='UAC', marker_color = 'rgb(204,204,204)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=uac_plot['Day'], y=uac_plot['Conversions'],
                    name='Conversions', marker_color = 'cyan'), row=1, col=1)
    #fig.add_trace(go.Scatter(x = np.array([uac_plot.set_index('Day').index[0], uac_plot.set_index('Day').index[-1]]), y = np.array([(uac_plot['Conversions'].sum()/71), (uac_plot_uni[uac_plot_uni['Year'] == '2020']['Conversions'].sum()/71)]), marker_color = 'cyan', name = 'Avg.', mode="lines+text", text=['Conv-20', '+115%']), row =1, col = 1)


    #fig.add_trace(go.Bar(x=uac_plot.Day, y=plot_rev.groupby(['Day','type']).sum()['Conversions'].loc[slice(None), 'Non-Branded'],
         #           name='Non-Branded', marker_color = '#FF6692'), row=1, col=1)
    #fig.add_trace(go.Bar(x=uac_plot.Day, y=plot_rev.groupby(['Day','type']).sum()['Conversions'].loc[slice(None), 'Branded'],
         #           name='Branded', marker_color = '#AB63FA'), row=1, col=1)
    
    #fig.add_trace(go.Scatter(x = np.array([uac_plot_uni[uac_plot_uni['Year'] == '2020'].set_index('Day').index[0], uac_plot_uni[uac_plot_uni['Year'] == '2020'].set_index('Day').index[-1]]), y = np.array([(uac_plot_uni[uac_plot_uni['Year'] == '2020']['Total conv. value'].sum()/71), (uac_plot_uni[uac_plot_uni['Year'] == '2020']['Total conv. value'].sum()/71)]), marker_color = 'cyan', showlegend = False, mode="lines+text", text=['Rev-20', '+33%']), row =1, col = 2)

    #fig.add_trace(go.Bar(x=plot_rev.groupby('Day').sum().index, y=plot_rev.groupby(['Day','type']).sum()['Total conv. value'].loc[slice(None), 'UAC'], marker_color = 'rgb(204,204,204)', name = 'UAC-Rev', showlegend = False),  row=1, col=2)
    #fig.add_trace(go.Bar(x=plot_rev.groupby('Day').sum().index, y=plot_rev.groupby(['Day','type']).sum()['Total conv. value'].loc[slice(None), 'Non-Branded'], marker_color = '#FF6692', name = 'Non-Branded-Rev', showlegend = False),  row=1, col=2)
    #fig.add_trace(go.Bar(x=plot_rev.groupby('Day').sum().index, y=plot_rev.groupby(['Day','type']).sum()['Total conv. value'].loc[slice(None), 'Branded'], marker_color = '#AB63FA', name = 'Branded-Rev', showlegend = False),  row=1, col=2)
    
    fig.add_trace(go.Scatter(x=plot_rev.groupby('Day').sum().index, y=plot_rev.groupby('Day').sum()['Total conv. value'],
                    mode='lines+markers',
                    name='Revenue', marker_color = '#FEAF16'), row =1 , col = 2)
    
    fig.update_layout(barmode = 'stack', height = 600, title_text = 'OVERVIEW')
            
    figs_gads.append(fig)
    #fig_19 = make_subplots( rows=1, cols=2, column_widths=[0.5, 0.5], specs=[[{'secondary_y':True}, {'secondary_y':True}]],
                   # subplot_titles=("Daily Adwords Conversions vs. CPC", "Daily Adwords Revenue KPIs" ))

    # Add traces

    #fig.add_trace(go.Scatter(x=uac_plot_19.Day, y=uac_plot_19['Cost'],
                   # mode='lines+markers',
                   # name='Cost', marker_color = '#109618', showlegend = False), row =2 , col = 2)
    #fig.add_trace(go.Scatter(x=uac_plot_19.Day, y=uac_plot_19.avgCPC, name = 'CPC', marker_color = '#EF553B', showlegend = False), secondary_y = True, row=2, col=1)
    #fig.add_trace(go.Scatter(x=uac_plot_uni[uac_plot_uni['Year'] == '2019']['Day'], y=uac_plot_uni[uac_plot_uni['Year'] == '2019']['Total conv. value'] / uac_plot_uni[uac_plot_uni['Year'] == '2019']['Cost'],
    #                mode='lines+markers',
    #                name='Daily ROAS-2019', marker_color = 'rgb(204,204,204)'), secondary_y = True, row =1 , col = 2)
    

    #fig.add_trace(go.Bar(x=uac_plot_19.Day, y=uac_plot_19.groupby(['Day','type']).sum()['Conversions'].loc[slice(None), 'UAC'],
     #               name='UAC', marker_color = 'rgb(204,204,204)'), row=1, col=1)
    #fig.add_trace(go.Scatter(x=uac_plot_uni[uac_plot_uni['Year'] == '2019']['Day'], y=uac_plot_uni[uac_plot_uni['Year'] == '2019']['Conversions'],
    #                name='Conversions-2019', marker_color = 'rgb(204,204,204)'), row=1, col=1)
    #fig.add_trace(go.Scatter(x = np.array([uac_plot_uni[uac_plot_uni['Year'] == '2019'].set_index('Day').index[0], uac_plot_uni[uac_plot_uni['Year'] == '2019'].set_index('Day').index[-1]]), y = np.array([(uac_plot_uni[uac_plot_uni['Year'] == '2019']['Conversions'].sum()/71), (uac_plot_uni[uac_plot_uni['Year'] == '2019']['Conversions'].sum()/71)]), marker_color = 'rgb(204,204,204)', showlegend = False, mode="lines+text", text=['Conv-19', 'xx.x k']), row =1, col = 1)

    #fig.add_trace(go.Bar(x=uac_plot_19.Day, y=uac_plot_19.groupby(['Day','type']).sum()['Conversions'].loc[slice(None), 'Non-Branded'],
         #           name='Non-Branded', marker_color = '#FF6692'), row=1, col=1)
    #fig.add_trace(go.Bar(x=uac_plot_19.Day, y=uac_plot_19.groupby(['Day','type']).sum()['Conversions'].loc[slice(None), 'Branded'],
         #           name='Branded', marker_color = '#AB63FA'), row=1, col=1)
    #fig.add_trace(go.Bar(x=uac_plot_19.groupby('Day').sum().index, y=uac_plot_19.groupby(['Day']).sum()['Total conv. value'], marker_color = '#FEAF16', name = 'Conv. Value', showlegend = False),  row=2, col=2)
    #fig.add_trace(go.Scatter(x = np.array([uac_plot_uni[uac_plot_uni['Year'] == '2019'].set_index('Day').index[0], uac_plot_uni[uac_plot_uni['Year'] == '2019'].set_index('Day').index[-1]]), y = np.array([(uac_plot_uni[uac_plot_uni['Year'] == '2019']['Total conv. value'].sum()/71), (uac_plot_uni[uac_plot_uni['Year'] == '2019']['Total conv. value'].sum()/71)]), marker_color = 'rgb(204,204,204)', showlegend = False, mode="lines+text", text=['Rev-19', 'xx.x k']), row =1, col = 2)
    #fig.add_trace(go.Bar(x=unified_19.groupby('Day').sum().index, y=unified_19.groupby(['Day','type']).sum()['Total conv. value'].loc[slice(None), 'UAC'], marker_color = 'rgb(204,204,204)', name = 'UAC-Rev', showlegend = False),  row=1, col=2)
    #fig.add_trace(go.Bar(x=unified_19.groupby('Day').sum().index, y=unified_19.groupby(['Day','type']).sum()['Total conv. value'].loc[slice(None), 'Non-Branded'], marker_color = '#FF6692', name = 'Non-Branded-Rev', showlegend = False),  row=1, col=2)
    #fig.add_trace(go.Bar(x=unified_19.groupby('Day').sum().index, y=unified_19.groupby(['Day','type']).sum()['Total conv. value'].loc[slice(None), 'Branded'], marker_color = '#AB63FA', name = 'Branded-Rev', showlegend = False),  row=1, col=2)
    
    #fig.add_trace(go.Scatter(x=unified_19.groupby('Day').sum().index, y=unified_19.groupby('Day').sum()['Total conv. value'],
                   # mode='lines+markers',
                   # name='Revenue', marker_color = '#FEAF16'), row =1 , col = 2)
    
    #fig.update_layout(barmode = 'stack', height = 600, title_text = '2020 EOY Season')

    fig.update_yaxes(tickvals=[0, 50000, 100000], secondary_y=False, row = 1, col = 2)
    
    fig.update_yaxes(tickvals=[0, 2, 4, 6, 8], secondary_y=True, row =1, col =2)

    #print((uac_plot_19.groupby(['Day']).sum()['Total conv. value'].sum()/71))
    #print((uac_plot_19.groupby(['Day']).sum()['Conversions'].sum()/71))
    #print((plot_rev.groupby('Day').sum()['Total conv. value'].sum()/71))
    #print((uac_plot.groupby('Day').sum()['Conversions'].sum()/71))
    
    fig_camp_ = px.scatter(geo_camp_total, x='Day', y='Conversions').update_traces(mode='lines+markers')
    fig_camp_.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig_camp_.update_yaxes(matches=None, showticklabels=True, title_text='')
    fig_camp_.update_xaxes(matches='x')
    fig_camp_.update_layout(
        title_text="Daily Conversions", height = 950)
    figs_gads.append(fig_camp_)


    #cut = geo_camp_total[geo_camp_total['type'] == 'UAC'][['Day', 'Total conv. value', 'Year', 'Cost','locationName', 'Conversions']]
    #cut = geo_camp_total[['Day', 'Total conv. value', 'Year', 'Cost','locationName', 'Conversions']]

    #cut = cut.groupby(['Day','locationName','Year']).sum().reset_index()
    #cut['ROAS'] = cut['Total conv. value'] / cut['Cost']
    #cut['Day'] = pd.to_datetime(cut['Day'], format = '%b-%d')
    #cut['Day'] = cut['Day'].mask(cut['Day'].dt.year == 1900, 
     #                        cut['Day'] + pd.offsets.DateOffset(year=2020))
    #& (cut['Day'] <= (datetime.now() - timedelta(days= 4)))
    #cut = cut[(cut['Day'] > (datetime.now() - timedelta(days= 93)))]
    #cut.sort_values('Day', inplace = True)
    #cut['Day'] = cut['Day'].apply(lambda x: x.strftime('%b-%d'))
    
    #fig_case = make_subplots( rows=1, cols=1, specs=[[{'secondary_y':True}]])

    # Add traces

    
    
    #fig_case.add_trace(go.Bar(x=cut[cut['Year'] == '2019']['Day'], y=cut[cut['Year'] == '2019']['Cost'], name = 'Cost-19', marker_color = '#FC6955'), row=1, col=1)
    #fig_case.add_trace(go.Bar(x=cut[cut['Year'] == '2020']['Day'], y=cut[cut['Year'] == '2020']['Cost'],
     #               name='Cost-20', marker_color = '#F6222E'), row =1 , col = 1)
    #fig_case.add_trace(go.Scatter(x=cut[cut['Year'] == '2019']['Day'], y=cut[cut['Year'] == '2019']['ROAS'], name = 'ROAS-19', marker_color = '#FEAF16'), secondary_y = True, row=1, col=1)
    #fig_case.add_trace(go.Scatter(x=cut[cut['Year'] == '2020']['Day'], y=cut[cut['Year'] == '2020']['ROAS'], name = 'ROAS-20', marker_color = '#17BECF'), secondary_y = True, row=1, col=1)
    #fig_case.update_layout(title_text = 'Daily ROAS 2020 vs 2019')

    #idx = [ i for i in cut.index if cut.loc[i,'locationName'] in ['United States', 'Mexico', 'Italy','Australia']]
    #cut = cut.loc[idx,:]

    #fig_camp = px.scatter(cut, x='Day', y='Total conv. value', color='Year', facet_col= 'locationName', facet_col_wrap= 2, color_discrete_map={"2020": 'red', '2019':'orange'}).update_traces(mode='lines+markers')
    #fig_camp.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    #fig_camp.update_yaxes(matches=None,title_text='',showticklabels=False,range=[0, 20000], row = 1, col = 1)
    #fig_camp.update_yaxes(matches=None,range=[0, 6000], row = 2, col = 2)
    #fig_camp.update_yaxes(matches=None,range=[0, 6000], row = 1, col = 2)




    #fig_camp.update_xaxes(matches='x', nticks=13)
    #fig_camp.update_layout(
       # title_text="Daily Revenue UAC Campaigns (size = Conversions)", height = 1200)
    
    #fig_camp.update_layout(
       # title_text="Our Client 2020 Revenue in Primary Countries", height = 800)

    
    #fig_camp1 = px.scatter(geo_camp_total[geo_camp_total['type'] == 'Branded'], x='Day', y='Total conv. value', color='Year',
       #         facet_col='locationName', facet_col_wrap=2, size = 'Conversions').update_traces(mode='lines+markers')
    #fig_camp1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    #fig_camp1.update_yaxes(matches=None, showticklabels=True, title_text='')
    #fig_camp1.update_xaxes(matches='x')
    #fig_camp1.update_layout(
       # title_text="Daily Branded Campaigns Revenue per Country", height = 950)
    
    #fig_camp2 = px.scatter(geo_camp_total[geo_camp_total['type'] == 'Non-Branded'], x='Day', y='Total conv. value', color='Year',
          #      facet_col='locationName', facet_col_wrap=2, size = 'Conversions').update_traces(mode='lines+markers')
    #fig_camp2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    #fig_camp2.update_yaxes(matches=None, showticklabels=True, title_text='')
    #fig_camp2.update_xaxes(matches='x')
    #fig_camp2.update_layout(
        #title_text="Daily Non-Branded Campaigns Revenue per Country", height = 950)
    
   

    ### Table last 7 days Roas
    #df_geo['Day'] = pd.to_datetime(df_geo['Day'])
    #df_geo_last = df_geo[df_geo['Day'] >= (datetime.now() - timedelta(days= 5))]
    #df_geo_last['Total conv. value'] = df_geo_last['Total conv. value'].astype('float')
    #df_geo_last = df_geo_last.groupby('locationName').sum().reset_index()
    #df_geo_last['ROAS_last'] =  df_geo_last['Total conv. value'] / df_geo_last['Cost']
    #df_geo_merge = df_geo_last.loc[:, ['locationName', 'ROAS_last']]

    #df_geo_loc = df_geo.groupby('locationName').sum().reset_index()
    #df_geo_fig= pd.merge(df_geo_loc, df_geo_merge, how = 'left', on = 'locationName')
    #df_geo_fig['ROAS'] = df_geo_fig['Total conv. value'].astype('float') / df_geo_fig['Cost'].astype('float')
    #df_geo_fig['ARPU'] = df_geo_fig['Total conv. value'].astype('float') / df_geo_fig['Conversions'].astype('float')
    #df_geo_fig['+/- 5 days'] = df_geo_fig['ROAS'].astype('float') - df_geo_fig['ROAS_last']
    ##df_geo_fig['+/- 5 days'] = df_geo_fig['+/- 5 days'].apply(lambda x : '+' + str(np.round(x, 1)) if x > 0 else str(np.round(x, 1)))
    #df_geo_fig.sort_values('ROAS', ascending = False, inplace = True)

    #trace = go.Table(header=dict(values=['Country', 'Conversions', 'Cost', 'Revenue', 'ARPU', 'ROAS', '+/- 5 days (ROAS)']),
         #        cells=dict(values=[df_geo_fig.locationName.values, df_geo_fig.Conversions.values, np.round(df_geo_fig.Cost.values, 0), np.round(df_geo_fig['Total conv. value'].values, 0), np.round(df_geo_fig.ARPU.values, 1), np.round(df_geo_fig.ROAS.values, 1), df_geo_fig['+/- 5 days']]), domain=dict(x=[0.52, 1],y=[0, 1]))

    #trace1 = go.Pie(values=df_geo_fig.Conversions, labels=df_geo_fig.locationName, hole=.4, name = 'Conversions', domain=dict(x=[0, 0.23],y=[0, 1]), title_text = 'Conversions', textposition='inside', textinfo='label', hoverinfo="label+value")   
    #trace2 = go.Pie(values=df_geo_fig.Cost, labels=df_geo_fig.locationName, hole=.4, name = 'Cost', domain=dict(x=[0.26, 0.49],y=[0, 1]), title_text = 'Cost', textposition='inside', textinfo='label', hoverinfo="label+value")

    #fig_dough = go.Figure(data = [trace,trace1, trace2])
    #fig_dough.update_layout(title_text="Performance Breakdown by Country")

    #df_geo = geo_camp_fig.groupby(['Campaign','type','Year']).sum().reset_index()
    #df_geo['ROAS'] = df_geo['Total conv. value'] / df_geo['Cost']
    #df_geo['ARPU'] = df_geo['Total conv. value'] / df_geo['Conversions']
    #print(df_geo)

    
    
    #df_subs = df_subs.groupby(['Date', 'type']).sum().reset_index()
    
    #fig_bar = make_subplots( rows=1, cols=2, column_widths=[0.5, 0.5],
       #             subplot_titles=("Subscriptions UAC", "Subscriptions Search" ))

    #fig_bar.add_trace(go.Scatter(x=df_subs.groupby('Date').sum().index, y = df_subs[df_subs['type'] == 'UAC']['af_subscribe (Sales in CAD)'], mode='lines+markers', name = 'UAC'),1,1)
    #fig_bar.add_trace(go.Scatter(x=df_subs.groupby('Date').sum().index, y = df_subs[df_subs['type'] == 'Branded']['af_subscribe (Sales in CAD)'], mode='lines+markers', name = 'Branded'),1,2)
    #fig_bar.add_trace(go.Scatter(x=df_subs.groupby('Date').sum().index, y = df_subs[df_subs['type'] == 'Non-Branded']['af_subscribe (Sales in CAD)'], mode='lines+markers', name = 'Non-Branded'),1,2)


    #report = pd.DataFrame({'Date': report.Day, 'Network': report.type, 'Installs': report.Conversions , 'Cost': report.Cost, 'Revenue' : (report['Total conv. value'] + report['af_subscribe (Sales in CAD)'])})

    #report.to_csv('adwordssanta.csv')

    #fig_tab = go.Figure()
    #fig_tab.add_trace(go.Table(header=dict(values=['Day','convRate', 'UAC', 'NB', 'BRANDED']),
    #             cells=dict(values=[unified.Day.values, np.round(unified[unified['type'] == 'UAC']['Conversions'].values / unified[unified['type'] == 'UAC']['Clicks'].values, 2), 
    #             np.round(unified[unified['type'] == 'Non-Branded']['Conversions'].values / unified[unified['type'] == 'Non-Branded']['Clicks'].values, 2),
    #             np.round(unified[unified['type'] == 'Branded']['Conversions'].values / unified[unified['type'] == 'Branded']['Clicks'].values, 2)])))

    #New Script Budget
    day = 15
    budgets = pd.DataFrame()
    while day >= 1:
        end_date_ = (datetime.now() - timedelta(days= day))
        df_b = get_budget_report(client_id, client_secret, refresh_token, developer_token, client_customer_id, end_date_, end_date_)
        df_b['Day'] = (datetime.now() - timedelta(days= day)).strftime('%b-%d')
        budgets = pd.concat([budgets, df_b], axis = 0)
        day -= 1
    #print(budgets)
    budgets['Cost'] = budgets['Cost'].astype('float') /1000000
    budgets['Budget'] = budgets['Budget'].astype('float') /1000000
    budgets = budgets[(budgets['Budget state'] == 'Enabled') & (budgets['Cost'] > 0 )] 

    budgets = budgets.groupby(['Day', 'Budget Name']).sum().reset_index()
    budgets['ROAS'] = budgets['Total conv. value'] / budgets['Cost']
    df['Date'] = pd.to_datetime(df['Day'], format="%Y-%m-%d")
    df['Date'] = df['Date'].apply(lambda y : y.strftime('%b-%d'))
    budgets = pd.merge(budgets, df[['Date', 'Campaign', 'Conversions']], how = 'left', left_on= ['Day', 'Budget Name'], right_on= ['Date', 'Campaign'])
    print(budgets)
    budgets['CPI'] = budgets['Cost'] / budgets['Conversions']


    day = 15
    def fbudgets(days, df):
        values = pd.DataFrame()
        totals = pd.DataFrame()
        while days >= 1:
            print(days)
            temp = (df[df['Day'] == (datetime.now() - timedelta(days= 15 - days)).strftime('%b-%d')]['Cost'].values / df[df['Day'] == (datetime.now() - timedelta(days= 15 - days)).strftime('%b-%d')]['Budget']) * 100
            df_1 = pd.DataFrame(pd.concat([temp,df[df['Day'] == (datetime.now() - timedelta(days= 15 - days)).strftime('%b-%d')]['Budget Name'], df[df['Day'] == (datetime.now() - timedelta(days= 15 - days)).strftime('%b-%d')]['CPI']], axis = 1))
            df_2 = pd.DataFrame(pd.concat([df[df['Day'] == (datetime.now() - timedelta(days= 15 - days)).strftime('%b-%d')]['Budget'], df[df['Day'] == (datetime.now() - timedelta(days= 15 - days)).strftime('%b-%d')]['Budget Name']], axis = 1))
            if days == 15:
                values = pd.concat([values, df_1], axis = 0)
                #print(values)
                totals = pd.concat([totals, df_2], axis = 0)
            else:
                values = pd.merge(df_1, values, left_on = 'Budget Name', right_on = 'Budget Name', how = 'outer')
                totals = pd.merge(df_2, totals , left_on = 'Budget Name', right_on = 'Budget Name', how = 'outer')
            days -= 1
        print(values)
        return values, totals

    bvalues, btotals = fbudgets(day, budgets)
    print(bvalues.info())
    bvalues.columns = ['Budget', 'Name', 'CPI', 'Budget_yes','CPI_yes', 'Budget_2', 'CPI_2','Budget_3', 'CPI_3', 'Budget_4', 'CPI_4', 'Budget_5', 'CPI_5', 'Budget_6', 'CPI_6','Budget_7', 'CPI_7',
                        'Budget_8', 'CPI_8', 'Budget_9', 'CPI_9', 'Budget_10', 'CPI_10', 'Budget_11','CPI_11','Budget_12', 'CPI_12','Budget_13', 'CPI_13','Budget_14','CPI_14']
    bvalues.fillna(0, inplace = True)
    btotals.columns = ['Budget_T', 'Name', 'Budget_yes_T', 'Budget_2_T', 'Budget_3_T','Budget_4_T', 'Budget_5_T', 'Budget_6_T', 'Budget_7_T', 'Budget_8_T', 'Budget_9_T', 'Budget_10_T', 'Budget_11_T', 'Budget_12_T', 'Budget_13_T','Budget_14_T']
    btotals.fillna(0, inplace = True)

    
    def favg(df,limit1, limit2, name):
        avg = []
        for i in range(len(df)):
            suma = 0
            num = 0
            for j in range(limit1, limit2):
                if ('Budget' in df.columns[j]) and (float(df.iloc[i,j]) > 0):
                    suma += df.iloc[i,j]
                    num += 1
            if num > 0:
                value = suma / num
                avg.append(value)
            else:
                avg.append(0)
        df[name] = avg
        

    favg(bvalues, 0, 7, 'Average_current')
    favg(bvalues, 7, 15, 'Average_past')
    favg(btotals, 0, 7, 'Average_current_T')
    favg(btotals, 7, 15, 'Average_past_T')


    #print(total_avg)

    colors = n_colors('rgb(102, 166, 30)', 'rgb(230, 245, 201)', 9, colortype='rgb')
    bvalues = pd.merge(bvalues, btotals, how = 'left', on = 'Name')
    bvalues.sort_values('Budget', inplace = True, ascending = False)


    tab = go.Figure()
    tab.add_trace(go.Table(header=dict(values=['Budget Name','Today (%)', 'Total B.', 'CPI','Yestr (%)', 'Total B.', 'CPI','2 Days Ago (%)', 'Total B.','CPI',  'Avg week (%)', 'Total_B_Avg']),
                 cells=dict(values=[bvalues['Name'].values, np.round(bvalues['Budget'],1),  np.round(bvalues['Budget_T'], 1) , np.round(bvalues['CPI'],1), np.round(bvalues['Budget_yes'], 1) , np.round(bvalues['Budget_yes_T'], 1), np.round(bvalues['CPI_yes'],1), np.round(bvalues['Budget_2'], 1) , np.round(bvalues['Budget_2_T'], 1), np.round(bvalues['CPI_2'],1), np.round(bvalues['Average_current'],1), np.round(bvalues['Average_current_T'], 1) ],
                  fill=dict(color=['rgb(245, 245, 245)',#unique color for the first column
                                            ['rgba(166, 216, 84, 0.8)' if val < 2 else 'rgba(251, 180, 174, 0.8)' for val in np.round(bvalues['CPI'],1)] ]))))
    tab.update_layout(title_text = "Budget Stats Current Week (Green Rows below 2 Today's CPI)")
    figs_gads.append(tab)
    #tab_past = go.Figure()
    #tab_past.add_trace(go.Table(header=dict(values=['Budget Name', 'Day 14 (%)', 'Total','CPI', 'Day 13 (%)', 'Total','ROAS', 'Day 12 (%)', 'Total', 'ROAS', 'Day 11 (%)', 'Total', 'ROAS', 'Day 10 (%)', 'Total', 'ROAS', 'Day 9 (%)', 'Total','ROAS', 'Day 8 (%)', 'Total','ROAS', 'Avg week (%)', 'Total_Avg']),
     #           cells=dict(values=[bvalues['Name'].values, np.round(bvalues['Budget_14'],1),  np.round(bvalues['Budget_14_T'], 1) , np.round(bvalues['ROAS_14'], 1), np.round(bvalues['Budget_13'], 1) , np.round(bvalues['Budget_13_T'], 1) , np.round(bvalues['ROAS_13'], 1), np.round(bvalues['Budget_12'], 1), np.round(bvalues['Budget_12_T'], 1), np.round(bvalues['ROAS_12'], 1), np.round(bvalues['Budget_11'], 1) , np.round(bvalues['Budget_11_T'], 1), np.round(bvalues['ROAS_11'], 1), np.round(bvalues['Budget_10'], 1) , np.round(bvalues['Budget_10_T'], 1), np.round(bvalues['ROAS_10'], 1), np.round(bvalues['Budget_9'], 1) , np.round(bvalues['Budget_9_T'], 1), np.round(bvalues['ROAS_9'], 1), np.round(bvalues['Budget_8'], 1) , np.round(bvalues['Budget_8_T'], 1), np.round(bvalues['ROAS_8'], 1), np.round(bvalues['Average_past'],1), np.round(bvalues['Average_past_T'], 1) ])))
    #tab_past.update_layout(title_text = 'Budget Stats Last Week')

    channels['Cost'] = channels['Cost'] / 100000
    ad_bar = channels.groupby('Ad group').sum().reset_index()
    #ad_name = channels.groupby(["Description", "Day"]).sum().reset_index()

    #ad_line = channels.groupby(['Day','Final URL']).sum().reset_index()
    #urls = ad_name['Description'].unique()
    #print(ad_line)

    #make_subplots(rows = 1, cols =1, subplot_titles= ('Total Impressions/Clicks/Conversions per Ad Group') )
    fig_url = go.Figure()
    fig_url.add_trace(go.Bar(y = ad_bar['Ad group'], x = ad_bar['Impressions'], orientation='h', name = 'Impressions'))
    fig_url.add_trace(go.Bar(y = ad_bar['Ad group'], x = ad_bar['Clicks'], orientation='h', name = 'Clicks'))
    fig_url.add_trace(go.Bar(y = ad_bar['Ad group'], x = ad_bar['Conversions'], orientation='h', name = 'Conversions'))
    #for url in urls:
        #fig_url.add_trace(go.Scatter(x = ad_name[ad_name['Description'] == url]['Day'], y = ad_name[ad_name['Description'] == url]['Total conv. value'], name = url), 1,2)
    fig_url.update_layout(barmode = 'stack', height = 750, title_text = 'Total Impressions/Clicks/Conversions per Ad Group')
    #legend=dict(orientation="h",yanchor="bottom",y=-0.75,xanchor="right",x=1), legend_title_text='Action'
    
    #figs_gads.append(fig_url)
    #ad_tab = channels.groupby(['Ad group', 'Description']).sum().reset_index()
    ##ad_tab = ad_tab[ad_tab['Cost'] > 0]
    #ad_tab["ROAS"] = ad_tab["Total conv. value"] / ad_tab["Cost"]
    #ad_tab["CTR"] = ad_tab["Clicks"] / ad_tab["Impressions"]
    #ad_tab.sort_values('ROAS', ascending = False, inplace = True)

    

    #tab_ads = go.Figure()
    #tab_ads.add_trace(go.Table(header=dict(values=['Ad group', 'Ad', 'CTR', 'Cost', 'ROAS']),
    #             cells=dict(values=[ad_tab['Ad group'].values, ad_tab['Description'].values, np.round(ad_tab['CTR'].values,1), np.round(ad_tab['Cost'].values,1), np.round(ad_tab['ROAS'].values, 1)])))
    #tab_ads.update_layout(title_text = 'Ads Performance Table')
    #figs_gads.append(tab_ads)
    #path = 'C:\\Users\\User\\Documents\\Python Scripts'

    #prueba_json = fig.to_html(full_html=False, include_plotlyjs='cdn')
    #json_s3 = json.dumps(prueba_json)

    with open('Adwords_franki_daily.html', 'w') as f:
        for fig in figs_gads:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))


    
def get_geo_by_date_report(app_id, api_token, start_date, end_date):
    
    client = AppsFlyer(api_token=api_token, app_id=app_id)
    df = client.geo_by_date_report(start_date, end_date, as_df=True)
    
    return df

def get_age(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date, end_date):

    start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y%m%d')
    end_date = end_date.strftime('%Y%m%d')

    oauth2_client = oauth2.GoogleRefreshTokenClient( client_id=client_id, client_secret=client_secret, refresh_token=refresh_token)

    # Define output as a string buffer
    output = io.StringIO()

    # Initialize appropriate service.
    adwords_client = adwords.AdWordsClient(developer_token, oauth2_client)

    report_downloader = adwords_client.GetReportDownloader()
    #CampaignName, CampaignStatus, CityCriteriaId, Clicks,  ConversionRate, Cost, ConversionValue, CostPerConversion, Impressions, Ctr, LocationType
    # Create report query.
    report_query = (f'''
    SELECT Criteria, CampaignName, CampaignStatus, Conversions, Impressions, Clicks, ConversionValue, Cost
    FROM AGE_RANGE_PERFORMANCE_REPORT
    DURING {start_date},{end_date}
    ''')

    print(report_query)

    # Write query result to output file
    report_downloader.DownloadReportWithAwql(report_query, 'CSV', output, client_customer_id=client_customer_id, skip_report_header=True, skip_column_header=False, skip_report_summary=True)


    output.seek(0)
    df = pd.read_csv(output)
    return df
    

def get_geo_performance(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date, end_date):

    start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y%m%d')
    end_date = end_date.strftime('%Y%m%d')

    oauth2_client = oauth2.GoogleRefreshTokenClient(client_id=client_id, client_secret=client_secret, refresh_token=refresh_token)

    # Define output as a string buffer
    output = io.StringIO()

    # Initialize appropriate service.
    adwords_client = adwords.AdWordsClient(developer_token, oauth2_client)

    report_downloader = adwords_client.GetReportDownloader()
    #CampaignName, CampaignStatus, CityCriteriaId, Clicks,  ConversionRate, Cost, ConversionValue, CostPerConversion, Impressions, Ctr, LocationType
    # Create report query.
    report_query = (f'''
    SELECT Id, Date, CampaignName, CampaignStatus, Conversions, Impressions, Clicks, ConversionValue, Cost
    FROM CAMPAIGN_LOCATION_TARGET_REPORT
    DURING {start_date},{end_date}
    ''')

    print(report_query)

    # Write query result to output file
    report_downloader.DownloadReportWithAwql( report_query, 'CSV',output,client_customer_id=client_customer_id,skip_report_header=True, skip_column_header=False,skip_report_summary=True)


    output.seek(0)
    df = pd.read_csv(output)
    return df

def get_ad_performance(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date, end_date):

    start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y%m%d')
    end_date = end_date.strftime('%Y%m%d')

    oauth2_client = oauth2.GoogleRefreshTokenClient(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token
    )

    # Define output as a string buffer
    output = io.StringIO()

    # Initialize appropriate service.
    adwords_client = adwords.AdWordsClient(developer_token, oauth2_client)

    report_downloader = adwords_client.GetReportDownloader()
    #CampaignName, CampaignStatus, CityCriteriaId, Clicks,  ConversionRate, Cost, ConversionValue, CostPerConversion, Impressions, Ctr, LocationType
    # Create report query.
    report_query = (f'''
    SELECT Date, AdGroupName, Headline, Description, AdType, CampaignName, CampaignStatus, VideoViewRate, Conversions, Impressions, Clicks, ConversionValue, Cost, Status
    FROM AD_PERFORMANCE_REPORT
    DURING {start_date},{end_date}
    ''')

    print(report_query)

    # Write query result to output file
    report_downloader.DownloadReportWithAwql(
        report_query, 
        'CSV',
        output,
        client_customer_id=client_customer_id,
        skip_report_header=True, 
        skip_column_header=False,
        skip_report_summary=True
        )


    output.seek(0)
    df = pd.read_csv(output)
    return df


def get_budget_report(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date, end_date):

    
    end_date = end_date.strftime('%Y%m%d')

    oauth2_client = oauth2.GoogleRefreshTokenClient(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token
    )

    # Define output as a string buffer
    output = io.StringIO()

    # Initialize appropriate service.
    adwords_client = adwords.AdWordsClient(developer_token, oauth2_client)

    report_downloader = adwords_client.GetReportDownloader()

    # Create report query.
    report_query = (f'''
    SELECT Amount, BudgetId, BudgetName, BudgetReferenceCount, BudgetStatus, AssociatedCampaignName, ConversionValue, Cost
    FROM BUDGET_PERFORMANCE_REPORT
    DURING {end_date},{end_date}
    ''')

    print(report_query)

    # Write query result to output file
    report_downloader.DownloadReportWithAwql(
        report_query, 
        'CSV',
        output,
        client_customer_id=client_customer_id,
        skip_report_header=True, 
        skip_column_header=False,
        skip_report_summary=True, 
        include_zero_impressions=True,
        )


    output.seek(0)
    df = pd.read_csv(output)
    return df

def get_campaign_performance_report(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date, end_date):

    start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y%m%d')
    end_date = end_date.strftime('%Y%m%d')

    oauth2_client = oauth2.GoogleRefreshTokenClient(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token
    )

    # Define output as a string buffer
    output = io.StringIO()

    # Initialize appropriate service.
    adwords_client = adwords.AdWordsClient(developer_token, oauth2_client)

    report_downloader = adwords_client.GetReportDownloader()

    # Create report query.
    report_query = (f'''
    SELECT CampaignName, Date, ServingStatus, Clicks, Impressions, Cost, Conversions, ConversionValue, BudgetId, AdvertisingChannelType, AdvertisingChannelSubType
    FROM CAMPAIGN_PERFORMANCE_REPORT
    DURING {start_date},{end_date}
    ''')

    print(report_query)

    # Write query result to output file
    report_downloader.DownloadReportWithAwql(
        report_query, 
        'CSV',
        output,
        client_customer_id=client_customer_id,
        skip_report_header=True, 
        skip_column_header=False,
        skip_report_summary=True, 
        include_zero_impressions=True,
        )


    output.seek(0)
    df = pd.read_csv(output)
    return df

def drive_g(df, sheet_name):
    spreadsheet_key = '1tsnBq1_ZW4o5MHbte_FuT6NYHbHdwzX4ScxjH9asKU4'
    spread = Spread(spreadsheet_key) 
    cell = spread.get_sheet_dims(sheet_name)
    startc = 'A' + str(cell[0] + 1)
    spread.df_to_sheet(df, index=False, sheet=sheet_name, start=startc, headers = False)

def get_installs_report(app_id, api_token, start_date, end_date):

    client = AppsFlyer(api_token=api_token, app_id=app_id)
    df = client.installs_report(start_date, end_date, as_df=True)
    
    return df


def get_location(client_id, client_secret, refresh_token, developer_token, client_customer_id, locations):
  
    oauth2_client = oauth2.GoogleRefreshTokenClient(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token
    )

    
    client = adwords.AdWordsClient(developer_token, oauth2_client)

    location_criterion_service = client.GetService('LocationCriterionService', version='v201809')

 
    selector = {
      'fields': ['Id', 'LocationName', 'DisplayType', 'CanonicalName',
                 'ParentLocations', 'Reach', 'TargetingStatus'],
      'predicates': [{
          'field': 'Id',
          'operator': 'IN',
          'values': locations
      }
      ]
    }

  
    location_criteria = location_criterion_service.get(selector)
    return location_criteria

def get_placement(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date, end_date):

    start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y%m%d')
    end_date = end_date.strftime('%Y%m%d')

    oauth2_client = oauth2.GoogleRefreshTokenClient(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token
    )

    # Define output as a string buffer
    output = io.StringIO()

    # Initialize appropriate service.
    adwords_client = adwords.AdWordsClient(developer_token, oauth2_client)

    report_downloader = adwords_client.GetReportDownloader()
    #CampaignName, CampaignStatus, CityCriteriaId, Clicks,  ConversionRate, Cost, ConversionValue, CostPerConversion, Impressions, Ctr, LocationType
    # Create report query.
    report_query = (f'''
    SELECT Id, Date, CampaignName, CampaignStatus, Conversions, Impressions, Clicks, ConversionValue, Cost, AdNetworkType1
    FROM PLACEMENT_PERFORMANCE_REPORT
    DURING {start_date},{end_date}
    ''')

    print(report_query)

    # Write query result to output file
    report_downloader.DownloadReportWithAwql(
        report_query, 
        'CSV',
        output,
        client_customer_id=client_customer_id,
        skip_report_header=True, 
        skip_column_header=False,
        skip_report_summary=True
        )


    output.seek(0)
    df = pd.read_csv(output)
    return df

def get_placement_yt(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date, end_date):

    start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y%m%d')
    end_date = end_date.strftime('%Y%m%d')

    oauth2_client = oauth2.GoogleRefreshTokenClient(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token
    )

    # Define output as a string buffer
    output = io.StringIO()

    # Initialize appropriate service.
    adwords_client = adwords.AdWordsClient(developer_token, oauth2_client)

    report_downloader = adwords_client.GetReportDownloader()
    #CampaignName, CampaignStatus, CityCriteriaId, Clicks,  ConversionRate, Cost, ConversionValue, CostPerConversion, Impressions, Ctr, LocationType
    # Create report query.
    report_query = (f'''
    SELECT Id, Date, CampaignName, CampaignStatus, Conversions, Impressions, Clicks, ConversionValue, Cost, AdNetworkType1
    FROM PLACEMENT_PERFORMANCE_REPORT
    WHERE AdNetworkType1 IN [YOUTUBE_SEARCH, YOUTUBE_WATCH]
    DURING {start_date},{end_date}
    ''')

    print(report_query)

    # Write query result to output file
    report_downloader.DownloadReportWithAwql(
        report_query, 
        'CSV',
        output,
        client_customer_id=client_customer_id,
        skip_report_header=True, 
        skip_column_header=False,
        skip_report_summary=True
        )


    output.seek(0)
    df = pd.read_csv(output)
    return df

if __name__ == "__main__":
    main()
