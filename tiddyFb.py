"""
CODE FOR SANTA - IT JOINS Appsflyer data with Facebook API data to report per country.
Appsflyer data consists of API aggregated data, raw data from the push API stored in bigquery, and skan data that is stored locally after extracting from S3.
Appsflyer is storing raw jsons for push and skan data on S3.
"""


import pandas as pd  
from os.path import join
from gspread_pandas import Spread
import datetime
import numpy as np

from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adsinsights import AdsInsights
from facebookads.api import FacebookAdsApi

from appsflyer import AppsFlyer

import plotly.express as px
from plotly.graph_objs import *
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from google.oauth2.service_account import Credentials


#Google APIs scopes and credentials for writing on google_sheets
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'C:\\Python39\\Lib\\site-packages\\gspread_pandas\\google_secret.json',
    scopes=scopes
)

def main():
    """
    Executes all calls to APIs or reads from local files and creates visuals.
    Returns an HTML file.
    """
    #Facebook credentials PNP
    my_app_id = '199410016605'
    my_app_secret = '1cf69208e777b876ef25fbf0e40a06fc'
    my_access_token = "EAAAALm3DYV0BAMg5Ehsfj0Ghy8TJ6Wm5eUMEvATDrknQYnvZCBnxgRwZAcUL54DqGZBxaNcINUNhbNEXayZB4oGBHQXZB94H9akPdSjQ0Svu3dTFs0APufNJA0q56tDjtaaLIW32qdTlbxWBFse52cuHZAyHxvVb0xxOULEPfaOJ5b0N9eQzlyp3nkCHJEthS9VsMkNr7cYgZDZD"
    
    #Initialize API
    FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

    #Creates session
    sess = AdAccount('act_1211330622238467')

    #Dates and parameters to query Appsflyer API and Facebook API
    START_DATE = '2021-09-09'
    END_DATE = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")
    FIELDS = ['buying_type', 'objective']

    #iOS Appsflyer creds
    app_id = "id902026228"
    api_token = "6ebbb043-2c07-4972-8678-9687ae87ee9a"

    #iOS df
    df_af_ios = get_geo_by_date_report(app_id, api_token, START_DATE, END_DATE)
    df_af_ios = df_af_ios[df_af_ios['Media Source (pid)'] == 'Facebook Ads'].reset_index(drop = True)
    df_ios = df_af_ios[['Date', 'Country', 'Campaign (c)', 'Impressions', 'Clicks', 'Installs', 'af_purchase (Sales in CAD)', 'Total Revenue', 'Total Cost']].reset_index(drop = True)
   
    #Android df
    app_id = 'com.ugroupmedia.pnp14'
    df_af_android = get_geo_by_date_report(app_id, api_token, START_DATE, END_DATE)
    df_af_android = df_af_android[df_af_android['Media Source (pid)'] == 'Facebook Ads'].reset_index(drop = True)
    df_android = df_af_android[['Date', 'Country', 'Campaign (c)', 'Impressions', 'Clicks', 'Installs', 'af_purchase (Sales in CAD)', 'Total Revenue', 'Total Cost']].reset_index(drop = True)
    
    #Concatenated dataframe
    df_af = pd.concat([df_ios, df_android], axis = 0)
    df_af.reset_index(inplace = True)
    
    #Lookback window to call Fb API (ie. assigning to 10 will call the api 10 times once for each of the past 10 days).
    #Its used at least with 3 or more days to look for skan installs that is attributed after 72 hrs.
    window_days = 2
    #Path use to save html and facebook data
    path = 'C:\\Users\\User\\Documents\\Python Scripts'

    for day in range(window_days):
        END_DATE = (datetime.datetime.now() - datetime.timedelta(days = window_days - day)).strftime("%Y-%m-%d")
        print(END_DATE)
        #Retrieves campaigns from the API
        campaigns = sess.get_campaigns(fields = FIELDS)
    
        #Params to be used for each campaign
        params = {
            'time_range': {'since': END_DATE, 'until': END_DATE},
            'fields': ['campaign_name','impressions', 'inline_link_clicks', 'spend', 'purchase_roas', 'actions', 'website_purchase_roas']
        }

        #Initialize empty dataframe to populate with campaigns' data
        df = pd.DataFrame(columns = ['campaign_name', 'date_start', 'date_stop', 'impressions', 'inline_link_clicks','spend', 'purchase_roas', 'actions', 'website_purchase_roas'])
    
        indx = 0
        #Iter throuhg each campaign and populate our dataframe
        for campaign in campaigns:
            response = campaign.get_insights(params=params)
            for i in response:
                for col in i:
                    df.loc[indx, col] = i[col]
            indx += 1
        #Transformations to clean data
        df['spend'] = df['spend'].astype('float')
        df['purchase_roas'] = df['purchase_roas'].apply(lambda x: x if x is np.nan else float(x[0]['value']) )
        df['website_purchase_roas'] = df['website_purchase_roas'].apply(lambda x: x if x is np.nan else float(x[0]['value']) )
        idx = df['actions'].notna()
        acq = df.loc[idx,: ]

        #Extract from action column (json) the value of mobile_app_install
        for i in acq.index:
            action = 0
            for j in acq.loc[i, 'actions']:
                if j['action_type'] == 'mobile_app_install':
                    action += int(j['value'])
            if type(action) != int:
                acq.loc[i, 'actions'] = 0
            else:
                acq.loc[i, 'actions'] = action

        #Creates some type casts neccesary and the CPI, Revenue and website_rev columns
        acq['actions'] = acq['actions'].astype('float')
        acq['CPI'] = acq['spend'] / acq['actions']
        acq['impressions'] = acq['impressions'].astype('float')
        acq['inline_link_clicks'] = acq['inline_link_clicks'].astype('float')
        acq.fillna('0', inplace = True)

        if len(acq['purchase_roas'].values) > 0:
            #if type(acq['purchase_roas'].values[0]) != float:
            acq['Revenue'] = acq['purchase_roas'].astype('float') * acq['spend']
            #else:
            #    acq['Revenue'] = float(0)
        else:
            acq['Revenue'] = float(0)

        acq['inline_link_clicks'] = acq['inline_link_clicks'].astype('float')
        acq['CPI'] = acq['CPI'].astype('float')
        acq['website_rev'] = acq['website_purchase_roas'].astype('float') * acq['spend']

        #Filters appslfyer dataframe for the season for just the end_date in the forloop to merge data that can be uploaded to the budget sheet in Google Sheets 
        day_af = df_af[df_af['Date'] == END_DATE].groupby(['Date', 'Campaign (c)']).sum().reset_index()

        #The following code is only for this 2021 season (mislabelling techniques)
        if "2021_FB_IT_IOS_ACQ" in day_af['Campaign (c)'].unique():
            day_af.set_index("Campaign (c)", inplace = True)
            print(day_af)
            day_af.loc['2021_FB_IT_IOS_IT_ACQ', 'Installs'] = day_af.loc['2021_FB_IT_IOS_IT_ACQ', 'Installs'] + day_af.loc['2021_FB_IT_IOS_ACQ', 'Installs']
            day_af.loc['2021_FB_IT_IOS_IT_ACQ', 'af_purchase (Sales in CAD)'] = day_af.loc['2021_FB_IT_IOS_IT_ACQ', 'af_purchase (Sales in CAD)'] + day_af.loc['2021_FB_IT_IOS_ACQ', 'af_purchase (Sales in CAD)']
            day_af.loc['2021_FB_IT_IOS_IT_ACQ', 'Total Revenue'] = day_af.loc['2021_FB_IT_IOS_IT_ACQ', 'Total Revenue'] + day_af.loc['2021_FB_IT_IOS_ACQ', 'Total Revenue']
            day_af.reset_index(inplace = True)
            day_af = day_af[day_af['Campaign (c)'] != "2021_FB_IT_IOS_ACQ"]
        if "2021_FB_IT_Android_AUD" in day_af['Campaign (c)'].unique():
            day_af.set_index("Campaign (c)", inplace = True)
            day_af.loc['2021_FB_IT_Android_IT_AUD', 'Installs'] = day_af.loc['2021_FB_IT_Android_IT_AUD', 'Installs'] + day_af.loc['2021_FB_IT_Android_AUD', 'Installs']
            day_af.loc['2021_FB_IT_Android_IT_AUD', 'af_purchase (Sales in CAD)'] = day_af.loc['2021_FB_IT_Android_IT_AUD', 'af_purchase (Sales in CAD)'] + day_af.loc['2021_FB_IT_Android_AUD', 'af_purchase (Sales in CAD)']
            day_af.loc['2021_FB_IT_Android_IT_AUD', 'Total Revenue'] = day_af.loc['2021_FB_IT_Android_IT_AUD', 'Total Revenue'] + day_af.loc['2021_FB_IT_Android_AUD', 'Total Revenue']
            day_af.reset_index(inplace = True)
            day_af = day_af[day_af['Campaign (c)'] != "2021_FB_IT_Android_AUD"]
        camps = ["2021_FB_AND_Buyers_Conversions_AUD","2021_FB_WEB_Buyers_Conversions_AUD", "2021_FB_AND_Freeusers_Conversions_AUD","2021_FB_WEB_Freeusers_Conversions_AUD","2021_FB_iOS_LAL(5%)_ACQ","2021_FB_iOS_Parents(0-8)_ACQ","2021_FB_WEB_LAL(5%)_ACQ","2021_FB_WEB_Parents(0-8)_ACQ","2021_FB_AND_LAL(5%)_ACQ","2021_FB_AND_Parents(0-8)_ACQ"]
        for camp in camps:
            if camp in day_af['Campaign (c)'].unique():
                mid = ""
                for i in camp.split("_")[2:-1]: mid = mid + i + "_"
                new_camp = camp.split('_')[0] + "_" + camp.split('_')[1] + '_NA_' + mid + "WW_" + camp.split("_")[-1]
                day_af.set_index("Campaign (c)", inplace = True)
                day_af.loc[new_camp, 'Installs'] = day_af.loc[new_camp, 'Installs'] + day_af.loc[camp, 'Installs']
                day_af.loc[new_camp, 'af_purchase (Sales in CAD)'] = day_af.loc[new_camp, 'af_purchase (Sales in CAD)'] + day_af.loc[camp, 'af_purchase (Sales in CAD)']
                day_af.loc[new_camp, 'Total Revenue'] = day_af.loc[new_camp, 'Total Revenue'] + day_af.loc[camp, 'Total Revenue']
                day_af.reset_index(inplace = True)
                day_af = day_af[day_af['Campaign (c)'] != camp]

        #Uses dataframe of campaigns from facebook API and inserts any campaigns from Appsflyer that need to show up in case 
        #Appsflyer is showing data for a campaign not listed in the facebook api for that particular day
        grouped = acq.groupby(['date_start', 'campaign_name']).sum().reset_index()
        for i in day_af['Campaign (c)'].unique():
            if i not in grouped['campaign_name'].unique():
                fi = [END_DATE, i]
                sc = [0] * (len(grouped.columns) - 2)
                fi.extend(sc)
                grouped = pd.concat([grouped, pd.DataFrame([fi], columns = grouped.columns, index = range(0,1))], axis = 0, ignore_index=True)
        
        #Merges both Facebook and Appsflyer dataframes
        plot_rev = pd.merge(grouped,day_af, how = 'left', left_on =['date_start', 'campaign_name'], right_on = ['Date', 'Campaign (c)'])
        
        #Extracts skan data saved locally (ran by pnp/skan.py script) to merge it to plot_rev
        skan = pd.read_csv('C:\\Users\\User\\Documents\\Python Scripts\\pnp\\data_skan.csv')
        skan = skan[skan['media_source'] == 'Facebook Ads']
        #Adds any campaigns in skan dataframe not showing in plot_rev(end_date's data from the fb api and appsflyer) before left merging.
        for i in skan[skan['date'] == END_DATE]['ad_network_campaign_name'].unique():
            if i not in plot_rev['campaign_name'].unique():
                fi = [END_DATE, i]
                sc = [0] * (len(plot_rev.columns) - 2)
                fi.extend(sc)
                plot_rev = pd.concat([plot_rev, pd.DataFrame([fi], columns = plot_rev.columns, index = range(0,1))], axis = 0, ignore_index=True)
        plot_rev = pd.merge(plot_rev, skan[skan['date'] == END_DATE].groupby(['date', 'ad_network_campaign_name']).count().reset_index(), how = 'left', left_on =['date_start', 'campaign_name'], right_on = ['date', 'ad_network_campaign_name'] )
        plot_rev = plot_rev.rename(columns = {'install_type': 'installs'})
        plot_rev['installs'] = plot_rev['installs'].astype('float')
        plot_rev.fillna(0, inplace= True)
        if 'skad_revenue' not in plot_rev.columns:
            plot_rev['skad_revenue'] = 0
        
        #Code to add web revenue from google analytics if required. In 2021 season, web revenue was retrieved from channels APIs no need to use Google Analytics.
        #web = pd.read_csv('C:\\Users\\User\\Documents\\Python Scripts\\web_santa21.csv')
        #idx = [i for i in web.index if 'facebook' in web.loc[i,'Source']]
        ##web = web.loc[idx, :].reset_index()
        #web['Campaign'] = web['Campaign'].apply(lambda x: x + '_AUD')
        #for i in web[web['Day'] == END_DATE]['Campaign'].unique():
        #    if i not in plot_rev[plot_rev['date_start'] == END_DATE]['campaign_name'].unique():
        #        fi = [END_DATE, i]
        #        sc = [0] * (len(plot_rev.columns) - 2)
        #        fi.extend(sc)
        #        plot_rev = pd.concat([plot_rev, pd.DataFrame([fi], columns = plot_rev.columns, index = range(0,1))], axis = 0, ignore_index=True)
        #plot_rev = pd.merge(plot_rev, web[web['Day'] == END_DATE].groupby(['Day', 'Campaign']).sum().reset_index(), how = 'left', left_on =['date_start', 'campaign_name'], right_on = ['Day', 'Campaign'] )
        #plot_rev = plot_rev.groupby(['date_start', 'campaign_name']).sum().reset_index()

        #Uses the type_df function to filter audience and acquisition campaigns into new dataframes to upload to Google Sheets
        plot_rev['type'] = 'facebook'
        aud_df = type_df(plot_rev, 'AUD', 'ACQ')        
        aud_df['type'] = 'audience'

        acq_df = type_df(plot_rev, 'ACQ', 'AUD')
        acq_df['type'] = 'acquisition'

        #Populates dataframes that can be written to PNP's budget sheet on Google Sheets.
        fb_aud = pd.DataFrame({'Date': END_DATE, 'Network': 'Facebook (audience)', 'Installs': aud_df['actions'].astype('float').sum() , 'Installs AF': aud_df['Installs'].astype('float').sum(), 'Installs skan': aud_df['installs'].astype('float').sum(), 'Cost': aud_df['spend'].astype('float').sum(), 'Cost AF': aud_df['Total Cost'].astype('float').sum(), 'Revenue Skan': aud_df['skad_revenue'].astype('float').sum(), 'Revenue': aud_df['Revenue'].astype('float').sum(), 'Revenue AF': aud_df['af_purchase (Sales in CAD)'].astype('float').sum(), 'Web Revenue': aud_df['website_rev'].astype('float').sum()}, index = range(0,1))
        fb_acq = pd.DataFrame({'Date': END_DATE, 'Network': 'Facebook (Acquisition)', 'Installs': acq_df['actions'].astype('float').sum() , 'Installs AF': acq_df['Installs'].astype('float').sum(), 'Installs skan': acq_df['installs'].astype('float').sum(), 'Cost': acq_df['spend'].astype('float').sum(), 'Cost AF': acq_df['Total Cost'].astype('float').sum(), 'Revenue Skan': acq_df['skad_revenue'].astype('float').sum(), 'Revenue': acq_df['Revenue'].astype('float').sum(), 'Revenue AF': acq_df['af_purchase (Sales in CAD)'].astype('float').sum(), 'Web Revenue': 0}, index = range(0,1))
        fb_totals = pd.concat([fb_aud, fb_acq], axis = 0)
        fb_totals['ROAS'] = fb_totals['Revenue AF'] / fb_totals['Cost']
    

        #Writes fb_totals to the tab Daily_Overview_2021 tab in Google Sheets
        sheet_name = 'Daily_overview_2021'
        drive_fb(fb_totals, sheet_name, credentials)

        #In 2021 we use Appsflyer revenue as the revenue of choice we need to add the 
        #web revenue portion from the FB API that Appsflyer doesn't track before we save end_date's data locally.
        aud_df['af_purchase (Sales in CAD)'] =  aud_df['af_purchase (Sales in CAD)'] + aud_df['website_rev']
        plot_rev = pd.concat([aud_df, acq_df], axis = 0)
        #Columns used to save end_date's data to a local file fb_santa21.csv
        cols = ['date_start','campaign_name','impressions','inline_link_clicks','spend','actions','CPI','Revenue','Impressions','Clicks','Installs','af_purchase (Sales in CAD)','Total Revenue','Total Cost','installs','skad_revenue']
        db_fb = plot_rev[cols]
        #It first reads the file to replace or update previous data for the day that is queried
        #since end_date data might already be saved in fb_santa21.csv
        df_cum_total = pd.read_csv(join(path,'fb_santa21.csv'))
        df_cum_total = df_cum_total[cols]
        #Checks if the day queried df has any data before updating and saving the new file
        if len(db_fb) > 0:
            if db_fb['date_start'].values[0] in df_cum_total['date_start'].unique():
                df_cum_total = df_cum_total[df_cum_total['date_start'] != db_fb['date_start'].values[0]]
            df_cum_total = pd.concat([df_cum_total, db_fb], axis = 0)
            df_cum_total.to_csv(join(path,'fb_santa21.csv'), index = False) #, mode = 'a', header = False
    
    #This code works now on the updated facebook data
    #There's 2020 data that can be used to plot against 2021 data
    #df_cum_20 = pd.read_csv(join(path,'fb_santa_a.csv'))

    #Since the type column was not saved we need to create one again
    aud_df = type_df(df_cum_total, 'AUD', 'ACQ')        
    aud_df['type'] = 'audience'

    acq_df = type_df(df_cum_total, 'ACQ', 'AUD')
    acq_df['type'] = 'acquisition'

    df_cum_total = pd.concat([aud_df, acq_df], axis = 0)

    #Dates to plot facebook data along with Appsflyer data
    STARTS = (datetime.datetime.now() - datetime.timedelta(days = 34))
    ENDS = (datetime.datetime.now() - datetime.timedelta(days = 1))
    #ENDS_20 = (datetime.datetime.now() - datetime.timedelta(days = 326))

    #
    #Transformations on main df
    #

    df_cum_total['af_purchase (Sales in CAD)'] = df_cum_total['af_purchase (Sales in CAD)'].astype('float') 
    #df_cum_20['Revenue'] = df_cum_20['Revenue'].astype('float')

    df_cum_total['date_start'] = pd.to_datetime(df_cum_total['date_start'], format= '%Y-%m-%d')
    #df_cum_20['date_start'] = pd.to_datetime(df_cum_20['date_start'], format= '%Y-%m-%d')

    df_cum_total = df_cum_total[(df_cum_total['date_start'] >= STARTS) & (df_cum_total['date_start'] <= ENDS)]
    #df_cum_20 = df_cum_20[(df_cum_20['date_start'] <= ENDS_20)]

    df_cum_total['date_start'] = df_cum_total['date_start'].apply(lambda x: x.strftime('%Y-%m-%d'))
    #df_cum_20['date_start'] = df_cum_20['date_start'].apply(lambda x: x.strftime('%Y-%m-%d'))


    #List of facebook figures to save all plots
    fb_figs = []

    #Prep for overview fig. Revenue is skad, web and af_revenue added together.
    df_cum_total['Revenue'] = df_cum_total['af_purchase (Sales in CAD)'] + df_cum_total['skad_revenue']
    df_daily = df_cum_total.groupby('date_start').sum()
    df_daily['CPI'] = df_daily['spend'] / (df_daily['Installs'] + df_daily['installs'])
    df_daily['ARPU'] = df_daily['Revenue'] / (df_daily['Installs'] + df_daily['installs'])

    

    #Overview fig usign plotly
    fig = make_subplots( rows=1, cols=2, column_widths=[0.5, 0.5], specs=[[{'secondary_y':True}, {'secondary_y':True}]],
                    subplot_titles=("Daily FB Conversions vs. CPI", "Daily Revenue FB KPIs" ))
    
    # Add traces
    fig.add_trace(go.Scatter(x=df_daily.index, y=df_daily.CPI, name = 'CPI', marker_color = '#AB63FA'), secondary_y = True, row=1, col=1)

    fig.add_trace(go.Bar(x=df_daily.index, y=df_daily.actions, name = 'Installs',marker_color = '#00B5F7' ), row=1, col=1)

    fig.add_trace(go.Bar(x=df_daily.index, y=df_daily.Revenue, name = 'Revenue', marker_color = 'rgb(204,204,204)'), row=1, col=2)

    fig.add_trace(go.Scatter(x=df_daily.index, y=df_daily['Revenue'] / df_daily['spend'],
                    mode='lines+markers',
                    name='ROAS', marker_color = '#511CFB'), secondary_y = True, row =1 , col = 2)
    fig.add_trace(go.Scatter(x=df_daily.index, y=df_daily['ARPU'],
                    mode='lines+markers',
                    name='ARPU', marker_color = '#FF9900'), secondary_y = True, row =1 , col = 2)
    fig.add_trace(go.Scatter(x=df_daily.index, y=df_daily['spend'],
                    mode='lines+markers',
                    name='Cost', marker_color = '#EF553B'), row =1 , col = 2)
    fb_figs.append(fig)

    #Prep for campaign figure
    df_camp = df_cum_total.groupby('campaign_name').sum().reset_index()
    df_camp['ROAS'] = df_camp['Revenue'] / df_camp['spend']
    df_camp = df_camp[df_camp['Revenue'] > 0].reset_index(drop = True)
    df_camp.sort_values('ROAS', ascending = False, inplace = True)

    #Traces
    trace = go.Table(header=dict(values=['Campaign','Revenue', 'ROAS']),
                cells=dict(values=[df_camp.campaign_name.values, np.round(df_camp.Revenue.values, 2), np.round(df_camp.ROAS.values, 1)]), domain=dict(x=[0.52, 1],y=[0, 1]))
            
    trace1 = go.Pie(values=df_camp.spend, labels=df_camp.campaign_name, hole=.4, name = 'Cost', domain=dict(x=[0, 0.23],y=[0, 1]), title_text = 'Cost', textposition='inside', textinfo='percent', hoverinfo="label+value")
    trace2 = go.Pie(values=df_camp.Revenue, labels=df_camp.campaign_name, hole=.4, name = 'Revenue', domain=dict(x=[0.26, 0.49],y=[0, 1]), title_text = 'Revenue', textposition='inside', textinfo='percent', hoverinfo="label+value")
    
    #Pies and table fig
    fig_dough = go.Figure(data = [trace,trace1, trace2])
    fig_dough.update_layout(title_text="FB Breakdown by Campaign")

    fb_figs.append(fig_dough)
    
    #Prep for country breakdown figure
    corte = df_af.groupby('Country').sum().reset_index()
    corte.sort_values('af_purchase (Sales in CAD)', ascending = False, inplace = True)
    corte = corte.head(15)
    #Only select 15 top countries
    parces = corte.Country.unique()
    idx = [ i for i in df_af.index if df_af.loc[i, 'Country'] in parces]
    df_country = df_af.loc[idx, :]
    df_country = df_country.groupby(['Date', 'Country', 'Campaign (c)']).sum().reset_index().sort_values('Date')
    df_country = df_country[df_country['af_purchase (Sales in CAD)'] > 0 ].reset_index(drop = True)

    #Campaign performance on each country
    fig_camp = px.bar(df_country, x='Date', y='af_purchase (Sales in CAD)', color='Campaign (c)',
               facet_col='Country', facet_col_wrap=2)
    fig_camp.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig_camp.update_yaxes(matches=None, showticklabels=True, title_text='')
    fig_camp.update_xaxes(matches=None, showticklabels=True, title_text='')
    fig_camp.update_layout(
        title_text="Daily FB Campaigns Revenue per Country", height = 750, barmode = 'stack')

    fb_figs.append(fig_camp)

    #Merging skan data and raw data to create KPIS based on number of installs and number of purchases (event based not campaign based).

    skan = pd.read_csv('C:\\Users\\User\\Documents\\Python Scripts\\pnp\\data_skan.csv')
    skan = skan[skan['media_source'] == 'Facebook Ads']

    #Join Facebook data with Appsflyer for the whole date range
    geo_report_tab = pd.merge(df_cum_total, df_af.groupby(['Date', 'Campaign (c)']).sum().reset_index(), how = 'left', left_on= ['date_start', 'campaign_name'], right_on= ['Date', 'Campaign (c)'])
    geo_report_tab = geo_report_tab.groupby(['date_start', 'campaign_name']).sum().reset_index()

    #Join geo_report_tab with SKAN dataframe for the whole date range
    geo_report_tab = pd.merge(geo_report_tab, skan.groupby(['date', 'ad_network_campaign_name']).count().reset_index(), how = 'left', left_on =['date_start', 'campaign_name'], right_on = ['date', 'ad_network_campaign_name'] )
    if 'skad_revenue' not in geo_report_tab.columns:
        geo_report_tab['skad_revenue'] = 0
    geo_report_tab = geo_report_tab.groupby(['date_start','campaign_name']).sum().reset_index()
    geo_report_tab['date_start'] = geo_report_tab['date_start'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    geo_report_tab['date_start'] = geo_report_tab['date_start'].apply(lambda x: x.date())
    geo_report_tab['ROAS'] = geo_report_tab['Revenue'] / geo_report_tab['spend']

    #Join raw data to geo_report_tab for the whole date range
    raw = pd.read_csv('C:\\Users\\User\\Documents\\Python Scripts\\pnp\\data_raw.csv')
    raw = raw[raw['media_source'] == 'Facebook Ads']
    raw['af_purchase'] = raw['event_name'].apply(lambda x: 1 if x == 'af_purchase' else 0)
    dic_country = {"AF":"AFGHANISTAN","AX":"ÅLAND ISLANDS","AL":"ALBANIA","DZ":"ALGERIA","AS":"AMERICAN SAMOA","AD":"ANDORRA","AO":"ANGOLA","AI":"ANGUILLA","AQ":"ANTARCTICA","AG":"ANTIGUA AND BARBUDA","AR":"ARGENTINA","AM":"ARMENIA","AW":"ARUBA","AU":"AUSTRALIA","AT":"AUSTRIA","AZ":"AZERBAIJAN","BS":"BAHAMAS","BH":"BAHRAIN","BD":"BANGLADESH","BB":"BARBADOS","BY":"BELARUS","BE":"BELGIUM","BZ":"BELIZE","BJ":"BENIN","BM":"BERMUDA","BT":"BHUTAN","BO":"BOLIVIA, PLURINATIONAL STATE OF","BQ":"BONAIRE, SINT EUSTATIUS AND SABA","BA":"BOSNIA AND HERZEGOVINA","BW":"BOTSWANA","BV":"BOUVET ISLAND","BR":"BRAZIL","IO":"BRITISH INDIAN OCEAN TERRITORY","BN":"BRUNEI DARUSSALAM","BG":"BULGARIA","BF":"BURKINA FASO","BI":"BURUNDI","KH":"CAMBODIA","CM":"CAMEROON","CA":"CANADA","CV":"CAPE VERDE","KY":"CAYMAN ISLANDS","CF":"CENTRAL AFRICAN REPUBLIC","TD":"CHAD","CL":"CHILE","CN":"CHINA","CX":"CHRISTMAS ISLAND","CC":"COCOS (KEELING) ISLANDS","CO":"COLOMBIA","KM":"COMOROS","CG":"CONGO","CD":"CONGO, THE DEMOCRATIC REPUBLIC OF THE","CK":"COOK ISLANDS","CR":"COSTA RICA","CI":"CÔTE D'IVOIRE","HR":"CROATIA","CU":"CUBA","CW":"CURAÇAO","CY":"CYPRUS","CZ":"CZECH REPUBLIC","DK":"DENMARK","DJ":"DJIBOUTI","DM":"DOMINICA","DO":"DOMINICAN REPUBLIC","EC":"ECUADOR","EG":"EGYPT","SV":"EL SALVADOR","GQ":"EQUATORIAL GUINEA","ER":"ERITREA","EE":"ESTONIA","ET":"ETHIOPIA","FK":"FALKLAND ISLANDS (MALVINAS)","FO":"FAROE ISLANDS","FJ":"FIJI","FI":"FINLAND","FR":"FRANCE","GF":"FRENCH GUIANA","PF":"FRENCH POLYNESIA","TF":"FRENCH SOUTHERN TERRITORIES","GA":"GABON","GM":"GAMBIA","GE":"GEORGIA","DE":"GERMANY","GH":"GHANA","GI":"GIBRALTAR","GR":"GREECE","GL":"GREENLAND","GD":"GRENADA","GP":"GUADELOUPE","GU":"GUAM","GT":"GUATEMALA","GG":"GUERNSEY","GN":"GUINEA","GW":"GUINEA-BISSAU","GY":"GUYANA","HT":"HAITI","HM":"HEARD ISLAND AND MCDONALD ISLANDS","VA":"HOLY SEE (VATICAN CITY STATE)","HN":"HONDURAS","HK":"HONG KONG","HU":"HUNGARY","IS":"ICELAND","IN":"INDIA","ID":"INDONESIA","IR":"IRAN, ISLAMIC REPUBLIC OF","IQ":"IRAQ","IE":"IRELAND","IM":"ISLE OF MAN","IL":"ISRAEL","IT":"ITALY","JM":"JAMAICA","JP":"JAPAN","JE":"JERSEY","JO":"JORDAN","KZ":"KAZAKHSTAN","KE":"KENYA","KI":"KIRIBATI","KP":"KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF","KR":"KOREA, REPUBLIC OF","KW":"KUWAIT","KG":"KYRGYZSTAN","LA":"LAO PEOPLE'S DEMOCRATIC REPUBLIC","LV":"LATVIA","LB":"LEBANON","LS":"LESOTHO","LR":"LIBERIA","LY":"LIBYA","LI":"LIECHTENSTEIN","LT":"LITHUANIA","LU":"LUXEMBOURG","MO":"MACAO","MK":"MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF","MG":"MADAGASCAR","MW":"MALAWI","MY":"MALAYSIA","MV":"MALDIVES","ML":"MALI","MT":"MALTA","MH":"MARSHALL ISLANDS","MQ":"MARTINIQUE","MR":"MAURITANIA","MU":"MAURITIUS","YT":"MAYOTTE","MX":"MEXICO","FM":"MICRONESIA, FEDERATED STATES OF","MD":"MOLDOVA, REPUBLIC OF","MC":"MONACO","MN":"MONGOLIA","ME":"MONTENEGRO","MS":"MONTSERRAT","MA":"MOROCCO","MZ":"MOZAMBIQUE","MM":"MYANMAR","NA":"NAMIBIA","NR":"NAURU","NP":"NEPAL","NL":"NETHERLANDS","NC":"NEW CALEDONIA","NZ":"NEW ZEALAND","NI":"NICARAGUA","NE":"NIGER","NG":"NIGERIA","NU":"NIUE","NF":"NORFOLK ISLAND","MP":"NORTHERN MARIANA ISLANDS","NO":"NORWAY","OM":"OMAN","PK":"PAKISTAN","PW":"PALAU","PS":"PALESTINE, STATE OF","PA":"PANAMA","PG":"PAPUA NEW GUINEA","PY":"PARAGUAY","PE":"PERU","PH":"PHILIPPINES","PN":"PITCAIRN","PL":"POLAND","PT":"PORTUGAL","PR":"PUERTO RICO","QA":"QATAR","RE":"RÉUNION","RO":"ROMANIA","RU":"RUSSIAN FEDERATION","RW":"RWANDA","BL":"SAINT BARTHÉLEMY","SH":"SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA","KN":"SAINT KITTS AND NEVIS","LC":"SAINT LUCIA","MF":"SAINT MARTIN (FRENCH PART)","PM":"SAINT PIERRE AND MIQUELON","VC":"SAINT VINCENT AND THE GRENADINES","WS":"SAMOA","SM":"SAN MARINO","ST":"SAO TOME AND PRINCIPE","SA":"SAUDI ARABIA","SN":"SENEGAL","RS":"SERBIA","SC":"SEYCHELLES","SL":"SIERRA LEONE","SG":"SINGAPORE","SX":"SINT MAARTEN (DUTCH PART)","SK":"SLOVAKIA","SI":"SLOVENIA","SB":"SOLOMON ISLANDS","SO":"SOMALIA","ZA":"SOUTH AFRICA","GS":"SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS","SS":"SOUTH SUDAN","ES":"SPAIN","LK":"SRI LANKA","SD":"SUDAN","SR":"SURINAME","SJ":"SVALBARD AND JAN MAYEN","SZ":"SWAZILAND","SE":"SWEDEN","CH":"SWITZERLAND","SY":"SYRIAN ARAB REPUBLIC","TW":"TAIWAN, PROVINCE OF CHINA","TJ":"TAJIKISTAN","TZ":"TANZANIA, UNITED REPUBLIC OF","TH":"THAILAND","TL":"TIMOR-LESTE","TG":"TOGO","TK":"TOKELAU","TO":"TONGA","TT":"TRINIDAD AND TOBAGO","TN":"TUNISIA","TR":"TURKEY","TM":"TURKMENISTAN","TC":"TURKS AND CAICOS ISLANDS","TV":"TUVALU","UG":"UGANDA","UA":"UKRAINE","AE":"UNITED ARAB EMIRATES","GB":"UNITED KINGDOM","UK":"UNITED KINGDOM","US":"UNITED STATES","USA":"UNITED STATES","UM":"UNITED STATES MINOR OUTLYING ISLANDS","UY":"URUGUAY","UZ":"UZBEKISTAN","VU":"VANUATU","VE":"VENEZUELA, BOLIVARIAN REPUBLIC OF","VN":"VIET NAM","VG":"VIRGIN ISLANDS, BRITISH","VI":"VIRGIN ISLANDS, U.S.","WF":"WALLIS AND FUTUNA","EH":"WESTERN SAHARA","YE":"YEMEN","ZM":"ZAMBIA","ZW":"ZIMBABWE"}
    raw['country_name'] = raw['country_code'].map(dic_country) 

    def capi(x):
        """
        Function to capitalize countries and remove inconsistencies on countries names
        """
        word = ''
        words = x.split(' ')
        for i in words:
            char = i.capitalize() + ' '
            word = word + char
        return word[:-1]

    #to datetime from timestamp
    raw['date'] = raw['event_time_selected_timezone'].apply(lambda x: datetime.datetime.strptime(x.split('.')[0], '%Y-%m-%d %H:%M:%S'))
    #transform date to same dateformat than geo_report_tab date_start column
    raw['date'] = raw['date'].apply(lambda x: x.date())
    #grouping before merge with geo_report_tab
    raw_tab = raw.groupby(['date', 'campaign']).sum().reset_index()
    #merge to form df for tables
    tab_tab = pd.merge(geo_report_tab, raw_tab, how = 'left', left_on = ['date_start','campaign_name'], right_on= ['date', 'campaign'])
    
    #first df per campaign
    tab_1 = tab_tab.groupby(['campaign']).sum().reset_index()
    tab_1['CPA(login)'] = tab_1['spend'] / (tab_1['Installs_x'] + tab_1['installs'])
    tab_1['CPA(buyer)'] = tab_1['spend'] / (tab_1['af_purchase'])
    #create table
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Campaign', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_1['campaign'].values, tab_1['Installs_x'].values + tab_1['installs'].values, np.round(tab_1['spend'].values / (tab_1['Installs_x'].values + tab_1['installs'].values), 2), np.round(tab_1['af_purchase (Sales in CAD)_x'].values, 2) , np.round(tab_1['CPA(login)'].values, 2) , np.round(tab_1['CPA(buyer)'].values,2), np.round(tab_1['af_purchase (Sales in CAD)_x'].values / tab_1['spend'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Campaign Table Breakdown From {} to {}".format(START_DATE, END_DATE))

    fb_figs.append(figkey_tab)

    #likewise for last 7 days
    tab_tab['date_start'] = tab_tab['date_start'].apply(lambda x: datetime.datetime.combine(x, datetime.time(0, 0)))
    tab_tab_7 = tab_tab[tab_tab['date_start'] >= (datetime.datetime.now() - datetime.timedelta(days = 7))]
    tab_1_7 = tab_tab_7.groupby(['campaign']).sum().reset_index()
    print(tab_1_7)
    tab_1_7['CPA(login)'] = tab_1_7['spend'] / (tab_1_7['Installs_x'] + tab_1_7['installs'])
    tab_1_7['CPA(buyer)'] = tab_1_7['spend'] / (tab_1_7['af_purchase'])
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Campaign', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_1_7['campaign'].values, tab_1_7['Installs_x'].values + tab_1_7['installs'].values, np.round(tab_1_7['spend'].values / (tab_1_7['Installs_x'].values + tab_1_7['installs'].values), 2), np.round(tab_1_7['af_purchase (Sales in CAD)_x'].values, 2) , np.round(tab_1_7['CPA(login)'].values, 2) , np.round(tab_1_7['CPA(buyer)'].values,2), np.round(tab_1_7['af_purchase (Sales in CAD)_x'].values / tab_1_7['spend'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Campaign Table Breakdown Last 7 days")

    fb_figs.append(figkey_tab)

    #transform for table per country
    tab_1['Country'] = tab_1['campaign'].apply(lambda x: x.split('_')[-2] if len(x.split('_')) > 1 else 'USA')
    tab_1['Country'] = tab_1['Country'].apply(lambda x: capi(dic_country[x]) if x in dic_country.keys() else x)
    tab_2 = tab_1.groupby('Country').sum().reset_index()
    tab_2['CPA(login)'] = tab_2['spend'] / (tab_2['Installs_x'] + tab_2['installs'])
    tab_2['CPA(buyer)'] = tab_2['spend'] / (tab_2['af_purchase'])
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Country', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_2['Country'].values, tab_2['Installs_x'].values + tab_2['installs'].values, np.round(tab_2['spend'].values / (tab_2['Installs_x'].values + tab_2['installs'].values), 2), np.round(tab_2['af_purchase (Sales in CAD)_x'].values, 2) , np.round(tab_2['CPA(login)'].values, 2) , np.round(tab_2['CPA(buyer)'].values,2), np.round(tab_2['af_purchase (Sales in CAD)_x'].values / tab_2['spend'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Country Table Breakdown From {} to {}".format(START_DATE, END_DATE))

    fb_figs.append(figkey_tab)

    #likewise for last 7 days
    tab_1_7['Country'] = tab_1_7['campaign'].apply(lambda x: x.split('_')[-2] if len(x.split('_')) > 1 else 'USA')
    tab_1_7['Country'] = tab_1_7['Country'].apply(lambda x: capi(dic_country[x]) if x in dic_country.keys() else x)
    tab_2_7 = tab_1_7.groupby('Country').sum().reset_index()
    tab_2_7['CPA(login)'] = tab_2_7['spend'] / (tab_2_7['Installs_x'] + tab_2_7['installs'])
    tab_2_7['CPA(buyer)'] = tab_2_7['spend'] / (tab_2_7['af_purchase'])
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Country', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_2_7['Country'].values, tab_2_7['Installs_x'].values + tab_2_7['installs'].values, np.round(tab_2_7['spend'].values / (tab_2_7['Installs_x'].values + tab_2_7['installs'].values), 2), np.round(tab_2_7['af_purchase (Sales in CAD)_x'].values, 2) , np.round(tab_2_7['CPA(login)'].values, 2) , np.round(tab_2_7['CPA(buyer)'].values,2), np.round(tab_2_7['af_purchase (Sales in CAD)_x'].values / tab_2_7['spend'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Country Table Breakdown Last 7 days")

    fb_figs.append(figkey_tab)

    #transformation for language table
    tab_1['Language'] = tab_1['campaign'].apply(lambda x: x.split('_')[-4] if len(x.split('_')) > 1 else 'EN')
    tab_3 = tab_1.groupby('Language').sum().reset_index()
    tab_3['CPA(login)'] = tab_3['spend'] / (tab_3['Installs_x'] + tab_3['installs'])
    tab_3['CPA(buyer)'] = tab_3['spend'] / (tab_3['af_purchase'])
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Language', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_3['Language'].values, tab_3['Installs_x'].values + tab_3['installs'].values, np.round(tab_3['spend'].values / (tab_3['Installs_x'].values + tab_3['installs'].values), 2), np.round(tab_3['af_purchase (Sales in CAD)_x'].values, 2) , np.round(tab_3['CPA(login)'].values, 2) , np.round(tab_3['CPA(buyer)'].values,2), np.round(tab_3['af_purchase (Sales in CAD)_x'].values / tab_3['spend'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Language Table Breakdown From {} to {}".format(START_DATE, END_DATE))

    fb_figs.append(figkey_tab)

    ##7 days

    #likewise for last 7 days
    tab_1_7['Language'] = tab_1_7['campaign'].apply(lambda x: x.split('_')[-4] if len(x.split('_')) > 1 else 'EN')
    tab_3_7 = tab_1_7.groupby('Language').sum().reset_index()
    tab_3_7['CPA(login)'] = tab_3_7['spend'] / (tab_3_7['Installs_x'] + tab_3_7['installs'])
    tab_3_7['CPA(buyer)'] = tab_3_7['spend'] / (tab_3_7['af_purchase'])
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Language', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_3_7['Language'].values, tab_3_7['Installs_x'].values + tab_3_7['installs'].values, np.round(tab_3_7['spend'].values / (tab_3_7['Installs_x'].values + tab_3_7['installs'].values), 2), np.round(tab_3_7['af_purchase (Sales in CAD)_x'].values, 2) , np.round(tab_3_7['CPA(login)'].values, 2) , np.round(tab_3_7['CPA(buyer)'].values,2), np.round(tab_3_7['af_purchase (Sales in CAD)_x'].values / tab_3_7['spend'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Language Table Breakdown Last 7 days")

    fb_figs.append(figkey_tab)

    #create report and writing file
    with open(join(path,'Fb_Prev.html'), 'w') as f:
        for fig in fb_figs:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    


#Detailing function

def drive_fb(df, sheet_name, credentials):
    spreadsheet_key = '1oNclOE5NOm9ruo6Arh-daYIaPnBRqpmKdunw8dxI2WI'
    spread = Spread(spreadsheet_key, creds = credentials) 
    cell = spread.get_sheet_dims(sheet_name)
    startc = 'A' + str(cell[0] + 1)
    spread.df_to_sheet(df, index=False, sheet=sheet_name, start=startc, headers = False)


def output_fb(df):
    temp = df.copy()
    select = ['Reporting Ends', 'Impressions', 'Unique Link Clicks', 'Clicks (All)', "App Installs", 'Amount Spent (USD)', 'unique_actions:post_reaction', 'Buying Type', 'Campaign Name',  'Country']
    upload = pd.DataFrame(columns = select)
    mycolumns = [c for c in temp.columns if c in select]
    set_sheet = df[mycolumns]
    upload  = upload.append(set_sheet)
    
    return upload

def upload_fb(df, sheet_name):
    spreadsheet_key = '1kaUb-j3vtEgchgAsgmyBZO2TGJ8zwl_7AQIXxwrlZIQ'
    spread = Spread(spreadsheet_key) 
    cell = spread.get_sheet_dims(sheet_name)
    startcell = 'A' + str(cell[0] + 1)
    #spread.df_to_sheet(df, index=False, sheet=sheet_name, start='A1', headers = True)
    spread.df_to_sheet(df, index=False, sheet=sheet_name, start=startcell, headers = False)

def get_geo_by_date_report(app_id, api_token, start_date, end_date):
    
    client = AppsFlyer(api_token=api_token, app_id=app_id)
    df = client.geo_by_date_report(start_date, end_date, as_df=True)
    
    return df

def get_installs_report(app_id, api_token, start_date, end_date):
    
    client = AppsFlyer(api_token=api_token, app_id=app_id)
    df = client.installs_report(start_date, end_date, as_df=True)
    
    return df

def type_df(df, type, notype):
            indx = [i for i in df.index if type in df.loc[i, 'campaign_name'] and notype not in df.loc[i, 'campaign_name']]
            new_df = df.loc[indx, :]
            return new_df

if __name__ == "__main__":
    main()