from googleads import adwords, oauth2
from appsflyer import AppsFlyer
from os.path import join
import pandas as pd
import io
from datetime import datetime, timedelta, time
import numpy as np
from gspread_pandas import Spread

import _locale

import plotly.express as px
from plotly.graph_objs import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import n_colors
from google.oauth2.service_account import Credentials


_locale._getdefaultlocale = (lambda *args: ['en_US', 'UTF-8'])
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'C:\\Python39\\Lib\\site-packages\\gspread_pandas\\google_secret.json',
    scopes=scopes
)


def main():
    # We call our main delivery-boy function to do all the work


    start_date_21 = '2021-12-09'
    end_date_21 = (datetime.now() - timedelta(days= 10))
    
    start_date = '2020-10-17'
    end_date = (datetime.now() - timedelta(days= 350))

    client_id = "422898392645-kq6mc00a3h0c857qdp8jsre7pi9gjntv.apps.googleusercontent.com"#'202961295237-37faefhbfejk51u8pku6m1k6m0qqmfd4.apps.googleusercontent.com'
    client_secret =  'AH28CNr8Lnuuhw-irN6smI_O' #'5QI2t1L40KKCoHbcwPhiUgag'
    refresh_token = '1//05qkK15saZ0leCgYIARAAGAUSNwF-L9Ir23RUfb8UTR1ynm9s__5CHHTKA7ms2aggZKC0tFsASch4cQU82-byRV3Ny7oBoGh3Z3U' 
    developer_token =  'PJY5mhXidEqXfbuCZES9PQ' #'lQ39Q72wJPICh7G8tvqgDA'
    client_customer_id = '3096033436'

    app_id = "id902026228"
    api_token = "6ebbb043-2c07-4972-8678-9687ae87ee9a"

    start_DATE_ = '2021-09-10'
    end_DATE_ = (datetime.now() - timedelta(days= 1)).strftime("%Y-%m-%d")

    df_af_asa = get_geo_by_date_report(app_id, api_token, start_DATE_, end_DATE_)
    df_af_asa = df_af_asa[df_af_asa['Media Source (pid)'] == 'googleadwords_int']
    #print(df_af_asa['Campaign (c)'].unique())

    api_id = "com.ugroupmedia.pnp14"
    
    df_af_g = get_geo_by_date_report(api_id, api_token, start_DATE_, end_DATE_)
    df_af_g = df_af_g[df_af_g['Media Source (pid)'] == 'googleadwords_int']
    
    #print(df_af_g.columns)
    df_date = pd.concat([df_af_asa, df_af_g], axis = 0)
    df_date = df_date.groupby(['Date', 'Campaign (c)', 'Country']).sum().reset_index()
    #print(df_date.columns)
    df_level = df_date[['Date','Campaign (c)','Installs', 'af_subscribe (Sales in CAD)', 'Country', 'af_purchase (Sales in CAD)','Total Revenue', 'Total Cost']]


    #df1 = get_age(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date_, end_date_)
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
       # demo.add_trace(go.Scatter(y = df1[df1['Campaign'] == i]['Total conv. value'], x = df1[df1['Campaign'] == i]['Age Range'], marker_color = scala[j], name = i ),1,2)
       # j+= 1
    #demo.update_layout(barmode = 'stack', title_text = 'Demographics')

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


    df = get_campaign_performance_report(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date_21, end_date_21)
    df_19 = get_campaign_performance_report(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date, end_date)
    channels = get_ad_performance(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date_21, end_date_21)
    #df_b = get_budget_report(client_id, client_secret, refresh_token, developer_token, client_customer_id, end_date_, end_date_)

    #and df.loc[i, 'Campaign serving status'] == 'eligible'
    #Pick uac campaigns
  

    index_uac = [i for i in df.index if 'S_NB' not in df.loc[i,'Campaign'] and 'Branded' not in df.loc[i,'Campaign'] and 'UAC' in df.loc[i,'Campaign']]
    uac_campaigns = df.iloc[index_uac,:]

    index_uac = [i for i in df_19.index if 'S_NB' not in df_19.loc[i,'Campaign'] and 'Branded' not in df_19.loc[i,'Campaign'] and 'UAC' in df_19.loc[i,'Campaign'] ]
    uac_campaigns_19 = df_19.iloc[index_uac,:]
    
    #Pick nb campaigns
    index_nb = [i for i in df.index if 'Branded' not in df.loc[i,'Campaign'] and 'UAC' not in df.loc[i,'Campaign'] and 'S_NB' in df.loc[i,'Campaign']]
    nb_campaigns = df.iloc[index_nb,:]

    index_nb = [i for i in df_19.index if 'Branded' not in df_19.loc[i,'Campaign'] and 'UAC' not in df_19.loc[i,'Campaign'] and 'S_NB' in df_19.loc[i,'Campaign'] ]
    nb_campaigns_19 = df_19.iloc[index_nb,:]

    #Pick branded campaigns
    index_b = [i for i in df.index if 'UAC' not in df.loc[i,'Campaign'] and 'S_NB' not in df.loc[i,'Campaign'] and 'Branded' in df.loc[i,'Campaign']  ]
    b_campaigns = df.iloc[index_b,:]

    index_b = [i for i in df_19.index if 'UAC' not in df_19.loc[i,'Campaign'] and 'S_NB' not in df_19.loc[i,'Campaign'] and 'Branded' in df_19.loc[i,'Campaign'] ]
    b_campaigns_19 = df_19.iloc[index_b,:]


    uac_campaigns['type'] = 'UAC'
    nb_campaigns['type'] = 'Non-Branded'
    b_campaigns['type'] = 'Branded'

    uac_campaigns_19['type'] = 'UAC'
    nb_campaigns_19['type'] = 'Non-Branded'
    b_campaigns_19['type'] = 'Branded'

    unified = pd.concat([uac_campaigns, nb_campaigns, b_campaigns], axis = 0)
    temp = unified.copy()
    

    ### Filtering by end_date

    df_level['type'] = 'Adwords'

    for i in df_level.index:
        if 'UAC' in df_level.loc[i, 'Campaign (c)'] and 'S_NB' not in df_level.loc[i, 'Campaign (c)'] and 'Branded' not in df_level.loc[i, 'Campaign (c)']:
            df_level.loc[i, 'type'] = 'UAC'
        if 'S_NB' in df_level.loc[i, 'Campaign (c)'] and 'UAC' not in df_level.loc[i, 'Campaign (c)'] and 'Branded' not in df_level.loc[i, 'Campaign (c)']:
            df_level.loc[i, 'type'] = 'Non-Branded'
        if 'Branded' in df_level.loc[i, 'Campaign (c)'] and 'S_NB' not in df_level.loc[i, 'Campaign (c)'] and 'UAC' not in df_level.loc[i, 'Campaign (c)']:
            df_level.loc[i, 'type'] = 'Branded'
    
    df_level = df_level[df_level['type'] != 'Adwords']    

    skan = pd.read_csv('C:\\Users\\User\\Documents\\Python Scripts\\pnp\\data_skan.csv')
    skan = skan[skan['media_source'] == 'googleadwords_int'] 

    skan['type'] = 'Adwords'
    
    for i in skan.index:
        if 'UAC' in skan.loc[i, 'ad_network_campaign_name'] and 'S_NB' not in skan.loc[i, 'ad_network_campaign_name'] and 'Branded' not in skan.loc[i, 'ad_network_campaign_name']:
            skan.loc[i, 'type'] = 'UAC'
        if 'S_NB' in skan.loc[i, 'ad_network_campaign_name'] and 'UAC' not in skan.loc[i, 'ad_network_campaign_name'] and 'Branded' not in skan.loc[i, 'ad_network_campaign_name']:
            skan.loc[i, 'type'] = 'Non-Branded'
        if 'Branded' in skan.loc[i, 'ad_network_campaign_name'] and 'S_NB' not in skan.loc[i, 'ad_network_campaign_name'] and 'UAC' not in skan.loc[i, 'ad_network_campaign_name']:
            skan.loc[i, 'type'] = 'Branded'
    
    skan = skan[skan['type'] != 'Adwords']

    ##WEB
    web = pd.read_csv('C:\\Users\\User\\Documents\\Python Scripts\\web_santa21.csv')

    web['type'] = 'Adwords'
    
    for i in web.index:
        if 'UAC' in web.loc[i, 'Campaign'] and 'S_NB' not in web.loc[i, 'Campaign'] and 'Branded' not in web.loc[i, 'Campaign']:
            web.loc[i, 'type'] = 'UAC'
        if 'S_NB' in web.loc[i, 'Campaign'] and 'UAC' not in web.loc[i, 'Campaign'] and 'Branded' not in web.loc[i, 'Campaign']:
            web.loc[i, 'type'] = 'Non-Branded'
        if 'Branded' in web.loc[i, 'Campaign'] and 'S_NB' not in web.loc[i, 'Campaign'] and 'UAC' not in web.loc[i, 'Campaign']:
            web.loc[i, 'type'] = 'Branded'
    
    web = web[web['type'] != 'Adwords']    
    web = web.rename(columns = {'Conversions': 'Conversion'})   
    
    plot_rev = pd.merge(temp.groupby(['Day','type']).sum().reset_index(),df_level.groupby(['Date', 'type']).sum().reset_index(), how = 'left', left_on =['Day', 'type'], right_on = ['Date', 'type'])
    plot_rev = plot_rev.groupby(['Day', 'type']).sum().reset_index()
    plot_rev = pd.merge(plot_rev, skan.groupby(['date', 'type']).count().reset_index(), how = 'left', left_on =['Day', 'type'], right_on = ['date', 'type'] )
    plot_rev = plot_rev.rename(columns = {'install_type': 'installs'})
    if 'skad_revenue' not in plot_rev.columns:
        plot_rev['skad_revenue'] = 0
    plot_rev = plot_rev.groupby(['Day','type']).sum().reset_index()
    plot_rev = pd.merge(plot_rev, web.groupby(['Day', 'type']).sum().reset_index(), how = 'left', left_on =['Day', 'type'], right_on = ['Day', 'type'] )
    plot_rev = plot_rev.groupby(['Day','type']).sum().reset_index()

    plot_rev['Day'] = pd.to_datetime(plot_rev['Day'], format ='%Y-%m-%d')
    plot_rev['Cost'] = plot_rev['Cost'] / 1000000
    plot_rev['ROAS'] = plot_rev['af_purchase (Sales in CAD)'] / plot_rev['Cost']
    plot_rev['Total installs'] = plot_rev['Installs'] + plot_rev['installs']
  
    ## Budget sheet (just end date totals)
    print(plot_rev)
    uac_campaigns_day = plot_rev[(plot_rev['Day'] >= (end_date_21 - timedelta(days= 45))) & (plot_rev['type'] == 'UAC')].groupby('Day').sum().reset_index()

    nb_campaigns_day = plot_rev[(plot_rev['Day'] >= (end_date_21 - timedelta(days= 45))) & (plot_rev['type'] == 'Non-Branded')].groupby('Day').sum().reset_index()

    b_campaigns_day = plot_rev[(plot_rev['Day'] >= (end_date_21 - timedelta(days= 45))) & (plot_rev['type'] == 'Branded')].groupby('Day').sum().reset_index()
    
    
    if len(uac_campaigns_day.columns) > 0:
        uac_campaigns_day['Network'] = 'Google UAC'
        uac_totals = uac_campaigns_day[['Day','Network', 'Conversions', 'Installs', 'installs', 'Cost', 'Total Cost', 'skad_revenue', 'Total conv. value', 'af_purchase (Sales in CAD)', 'totalRevenue']]
        #uac_totals = pd.DataFrame({'Date': end_date_.strftime('%Y-%m-%d'), 'Network': 'Google UAC', 'Installs': uac_campaigns_day['Conversions'].sum(), 'Installs AF': uac_campaigns_day['Installs'].sum() , 'Installs Skan': uac_campaigns_day['installs'].sum(), 'Cost': uac_campaigns_day['Cost'].sum(), 'Cost AF': uac_campaigns_day['Total Cost'].sum(), 'Revenue Skan' : uac_campaigns_day['skad_revenue'].sum(), 'Revenue' : uac_campaigns_day['Total conv. value'].sum(), 'Revenue AF' : uac_campaigns_day['af_purchase (Sales in CAD)'].sum()}, index = range(0,1))
    #else:
    #    uac_totals = pd.DataFrame({'Date': end_date_.strftime('%Y-%m-%d'), 'Network': 'Google UAC', 'Installs': 0, 'Installs AF': 0, 'Installs Skan': 0, 'Cost': 0, 'Cost AF': 0, 'Revenue Skan': 0, 'Revenue': 0, 'Revenue AF': 0}, index = range(0,1))
    if len(nb_campaigns_day.columns) > 0:
        nb_campaigns_day['Network'] = 'Google Search (Non-Branded)'
        nb_totals = nb_campaigns_day[['Day','Network', 'Conversions', 'Installs', 'installs', 'Cost', 'Total Cost', 'skad_revenue', 'Total conv. value', 'af_purchase (Sales in CAD)', 'totalRevenue']]
        #nb_totals = pd.DataFrame({'Date': end_date_.strftime('%Y-%m-%d'), 'Network': 'Google Search (Branded)', 'Installs': nb_campaigns_day['Conversions'].sum(), 'Installs AF': nb_campaigns_day['Installs'].sum() , 'Installs Skan': nb_campaigns_day['installs'].sum(), 'Cost': nb_campaigns_day['Cost'].sum(), 'Cost AF': nb_campaigns_day['Total Cost'].sum(), 'Revenue Skan' : nb_campaigns_day['skad_revenue'].sum(),'Revenue' : nb_campaigns_day['Total conv. value'].sum(), 'Revenue AF' : nb_campaigns_day['af_purchase (Sales in CAD)'].sum()}, index = range(0,1))
    #else:
    #    nb_totals = pd.DataFrame({'Date': end_date_.strftime('%Y-%m-%d'), 'Network': 'Google Search (Branded)', 'Installs': 0, 'Installs AF': 0, 'Installs Skan': 0, 'Cost': 0, 'Cost AF': 0, 'Revenue Skan': 0, 'Revenue': 0, 'Revenue AF': 0}, index = range(0,1))
    if len(b_campaigns_day.columns) > 0:
        b_campaigns_day['Network'] = 'Google Search (Branded)'
        branded_totals = b_campaigns_day[['Day','Network', 'Conversions', 'Installs', 'installs', 'Cost', 'Total Cost', 'skad_revenue', 'Total conv. value', 'af_purchase (Sales in CAD)', 'totalRevenue']]
        #branded_totals = pd.DataFrame({'Date': end_date_.strftime('%Y-%m-%d'), 'Network': 'Google Search (Non-Branded)', 'Installs': b_campaigns_day['Conversions'].sum(), 'Installs AF': b_campaigns_day['Installs'].sum() , 'Installs Skan': b_campaigns_day['installs'].sum(), 'Cost': b_campaigns_day['Cost'].sum(), 'Cost AF': b_campaigns_day['Total Cost'].sum(), 'Revenue Skan' : b_campaigns_day['skad_revenue'].sum(), 'Revenue' : b_campaigns_day['Total conv. value'].sum(), 'Revenue AF' : b_campaigns_day['af_purchase (Sales in CAD)'].sum()}, index = range(0,1))
    #else:
    #    branded_totals = pd.DataFrame({'Date': end_date_.strftime('%Y-%m-%d'), 'Network': 'Google Search (Non-Branded)', 'Installs': 0, 'Installs AF': 0, 'Installs Skan': 0, 'Cost': 0, 'Cost AF': 0, 'Revenue Skan': 0, 'Revenue': 0, 'Revenue AF': 0}, index = range(0,1))

    

    upload = pd.concat([uac_totals,branded_totals, nb_totals], axis =0)
    upload.sort_values('Day', inplace = True)
    #upload['Cost'] = upload['Cost'] / 1000000
    upload['ROAS'] = upload['af_purchase (Sales in CAD)'] / upload['Cost']
    upload['Day'] = upload['Day'].apply(lambda x: x.strftime("%Y-%m-%d"))
    print(upload)
    print('ok')
    sheet_name = 'Daily_overview_2021'
    #drive_g(upload, sheet_name, credentials)

    
    unified_19 = pd.concat([uac_campaigns_19, nb_campaigns_19, b_campaigns_19], axis = 0)    
    #unified_19 = df_19.copy()

    unified_19['Day'] = pd.to_datetime(unified_19['Day'], format ='%Y-%m-%d')
    unified_19['Cost'] = unified_19['Cost'] / 1000000
    unified_19['ROAS'] = unified_19['Total conv. value'] / unified_19['Cost']
    unified_19[['Day','type','Conversions','Cost','Total conv. value', 'ROAS']].to_csv('upload_Adwords.csv')
    unified_19['Day'] = unified_19['Day'].apply(lambda x: x.strftime('%Y-%m-%d'))

    

    uac_plot_19 = unified_19.groupby('Day').sum().reset_index()
    uac_plot_19['avgCPC'] = uac_plot_19['Cost'] / uac_plot_19['Conversions']
    uac_plot_19['TTR'] = uac_plot_19['Clicks'] / uac_plot_19['Impressions']
    uac_plot_19['convRate'] = uac_plot_19['Conversions'] / uac_plot_19['Clicks']
    uac_plot_19['ROAS'] = uac_plot_19['Total conv. value'] / uac_plot_19['Cost']


    uac_plot = plot_rev.groupby('Day').sum().reset_index()
    uac_plot['avgCPC'] = uac_plot['Cost'] / (uac_plot['Installs'] + uac_plot['installs'])
    uac_plot['TTR'] = uac_plot['Clicks'] / uac_plot['Impressions']
    uac_plot['convRate'] = (uac_plot['Installs'] + uac_plot['installs']) / uac_plot['Clicks']
    #uac_plot['ROAS'] = uac_plot['Total conv. value'] / uac_plot['Cost']
    #print(uac_plot)

    uac_plot_uni = pd.concat([uac_plot_19, uac_plot])
    uac_plot_uni['Year'] = uac_plot_uni['Day'].apply(lambda x: str(x)[:4])
    uac_plot_uni['Day'] = pd.to_datetime(uac_plot_uni['Day'], format='%Y-%m-%d')
    uac_plot_uni = uac_plot_uni.groupby(['Day','Year']).sum().reset_index().sort_values('Day', ascending = True)
    uac_plot_uni['Day'] = uac_plot_uni['Day'].apply(lambda x: x.strftime('%b-%d'))
    


    df_geo = get_geo_performance(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date_21, end_date_21)
    end_date = (datetime.now() - timedelta(days= 350))
    #print(df_geo.columns)
    df_geo_19 = get_geo_performance(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date, end_date)
    print(df_geo_19)
    #df_geo = df_geo[df_geo['Campaign state'] == 'enabled']
    locations = list(df_geo[df_geo['Location'] != ' --']['Location'].unique())
    locations_19 = list(df_geo_19[df_geo_19['Location'] != ' --']['Location'].unique())
    print(locations_19)
    loc_details = get_location(client_id, client_secret, refresh_token, developer_token, client_customer_id, locations)
    loc_details_19 = get_location(client_id, client_secret, refresh_token, developer_token, client_customer_id, locations_19)
    dict_loc = {}
    dict_loc_19 = {}
    for location in loc_details:
        dict_loc[str(location['location']['id'])] = location['location']['locationName']
    for location in loc_details_19:
        dict_loc_19[str(location['location']['id'])] = location['location']['locationName']

    df_geo['Cost'] = df_geo['Cost'] / 1000000
    df_geo['locationName'] = df_geo['Location'].astype('str').map(dict_loc) 
    df_geo['ROAS'] = df_geo['Total conv. value'].astype('float') / df_geo['Cost'].astype('float')
    df_geo['ARPU'] = df_geo['Total conv. value'].astype('float') / df_geo['Conversions'].astype('float')
    df_geo['locationName'] = df_geo['locationName'].fillna('Other')

    df_geo_19['Cost'] = df_geo_19['Cost'] / 1000000
    df_geo_19['locationName'] = df_geo_19['Location'].astype('str').map(dict_loc_19) 
    df_geo_19['ROAS'] = df_geo_19['Total conv. value'].astype('float') / df_geo_19['Cost'].astype('float')
    df_geo_19['ARPU'] = df_geo_19['Total conv. value'].astype('float') / df_geo_19['Conversions'].astype('float')
    df_geo_19['locationName'] = df_geo_19['locationName'].fillna('Other')

    
    ### Per campaign/country

    #uac
    indx = [i for i in df_geo.index if 'UAC' in df_geo.loc[i, 'Campaign'] and 'NB' not in df_geo.loc[i, 'Campaign'] and 'BRANDED' not in df_geo.loc[i, 'Campaign']]
    df_geo_camp_uac = df_geo.loc[indx, :]

    indx = [i for i in df_geo_19.index if 'UAC' in df_geo_19.loc[i, 'Campaign'] and 'NB' not in df_geo_19.loc[i, 'Campaign'] and 'BRANDED' not in df_geo_19.loc[i, 'Campaign']]
    df_geo_camp_uac_19 = df_geo_19.loc[indx,:]

    #nb
    indx = [i for i in df_geo.index if 'NB' in df_geo.loc[i, 'Campaign'] and 'UAC' not in df_geo.loc[i, 'Campaign'] and 'BRANDED' not in df_geo.loc[i, 'Campaign']]
    df_geo_camp_nb = df_geo.loc[indx, :]

    indx = [i for i in df_geo_19.index if 'NB' in df_geo_19.loc[i, 'Campaign'] and 'UAC' not in df_geo_19.loc[i, 'Campaign'] and 'BRANDED' not in df_geo_19.loc[i, 'Campaign']]
    df_geo_camp_nb_19 = df_geo_19.loc[indx,:]

    #b
    indx = [i for i in df_geo.index if 'BRANDED' in df_geo.loc[i, 'Campaign'] and 'NB' not in df_geo.loc[i, 'Campaign'] and 'UAC' not in df_geo.loc[i, 'Campaign']]
    df_geo_camp_b = df_geo.loc[indx, :]
    
    indx = [i for i in df_geo_19.index if 'BRANDED' in df_geo_19.loc[i, 'Campaign'] and 'NB' not in df_geo_19.loc[i, 'Campaign'] and 'UAC' not in df_geo_19.loc[i, 'Campaign']]
    df_geo_camp_b_19 = df_geo_19.loc[indx,:]

    #uac merged campaigns 20 and 19
    df_geo_camp_uac['type'] = 'UAC'
    df_geo_camp_nb['type'] = 'Non-Branded'
    df_geo_camp_b['type'] = 'Branded'
    df_geo_camp_uac_19['type'] = 'UAC'
    df_geo_camp_nb_19['type'] = 'Non-Branded'
    df_geo_camp_b_19['type'] = 'Branded'

    geo_camp_uni = pd.concat([df_geo_camp_uac, df_geo_camp_nb, df_geo_camp_b], axis = 0)
    #geo_camp_uni = df_geo.copy()
    geo_camp_uni_19 = pd.concat([df_geo_camp_uac_19, df_geo_camp_nb_19, df_geo_camp_b_19], axis = 0)
    #geo_camp_uni_19 = df_geo_19.copy()

    #print(geo_camp_uni['locationName'].unique())
    dic_country = {'AU' :'Australia', 'CA': 'Canada', 'UK': 'United Kingdom', 'IT': 'Italy', 'FR': 'France', 'US': 'United States',
                    'AR': 'Argentina', 'MX': 'Mexico', 'BE':'Belgium', 'ES':'Spain', 'ZA':'South Africa', 'NZ': 'New Zealand', 'CH':'Switzerland', 'IE':'Ireland'}
    df_level['Country'] = df_level['Country'].map(dic_country)
    df_subs = df_level.groupby(['Date','type', 'Country']).sum().reset_index()

    geo_report_ = geo_camp_uni.groupby(['Day','type', 'locationName']).sum().reset_index()
    #geo_report_ = geo_camp_uni.groupby(['Day', 'locationName']).sum().reset_index()

    geo_report19 = geo_camp_uni_19.groupby(['Day', 'type', 'locationName']).sum().reset_index()
    
    geo_report = pd.merge(geo_report_, df_subs, how = 'left', left_on= ['Day', 'type', 'locationName'], right_on= ['Date', 'type', 'Country'])
    #geo_report['Total conv. value'] = geo_report['Total conv. value'].astype('float') + geo_report['af_subscribe (Sales in CAD)'].astype('float')

    geo_camp_total = pd.concat([geo_report, geo_report19], axis = 0)
    geo_camp_total['Year'] = geo_camp_total['Day'].apply(lambda x: str(x)[:4])
    geo_camp_total['Day'] = pd.to_datetime(geo_camp_total['Day'], format='%Y-%m-%d')

    geo_camp_fig = pd.concat([geo_camp_uni.groupby(['Day','type', 'locationName', 'Campaign']).sum().reset_index(), geo_camp_uni_19.groupby(['Day', 'type', 'locationName', 'Campaign']).sum().reset_index()], axis = 0)
    geo_camp_fig['Year'] = geo_camp_fig['Day'].apply(lambda x: str(x)[:4])
    geo_camp_fig['Day'] = pd.to_datetime(geo_camp_fig['Day'], format='%Y-%m-%d')

    geo_camp_total = geo_camp_total[geo_camp_total['locationName'] != 'Other']
    geo_camp_total = geo_camp_total.groupby(['Day', 'locationName','type', 'Year']).sum().reset_index().sort_values('Day', ascending = True)
    #geo_camp_total = geo_camp_total.groupby(['Day', 'locationName', 'Year']).sum().reset_index().sort_values('Day', ascending = True)
    #geo_camp_total['Day'] = geo_camp_total['Day'].apply(lambda x: x.strftime('%b-%d'))
    
    
    figs_pnp = []
    
    fig = make_subplots( rows=1, cols=2, column_widths=[0.5, 0.5], specs=[[{'secondary_y':True}, {'secondary_y':True}]],
                    subplot_titles=("Daily Adwords Conversions vs. CPC", "Daily Adwords Revenue KPIs" ))

    # Add traces

    fig.add_trace(go.Scatter(x=uac_plot.Day, y=uac_plot['Cost'],
                    mode='lines+markers',
                    name='Cost', marker_color = '#109618'), row =1 , col = 2)
    fig.add_trace(go.Scatter(x=uac_plot.Day, y=uac_plot.avgCPC, name = 'CPC', marker_color = '#EF553B'), secondary_y = True, row=1, col=1)
    fig.add_trace(go.Bar(x=plot_rev.groupby('Day').sum().index, y=plot_rev.groupby('Day').sum()['af_purchase (Sales in CAD)'], marker_color = '#FEAF16', name = 'Conv. Value'),  row=1, col=2)

    #fig.add_trace(go.Scatter(x=uac_plot_uni[uac_plot_uni['Year'] == '2020']['Day'], y=uac_plot_uni[uac_plot_uni['Year'] == '2020']['Total conv. value'] / uac_plot_uni[uac_plot_uni['Year'] == '2020']['Cost'],
    #                mode='lines+markers',
    #                name='Daily ROAS-2020', marker_color = '#511CFB'), secondary_y = True, row =1 , col = 2)

    fig.add_trace(go.Bar(x=uac_plot.Day, y=plot_rev.groupby(['Day','type']).sum()['Total installs'].loc[slice(None), 'UAC'],
                    name='UAC', marker_color = 'rgb(204,204,204)'), row=1, col=1)
    #fig.add_trace(go.Scatter(x=uac_plot_uni[uac_plot_uni['Year'] == '2020']['Day'], y=uac_plot_uni[uac_plot_uni['Year'] == '2020']['Conversions'],
    #                name='Conversions-2020', marker_color = '#EF553B'), row=1, col=1)
    #fig.add_trace(go.Scatter(x = np.array([uac_plot_uni[uac_plot_uni['Year'] == '2020'].set_index('Day').index[0], uac_plot_uni[uac_plot_uni['Year'] == '2020'].set_index('Day').index[-1]]), y = np.array([(uac_plot_uni[uac_plot_uni['Year'] == '2020']['Conversions'].sum()/71), (uac_plot_uni[uac_plot_uni['Year'] == '2020']['Conversions'].sum()/71)]), marker_color = 'cyan', name = 'Avg.', mode="lines+text", text=['Conv-20', '+115%']), row =1, col = 1)


    fig.add_trace(go.Bar(x=uac_plot.Day, y=plot_rev.groupby(['Day','type']).sum()['Total installs'].loc[slice(None), 'Non-Branded'],
                    name='Non-Branded', marker_color = '#FF6692'), row=1, col=1)
    fig.add_trace(go.Bar(x=uac_plot.Day, y=plot_rev.groupby(['Day','type']).sum()['Total installs'].loc[slice(None), 'Branded'],
                    name='Branded', marker_color = '#AB63FA'), row=1, col=1)
    
    #fig.add_trace(go.Scatter(x = np.array([uac_plot_uni[uac_plot_uni['Year'] == '2020'].set_index('Day').index[0], uac_plot_uni[uac_plot_uni['Year'] == '2020'].set_index('Day').index[-1]]), y = np.array([(uac_plot_uni[uac_plot_uni['Year'] == '2020']['Total conv. value'].sum()/71), (uac_plot_uni[uac_plot_uni['Year'] == '2020']['Total conv. value'].sum()/71)]), marker_color = 'cyan', showlegend = False, mode="lines+text", text=['Rev-20', '+33%']), row =1, col = 2)

    fig.add_trace(go.Bar(x=plot_rev.groupby('Day').sum().index, y=plot_rev.groupby(['Day','type']).sum()['af_purchase (Sales in CAD)'].loc[slice(None), 'UAC'], marker_color = 'rgb(204,204,204)', name = 'UAC-Rev', showlegend = False),  row=1, col=2)
    fig.add_trace(go.Bar(x=plot_rev.groupby('Day').sum().index, y=plot_rev.groupby(['Day','type']).sum()['af_purchase (Sales in CAD)'].loc[slice(None), 'Non-Branded'], marker_color = '#FF6692', name = 'Non-Branded-Rev', showlegend = False),  row=1, col=2)
    fig.add_trace(go.Bar(x=plot_rev.groupby('Day').sum().index, y=plot_rev.groupby(['Day','type']).sum()['af_purchase (Sales in CAD)'].loc[slice(None), 'Branded'], marker_color = '#AB63FA', name = 'Branded-Rev', showlegend = False),  row=1, col=2)
    
    fig.add_trace(go.Scatter(x=plot_rev.groupby('Day').sum().index, y=plot_rev.groupby('Day').sum()['af_purchase (Sales in CAD)'],
                    mode='lines+markers',
                    name='Revenue', marker_color = '#FEAF16'), row =1 , col = 2)
    
    #fig.update_layout(barmode = 'stack', height = 600, title_text = 'RESULTS (AGN Effect)')


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
                    #name='Conversions-2019', marker_color = 'rgb(204,204,204)'), row=1, col=1)
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
    
    fig.update_layout(barmode = 'stack', height = 600, title_text = 'Adwords KPIs Overview')

    fig.update_yaxes(tickvals=[0, 50000, 100000], secondary_y=False, row = 1, col = 2)
    
    fig.update_yaxes(tickvals=[0, 2, 4, 6, 8], secondary_y=True, row =1, col =2)

    figs_pnp.append(fig)

    #print((uac_plot_19.groupby(['Day']).sum()['Total conv. value'].sum()/71))
    ##print((uac_plot_19.groupby(['Day']).sum()['Conversions'].sum()/71))
    #print((plot_rev.groupby('Day').sum()['Total conv. value'].sum()/71))
    #print((uac_plot.groupby('Day').sum()['Conversions'].sum()/71))

    #temp = geo_camp_total[geo_camp_total['Year'] == '2021'].reset_index()
    #parce = geo_camp_total[geo_camp_total['Year'] == '2021'].groupby('locationName').sum().reset_index().sort_values('Conversions', ascending= False).head(10)['locationName'].values
    #idx = [i for i in temp.index if temp.loc[i,'locationName'] in parce]
    #temp = temp.loc[idx, :]
    #fig_camp_ = px.scatter(temp, x='Day', y='Conversions', color='type',
    #           facet_col='locationName', facet_col_wrap=2).update_traces(mode='lines+markers')
    #fig_camp_.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    #fig_camp_.update_yaxes(matches=None, showticklabels=True, title_text='')
    ##fig_camp_.update_xaxes(matches='x')
    ##fig_camp_.update_layout(
     #   title_text="Daily Conversions per Country", height = 950)
    #figs_pnp.append(fig_camp_)
    
    temp = geo_camp_total.reset_index()
    parce = geo_camp_total.groupby('locationName').sum().reset_index().sort_values('Conversions', ascending= False).head(10)['locationName'].values
    idx = [i for i in temp.index if temp.loc[i,'locationName'] in parce]
    temp['Day'] = temp['Day'].apply(lambda x: x.strftime('%b-%d'))
    temp = temp.loc[idx, :].groupby(['Day','Year', 'locationName']).sum().reset_index()
    temp['Day'] = temp['Day'].apply(lambda x: datetime.strptime(x, '%b-%d'))
    temp = temp.sort_values('Day', ascending = True).reset_index()
    temp['Day'] = temp['Day'].apply(lambda x: x.strftime('%b-%d'))
    print(temp)
    fig_camp_ = px.scatter(temp, x='Day', y='Conversions', color='Year',
               facet_col='locationName', facet_col_wrap=2).update_traces(mode='lines+markers')
    fig_camp_.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig_camp_.update_yaxes(matches=None, showticklabels=True, title_text='')
    fig_camp_.update_xaxes(matches='x')
    fig_camp_.update_layout(
        title_text="Daily Conversions per Country", height = 950)
    
    figs_pnp.append(fig_camp_)
    #cut = geo_camp_total[geo_camp_total['type'] == 'UAC'][['Day', 'Total conv. value', 'Year', 'Cost','locationName', 'Conversions']]
    cut = geo_camp_total[['Day', 'Total conv. value', 'Year', 'Cost','locationName', 'Conversions']]

    cut = cut.groupby(['Day','locationName','Year']).sum().reset_index()
    cut['ROAS'] = cut['Total conv. value'] / cut['Cost']
    #cut['Day'] = pd.to_datetime(cut['Day'], format = '%b-%d')
    #cut['Day'] = cut['Day'].mask(cut['Day'].dt.year == 1900, 
                             #cut['Day'] + pd.offsets.DateOffset(year=2020))
    #& (cut['Day'] <= (datetime.now() - timedelta(days= 4)))
    #cut = cut[(cut['Day'] > (datetime.now() - timedelta(days= 93)))]
    cut.sort_values('Day', inplace = True)
    cut['Day'] = cut['Day'].apply(lambda x: x.strftime('%b-%d'))
    
    #fig_case = make_subplots( rows=1, cols=1, specs=[[{'secondary_y':True}]])

    # Add traces

    #fig_case.add_trace(go.Bar(x=cut[cut['Year'] == '2019']['Day'], y=cut[cut['Year'] == '2019']['Cost'], name = 'Cost-19', marker_color = '#FC6955'), row=1, col=1)
    #fig_case.add_trace(go.Bar(x=cut[cut['Year'] == '2020']['Day'], y=cut[cut['Year'] == '2020']['Cost'],
     #               name='Cost-20', marker_color = '#F6222E'), row =1 , col = 1)
    #fig_case.add_trace(go.Scatter(x=cut[cut['Year'] == '2019']['Day'], y=cut[cut['Year'] == '2019']['ROAS'], name = 'ROAS-19', marker_color = '#FEAF16'), secondary_y = True, row=1, col=1)
    #fig_case.add_trace(go.Scatter(x=cut[cut['Year'] == '2020']['Day'], y=cut[cut['Year'] == '2020']['ROAS'], name = 'ROAS-20', marker_color = '#17BECF'), secondary_y = True, row=1, col=1)
    #fig_case.update_layout(title_text = 'Daily ROAS 2020 vs 2019')

    idx = [ i for i in cut.index if cut.loc[i,'locationName'] in ['United States', 'Mexico', 'Italy','Australia']]
    cut = cut.loc[idx,:]

    #fig_camp = px.scatter(cut, x='Day', y='Total conv. value', color='Year', facet_col= 'locationName', facet_col_wrap= 2, color_discrete_map={"2020": 'red', '2019':'orange'}).update_traces(mode='lines+markers')
    #fig_camp.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    #fig_camp.update_yaxes(matches=None,title_text='',showticklabels=False,range=[0, 20000], row = 1, col = 1)
    #fig_camp.update_yaxes(matches=None,range=[0, 6000], row = 2, col = 2)
    #fig_camp.update_yaxes(matches=None,range=[0, 6000], row = 1, col = 2)




    #fig_camp.update_xaxes(matches='x', nticks=13)
    #fig_camp.update_layout(
       # title_text="Daily Revenue UAC Campaigns (size = Conversions)", height = 1200)
    
    #fig_camp.update_layout(
    #    title_text="Our Client 2020 Revenue in Primary Countries", height = 800)

    
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
    df_geo['Day'] = pd.to_datetime(df_geo['Day'])
    df_geo_last = df_geo[df_geo['Day'] >= (datetime.now() - timedelta(days= 266))]
    df_geo_last['Total conv. value'] = df_geo_last['Total conv. value'].astype('float')
    df_geo_last = df_geo_last.groupby('locationName').sum().reset_index()
    df_geo_last['ROAS_last'] =  df_geo_last['Total conv. value'] / df_geo_last['Cost']
    df_geo_merge = df_geo_last.loc[:, ['locationName', 'ROAS_last']]

    df_geo_loc = df_geo.groupby('locationName').sum().reset_index()
    df_geo_fig= pd.merge(df_geo_loc, df_geo_merge, how = 'left', on = 'locationName')
    df_geo_fig['ROAS'] = df_geo_fig['Total conv. value'].astype('float') / df_geo_fig['Cost'].astype('float')
    df_geo_fig['ARPU'] = df_geo_fig['Total conv. value'].astype('float') / df_geo_fig['Conversions'].astype('float')
    df_geo_fig['+/- 5 days'] = df_geo_fig['ROAS'].astype('float') - df_geo_fig['ROAS_last']
    df_geo_fig['+/- 5 days'] = df_geo_fig['+/- 5 days'].apply(lambda x : '+' + str(np.round(x, 1)) if x > 0 else str(np.round(x, 1)))
    df_geo_fig.sort_values('ROAS', ascending = False, inplace = True)

    trace = go.Table(header=dict(values=['Country', 'Conversions', 'Cost', 'Revenue', 'ARPU', 'ROAS', '+/- 5 days (ROAS)']),
                 cells=dict(values=[df_geo_fig.locationName.values, df_geo_fig.Conversions.values, np.round(df_geo_fig.Cost.values, 0), np.round(df_geo_fig['Total conv. value'].values, 0), np.round(df_geo_fig.ARPU.values, 1), np.round(df_geo_fig.ROAS.values, 1), df_geo_fig['+/- 5 days']]), domain=dict(x=[0.52, 1],y=[0, 1]))

    trace1 = go.Pie(values=df_geo_fig.Conversions, labels=df_geo_fig.locationName, hole=.4, name = 'Conversions', domain=dict(x=[0, 0.23],y=[0, 1]), title_text = 'Conversions', textposition='inside', textinfo='label', hoverinfo="label+value")   
    trace2 = go.Pie(values=df_geo_fig.Cost, labels=df_geo_fig.locationName, hole=.4, name = 'Cost', domain=dict(x=[0.26, 0.49],y=[0, 1]), title_text = 'Cost', textposition='inside', textinfo='label', hoverinfo="label+value")

    fig_dough = go.Figure(data = [trace,trace1, trace2])
    fig_dough.update_layout(title_text="Performance Breakdown by Country")

    figs_pnp.append(fig_dough)

    df_geo = geo_camp_fig.groupby(['Campaign','type','Year']).sum().reset_index()
    df_geo['ROAS'] = df_geo['Total conv. value'] / df_geo['Cost']
    df_geo['ARPU'] = df_geo['Total conv. value'] / df_geo['Conversions']
    #print(df_geo)
    
    df_subs = df_subs.groupby(['Date', 'type']).sum().reset_index()
    
    fig_bar = make_subplots( rows=1, cols=2, column_widths=[0.5, 0.5],
                    subplot_titles=("Subscriptions UAC", "Subscriptions Search" ))

    fig_bar.add_trace(go.Scatter(x=df_subs.groupby('Date').sum().index, y = df_subs[df_subs['type'] == 'UAC']['af_subscribe (Sales in CAD)'], mode='lines+markers', name = 'UAC'),1,1)
    fig_bar.add_trace(go.Scatter(x=df_subs.groupby('Date').sum().index, y = df_subs[df_subs['type'] == 'Branded']['af_subscribe (Sales in CAD)'], mode='lines+markers', name = 'Branded'),1,2)
    fig_bar.add_trace(go.Scatter(x=df_subs.groupby('Date').sum().index, y = df_subs[df_subs['type'] == 'Non-Branded']['af_subscribe (Sales in CAD)'], mode='lines+markers', name = 'Non-Branded'),1,2)

    figs_pnp.append(fig_bar)
    #report = pd.DataFrame({'Date': report.Day, 'Network': report.type, 'Installs': report.Conversions , 'Cost': report.Cost, 'Revenue' : (report['Total conv. value'] + report['af_subscribe (Sales in CAD)'])})

    #report.to_csv('adwordssanta.csv')

    #uni_tab = unified.groupby('Day').sum().reset_index()
    #fig_tab = go.Figure()
    #fig_tab.add_trace(go.Table(header=dict(values=['Day','convRate', 'UAC', 'NB', 'BRANDED']),
    #             cells=dict(values=[uni_tab.Day.values, np.round(unified[unified['type'] == 'UAC']['Conversions'].values / unified[unified['type'] == 'UAC']['Clicks'].values, 2), 
    #             np.round(unified[unified['type'] == 'Non-Branded']['Conversions'].values / unified[unified['type'] == 'Non-Branded']['Clicks'].values, 2),
    #             np.round(unified[unified['type'] == 'Branded']['Conversions'].values / unified[unified['type'] == 'Branded']['Clicks'].values, 2)])))

    #figs_pnp.append(fig_tab)
    #New Script Budget
    day = 4
    budgets = pd.DataFrame()
    while day >= 0:
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
    print(budgets)

    day = 5
    def fbudgets(days, df):
        values = pd.DataFrame()
        totals = pd.DataFrame()
        while days >=1:
            print(days)
            temp = (df[df['Day'] == (datetime.now() - timedelta(days= 5 - days)).strftime('%b-%d')]['Cost'].values / df[df['Day'] == (datetime.now() - timedelta(days= 5 - days)).strftime('%b-%d')]['Budget']) * 100
            df_1 = pd.DataFrame(pd.concat([temp,df[df['Day'] == (datetime.now() - timedelta(days= 5 - days)).strftime('%b-%d')]['Budget Name'], df[df['Day'] == (datetime.now() - timedelta(days= 5 - days)).strftime('%b-%d')]['ROAS']], axis = 1))
            df_2 = pd.DataFrame(pd.concat([df[df['Day'] == (datetime.now() - timedelta(days= 5 - days)).strftime('%b-%d')]['Budget'], df[df['Day'] == (datetime.now() - timedelta(days= 5 - days)).strftime('%b-%d')]['Budget Name']], axis = 1))
            if days == 5:
                values = pd.concat([values, df_1], axis = 0)
                #print(values)
                totals = pd.concat([totals, df_2], axis = 0)
            else:
                values = pd.merge(values,df_1, left_on = 'Budget Name', right_on = 'Budget Name', how = 'outer')
                totals = pd.merge(totals, df_2 , left_on = 'Budget Name', right_on = 'Budget Name', how = 'outer')
            days -= 1
        print(values)
        return values, totals

    bvalues, btotals = fbudgets(day, budgets)
    print(bvalues)
    #print(btotals.info())
    bvalues.columns = ['Budget', 'Name', 'ROAS', 'Budget_yes','ROAS_yes', 'Budget_2', 'ROAS_2','Budget_3', 'ROAS_3', 'Budget_4', 'ROAS_4']
                            #'Budget_5', 'ROAS_5', 'Budget_6', 'ROAS_6','Budget_7', 'ROAS_7',
                           #'Budget_8', 'ROAS_8', 'Budget_9', 'ROAS_9', 'Budget_10', 'ROAS_10', 'Budget_11','ROAS_11','Budget_12', 'ROAS_12','Budget_13', 'ROAS_13','Budget_14','ROAS_14']
    bvalues.fillna(0, inplace = True)
    btotals.columns = ['Budget_T', 'Name', 'Budget_yes_T', 'Budget_2_T', 'Budget_3_T','Budget_4_T'] 
                        #'Budget_5_T', 'Budget_6_T', 'Budget_7_T', 'Budget_8_T', 'Budget_9_T', 'Budget_10_T', 'Budget_11_T', 'Budget_12_T', 'Budget_13_T','Budget_14_T']
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
        

    favg(bvalues, 0, 5, 'Average_current')
    #favg(bvalues, 7, 15, 'Average_past')
    favg(btotals, 0, 5, 'Average_current_T')
    #favg(btotals, 7, 15, 'Average_past_T')


    #print(total_avg)

    colors = n_colors('rgb(102, 166, 30)', 'rgb(230, 245, 201)', 9, colortype='rgb')
    bvalues = pd.merge(bvalues, btotals, how = 'left', on = 'Name')
    bvalues.sort_values('Budget', inplace = True, ascending = False)


    tab = go.Figure()
    tab.add_trace(go.Table(header=dict(values=['Budget Name','Today (%)', 'Total B.', 'ROAS','Yestr (%)', 'ROAS', 'Avg week (%)', 'Total_B_Avg']),
                 cells=dict(values=[bvalues['Name'].values, np.round(bvalues['Budget'],1),  np.round(bvalues['Budget_T'], 1) , np.round(bvalues['ROAS'],1), np.round(bvalues['Budget_yes'], 1) , np.round(bvalues['ROAS_yes'],1), np.round(bvalues['Average_current'],1), np.round(bvalues['Average_current_T'], 1) ],
                  fill=dict(color=['rgb(245, 245, 245)',#unique color for the first column
                                            ['rgba(166, 216, 84, 0.8)' if val >= 1 else 'rgba(251, 180, 174, 0.8)' for val in np.round(bvalues['ROAS'],1)] ]))))
    tab.update_layout(height = 400, title_text = "Budget Stats Current Week (Green Rows above 1 Today's ROAS)")
    
    figs_pnp.append(tab)

    #tab_past = go.Figure()
    #tab_past.add_trace(go.Table(header=dict(values=['Budget Name', 'Day 14 (%)', 'Total','ROAS', 'Day 13 (%)', 'Total','ROAS', 'Day 12 (%)', 'Total', 'ROAS', 'Day 11 (%)', 'Total', 'ROAS', 'Day 10 (%)', 'Total', 'ROAS', 'Day 9 (%)', 'Total','ROAS', 'Day 8 (%)', 'Total','ROAS', 'Avg week (%)', 'Total_Avg']),
         #        cells=dict(values=[bvalues['Name'].values, np.round(bvalues['Budget_14'],1),  np.round(bvalues['Budget_14_T'], 1) , np.round(bvalues['ROAS_14'], 1), np.round(bvalues['Budget_13'], 1) , np.round(bvalues['Budget_13_T'], 1) , np.round(bvalues['ROAS_13'], 1), np.round(bvalues['Budget_12'], 1), np.round(bvalues['Budget_12_T'], 1), np.round(bvalues['ROAS_12'], 1), np.round(bvalues['Budget_11'], 1) , np.round(bvalues['Budget_11_T'], 1), np.round(bvalues['ROAS_11'], 1), np.round(bvalues['Budget_10'], 1) , np.round(bvalues['Budget_10_T'], 1), np.round(bvalues['ROAS_10'], 1), np.round(bvalues['Budget_9'], 1) , np.round(bvalues['Budget_9_T'], 1), np.round(bvalues['ROAS_9'], 1), np.round(bvalues['Budget_8'], 1) , np.round(bvalues['Budget_8_T'], 1), np.round(bvalues['ROAS_8'], 1), np.round(bvalues['Average_past'],1), np.round(bvalues['Average_past_T'], 1) ])))
    #tab_past.update_layout(title_text = 'Budget Stats Last Week')

    channels['Cost'] = channels['Cost'] / 100000
    #print(channels.columns)
    #ad_bar = channels.groupby('Ad group').sum().reset_index()
    #ad_name = channels.groupby(["Description", "Day"]).sum().reset_index()

    #ad_line = channels.groupby(['Day','Final URL']).sum().reset_index()
    #print(ad_name.columns)
    #urls = ad_name['Description'].unique()
    #print(ad_line)

    #make_subplots(rows = 1, cols =1, subplot_titles= ('Total Impressions/Clicks/Conversions per Ad Group') )
    #fig_url = go.Figure()
    #fig_url.add_trace(go.Bar(y = ad_bar['Ad group'], x = ad_bar['Impressions'], orientation='h', name = 'Impressions'))
    #fig_url.add_trace(go.Bar(y = ad_bar['Ad group'], x = ad_bar['Clicks'], orientation='h', name = 'Clicks'))
    #fig_url.add_trace(go.Bar(y = ad_bar['Ad group'], x = ad_bar['Conversions'], orientation='h', name = 'Conversions'))
    #for url in urls:
    #    fig_url.add_trace(go.Scatter(x = ad_name[ad_name['Description'] == url]['Day'], y = ad_name[ad_name['Description'] == url]['Total conv. value'], name = url), 1,2)
    #fig_url.update_layout(barmode = 'stack', height = 750, title_text = 'Total Impressions/Clicks/Conversions per Ad Group')
    
    #figs_pnp.append(fig_url)
    #legend=dict(orientation="h",yanchor="bottom",y=-0.75,xanchor="right",x=1), legend_title_text='Action'
    #ad_tab = channels.groupby(['Ad group', 'Description']).sum().reset_index()
    #ad_tab = ad_tab[ad_tab['Cost'] > 0]
    #ad_tab["ROAS"] = ad_tab["Total conv. value"] / ad_tab["Cost"]
    #ad_tab["CTR"] = ad_tab["Clicks"] / ad_tab["Impressions"]
    #ad_tab.sort_values('ROAS', ascending = False, inplace = True)
    #tab_ads = go.Figure()
    #tab_ads.add_trace(go.Table(header=dict(values=['Ad group', 'Ad', 'CTR', 'Cost', 'ROAS']),
    #             cells=dict(values=[ad_tab['Ad group'].values, ad_tab['Description'].values, np.round(ad_tab['CTR'].values,1), np.round(ad_tab['Cost'].values,1), np.round(ad_tab['ROAS'].values, 1)])))
    #tab_ads.update_layout(title_text = 'Ads Performance Table')

    #figs_pnp.append(tab_ads)
    geo_report_ = geo_camp_uni.groupby(['Day','Campaign']).sum().reset_index()
    #geo_report_ = geo_camp_uni.groupby(['Day', 'locationName']).sum().reset_index()

    #geo_report19 = geo_camp_uni_19.groupby(['Day', 'type', 'locationName']).sum().reset_index()
    
    geo_report_tab = pd.merge(geo_report_, df_level.groupby(['Date', 'Campaign (c)']).sum().reset_index(), how = 'left', left_on= ['Day', 'Campaign'], right_on= ['Date', 'Campaign (c)'])
    geo_report_tab = geo_report_tab.groupby(['Day', 'Campaign']).sum().reset_index()
    ##MISSING SKAD REVENUE
    geo_report_tab = pd.merge(geo_report_tab, skan.groupby(['date', 'ad_network_campaign_name']).count().reset_index(), how = 'left', left_on =['Day', 'Campaign'], right_on = ['date', 'ad_network_campaign_name'] )
    geo_report_tab = geo_report_tab.rename(columns = {'install_type': 'installs'})
    if 'skad_revenue' not in geo_report_tab.columns:
        geo_report_tab['skad_revenue'] = 0
    geo_report_tab = geo_report_tab.groupby(['Day','Campaign']).sum().reset_index()

    geo_report_tab['Day'] = geo_report_tab['Day'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    geo_report_tab['Day'] = geo_report_tab['Day'].apply(lambda x: x.date())
    #geo_report_tab['Cost'] = geo_report_tab['Cost'] / 1000000
    geo_report_tab['ROAS'] = geo_report_tab['af_purchase (Sales in CAD)'] / geo_report_tab['Cost']

    raw = pd.read_csv('C:\\Users\\User\\Documents\\Python Scripts\\pnp\\data_raw.csv')
    raw = raw[raw['media_source'] == 'googleadwords_int']
    raw['af_purchase'] = raw['event_name'].apply(lambda x: 1 if x == 'af_purchase' else 0)
    dic_country = {"AF":"AFGHANISTAN","AX":"ÅLAND ISLANDS","AL":"ALBANIA","DZ":"ALGERIA","AS":"AMERICAN SAMOA","AD":"ANDORRA","AO":"ANGOLA","AI":"ANGUILLA","AQ":"ANTARCTICA","AG":"ANTIGUA AND BARBUDA","AR":"ARGENTINA","AM":"ARMENIA","AW":"ARUBA","AU":"AUSTRALIA","AT":"AUSTRIA","AZ":"AZERBAIJAN","BS":"BAHAMAS","BH":"BAHRAIN","BD":"BANGLADESH","BB":"BARBADOS","BY":"BELARUS","BE":"BELGIUM","BZ":"BELIZE","BJ":"BENIN","BM":"BERMUDA","BT":"BHUTAN","BO":"BOLIVIA, PLURINATIONAL STATE OF","BQ":"BONAIRE, SINT EUSTATIUS AND SABA","BA":"BOSNIA AND HERZEGOVINA","BW":"BOTSWANA","BV":"BOUVET ISLAND","BR":"BRAZIL","IO":"BRITISH INDIAN OCEAN TERRITORY","BN":"BRUNEI DARUSSALAM","BG":"BULGARIA","BF":"BURKINA FASO","BI":"BURUNDI","KH":"CAMBODIA","CM":"CAMEROON","CA":"CANADA","CV":"CAPE VERDE","KY":"CAYMAN ISLANDS","CF":"CENTRAL AFRICAN REPUBLIC","TD":"CHAD","CL":"CHILE","CN":"CHINA","CX":"CHRISTMAS ISLAND","CC":"COCOS (KEELING) ISLANDS","CO":"COLOMBIA","KM":"COMOROS","CG":"CONGO","CD":"CONGO, THE DEMOCRATIC REPUBLIC OF THE","CK":"COOK ISLANDS","CR":"COSTA RICA","CI":"CÔTE D'IVOIRE","HR":"CROATIA","CU":"CUBA","CW":"CURAÇAO","CY":"CYPRUS","CZ":"CZECH REPUBLIC","DK":"DENMARK","DJ":"DJIBOUTI","DM":"DOMINICA","DO":"DOMINICAN REPUBLIC","EC":"ECUADOR","EG":"EGYPT","SV":"EL SALVADOR","GQ":"EQUATORIAL GUINEA","ER":"ERITREA","EE":"ESTONIA","ET":"ETHIOPIA","FK":"FALKLAND ISLANDS (MALVINAS)","FO":"FAROE ISLANDS","FJ":"FIJI","FI":"FINLAND","FR":"FRANCE","GF":"FRENCH GUIANA","PF":"FRENCH POLYNESIA","TF":"FRENCH SOUTHERN TERRITORIES","GA":"GABON","GM":"GAMBIA","GE":"GEORGIA","DE":"GERMANY","GH":"GHANA","GI":"GIBRALTAR","GR":"GREECE","GL":"GREENLAND","GD":"GRENADA","GP":"GUADELOUPE","GU":"GUAM","GT":"GUATEMALA","GG":"GUERNSEY","GN":"GUINEA","GW":"GUINEA-BISSAU","GY":"GUYANA","HT":"HAITI","HM":"HEARD ISLAND AND MCDONALD ISLANDS","VA":"HOLY SEE (VATICAN CITY STATE)","HN":"HONDURAS","HK":"HONG KONG","HU":"HUNGARY","IS":"ICELAND","IN":"INDIA","ID":"INDONESIA","IR":"IRAN, ISLAMIC REPUBLIC OF","IQ":"IRAQ","IE":"IRELAND","IM":"ISLE OF MAN","IL":"ISRAEL","IT":"ITALY","JM":"JAMAICA","JP":"JAPAN","JE":"JERSEY","JO":"JORDAN","KZ":"KAZAKHSTAN","KE":"KENYA","KI":"KIRIBATI","KP":"KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF","KR":"KOREA, REPUBLIC OF","KW":"KUWAIT","KG":"KYRGYZSTAN","LA":"LAO PEOPLE'S DEMOCRATIC REPUBLIC","LV":"LATVIA","LB":"LEBANON","LS":"LESOTHO","LR":"LIBERIA","LY":"LIBYA","LI":"LIECHTENSTEIN","LT":"LITHUANIA","LU":"LUXEMBOURG","MO":"MACAO","MK":"MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF","MG":"MADAGASCAR","MW":"MALAWI","MY":"MALAYSIA","MV":"MALDIVES","ML":"MALI","MT":"MALTA","MH":"MARSHALL ISLANDS","MQ":"MARTINIQUE","MR":"MAURITANIA","MU":"MAURITIUS","YT":"MAYOTTE","MX":"MEXICO","FM":"MICRONESIA, FEDERATED STATES OF","MD":"MOLDOVA, REPUBLIC OF","MC":"MONACO","MN":"MONGOLIA","ME":"MONTENEGRO","MS":"MONTSERRAT","MA":"MOROCCO","MZ":"MOZAMBIQUE","MM":"MYANMAR","NA":"NAMIBIA","NR":"NAURU","NP":"NEPAL","NL":"NETHERLANDS","NC":"NEW CALEDONIA","NZ":"NEW ZEALAND","NI":"NICARAGUA","NE":"NIGER","NG":"NIGERIA","NU":"NIUE","NF":"NORFOLK ISLAND","MP":"NORTHERN MARIANA ISLANDS","NO":"NORWAY","OM":"OMAN","PK":"PAKISTAN","PW":"PALAU","PS":"PALESTINE, STATE OF","PA":"PANAMA","PG":"PAPUA NEW GUINEA","PY":"PARAGUAY","PE":"PERU","PH":"PHILIPPINES","PN":"PITCAIRN","PL":"POLAND","PT":"PORTUGAL","PR":"PUERTO RICO","QA":"QATAR","RE":"RÉUNION","RO":"ROMANIA","RU":"RUSSIAN FEDERATION","RW":"RWANDA","BL":"SAINT BARTHÉLEMY","SH":"SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA","KN":"SAINT KITTS AND NEVIS","LC":"SAINT LUCIA","MF":"SAINT MARTIN (FRENCH PART)","PM":"SAINT PIERRE AND MIQUELON","VC":"SAINT VINCENT AND THE GRENADINES","WS":"SAMOA","SM":"SAN MARINO","ST":"SAO TOME AND PRINCIPE","SA":"SAUDI ARABIA","SN":"SENEGAL","RS":"SERBIA","SC":"SEYCHELLES","SL":"SIERRA LEONE","SG":"SINGAPORE","SX":"SINT MAARTEN (DUTCH PART)","SK":"SLOVAKIA","SI":"SLOVENIA","SB":"SOLOMON ISLANDS","SO":"SOMALIA","ZA":"SOUTH AFRICA","GS":"SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS","SS":"SOUTH SUDAN","ES":"SPAIN","LK":"SRI LANKA","SD":"SUDAN","SR":"SURINAME","SJ":"SVALBARD AND JAN MAYEN","SZ":"SWAZILAND","SE":"SWEDEN","CH":"SWITZERLAND","SY":"SYRIAN ARAB REPUBLIC","TW":"TAIWAN, PROVINCE OF CHINA","TJ":"TAJIKISTAN","TZ":"TANZANIA, UNITED REPUBLIC OF","TH":"THAILAND","TL":"TIMOR-LESTE","TG":"TOGO","TK":"TOKELAU","TO":"TONGA","TT":"TRINIDAD AND TOBAGO","TN":"TUNISIA","TR":"TURKEY","TM":"TURKMENISTAN","TC":"TURKS AND CAICOS ISLANDS","TV":"TUVALU","UG":"UGANDA","UA":"UKRAINE","AE":"UNITED ARAB EMIRATES","GB":"UNITED KINGDOM","UK":"UNITED KINGDOM","US":"UNITED STATES","USA":"UNITED STATES","UM":"UNITED STATES MINOR OUTLYING ISLANDS","UY":"URUGUAY","UZ":"UZBEKISTAN","VU":"VANUATU","VE":"VENEZUELA, BOLIVARIAN REPUBLIC OF","VN":"VIET NAM","VG":"VIRGIN ISLANDS, BRITISH","VI":"VIRGIN ISLANDS, U.S.","WF":"WALLIS AND FUTUNA","EH":"WESTERN SAHARA","YE":"YEMEN","ZM":"ZAMBIA","ZW":"ZIMBABWE"}
    raw['country_name'] = raw['country_code'].map(dic_country) 
    def capi(x):
        word = ''
        words = x.split(' ')
        for i in words:
            char = i.capitalize() + ' '
            word = word + char
        return word[:-1]
    raw['country_name'] = raw['country_name'].apply(lambda x: capi(x))
    raw['date'] = raw['event_time_selected_timezone'].apply(lambda x: datetime.strptime(x.split('.')[0], '%Y-%m-%d %H:%M:%S'))
    raw['date'] = raw['date'].apply(lambda x: x.date())
    raw_tab = raw.groupby(['date', 'campaign']).sum().reset_index()
    tab_tab = pd.merge(geo_report_tab, raw_tab, how = 'left', left_on = ['Day','Campaign'], right_on= ['date', 'campaign'])

    tab_tab['Day'] = tab_tab['Day'].apply(lambda x: datetime.combine(x, time(0, 0)))
    tab_tab_7 = tab_tab[tab_tab['Day'] >= datetime.now() - timedelta(days = 7)]

    tab_1 = tab_tab.groupby(['campaign']).sum().reset_index()
    tab_1['CPA(login)'] = tab_1['Cost'] / (tab_1['Installs'] + tab_1['installs'])
    tab_1['CPA(buyer)'] = tab_1['Cost'] / (tab_1['af_purchase'])
    tab_1['ROAS'] = tab_1['af_purchase (Sales in CAD)'] / tab_1['Cost']
    tab_1.sort_values('ROAS', ascending = False, inplace = True)
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Campaign', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_1['campaign'].values, tab_1['Installs'].values + tab_1['installs'].values, np.round(tab_1['Cost'].values / (tab_1['Installs'].values + tab_1['installs'].values), 2), np.round(tab_1['af_purchase (Sales in CAD)'].values, 2) , np.round(tab_1['CPA(login)'].values, 2) , np.round(tab_1['CPA(buyer)'].values,2), np.round(tab_1['ROAS'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Campaign Table Breakdown From {} to {}".format(start_date_21, end_date_21))

    figs_pnp.append(figkey_tab)

    tab_1_7 = tab_tab_7.groupby(['campaign']).sum().reset_index()
    tab_1_7['CPA(login)'] = tab_1_7['Cost'] / (tab_1_7['Installs'] + tab_1_7['installs'])
    tab_1_7['CPA(buyer)'] = tab_1_7['Cost'] / (tab_1_7['af_purchase'])
    tab_1_7['ROAS'] = tab_1_7['af_purchase (Sales in CAD)'] / tab_1_7['Cost']
    tab_1_7.sort_values('ROAS', ascending = False, inplace = True)
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Campaign', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_1_7['campaign'].values, tab_1_7['Installs'].values + tab_1_7['installs'].values, np.round(tab_1_7['Cost'].values / (tab_1_7['Installs'].values + tab_1_7['installs'].values), 2), np.round(tab_1_7['af_purchase (Sales in CAD)'].values, 2) , np.round(tab_1_7['CPA(login)'].values, 2) , np.round(tab_1_7['CPA(buyer)'].values,2), np.round(tab_1_7['ROAS'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Campaign Table Breakdown Last 7 days")

    figs_pnp.append(figkey_tab)

    tab_1['Country'] = tab_1['campaign'].apply(lambda x: x.split('_')[-1])
    tab_1['Country'] = tab_1['Country'].apply(lambda x: capi(dic_country[x]) if x in dic_country.keys() else x)
    tab_2 = tab_1.groupby('Country').sum().reset_index()
    tab_2['CPA(login)'] = tab_2['Cost'] / (tab_2['Installs'] + tab_2['installs'])
    tab_2['CPA(buyer)'] = tab_2['Cost'] / (tab_2['af_purchase'])
    tab_2['ROAS'] = tab_2['af_purchase (Sales in CAD)'] / tab_2['Cost']
    tab_2.sort_values('ROAS', ascending = False, inplace = True)
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Country', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_2['Country'].values, tab_2['Installs'].values + tab_2['installs'].values, np.round(tab_2['Cost'].values / (tab_2['Installs'].values + tab_2['installs'].values), 2), np.round(tab_2['af_purchase (Sales in CAD)'].values, 2) , np.round(tab_2['CPA(login)'].values, 2) , np.round(tab_2['CPA(buyer)'].values,2), np.round(tab_2['ROAS'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Country Table Breakdown From {} to {}".format(start_date_21, end_date_21))

    figs_pnp.append(figkey_tab)

    tab_1_7['Country'] = tab_1_7['campaign'].apply(lambda x: x.split('_')[-1])
    tab_1_7['Country'] = tab_1_7['Country'].apply(lambda x: capi(dic_country[x]) if x in dic_country.keys() else x)
    tab_2_7 = tab_1_7.groupby('Country').sum().reset_index()
    tab_2_7['CPA(login)'] = tab_2_7['Cost'] / (tab_2_7['Installs'] + tab_2_7['installs'])
    tab_2_7['CPA(buyer)'] = tab_2_7['Cost'] / (tab_2_7['af_purchase'])
    tab_2_7['ROAS'] = tab_2_7['af_purchase (Sales in CAD)'] / tab_2_7['Cost']
    tab_2_7.sort_values('ROAS', ascending = False, inplace = True)
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Country', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_2_7['Country'].values, tab_2_7['Installs'].values + tab_2_7['installs'].values, np.round(tab_2_7['Cost'].values / (tab_2_7['Installs'].values + tab_2_7['installs'].values), 2), np.round(tab_2_7['af_purchase (Sales in CAD)'].values, 2) , np.round(tab_2_7['CPA(login)'].values, 2) , np.round(tab_2_7['CPA(buyer)'].values,2), np.round(tab_2_7['ROAS'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Country Table Breakdown Last 7 days")

    figs_pnp.append(figkey_tab)

    tab_1['Language'] = tab_1['campaign'].apply(lambda x: x.split('_')[-2])
    tab_3 = tab_1.groupby('Language').sum().reset_index()
    tab_3['CPA(login)'] = tab_3['Cost'] / (tab_3['Installs'] + tab_3['installs'])
    tab_3['CPA(buyer)'] = tab_3['Cost'] / (tab_3['af_purchase'])
    tab_3['ROAS'] = tab_3['af_purchase (Sales in CAD)'] / tab_3['Cost']
    tab_3.sort_values('ROAS', ascending = False, inplace = True)
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Language', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_3['Language'].values, tab_3['Installs'].values + tab_3['installs'].values, np.round(tab_3['Cost'].values / (tab_3['Installs'].values + tab_3['installs'].values), 2), np.round(tab_3['af_purchase (Sales in CAD)'].values, 2) , np.round(tab_3['CPA(login)'].values, 2) , np.round(tab_3['CPA(buyer)'].values,2), np.round(tab_3['ROAS'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Language Table Breakdown From {} to {}".format(start_date_21, end_date_21))

    figs_pnp.append(figkey_tab)

    tab_1_7['Language'] = tab_1_7['campaign'].apply(lambda x: x.split('_')[-2])
    tab_3_7 = tab_1_7.groupby('Language').sum().reset_index()
    tab_3_7['CPA(login)'] = tab_3_7['Cost'] / (tab_3_7['Installs'] + tab_3_7['installs'])
    tab_3_7['CPA(buyer)'] = tab_3_7['Cost'] / (tab_3_7['af_purchase'])
    tab_3_7['ROAS'] = tab_3_7['af_purchase (Sales in CAD)'] / tab_3_7['Cost']
    tab_3_7.sort_values('ROAS', ascending = False, inplace = True)
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Language', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_3_7['Language'].values, tab_3_7['Installs'].values + tab_3_7['installs'].values, np.round(tab_3_7['Cost'].values / (tab_3_7['Installs'].values + tab_3_7['installs'].values), 2), np.round(tab_3_7['af_purchase (Sales in CAD)'].values, 2) , np.round(tab_3_7['CPA(login)'].values, 2) , np.round(tab_3_7['CPA(buyer)'].values,2), np.round(tab_3_7['ROAS'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Language Table Breakdown Last 7 days")

    figs_pnp.append(figkey_tab)
    
    
    path = 'C:\\Users\\User\\Documents\\Python Scripts'

    #prueba_json = fig.to_html(full_html=False, include_plotlyjs='cdn')
    #json_s3 = json.dumps(prueba_json)

    with open(join(path,'Adwords_Prev.html'), 'w') as f:
        for figure in figs_pnp:
            f.write(figure.to_html(full_html=False, include_plotlyjs='cdn'))
     


    
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

def drive_g(df, sheet_name, credentials):
    spreadsheet_key = '1oNclOE5NOm9ruo6Arh-daYIaPnBRqpmKdunw8dxI2WI'
    spread = Spread(spreadsheet_key, creds = credentials) 
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
