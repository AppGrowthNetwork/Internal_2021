import requests   
from pandas.io.json import json_normalize 
import pandas as pd  
from os.path import join
import os
import numpy as np
#import gspread
#from gspread_pandas import Spread, Client
import datetime
from appsflyer import AppsFlyer

from plotly.offline import plot
import plotly.express as px
from plotly.graph_objs import *
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots


access_token = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwia2lkIjpudWxsfQ..mJftZSX3b7czdpzZ.alzUOEivVQkJUhuLQO4J6vIadUTZ9R8PGBblb7erDgwcL7ZTeXMAtf0b6q1nBMrqh8J-JCoFg0i3LAokCeAGqrhxRlxJ6p64QdzPq61Xl_DI9wFynSJcr_k85dCelZsDRvEk70CVKo7DPqdo1n4-cs82N5zkJsYYeNNtpSisoj-m4HoRbFyEglVRBy4w6IKMUOz9L4afPAGxKZPPOE-cYb28ITK7YlqDvjGQOCzxitCVy9mG5WWyP2MEXVS1r0ArEIK_G3Tb_EThOL6L9XSgqLk.c7IJOpflBuWjO_AFxcHeqA"
##gc = gspread.service_account(filename = "C://Users//User//AppData//Local//Programs//Python//Python38//Lib//site-packages//gspread//service_account.json")

#path = 'C:\\Users\\User\\Downloads\\Santa_Admin_ASA_Cert\\'
ORG_ID = "1723370" # Your ORG_ID, you can find in Apple Search ads, cabinet in the top right menu
#APPLE_CERT = (join(path, 'AGN1.pem'), join(path, 'AGN1.key'))

START_DATE = "2021-09-20"
END_DATE = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")
#revenue and by campaign nb and b


def main(START_CURRENT, END_CURRENT, START, END):

    app_id = "id902026228"
    api_token = "94c1018e-ab1a-4eb2-95b4-b46dc0c5de89"

    #df_af = get_geo_by_date_report(app_id, api_token, START_DATE, END_DATE)
    #print(df_af.sort_values('af_purchase (Sales in CAD)', ascending = False))
    #df_af.to_csv('AF_santa_geo_asa_22.csv')
    #print(df_af.columns)
    #df_af = df_af[df_af['Media Source (pid)'] == 'Apple Search Ads'].reset_index(drop = True)
    #print(df_af)
    
    # We call our main delivery-boy function to do all the work
    df = download_campaigns_report()

    # We rename some columns names to make them more beautiful
    new_columns = {x: x.replace("metadata.","") for x in df.columns}
    df = df.rename(columns=new_columns)

    # We fill empty rows with zeros
    df = df.fillna(0)

    #if len(df.columns) == 0:
        #df = pd.DataFrame(columns = columns_, index = range(0,1))
        #df.iloc[0] = [0] * 18

    print(df)
    custom = pd.DataFrame()
    for i in range(0,len(df)):
        temp = pd.DataFrame()
        for j in range(0,len(df['granularity'][i])):
            data = df['granularity'][i][j]
            data['campaignId'] = df.loc[i,'campaignId']
            data['campaignName'] = df.loc[i,'campaignName']
            data['Country'] = df.loc[i,'countryOrRegion' ]
            if 'avgCPA' in df['granularity'][i][j].keys():
                data['avgCPA'] = df['granularity'][i][j]['avgCPA']['amount']
                data['avgCPT'] = df['granularity'][i][j]['avgCPT']['amount']
                data['localSpend'] = df['granularity'][i][j]['localSpend']['amount']
            concat = pd.DataFrame(data, index = range(0,1))
            temp= pd.concat([temp, concat], axis = 0)
        custom = pd.concat([custom, temp], axis = 0)
    custom.reset_index(drop = True, inplace= True)
    custom = custom.fillna(0)
    custom['localSpend'] = custom['localSpend'].astype('float')
    print(custom.columns)
    custom.to_csv('custom')
    print(custom['campaignName'].unique())

    #Pick nb campaigns
    index_generic = [i for i in custom.index if 'Generic' in custom.loc[i,'campaignName']]
    generic_campaigns = custom.iloc[index_generic,:]
    generic_campaigns['type'] = 'Generic'

    index_discovery = [i for i in custom.index if 'Discovery' in custom.loc[i,'campaignName']]
    discovery_campaigns = custom.iloc[index_discovery,:]
    discovery_campaigns['type'] = 'Discovery'

    #index_nb = [i for i in df_af.index if ('GENERIC' in df_af.loc[i,'Campaign (c)'] or 'DISCOVERY' in df_af.loc[i,'Campaign (c)'] or 'COMPETITOR' in df_af.loc[i,'Campaign (c)']) and df_af.loc[i, 'Date'] == END_DATE]
    #nb_campaigns_af = df_af.iloc[index_nb,:]
    
    #Pick branded campaigns
    index_branded = [i for i in custom.index if 'Brand' in custom.loc[i,'campaignName']]
    branded_campaigns = custom.iloc[index_branded, :]
    branded_campaigns['type'] = 'Branded'

    index_competitor = [i for i in custom.index if 'Competitor' in custom.loc[i,'campaignName']]
    competitor_campaigns = custom.iloc[index_competitor,:]
    competitor_campaigns['type'] = 'Competitor'

    #index_branded = [i for i in df_af.index if 'BRAND' in df_af.loc[i,'Campaign (c)'] and df_af.loc[i, 'Date'] == END_DATE]
    #branded_campaigns_af = df_af.iloc[index_branded, :]


    #if 'installs' in nb_campaigns.columns:
    #    nb_totals = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Non- Branded)', 'Installs': nb_campaigns['installs'].sum() , 'Cost': nb_campaigns['localSpend'].sum()}, index = range(0,1))
        #nb_totals_af = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Non- Branded)', 'Installs': nb_campaigns_af['Installs'].sum() , 'Cost': nb_campaigns_af['Total Cost'].sum(), 'Revenue': nb_campaigns_af['Total Revenue'].sum()}, index = range(0,1))
    #else:
    #    nb_totals = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Non- Branded)', 'Installs': 0, 'Cost': 0}, index = range(0,1))
        #nb_totals_af = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Non- Branded)', 'Installs': 0, 'Cost': 0}, index = range(0,1))


    #if 'installs' in branded_campaigns.columns:
    #    branded_totals = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Branded)', 'Installs': branded_campaigns['installs'].sum() , 'Cost': branded_campaigns['localSpend'].sum()}, index = range(0,1))
        #branded_totals_af = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Branded)', 'Installs': branded_campaigns_af['Installs'].sum() , 'Cost': branded_campaigns_af['Total Cost'].sum(), 'Revenue': branded_campaigns_af['Total Revenue'].sum()}, index = range(0,1))
    #else:
    #    branded_totals = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Branded)', 'Installs': 0, 'Cost': 0}, index = range(0,1))
        #branded_totals_af = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Branded)', 'Installs': 0, 'Cost': 0}, index = range(0,1))


    upload = pd.concat([branded_campaigns, discovery_campaigns, generic_campaigns, competitor_campaigns], axis =0)
    #upload_af = pd.concat([branded_totals_af, nb_totals_af], axis =0)
    #upload_af['ARPU'] = upload_af['Revenue'] / upload_af['Installs']
    #print(upload_af)
    #upload['Revenue'] = upload_af['ARPU'] * upload['Installs']
    #upload['ROAS'] = upload['Revenue'] / upload['Cost']
    print(upload)
    #print(upload_af)
    #sheet_name = 'Daily_overview'
    #drive_g(upload, sheet_name)  

    keywords = pd.DataFrame()

    campaigns = dict(zip(custom.campaignId.unique(), custom.campaignName.unique()))

    for campaign in custom.campaignId.unique():
        df_key = download_keywords_report(campaign)
        df_key['campaignId'] = campaign
        df_key['campaignName'] = campaigns[campaign]
        keywords = pd.concat([keywords, df_key], axis = 0)
    
    keywords.reset_index(inplace = True)
    custom_key = pd.DataFrame()

    for i in range(0,len(keywords)):
        temp = pd.DataFrame()
        for j in range(0,len(keywords['granularity'][i])):
            data = keywords['granularity'][i][j]
            data['campaignId'] = keywords.loc[i,'campaignId']
            data['keyword'] = keywords.loc[i, 'metadata.keyword']
            data['keywordStatus'] = keywords.loc[i, 'metadata.keywordStatus']
            data['campaignName'] = keywords.loc[i,'campaignName']
            data['Country'] = keywords.loc[i,'metadata.countryOrRegion']
            data['Adgroup'] = keywords.loc[i, 'metadata.adGroupName']
            if 'avgCPA' in keywords['granularity'][i][j].keys():
                data['avgCPA'] = keywords['granularity'][i][j]['avgCPA']['amount']
                data['avgCPT'] = keywords['granularity'][i][j]['avgCPT']['amount']
                data['localSpend'] = keywords['granularity'][i][j]['localSpend']['amount']
            concat = pd.DataFrame(data, index =  range(0, len(keywords['granularity'][i][j])))
            temp= pd.concat([temp, concat], axis =0 )
        custom_key = pd.concat([custom_key, temp], axis = 0)
    custom_key.reset_index(drop = True, inplace= True)
    custom_key.drop_duplicates(inplace = True)
    custom_key.reset_index(inplace = True, drop = True)
    print(custom_key)
    print(custom_key.columns)

    custom_key['avgCPA'] = custom_key['avgCPA'].astype('float')
    custom_key['avgCPT'] = custom_key['avgCPT'].astype('float')
    custom_key['localSpend'] = custom_key['localSpend'].astype('float')

    custom['avgCPA'] = custom['avgCPA'].astype('float')
    custom['avgCPT'] = custom['avgCPT'].astype('float')
    custom['localSpend'] = custom['localSpend'].astype('float')


    figs_asa = []
    fig = make_subplots( rows=2, cols=2, column_widths=[0.5, 0.5], row_heights=[0.4, 0.6], specs=[[{"secondary_y": True}, {}],[ { "colspan": 2, "secondary_y": True}   , None]],
                subplot_titles=("ASA Installs vs. CPI (per day)", "New vs. Redownloads (per day)", "Downloads per country" ))

    # Add traces
    
    fig.add_trace(go.Scatter(x=custom.date, y=custom.groupby('date').sum()['installs'],
                    mode='lines+markers',
                    name='Installs'), row=1, col=1)
    fig.add_trace(go.Scatter(x=custom.date, y=custom.groupby('date').sum()['localSpend'],
                    mode='lines+markers',
                    name='Spend'), row=1, col=1)
    fig.add_trace(go.Scatter(x=custom.date, y=custom.groupby('date').sum()['newDownloads'],
                   mode='lines+markers',
                    name='newDownloads', marker_color = 'orange'), row=1, col=2)

    fig.add_trace(go.Scatter(x=custom.date, y=custom.groupby('date').sum()['localSpend']/custom.groupby('date').sum()['installs'],
                    mode='lines+markers',
                    name='avgCPI', yaxis='y2'), secondary_y=True, row=1, col=1)

    fig.add_trace(go.Scatter(x=custom.date, y=custom.groupby('date').sum()['redownloads'],
                    mode='lines+markers',
                    name='reDownloads', marker_color = '#2CA02C'), row=1, col=2)

    fig.add_trace(go.Bar(x=custom.groupby('Country').sum().index, y = custom.groupby('Country').sum()["newDownloads"], 
                    name = 'newDownloads', marker_color = 'orange'), row= 2, col = 1)

    fig.add_trace(go.Bar(x=custom.groupby('Country').sum().index, y = custom.groupby('Country').sum()["redownloads"], 
                    name='reDownloads', marker_color = '#2CA02C'), row= 2, col = 1)

    figs_asa.append(fig)

    camp = custom.groupby(['date', 'campaignName']).sum().reset_index()

    fig = make_subplots( rows=3, cols=2, column_widths=[0.5, 0.5], row_heights=[0.3, .2, 0.5], specs=[[{ "colspan": 2, "secondary_y": True}, None], [{ "colspan": 2, "secondary_y": True}, None], [ { "colspan": 2, "secondary_y": True}   , None]],
                subplot_titles=("ASA KPIs overall", "CPA vs CPT", "ASA CPA per campaign" ))

    # Add traces
    
    fig.add_trace(go.Scatter(x=custom.date, y=custom.groupby('date').sum()['localSpend'],
                    mode='lines+markers',
                    name='Spend', yaxis='y2'), secondary_y=True, row=1, col=1)
    fig.add_trace(go.Scatter(x=custom.date, y=custom.groupby('date').sum()['ttr'],
                    mode='lines+markers',
                    name='TTR', yaxis='y2'), secondary_y=True, row=2, col=1)
    for i in custom.groupby('campaignName').sum().reset_index()['campaignName'].unique():
        fig.add_trace(go.Scatter(x=custom.date, y=camp[camp['campaignName'] == i]['avgCPA'],
                   mode='lines+markers', name=i + ' avgCPA'), row=3, col=1)

    #fig.add_trace(go.Scatter(x=custom.date, y=custom.groupby('date').sum()['localSpend']/custom.groupby('date').sum()['installs'],
    #                mode='lines+markers',
    #                name='avgCPI', yaxis='y2', marker_color = 'orange'), secondary_y=True, row=1, col=1)
    fig.add_trace(go.Scatter(x=custom.date, y=custom.groupby('date').sum()['localSpend']/custom.groupby('date').sum()['installs'],
                    mode='lines+markers',
                    name='avgCPI',  showlegend = False, marker_color = 'orange'), row=2, col=1)

    fig.add_trace(go.Bar(x=custom.groupby('date').sum().index, y = custom.groupby('date').sum()["impressions"], name='Impressions',
                    marker_color = 'grey'), row= 1, col = 1)

    fig.add_trace(go.Bar(x=custom.groupby('date').sum().index, y = custom.groupby('date').sum()["taps"], name='taps',
                     marker_color = '#2CA02C'), row= 1, col = 1)

    fig.add_trace(go.Bar(x=custom.groupby('date').sum().index, y = custom.groupby('date').sum()["installs"], name='installs',
                     marker_color = 'brown'), row= 1, col = 1)
    fig.update_layout(barmode = 'stack')

    figs_asa.append(fig)
    #fig_installs= make_subplots(rows=1, cols=2, subplot_titles=['New vs ReDownloads', "New vs ReDownloads per Country"])

   
    '''
    fig_installs.add_trace(go.Scatter(x=custom.date, y=custom.groupby(['date','Country']).sum()['newDownloads'].loc[slice(None),'GB'], 
                    name='GB-new', marker_color = '#19D3F3', mode='lines'), 1,2)
    
    fig_installs.add_trace(go.Scatter(x=custom.date, y=custom.groupby(['date','Country']).sum()['newDownloads'].loc[slice(None),'FR'], 
                    name='FR-new', mode='lines'), 1,2)
    
    fig_installs.add_trace(go.Scatter(x=custom.date, y=custom.groupby(['date','Country']).sum()['newDownloads'].loc[slice(None),'US'], 
                    name='US-new', marker_color = '#6A76FC', mode='lines'), 1,2)

    fig_installs.add_trace(go.Scatter(x=custom.date, y=custom.groupby(['date','Country']).sum()['redownloads'].loc[slice(None),'GB'], 
                    name='GB-re', marker_color = '#FF9900', mode='lines'), 1,2)

    fig_installs.add_trace(go.Scatter(x=custom.date, y=custom.groupby(['date','Country']).sum()['redownloads'].loc[slice(None),'FR'], 
                    name='FR-re', mode='lines'), 1,2)

    fig_installs.add_trace(go.Scatter(x=custom.date, y=custom.groupby(['date','Country']).sum()['redownloads'].loc[slice(None),'US'], 
                    name='US-re', mode='lines'), 1,2)
    '''

    bar_key = custom_key.groupby(['keyword', 'Country']).sum()
    bar_key.reset_index(inplace = True)

    def competitor_filter(string):
        if 'Competitor' in string:
            x = 'Competitor'
        elif 'Brand' in string:
            x = 'Brand'
        elif 'Generic' in string:
            x = 'Generic'
        elif 'Discovery' in string:
            x = 'Discovery'  
        return x

    custom_key['type']  = custom_key['campaignName'].apply(lambda x : competitor_filter(x)) 
    bar_comp = custom_key.groupby(['type']).sum()
    bar_comp.reset_index(inplace = True)
    bar_comp['conversionRate'] = bar_comp['installs'] / bar_comp['taps']
    

    '''
    fig_cum = go.Figure()

    fig_cum.add_trace(go.Scatter(x=custom.date, y=custom.groupby('date').sum()['newDownloads'].cumsum(),
                    mode='lines+markers',
                    name='newDownloads', marker_color = '#511CFB'))
    fig_cum.add_trace(go.Scatter(x=custom.date, y=custom.groupby('date').sum()['installs'].cumsum(),
                    mode='lines+markers',
                    name='Installs', marker_color = '#EECA3B'))
    fig_cum.add_trace(go.Scatter(x=custom.date, y=custom.groupby('date').sum()['localSpend'].cumsum(),
                    mode='lines+markers',
                    name='Cost', marker_color = '#EF553B'))
    fig_cum.update_layout(
        title_text="Cumulative KPI's for ASA")
        
    figs_asa.append(fig_cum)
    '''

    df_camp = camp.groupby('campaignName').sum().reset_index()
    df_camp['CTR'] = df_camp['taps'] / df_camp['impressions']
    df_camp['Conv.Rate'] = df_camp['installs'] / df_camp['taps']
    df_camp.sort_values('Conv.Rate', ascending = False, inplace = True)
    print(df_camp.head())

    trace0 = go.Pie(values=df_camp.impressions, labels=df_camp.campaignName, hole=.4, name = 'Impressions', domain=dict(x=[0, 0.24],y=[0, 1]), title_text = 'Impressions', textposition='inside', textinfo='percent', hoverinfo="label+value")
    trace1 = go.Pie(values=df_camp.taps, labels=df_camp.campaignName, hole=.4, name = 'Clicks', domain=dict(x=[0.25, 0.49],y=[0, 1]), title_text = 'Clicks', textposition='inside', textinfo='percent', hoverinfo="label+value")
    trace2 = go.Pie(values=df_camp.installs, labels=df_camp.campaignName, hole=.4, name = 'Installs', domain=dict(x=[0.50, 0.74],y=[0, 1]), title_text = 'Installs', textposition='inside', textinfo='percent', hoverinfo="label+value")
    trace3 = go.Pie(values=df_camp.localSpend, labels=df_camp.campaignName, hole=.4, name = 'Cost', domain=dict(x=[0.75, .99],y=[0, 1]), title_text = 'Cost', textposition='inside', textinfo='percent', hoverinfo="label+value")
    
   
    
    fig_dough = go.Figure(data = [trace0,trace1, trace2,trace3])
    fig_dough.update_layout(title_text="ASA Breakdown by Campaign")
    fig_dough.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.96,
        xanchor="right",
        x=1), height = 600)

    figs_asa.append(fig_dough)

    ###ALL
    fig_key = px.bar(custom_key.groupby(['keyword', 'type']).sum().reset_index(), x="keyword", y = "installs", color="localSpend", facet_col="type", facet_col_wrap=1, 
           hover_data=["newDownloads", "redownloads"],  hover_name='keyword', title = 'Keywords performance by Label (All time)')
    fig_key.update_xaxes(matches='x')

    figs_asa.append(fig_key)

    tab = bar_key.sort_values('installs', ascending = False).head(20)
    
    #fig_key_sub = make_subplots(rows=1, cols=2,
    #        subplot_titles=['Installs (per Label)', 'ConversionRate (per label)'])
    
    #fig_key_sub.add_trace(go.Bar(x=bar_comp['type'], y = bar_comp["installs"], marker_color='rgb(55, 83, 109)', showlegend=False), 1,1)
    #fig_key_sub.add_trace(go.Bar(x=bar_comp['type'], y = bar_comp["conversionRate"], marker_color='rgb(26, 118, 255)', showlegend=False), 1,2)
    #fig_key_sub.update_layout(barmode='group', xaxis_tickangle=-45)
    
    #figs_asa.append(fig_key_sub)

    ##CURRENT
    custom_slice = custom_key.copy()

    custom_slice['date'] = pd.to_datetime(custom_slice['date'], format = "%Y-%m-%d")
    START_DATE = pd.to_datetime(START_CURRENT, format = '%Y-%m-%d')
    END_DATE = pd.to_datetime(END_CURRENT, format = '%Y-%m-%d')
    custom_key_current = [ i for i in custom_slice.index if custom_slice.loc[i,'date'] >= START_DATE and custom_slice.loc[i, 'date'] <= END_DATE]
    custom_key_current = custom_slice.loc[custom_key_current, :]
    fig_key = px.bar(custom_key_current.groupby(['keyword', 'type']).sum().reset_index(), x="keyword", y = "installs", color="localSpend", facet_col="type", facet_col_wrap=1, 
           hover_data=["newDownloads", "redownloads"], title = 'Keywords performance by Label (last 15 days)')
    figs_asa.append(fig_key)
    
    bar_slice = custom_key.groupby(['keyword', 'Country', 'date']).sum().reset_index()
    bar_slice['date'] = pd.to_datetime(bar_slice['date'], format = "%Y-%m-%d")
    bar_current = [i for i in bar_slice.index if bar_slice.loc[i,'date'] >= START_DATE and bar_slice.loc[i, 'date'] <= END_DATE]
    bar_current = bar_slice.loc[bar_current, :]
    bar = bar_current.sort_values('installs', ascending = False).head(20)
    #figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Keyword','installs', 'Country']),
    #             cells=dict(values=[bar.keyword.values, bar.installs.values, bar.Country.values]))
    #                 ])
    #figs_asa.append(figkey_tab)
    #fig_key_sub = make_subplots(rows=1, cols=2,
     #       subplot_titles=['Installs per Label (last 15 days)', 'ConversionRate per label (last 15 days)'])
    
    #fig_key_sub.add_trace(go.Bar(x=bar_comp['type'], y = bar_comp["installs"], marker_color='rgb(55, 83, 109)', showlegend=False), 1,1)
    #fig_key_sub.add_trace(go.Bar(x=bar_comp['type'], y = bar_comp["conversionRate"], marker_color='rgb(26, 118, 255)', showlegend=False), 1,2)
    #fig_key_sub.update_layout(barmode='group', xaxis_tickangle=-45)
    
    #figs_asa.append(fig_key_sub)

    ##PAST
    START = pd.to_datetime(START, format = '%Y-%m-%d')
    END = pd.to_datetime(END, format = '%Y-%m-%d')
    custom_key_past = [ i for i in custom_slice.index if custom_slice.loc[i,'date'] >= START and custom_slice.loc[i, 'date'] <= END]
    custom_key_past = custom_slice.loc[custom_key_past, :]
    fig_key = px.bar(custom_key_past.groupby(['keyword', 'type']).sum().reset_index(), x="keyword", y = "installs", color="localSpend", facet_col="type", facet_col_wrap=1, 
           hover_data=["newDownloads", "redownloads"], title = 'Keywords performance by Label (last report)')
    figs_asa.append(fig_key)

    bar_past = [i for i in bar_slice.index if bar_slice.loc[i,'date'] >= START and bar_slice.loc[i, 'date'] <= END]
    bar_past = bar_slice.loc[bar_past, :]

    PREV_END = END - datetime.timedelta(days = 1)
    START_END = END - datetime.timedelta(days = 2)
    bar_last = [i for i in bar_slice.index if bar_slice.loc[i, 'date'] == END]
    bar_last = bar_slice.loc[bar_last, :][['keyword','avgCPA']]
    bar_last.columns = ['keyword', 'CPA']
    bar_2last = [i for i in bar_slice.index if bar_slice.loc[i, 'date'] == PREV_END]
    bar_2last = bar_slice.loc[bar_2last, :][['keyword','avgCPA']]
    bar_2last.columns = ['keyword', 'CPA']
    bar_days = pd.merge(bar_last, bar_2last, how = 'left', on = 'keyword')
    bar_startlast = [i for i in bar_slice.index if bar_slice.loc[i, 'date'] == START_END]
    bar_startlast = bar_slice.loc[bar_startlast, :][['keyword','avgCPA']]
    bar_startlast.columns = ['keyword', 'CPA']
    bar_days = pd.merge(bar_days, bar_startlast, how = 'left', on = 'keyword')
    

    bar = bar_past.sort_values('installs', ascending = False).head(20)
    #figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Keyword','installs', 'Country']),
      #           cells=dict(values=[bar.keyword.values, bar.installs.values, bar.Country.values]))
       #              ])
    #figs_asa.append(figkey_tab)
    #fig_key_sub = make_subplots(rows=1, cols=2,
          #  subplot_titles=['Installs per Label (last report)', 'ConversionRate per label (last report)'])
    
    #fig_key_sub.add_trace(go.Bar(x=bar_comp['type'], y = bar_comp["installs"], marker_color='rgb(55, 83, 109)', showlegend=False), 1,1)
    #fig_key_sub.add_trace(go.Bar(x=bar_comp['type'], y = bar_comp["conversionRate"], marker_color='rgb(26, 118, 255)', showlegend=False), 1,2)
    #fig_key_sub.update_layout(barmode='group', xaxis_tickangle=-45)
    
    #figs_asa.append(fig_key_sub)

    tab_plot = pd.merge(tab.groupby(['keyword']).sum().reset_index()[['keyword','installs','localSpend', 'avgCPA']], bar_current.groupby(['keyword']).sum().reset_index()[['keyword','installs','localSpend', 'avgCPA']], on= 'keyword', how = 'left')
    tab_plot = pd.merge(tab_plot, bar_past.groupby(['keyword']).sum().reset_index()[['keyword','installs','localSpend', 'avgCPA']], on= 'keyword', how = 'left')
    tab_plot.sort_values('installs_x', ascending= False, inplace= True)

    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Keyword', 'Total installs', 'Previous report', 'Last 15 days', '% change']),
                 cells=dict(values=[tab_plot.keyword.values, tab_plot.installs_x.values, tab_plot.installs.values, tab_plot.installs_y.values, np.round(((tab_plot.installs_y.values - tab_plot.installs.values)/tab_plot.installs.values)*100, 1)]))
                     ])
    figs_asa.append(figkey_tab)
    tab_plot.set_index('keyword', inplace = True)
    print(tab_plot)

    tab_tab = pd.merge(tab_plot.groupby(['keyword']).mean().reset_index()[['keyword','installs','localSpend', 'avgCPA']], bar_current.groupby(['keyword']).mean().reset_index()[['keyword','installs','localSpend', 'avgCPA']], on= 'keyword', how = 'left')
    tab_tab = pd.merge(tab_tab, bar_past.groupby(['keyword']).mean().reset_index()[['keyword','installs','localSpend', 'avgCPA']], on= 'keyword', how = 'left')
    tab_tab = pd.merge(tab_tab, bar_days.groupby(['keyword']).mean().reset_index(), on = 'keyword', how = 'left' )
    tab_tab.set_index('keyword', inplace = True)
    tab_tab = tab_tab.reindex(tab_plot.index)
    tab_tab.reset_index(drop = False, inplace = True)
    tab_tab.fillna(0, inplace = True)
    print(tab_tab)
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Keyword', '$ Avg localSpend', '$ Avg CPA', ' $ Previous report', '$ Last 15 days', '% change 15', '% change 2 days ago', '% change 1 day ago' ]),
                 cells=dict(values=[tab_tab.keyword.values, np.round(tab_tab.localSpend_x.values, 1), np.round(tab_tab.avgCPA_x.values, 1), np.round(tab_tab.avgCPA.values, 1), np.round(tab_tab.avgCPA_y.values, 1), np.round(((tab_tab.avgCPA_y.values - tab_tab.avgCPA.values)/tab_tab.avgCPA.values)*100, 1), np.round(((tab_tab.CPA_x.values - tab_tab.CPA_y.values)/tab_tab.CPA_y.values)*100, 1), np.round(((tab_tab.CPA_x.values - tab_tab.CPA.values)/tab_tab.CPA.values)*100, 1)]))
                     ])
    figs_asa.append(figkey_tab)

    tab_tab = tab_tab.rename(columns={'installs_x': 'avgInstalls', 'avgCPA_y': "avgCPI", 'localSpend_x': 'avglocalSpend' })
    tab_tab['avgCPI'] = np.round(tab_tab['avgCPI'], 1)
    tab_tab['avglocalSpend'] = np.round(tab_tab['avglocalSpend'], 1)
    figkey_plot = px.scatter(tab_tab, x = 'avgInstalls', y = 'avgCPI', color = 'avglocalSpend', hover_name = "keyword", text="keyword")
    figkey_plot.update_layout(title_text = "Keywords Highlights")
    figkey_plot.update_traces(textposition='top center')

    figs_asa.append(figkey_plot)

    fig_dough = make_subplots(rows=1, cols=4, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}]],
            subplot_titles=['Impressions', 'Taps', 'Installs', 'Spend'])
            
    fig_dough.add_trace(go.Pie(values=custom_key.impressions, labels=custom_key.Country, hole=.4, name = 'Impressions'),1, 1)
    fig_dough.add_trace(go.Pie(values=custom_key.taps, labels=custom_key.Country,hole=.4, name = 'Taps'),1, 2)
    fig_dough.add_trace(go.Pie(values=custom_key.installs, labels=custom_key.Country, hole=.4, name = 'Installs'),1, 3)
    fig_dough.add_trace(go.Pie(values=custom_key.localSpend, labels=custom_key.Country, hole=.4, name = 'localSpend'),1, 4)
    fig_dough.update_traces(hoverinfo="label+percent+name+value")

    fig_dough.update_layout(
        title_text="ASA Breakdown by Country")

    #figs_asa.append(fig_dough)

    with open('dash_asa_daily_keap.html', 'w') as f:
        for fig in figs_asa:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
        
        
        
           


def download_campaigns_report():
    # URL, where we through out request
    url = "https://api.searchads.apple.com/api/v4/reports/campaigns"
    #"https://api.searchads.apple.com/api/v4/campaigns" -H "Authorization: Bearer {access_token}" \
    # We call our function, that creates a JSON request for us
    report = create_campaigns_report()

    # Now we construct everything together
    headers = {"Authorization": "Bearer {}".format(access_token), "X-AP-Context": "orgId={}".format(ORG_ID)} 
    response = requests.post(url, json=report, headers=headers) #cert=APPLE_CERT
    response.encoding = "utf-8"

    # Id status code is not 200 - something went wrong. We stop the program and show exact mistake
    if response.status_code != 200:
        raise ValueError(response.content)

    # If we ger here - the status is 200 and response contains our report
    # So we need to get it from JSON and ask json_normalize() to convert it to the table
    data = response.json()['data']['reportingDataResponse']['row']
    data = json_normalize(data)
    return data


def create_campaigns_report():
    report = \
        {
            "startTime": START_DATE,  # WE USE OUR START DATE HERE
            "endTime": END_DATE,      # WE USE OUR END DATE HERE
            "granularity": "DAILY",
            "selector": {
                "orderBy": [
                    {
                        "field": "countryOrRegion",
                        "sortOrder": "ASCENDING"
                    }
                ],
                "conditions": [
                    {
                        "field": "deleted",
                        "operator": "EQUALS",
                        "values": [
                            "false"
                        ]
                    },
                    {
                        "field": "campaignStatus",
                        "operator": "EQUALS",
                        "values": [
                            "ENABLED"
                        ]
                    }
                ],
                "pagination": {
                    "offset": 0,
                    "limit": 1000
                }
            },
            "groupBy": [
                "countryOrRegion"
            ],
            "timeZone": "UTC",
            "returnRecordsWithNoMetrics": True
        }
    return report

def download_keywords_report(campaignId):
    # URL, where we through out request
    url = "https://api.searchads.apple.com/api/v4/reports/campaigns/{}/keywords".format(campaignId)

    # We call our function, that creates a JSON request for us
    report = create_keywords_report()

    # Now we construct everything together
    headers = {"Authorization": "Bearer {}".format(access_token), "X-AP-Context": "orgId={}".format(ORG_ID)} 
    response = requests.post(url, json=report, headers=headers) #cert=APPLE_CERT
    response.encoding = "utf-8"

    # Id status code is not 200 - something went wrong. We stop the program and show exact mistake
    if response.status_code != 200:
        raise ValueError(response.content)

    # If we ger here - the status is 200 and response contains our report
    # So we need to get it from JSON and ask json_normalize() to convert it to the table
    data = response.json()['data']['reportingDataResponse']['row']
    data = json_normalize(data)
    return data


def create_keywords_report():
    report = \
        {
    "startTime": START_DATE,
    "endTime": END_DATE,
    "granularity": "DAILY",
    "selector": {
        "orderBy": [
            {
                "field": "countryOrRegion",
                "sortOrder": "ASCENDING"
            }
        ],
        "conditions": [
        ],
        "pagination": {
            "offset": 0,
            "limit": 1000
        }
    },
     "groupBy": [
        "countryOrRegion"
    ],
    "timeZone": "UTC",
    "returnRecordsWithNoMetrics": True
    }
    return report

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
def get_geo_by_date_report(app_id, api_token, start_date, end_date):
    
    client = AppsFlyer(api_token=api_token, app_id=app_id)
    df = client.geo_by_date_report(start_date, end_date, as_df=True)
    
    return df

if __name__ == "__main__":
    current_start= "2021-11-27"
    current_end= "2021-12-12"
    past_start= "2021-11-11"
    past_end= "2021-11-26"
    main(current_start, current_end, past_start, past_end)