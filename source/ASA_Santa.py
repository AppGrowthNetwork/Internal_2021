import requests   
from pandas.io.json import json_normalize 
import pandas as pd  
from os.path import join
from gspread_pandas import Spread, Client
import datetime
from appsflyer import AppsFlyer
import numpy as np

import plotly.express as px
from plotly.graph_objs import *
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from google.oauth2.service_account import Credentials

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'C:\\Python39\\Lib\\site-packages\\gspread_pandas\\google_secret.json',
    scopes=scopes
)


path = 'C:\\Users\\User\\Downloads\\Santa_Admin_ASA_Cert\\'
ORG_ID = "396670" # Your ORG_ID, you can find in Apple Search ads, cabinet in the top right menu
APPLE_CERT = (join(path, 'AGN1.pem'), join(path, 'AGN1.key'))


#revenue and by campaign nb and b


def main():

    app_id = "id902026228"
    api_token = "6ebbb043-2c07-4972-8678-9687ae87ee9a"

    START_DATE = "2021-10-20"
    END_DATE = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")

    df_af = get_geo_by_date_report(app_id, api_token, START_DATE, END_DATE)
    

    df_af = df_af[df_af['Media Source (pid)'] == 'Apple Search Ads'].reset_index(drop = True)
   

    # We call our main delivery-boy function to do all the work
    df = download_campaigns_report(START_DATE, END_DATE)

    START_DATE_ = "2020-09-30"
    END_DATE_ = "2020-11-30" #(datetime.datetime.now() - datetime.timedelta(days = 387))

    df_19 = download_campaigns_report(START_DATE_, END_DATE_)
    # We rename some columns names to make them more beautiful
    new_columns = {x: x.replace("metadata.","") for x in df.columns}
    df = df.rename(columns=new_columns)
    df_19 = df_19.rename(columns=new_columns)

    

    # We fill empty rows with zeros
    df = df.fillna(0)
    df_19 = df_19.fillna(0)

    custom = pd.DataFrame()
    for i in range(0,len(df)):
        temp = pd.DataFrame()
        for j in range(0,len(df['granularity'][i])):
            data = df['granularity'][i][j]
            data['campaignId'] = df.loc[i,'campaignId']
            data['campaignName'] = df.loc[i,'campaignName']
            data['Country'] = df.loc[i,'countryOrRegion' ]
            if 'avgCPA' in df['granularity'][i][j].keys():
                data['avgCPA'] = df['granularity'][i][j]['avgCPA']
                data['avgCPT'] = df['granularity'][i][j]['avgCPT']
            if 'localSpend' in df['granularity'][i][j].keys():
                data['localSpend'] = df['granularity'][i][j]['localSpend']
            concat = pd.DataFrame(data, index = range(0,1))
            temp= pd.concat([temp, concat], axis = 0)
        custom = pd.concat([custom, temp], axis = 0)
    custom.reset_index(drop = True, inplace= True)
    custom = custom.fillna(0)
    custom['localSpend'] = custom['localSpend'].astype('float')
    
    print(custom.columns)

    custom_19 = pd.DataFrame()
    for i in range(0,len(df_19)):
        temp = pd.DataFrame()
        for j in range(0,len(df_19['granularity'][i])):
            data = df_19['granularity'][i][j]
            data['campaignId'] = df_19.loc[i,'campaignId']
            data['campaignName'] = df_19.loc[i,'campaignName']
            data['Country'] = df_19.loc[i,'countryOrRegion' ]
            if 'avgCPA' in df_19['granularity'][i][j].keys():
                data['avgCPA'] = df_19['granularity'][i][j]['avgCPA']
                data['avgCPT'] = df_19['granularity'][i][j]['avgCPT']
            if 'localSpend' in df_19['granularity'][i][j].keys():
                data['localSpend'] = df_19['granularity'][i][j]['localSpend']
            concat = pd.DataFrame(data, index = range(0,1))
            temp= pd.concat([temp, concat], axis = 0)
        custom_19 = pd.concat([custom_19, temp], axis = 0)
    custom_19.reset_index(drop = True, inplace= True)
    custom_19 = custom_19.fillna(0)
    custom_19['localSpend'] = custom_19['localSpend'].astype('float')
    print(custom_19)

    skan = pd.read_csv('C:\\Users\\User\\Documents\\Python Scripts\\pnp\\data_skan.csv')
    skan = skan[skan['media_source'] == 'Apple Search Ads']
    if 'skad_revenue' not in skan.columns:
        skan['skad_revenue'] = 0
    
    #Pick nb campaigns

    index_branded = [i for i in custom.index if ('BRAND' in custom.loc[i,'campaignName'] or 'Brand' in custom.loc[i, 'campaignName']) and 'BRANDED' not in custom.loc[i, 'campaignName'] and 'Non Branded' not in custom.loc[i, 'campaignName']]
    branded_campaigns = custom.iloc[index_branded, :]

    index_branded_af = [i for i in df_af.index if ('BRAND' in df_af.loc[i,'Campaign (c)'] )]
    branded_campaigns_af = df_af.iloc[index_branded_af, :]

    index_branded_skan = [i for i in skan.index if 'BRAND' in skan.loc[i,'ad_network_campaign_name']]
    branded_campaigns_skan = skan.iloc[index_branded_skan, :]

    #index_nb = [i for i in custom.index if ('Generic' in custom.loc[i,'campaignName'] or 'GENERIC' in custom.loc[i,'campaignName'] or 'Non Branded' in custom.loc[i,'campaignName'] or 'NON BRANDED' in custom.loc[i,'campaignName'] or 'DISCOVERY' in custom.loc[i,'campaignName'] or 'Discovery' in custom.loc[i,'campaignName'] or 'COMPETITOR' in custom.loc[i,'campaignName'] or 'Competitor' in custom.loc[i,'campaignName'])]
    index_nb = [i for i in custom.index if ('GENERIC' in custom.loc[i,'campaignName'] or 'DISCOVERY' in custom.loc[i,'campaignName'] or 'COMPETITOR' in custom.loc[i,'campaignName'])]
    nb_campaigns = custom.iloc[index_nb,:]
    
    index_nb = [i for i in df_af.index if ('GENERIC' in df_af.loc[i,'Campaign (c)'] or 'DISCOVERY' in df_af.loc[i,'Campaign (c)'] or 'COMPETITOR' in df_af.loc[i,'Campaign (c)'])]
    nb_campaigns_af = df_af.iloc[index_nb,:]

    index_nb = [i for i in skan.index if ('GENERIC' in skan.loc[i,'ad_network_campaign_name'] or 'DISCOVERY' in skan.loc[i,'ad_network_campaign_name'] or 'COMPETITOR' in skan.loc[i,'ad_network_campaign_name'])]
    nb_campaigns_skan = skan.iloc[index_nb,:]
    
    #nb = ~custom.index.isin(index_branded)
    #nb_campaigns = custom.iloc[nb,:]

    #nb_af = ~df_af.index.isin(index_branded_af)
    #nb_campaigns_af = df_af.iloc[nb_af,:]

    #nb_skan = ~skan.index.isin(index_branded_skan)
    #nb_campaigns_skan = skan.iloc[nb_skan,:]
    
    #index_nb = [i for i in df_af.index if ('Generic' in df_af.loc[i,'Campaign (c)'] or 'GENERIC' in df_af.loc[i,'Campaign (c)'] or 'Non Branded' in df_af.loc[i,'Campaign (c)'] or 'NON BRANDED' in df_af.loc[i,'Campaign (c)'] or 'DISCOVERY' in df_af.loc[i,'Campaign (c)'] or 'Discovery' in df_af.loc[i,'Campaign (c)'] or 'COMPETITOR' in df_af.loc[i,'Campaign (c)'] or 'Competitor' in df_af.loc[i,'Campaign (c)'])]
    #nb_campaigns_af = df_af.iloc[index_nb,:]
    
    #Pick branded campaigns
    ##ADD missing campaigns

    nb_campaigns = pd.merge(nb_campaigns.groupby(['date', 'campaignName']).sum().reset_index(),nb_campaigns_af.groupby(['Date', 'Campaign (c)']).sum().reset_index(), how = 'left', left_on =['date', 'campaignName'], right_on = ['Date', 'Campaign (c)'])
    nb_campaigns = pd.merge(nb_campaigns, nb_campaigns_skan.groupby(['date', 'ad_network_campaign_name']).count().reset_index() , how = 'left', left_on=['date', 'campaignName'], right_on= ['date', 'ad_network_campaign_name'])
    nb_campaigns= nb_campaigns.groupby(['date', 'campaignName']).sum().reset_index()

    branded_campaigns = pd.merge(branded_campaigns.groupby(['date', 'campaignName']).sum().reset_index(),branded_campaigns_af.groupby(['Date', 'Campaign (c)']).sum().reset_index(), how = 'left', left_on =['date', 'campaignName'], right_on = ['Date', 'Campaign (c)'])
    branded_campaigns = pd.merge(branded_campaigns, branded_campaigns_skan.groupby(['date', 'ad_network_campaign_name']).count().reset_index(), how = 'left', left_on=['date', 'campaignName'], right_on= ['date', 'ad_network_campaign_name'])
    branded_campaigns = branded_campaigns.groupby(['date', 'campaignName']).sum().reset_index()

    nb_campaigns['type'] = 'Non-Branded'
    nb_campaigns_af['type'] = 'Non-Branded'
    nb_campaigns_skan['type'] = 'Non-Branded'
    branded_campaigns['type'] = 'Branded'
    branded_campaigns_af['type'] = 'Branded'
    branded_campaigns_skan['type'] = 'Branded'

    end_date_ = datetime.datetime.strptime(END_DATE, '%Y-%m-%d')

    nb_campaigns['date'] = nb_campaigns['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    nb_campaigns_day = nb_campaigns[nb_campaigns['date'] >= (end_date_ - datetime.timedelta(days= 45))].groupby('date').sum().reset_index()

    branded_campaigns['date'] = branded_campaigns['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    branded_campaigns_day = branded_campaigns[branded_campaigns['date'] >= (end_date_ - datetime.timedelta(days= 45))].groupby('date').sum().reset_index()

    if 'installs' in nb_campaigns_day.columns:
        nb_campaigns_day['Network'] = 'ASA ( Non- Branded)'
        nb_campaigns_day['Revenue'] = 0
        nb_totals = nb_campaigns_day[['date','Network', 'installs', 'Installs', 'install_type', 'localSpend', 'Total Cost', 'skad_revenue', 'Revenue', 'af_purchase (Sales in CAD)']]
        
        #nb_totals = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Non- Branded)', 'Installs': nb_campaigns['installs'].sum(), 'Installs AF': nb_campaigns['Installs'].sum(), 'Installs skan': nb_campaigns['install_type'].sum(),  'Cost': nb_campaigns['localSpend'].sum(), 'Cost AF': nb_campaigns['Total Cost'].sum(), 'Revenue Skan': nb_campaigns['skad_revenue'].sum(), 'Revenue': 0, 'Revenue AF': nb_campaigns['af_purchase (Sales in CAD)'].sum()}, index = range(0,1))
    #else:
    #    nb_totals = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Non- Branded)', 'Installs': 0, 'Installs AF': 0, 'Installs skan': 0,  'Cost': 0, 'Cost AF': 0, 'Revenue Skan':0, 'Revenue':0, 'Revenue AF': 0}, index = range(0,1))


    if 'installs' in branded_campaigns_day.columns:
        branded_campaigns_day['Network'] = 'ASA ( Branded)'
        branded_campaigns_day['Revenue'] = 0
        branded_totals = branded_campaigns_day[['date','Network', 'installs', 'Installs', 'install_type', 'localSpend', 'Total Cost', 'skad_revenue', 'Revenue', 'af_purchase (Sales in CAD)']]
        
        #branded_totals = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Branded)', 'Installs': branded_campaigns['installs'].sum(), 'Installs AF': branded_campaigns['Installs'].sum(), 'Installs skan': branded_campaigns['install_type'].sum(),  'Cost': branded_campaigns['localSpend'].sum(), 'Cost AF': branded_campaigns['Total Cost'].sum(), 'Revenue Skan': branded_campaigns['skad_revenue'].sum(), 'Revenue': 0, 'Revenue AF': branded_campaigns['af_purchase (Sales in CAD)'].sum()}, index = range(0,1))
    #else:
    #    branded_totals = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Branded)', 'Installs': 0, 'Installs AF': 0, 'Installs skan': 0,  'Cost': 0, 'Cost AF': 0, 'Revenue Skan':0, 'Revenue':0, 'Revenue AF': 0}, index = range(0,1))


    rev = pd.concat([nb_campaigns, branded_campaigns], axis = 0)
    
    rev_af = pd.concat([nb_campaigns_af, branded_campaigns_af], axis = 0)
    
    #nb_campaigns= nb_campaigns.groupby('date').sum().reset_index()
    #branded_campaigns= branded_campaigns.groupby('date').sum().reset_index()
    #nb_campaigns_af= nb_campaigns_af.groupby('Date').sum().reset_index()
    #branded_campaigns_af= branded_campaigns_af.groupby('Date').sum().reset_index()

    
    #nb_totals = pd.DataFrame({'Date': nb_campaigns['date'], 'Network': 'ASA ( Non- Branded)', 'Installs': nb_campaigns['installs'] , 'Cost': nb_campaigns['localSpend']})
    #nb_totals_af = pd.DataFrame({'Date': nb_campaigns_af['Date'], 'Network': 'ASA ( Non- Branded)', 'Installs': nb_campaigns_af['Installs'] , 'Cost': nb_campaigns_af['Total Cost'], 'Revenue': nb_campaigns_af['af_purchase (Sales in CAD)']})
    #branded_totals = pd.DataFrame({'Date': branded_campaigns['date'], 'Network': 'ASA ( Branded)', 'Installs': branded_campaigns['installs'] , 'Cost': branded_campaigns['localSpend']})  
    #branded_totals_af = pd.DataFrame({'Date': branded_campaigns_af['Date'], 'Network': 'ASA ( Branded)', 'Installs': branded_campaigns_af['Installs'] , 'Cost': branded_campaigns_af['Total Cost'], 'Revenue': branded_campaigns_af['af_purchase (Sales in CAD)']})
    
    upload = pd.concat([branded_totals, nb_totals], axis =0)
    if 'af_purchase (Sales in CAD)' in upload.columns:
        ARPU = upload['af_purchase (Sales in CAD)'] / upload['Installs']
    upload['Revenue'] = ARPU * upload['installs']
    upload['ROAS'] = upload['af_purchase (Sales in CAD)'] / upload['Total Cost']
    upload.sort_values('date', inplace = True)
    upload['date'] = upload['date'].apply(lambda x: x.strftime("%Y-%m-%d"))
    print(upload)
    sheet_name = 'Daily_overview_2021'
    drive_g(upload, sheet_name, credentials)
    

    #print(upload)
    #upload.sort_values('Date', inplace = True)
    #upload.drop('ARPU', axis = 1, inplace = True)
    
        
    
    rev['Total Installs'] = rev['Installs'] + rev['install_type']
    rev_af['Country'] = rev_af['Country'].apply(lambda x: 'GB' if x == 'UK' else x)
    rev_date = rev.groupby(['date', 'type']).sum().reset_index()
    rev_af = rev_af.groupby(['Date', 'type', 'Country']).sum().reset_index()
    #rev_date = pd.merge(rev_date, rev_af[['Date', 'af_purchase (Sales in CAD)', 'Installs', 'type', 'Country', 'Total Cost']], how= 'left', left_on= ['date', 'type', 'Country'], right_on=['Date', 'type', 'Country'])
    rev_date['Revenue'] = rev_date['af_purchase (Sales in CAD)']
    
    #rev_date = rev_date.groupby(['Date', 'type', 'Country]).sum().reset_index()
    #rev_date['Revenue'] = rev_date['installs'] * (rev_date['Total Revenue'] / rev_date['Installs'])
    

    keywords = pd.DataFrame()

    campaigns = dict(zip(custom.campaignId.unique(), custom.campaignName.unique()))

    for campaign in custom.campaignId.unique():
        df_key = download_keywords_report(campaign, START_DATE, END_DATE)
        df_key['campaignId'] = campaign
        df_key['campaignName'] = campaigns[campaign]
        keywords = pd.concat([keywords, df_key], axis = 0)
    
    keywords.reset_index(inplace = True)
    custom_key = pd.DataFrame()
    #print(keywords)

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
    #print(custom_key)

    custom_key['type'] = custom_key['campaignName'].apply(lambda x: 'Branded' if ('BRAND' in str(x)) else 'Non-Branded')

    custom_key['avgCPA'] = custom_key['avgCPA'].astype('float')
    custom_key['avgCPT'] = custom_key['avgCPT'].astype('float')
    custom_key['localSpend'] = custom_key['localSpend'].astype('float')

    custom['avgCPA'] = custom['avgCPA'].astype('float')
    custom['avgCPT'] = custom['avgCPT'].astype('float')
    custom['localSpend'] = custom['localSpend'].astype('float')

    figs_asa = []

    fig = make_subplots( rows=1, cols=2, column_widths=[0.65, 0.35], specs=[[{"secondary_y": True}, {"secondary_y": True}]],
                subplot_titles=("Daily ASA Installs vs. CPI", "Daily Revenue KPIs" ))


    print(custom.groupby('date').sum())
    # Add traces
    fig.add_trace(go.Scatter(x=custom.date, y=rev_date.groupby('date').sum()['Total Cost']/rev_date.groupby('date').sum()['Total Installs'],
                    mode='lines+markers',
                    name='avgCPI', yaxis='y2'), secondary_y=True, row=1, col=1)

    fig.add_trace(go.Bar(x=custom.date, y=rev_date.groupby('date').sum()['newDownloads'],
                    name='newDownloads', marker_color = 'rgb(158,185,243)'), row=1, col=1)

    fig.add_trace(go.Bar(x=custom.date, y=rev_date.groupby('date').sum()['redownloads'],
                    name='reDownloads', marker_color = 'rgb(229,196,148)'), row=1, col=1)
    
    fig.add_trace(go.Scatter(x=rev_date.groupby('date').sum().index, y=rev_date.groupby('date').sum()['Revenue'] / rev_date.groupby('date').sum()['Total Cost'],
                    mode='lines+markers',
                    name='ROAS', marker_color = '#511CFB'), secondary_y=True, row=1, col=2)
    
    fig.add_trace(go.Scatter(x=rev.groupby('date').sum().index, y=rev_date.groupby('date').sum()['Revenue'] / rev_date.groupby('date').sum()['Total Installs'],
                    mode='lines+markers',
                    name='ARPU', marker_color = '#2CA02C'), secondary_y=True, row=1, col=2)

    fig.add_trace(go.Bar(x=rev.groupby('date').sum().index, y = rev_date.groupby(['date', 'type']).sum()['Revenue'].loc[slice(None),'Non-Branded'], 
                    name = 'Non-Branded'), row= 1, col = 2)
    fig.add_trace(go.Bar(x=rev.groupby('date').sum().index, y = rev_date.groupby(['date', 'type']).sum()['Revenue'].loc[slice(None),'Branded'], 
                    name = 'Branded'), row= 1, col = 2)
    
    fig.add_trace(go.Scatter(x=rev.groupby('date').sum().index, y=rev.groupby('date').sum()['Total Cost'],
                    mode='lines+markers', marker_color = '#EF553B',
                    name='Cost'),row=1, col=2)
    fig.add_trace(go.Scatter(x=rev.groupby('date').sum().index, y=rev.groupby('date').sum()['Total Installs'],
                    mode='lines+markers', marker_color = 'orange',
                    name='Total Installs'),row=1, col=1)
    
    fig.update_layout(barmode = 'stack', height = 600)

    figs_asa.append(fig)

    
    print('revenue')
    rev['Country'] = rev['campaignName'].apply(lambda x: x.split('-')[0].replace(' ', ''))
    lista = rev.groupby(['Country']).sum().reset_index()
    lista.sort_values('af_purchase (Sales in CAD)', inplace = True, ascending = False)
    corte = lista.head(3)
    parces = corte['Country'].unique()
    corte = rev.groupby(['date', 'type', 'Country']).sum().reset_index()
    idx = [i for i in corte.index if corte.loc[i, 'Country'] in parces]
    corte = corte.loc[idx, :]
    fig_camp_ = px.bar(corte, x='date', y='af_purchase (Sales in CAD)', color = 'type',
                facet_col='Country', facet_col_wrap=2, facet_row_spacing=0.03, facet_col_spacing=0.03)
    fig_camp_.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig_camp_.update_yaxes(matches=None, showticklabels=True, title_text='')
    fig_camp_.update_xaxes(matches='x')
    fig_camp_.update_layout(title_text="Daily Revenue per Country", height = 1000, barmode = 'stack')

    figs_asa.append(fig_camp_)

    #fig.add_trace(go.Bar(x=custom.groupby('Country').sum().index, y = custom.groupby('Country').sum()["newDownloads"], 
                   # showlegend = False, marker_color = 'rgb(158,185,243)'), row= 1, col = 2)

    #fig.add_trace(go.Bar(x=custom.groupby('Country').sum().index, y = custom.groupby('Country').sum()["redownloads"], 
                   # showlegend = False, marker_color = 'rgb(229,196,148)'), row= 1, col = 2)
            

    

    #bar_key = custom_key.groupby(['keyword', 'Country', 'type']).sum()
    #bar_key.reset_index(inplace = True)

    def competitor_filter(string):
        if 'COMPETITOR' in string:
            x = 'COMPETITOR'
        else:
            x = 'NON-COMPETITOR'
        return x

    #custom_key['type']  = custom_key['campaignName'].apply(lambda x : competitor_filter(x)) 
    #bar_comp = custom_key.groupby(['Country','type']).sum().reset_index()
    #bar_comp['conversionRate'] = bar_comp['installs'] / bar_comp['taps']

    #fig_key = px.bar(bar_key, x="keyword", y = "installs", color="localSpend", facet_col="type", facet_col_wrap=1, 
           #hover_data=["localSpend", "taps", 'Country'], title = 'Keywords performance Branded vs Non-Branded (Stacked = Country)')
    #fig_key.update_layout(height = 1000, xaxis={'visible': False, 'showticklabels': False})
    
    #path = 'C:\\Users\\User\\Downloads'
    #merged = pd.read_csv(join(path, 'merged_Dec21.csv'))
    #merged = merged.head(100)

    #tab = bar_key.sort_values('installs', ascending = False).head(20)
    #figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Keyword','Campaign', 'Country', 'Type', 'Installs', 'Revenue']),
    #             cells=dict(values=[merged.Keywords.values, merged.Campaign.values, merged['Country Code'].values, merged.type.values, merged.Installs.values, np.round(merged['Event Revenue'].values, 2)]))
    #                 ])
    #figkey_tab.update_layout(title_text="ASA Keywords Revenue Table")
    
    rev['year'] ='2021'
    custom_19['year'] ='2020'
    rev['date_'] = pd.to_datetime(rev['date'], format = '%Y-%m-%d')
    custom_19['date_'] = pd.to_datetime(custom_19['date'], format = '%Y-%m-%d')
    rev['date_'] = rev['date_'].apply(lambda x: x.strftime('%b-%d'))
    custom_19['date_'] = custom_19['date_'].apply(lambda x: x.strftime('%b-%d'))
    
    custom_plot = rev.groupby(['year', 'Country', 'date_']).sum().reset_index()
    custom_19['Country'] = custom_19['campaignName'].apply(lambda x: x.split('-')[0].replace(' ', ''))
    print(custom_19)
    custom_19['Total Installs'] = custom_19['installs']
    custom_19['Total Cost'] = custom_19['localSpend']
    custom_19_plot = custom_19.groupby(['year', 'Country', 'date_']).sum().reset_index()

    year_over = pd.concat([custom_plot, custom_19_plot], axis=0)
    year_over.reset_index(inplace = True)


    lista = year_over.groupby(['Country']).sum().reset_index()
    lista.sort_values('installs', inplace = True, ascending = False)
    corte = lista.head(15)
    parces = corte['Country'].unique()
    #print(parces)
    idx = [i for i in year_over.index if year_over.loc[i, 'Country'] in parces]
    year_over = year_over.loc[idx, :]
    year_over['date_'] = pd.to_datetime(year_over['date_'], format = '%b-%d')
    year_over['date_'] = year_over['date_'].mask(year_over['date_'].dt.year == 1900, 
                             year_over['date_'] + pd.offsets.DateOffset(year=2020))
    #& (cut['Day'] <= (datetime.now() - timedelta(days= 4)))
    year_over.sort_values('date_', inplace = True)
    year_over['date_'] = year_over['date_'].apply(lambda x: x.strftime('%b-%d'))

    fig_camp2 = px.scatter(year_over, x='date_', y='Total Installs', color='year', facet_col= 'Country', facet_col_wrap= 2, facet_row_spacing=0.03, facet_col_spacing=0.03, size = 'Total Cost',  color_discrete_map={"2021": 'red', '2020':'orange'}).update_traces(mode='lines+markers')
    fig_camp2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig_camp2.update_yaxes(matches=None, showticklabels=True, title_text='')
    fig_camp2.update_xaxes(matches='x')
    fig_camp2.update_layout(
        title_text="Daily Installs per Country (size = Total Cost)", height = 1200)
    
    figs_asa.append(fig_camp2)
    #fig_key_sub = make_subplots(rows=1, cols=2, specs=[[{"secondary_y": True}, {"secondary_y": True}]],
            #subplot_titles=('Installs KPIs (Competitor)', 'Installs KPIs (Non-competitor)'))
    
    #lista = custom_key.groupby(['keyword', 'Country', 'type']).sum().reset_index()

    #fig_key_sub.add_trace(go.Bar(x=bar_comp[bar_comp['type'] == 'COMPETITOR']["Country"], y = bar_comp[bar_comp['type'] == 'COMPETITOR']["installs"], name = 'installs', marker_color='rgb(55, 83, 109)'), 1,1)
    #fig_key_sub.add_trace(go.Line(x=bar_comp[bar_comp['type'] == 'COMPETITOR']["Country"], y = bar_comp[bar_comp['type'] == 'COMPETITOR']["conversionRate"], name = 'conversionRate', marker_color='rgb(26, 118, 255)'), secondary_y = True, row = 1, col = 1)
    #fig_key_sub.add_trace(go.Bar(x=bar_comp[bar_comp['type'] == 'NON-COMPETITOR']["Country"], y = bar_comp[bar_comp['type'] == 'NON-COMPETITOR']["installs"], name = 'installs', marker_color='rgb(55, 83, 109)', showlegend=False), 1,2)
    #fig_key_sub.add_trace(go.Line(x=bar_comp[bar_comp['type'] == 'NON-COMPETITOR']["Country"], y = bar_comp[bar_comp['type'] == 'NON-COMPETITOR']["conversionRate"], name = 'conversionRate', marker_color='rgb(26, 118, 255)', showlegend=False), secondary_y = True, row = 1, col = 2)
    #fig_key_sub.update_layout(barmode='group', xaxis_tickangle=-45, width=1500, height=620)
    
    
    rev['Revenue'] = rev['af_purchase (Sales in CAD)']
    rev_country = rev.groupby('Country').sum().reset_index()
    rev_country['ROAS'] = rev_country['Revenue'] / rev_country['Total Cost']
    rev_country.sort_values('ROAS', ascending = False, inplace = True)

    trace = go.Table(header=dict(values=['Country','Revenue', 'ROAS']),
                 cells=dict(values=[rev_country.Country.values, np.round(rev_country.Revenue.values, 2), np.round(rev_country.ROAS.values, 1)]), domain=dict(x=[0.52, 1],y=[0, 1]))
            
    trace1 = go.Pie(values=rev_country.localSpend, labels=rev_country.Country, hole=.4, name = 'localSpend', domain=dict(x=[0, 0.23],y=[0, 1]), title_text = 'Cost', textposition='inside', textinfo='label', hoverinfo="label+value")
    trace2 = go.Pie(values=rev_country.Revenue, labels=rev_country.Country, hole=.4, name = 'Revenue', domain=dict(x=[0.26, 0.49],y=[0, 1]), title_text = 'Revenue', textposition='inside', textinfo='label', hoverinfo="label+value")
    
    
    fig_dough = go.Figure(data = [trace,trace1, trace2])
    fig_dough.update_layout(title_text="ASA Breakdown by Country")

    figs_asa.append(fig_dough)

    raw = pd.read_csv('C:\\Users\\User\\Documents\\Python Scripts\\pnp\\data_raw.csv')
    raw = raw[raw['media_source'] == 'Apple Search Ads']
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
    
    raw['date'] = raw['event_time_selected_timezone'].apply(lambda x: datetime.datetime.strptime(x.split('.')[0], '%Y-%m-%d %H:%M:%S'))
    raw['date'] = raw['date'].apply(lambda x: x.date())
    #rev['date'] = rev['date'].apply(lambda x: datetime.datetime.strftime(x, '%Y-%m-%d'))
    #rev['date'] = rev['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    rev['date'] = rev['date'].apply(lambda x: x.date())
    raw_tab = raw.groupby(['date', 'campaign']).sum().reset_index()
    tab_tab = pd.merge(rev, raw_tab, how = 'left', left_on = ['date','campaignName'], right_on= ['date', 'campaign'])
    tab_1 = tab_tab.groupby(['campaignName']).sum().reset_index()
    print(tab_1.columns)
    tab_1['CPA(login)'] = tab_1['Total Cost'] / (tab_1['Installs'] + tab_1['install_type'])
    tab_1['CPA(buyer)'] = tab_1['Total Cost'] / (tab_1['af_purchase'])
    tab_1['ROAS'] = tab_1['af_purchase (Sales in CAD)'] / tab_1['Total Cost']
    tab_1['Total Installs'] = tab_1['Installs'] + tab_1['install_type']
    tab_1 = tab_1.sort_values('ROAS', ascending = False)
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Campaign', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_1['campaignName'].values, tab_1['Total Installs'].values, np.round(tab_1['Total Cost'].values / tab_1['Total Installs'].values, 2), np.round(tab_1['af_purchase (Sales in CAD)'].values, 2) , np.round(tab_1['CPA(login)'].values, 2) , np.round(tab_1['CPA(buyer)'].values,2), np.round(tab_1['ROAS'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Campaign Table Breakdown From {} to {}".format(START_DATE, END_DATE))

    figs_asa.append(figkey_tab)

    tab_tab['date'] = tab_tab['date'].apply(lambda x: datetime.datetime.combine(x, datetime.time(0, 0)))
    tab_tab_7 = tab_tab[tab_tab['date'] >= datetime.datetime.now() - datetime.timedelta(days = 7)]
    tab_1_7 = tab_tab_7.groupby(['campaignName']).sum().reset_index()
    tab_1_7['CPA(login)'] = tab_1_7['Total Cost'] / (tab_1_7['Installs'] + tab_1_7['install_type'])
    tab_1_7['CPA(buyer)'] = tab_1_7['Total Cost'] / (tab_1_7['af_purchase'])
    tab_1_7['ROAS'] = tab_1_7['af_purchase (Sales in CAD)'] / tab_1_7['Total Cost']
    tab_1_7['Total Installs'] = tab_1_7['Installs'] + tab_1_7['install_type']
    tab_1_7 = tab_1_7.sort_values('ROAS', ascending = False)
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Campaign', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_1_7['campaignName'].values, tab_1_7['Total Installs'].values, np.round(tab_1_7['Total Cost'].values / tab_1_7['Total Installs'].values, 2), np.round(tab_1_7['af_purchase (Sales in CAD)'].values, 2) , np.round(tab_1_7['CPA(login)'].values, 2) , np.round(tab_1_7['CPA(buyer)'].values,2), np.round(tab_1_7['ROAS'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Campaign Table Breakdown Last 7 days")

    figs_asa.append(figkey_tab)

    tab_1['Country'] = tab_1['campaignName'].apply(lambda x: x.split('-')[0].replace(' ', ''))
    tab_1['Country'] = tab_1['Country'].apply(lambda x: capi(dic_country[x]) if x in dic_country.keys() else x)
    tab_2 = tab_1.groupby('Country').sum().reset_index()
    tab_2['CPA(login)'] = tab_2['Total Cost'] / (tab_2['Installs'] + tab_2['install_type'])
    tab_2['CPA(buyer)'] = tab_2['Total Cost'] / (tab_2['af_purchase'])
    tab_2 = tab_2.sort_values('Total Installs', ascending = False)
    print(tab_2.head())
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Country', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_2['Country'].values, tab_2['Total Installs'].values , np.round(tab_2['Total Cost'].values / tab_2['Total Installs'].values, 2), np.round(tab_2['af_purchase (Sales in CAD)'].values, 2) , np.round(tab_2['CPA(login)'].values, 2) , np.round(tab_2['CPA(buyer)'].values,2), np.round(tab_2['ROAS'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Country Table Breakdown From {} to {}".format(START_DATE, END_DATE))

    figs_asa.append(figkey_tab)

    tab_1_7['Country'] = tab_1_7['campaignName'].apply(lambda x: x.split('-')[0].replace(' ', ''))
    tab_1_7['Country'] = tab_1_7['Country'].apply(lambda x: capi(dic_country[x]) if x in dic_country.keys() else x)
    tab_2_7 = tab_1_7.groupby('Country').sum().reset_index()
    tab_2_7['CPA(login)'] = tab_2_7['Total Cost'] / (tab_2_7['Installs'] + tab_2_7['install_type'])
    tab_2_7['CPA(buyer)'] = tab_2_7['Total Cost'] / (tab_2_7['af_purchase'])
    tab_2_7 = tab_2_7.sort_values('Total Installs', ascending = False)
    print(tab_2_7.head())
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Country', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_2_7['Country'].values, tab_2_7['Total Installs'].values , np.round(tab_2_7['Total Cost'].values / tab_2_7['Total Installs'].values, 2), np.round(tab_2_7['af_purchase (Sales in CAD)'].values, 2) , np.round(tab_2_7['CPA(login)'].values, 2) , np.round(tab_2_7['CPA(buyer)'].values,2), np.round(tab_2_7['ROAS'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Country Table Breakdown Last 7 days")

    figs_asa.append(figkey_tab)

    tab_1['Language'] = tab_1['campaignName'].apply(lambda x: x.split('-')[1].replace(' ', ''))
    tab_3 = tab_1.groupby('Language').sum().reset_index()
    print(tab_3)
    tab_3['CPA(login)'] = tab_3['Total Cost'] / (tab_3['Installs'] + tab_3['install_type'])
    tab_3['CPA(buyer)'] = tab_3['Total Cost'] / (tab_3['af_purchase'])
    tab_3 = tab_3.sort_values('ROAS', ascending = False)
    idx = [i for i in tab_3.index if tab_3.loc[i, 'Language'] not in ['BRAND', 'Brand', 'COMPETITOR','DISCOVERY', 'GENERIC']]
    tab_3 = tab_3.loc[idx]
    print(tab_3)
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Language', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_3['Language'].values, tab_3['Total Installs'].values, np.round(tab_3['Total Cost'].values / (tab_3['Total Installs'].values), 2), np.round(tab_3['af_purchase (Sales in CAD)'].values, 2) , np.round(tab_3['CPA(login)'].values, 2) , np.round(tab_3['CPA(buyer)'].values,2), np.round(tab_3['ROAS'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Language Table Breakdown From {} to {}".format(START_DATE, END_DATE))

    figs_asa.append(figkey_tab)


    ##Last 7 days

    tab_1_7['Language'] = tab_1_7['campaignName'].apply(lambda x: x.split('-')[1].replace(' ', ''))
    tab_3_7 = tab_1_7.groupby('Language').sum().reset_index()
    print(tab_3_7)
    tab_3_7['CPA(login)'] = tab_3_7['Total Cost'] / (tab_3_7['Installs'] + tab_3_7['install_type'])
    tab_3_7['CPA(buyer)'] = tab_3_7['Total Cost'] / (tab_3_7['af_purchase'])
    tab_3_7 = tab_3_7.sort_values('ROAS', ascending = False)
    idx = [i for i in tab_3_7.index if tab_3_7.loc[i, 'Language'] not in ['BRAND', 'Brand', 'COMPETITOR','DISCOVERY', 'GENERIC']]
    tab_3_7 = tab_3_7.loc[idx]
    print(tab_3_7)
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Language', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_3_7['Language'].values, tab_3_7['Total Installs'].values, np.round(tab_3_7['Total Cost'].values / (tab_3_7['Total Installs'].values), 2), np.round(tab_3_7['af_purchase (Sales in CAD)'].values, 2) , np.round(tab_3_7['CPA(login)'].values, 2) , np.round(tab_3_7['CPA(buyer)'].values,2), np.round(tab_3_7['ROAS'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Language Table Breakdown Last 7 days")

    figs_asa.append(figkey_tab)

    path = 'C:\\Users\\User\\Documents\\Python Scripts'

    with open('Asa_Prev.html', 'w') as f:
        for fig in figs_asa:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
        
        
        
        
        
           


def download_campaigns_report(START_DATE, END_DATE):
    # URL, where we through out request
    url = "https://api.searchads.apple.com/api/v3/reports/campaigns"

    # We call our function, that creates a JSON request for us
    report = create_campaigns_report(START_DATE, END_DATE)

    # Now we construct everything together
    headers = {"Authorization": "orgId={}".format(ORG_ID)}
    response = requests.post(url, cert=APPLE_CERT, json=report, headers=headers)
    response.encoding = "utf-8"

    # Id status code is not 200 - something went wrong. We stop the program and show exact mistake
    if response.status_code != 200:
        raise ValueError(response.content)

    # If we ger here - the status is 200 and response contains our report
    # So we need to get it from JSON and ask json_normalize() to convert it to the table
    data = response.json()['data']['reportingDataResponse']['row']
    data = json_normalize(data)
    return data


def create_campaigns_report(START_DATE, END_DATE):
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
                        "operator": "IN",
                        "values": [
                            "ENABLED", "PAUSED"
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


def download_keywords_report(campaignId, START_DATE, END_DATE):
    # URL, where we through out request
    url = "https://api.searchads.apple.com/api/v3/reports/campaigns/{}/keywords".format(campaignId)

    # We call our function, that creates a JSON request for us
    report = create_keywords_report(START_DATE, END_DATE)

    # Now we construct everything together
    headers = {"Authorization": "orgId={}".format(ORG_ID)}
    response = requests.post(url, cert=APPLE_CERT, json=report, headers=headers)
    response.encoding = "utf-8"

    # Id status code is not 200 - something went wrong. We stop the program and show exact mistake
    if response.status_code != 200:
        raise ValueError(response.content)

    # If we ger here - the status is 200 and response contains our report
    # So we need to get it from JSON and ask json_normalize() to convert it to the table
    data = response.json()['data']['reportingDataResponse']['row']
    data = json_normalize(data)
    return data


def create_keywords_report(START_DATE, END_DATE):
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


def get_geo_by_date_report(app_id, api_token, start_date, end_date):
    
    client = AppsFlyer(api_token=api_token, app_id=app_id)
    df = client.geo_by_date_report(start_date, end_date, as_df=True)
    
    return df

if __name__ == "__main__":
    main()