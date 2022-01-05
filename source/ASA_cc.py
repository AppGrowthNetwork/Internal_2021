import requests   
from pandas.io.json import json_normalize 
import pandas as pd  
from os.path import join
import os
import gspread

import datetime
from appsflyer import AppsFlyer
import numpy as np
from plotly.offline import plot
import plotly.express as px
from plotly.graph_objs import *
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots



path = 'C:\\Users\\User\\Downloads\\Certificates_asa\\'
ORG_ID = "2161070" # Your ORG_ID, you can find in Apple Search ads, cabinet in the top right menu
APPLE_CERT = (join(path, 'AGN.pem'), join(path, 'AGN.key'))

START_DATE = "2020-12-01"
END_DATE = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")
#revenue and by campaign nb and b


def main():

    app_id = "id1506654910"
    api_token = "f0cbd5d4-1f74-412e-bead-d6c93dc226fb"

    df_af = get_geo_by_date_report(app_id, api_token, START_DATE, END_DATE)

    df_af = df_af[df_af['Media Source (pid)'] == 'Apple Search Ads'].reset_index(drop = True)
   
    
    # We call our main delivery-boy function to do all the work
    df = download_campaigns_report()

    # We rename some columns names to make them more beautiful
    new_columns = {x: x.replace("metadata.","") for x in df.columns}
    df = df.rename(columns=new_columns)

    # We fill empty rows with zeros
    df = df.fillna(0)
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
    print(custom)
    custom['localSpend'] = custom['localSpend'].astype('float')
    

    #Pick nb campaigns
    #index_nb = [i for i in custom.index if ('Generic' in custom.loc[i,'campaignName'] or 'Discovery' in custom.loc[i,'campaignName'] or 'Competitor' in custom.loc[i,'campaignName'])]
    #nb_campaigns = custom.iloc[index_nb,:]
    
    #index_nb = [i for i in df_af.index if ('GENERIC' in df_af.loc[i,'Campaign (c)'] or 'DISCOVERY' in df_af.loc[i,'Campaign (c)'] or 'COMPETITOR' in df_af.loc[i,'Campaign (c)'])]
    #nb_campaigns_af = df_af.iloc[index_nb,:]
    
    #Pick branded campaigns
    #index_branded = [i for i in custom.index if 'Brand' in custom.loc[i,'campaignName']]
    #branded_campaigns = custom.iloc[index_branded, :]

    #index_branded = [i for i in df_af.index if 'BRAND' in df_af.loc[i,'Campaign (c)']]
    #branded_campaigns_af = df_af.iloc[index_branded, :]

    #nb_campaigns['type'] = 'Non-Branded'
    #nb_campaigns_af['type'] = 'Non-Branded'
    #branded_campaigns['type'] = 'Branded'
    #branded_campaigns_af['type'] = 'Branded'
    #rev = pd.concat([nb_campaigns, branded_campaigns], axis = 0)
    #print(rev)
    #rev_af = pd.concat([nb_campaigns_af, branded_campaigns_af], axis = 0)
    #print(rev_af)


    #nb_campaigns = nb_campaigns[nb_campaigns['date'] == END_DATE]
    #nb_campaigns_af = nb_campaigns_af[nb_campaigns_af['Date'] == END_DATE]
    #branded_campaigns = branded_campaigns[branded_campaigns['date'] == END_DATE]
    #branded_campaigns_af = branded_campaigns_af[branded_campaigns_af['Date'] == END_DATE]

    #if 'installs' in nb_campaigns.columns:
        #nb_totals = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Non- Branded)', 'Installs': nb_campaigns['installs'].sum() , 'Cost': nb_campaigns['localSpend'].sum()}, index = range(0,1))
        #nb_totals_af = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Non- Branded)', 'Installs': nb_campaigns_af['Installs'].sum() , 'Cost': nb_campaigns_af['Total Cost'].sum(), 'Revenue': nb_campaigns_af['Total Revenue'].sum()}, index = range(0,1))
    #else:
        #nb_totals = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Non- Branded)', 'Installs': 0, 'Cost': 0}, index = range(0,1))
        #nb_totals_af = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Non- Branded)', 'Installs': 0, 'Cost': 0}, index = range(0,1))


    #if 'installs' in branded_campaigns.columns:
        #branded_totals = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Branded)', 'Installs': branded_campaigns['installs'].sum() , 'Cost': branded_campaigns['localSpend'].sum()}, index = range(0,1))
        #branded_totals_af = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Branded)', 'Installs': branded_campaigns_af['Installs'].sum() , 'Cost': branded_campaigns_af['Total Cost'].sum(), 'Revenue': branded_campaigns_af['Total Revenue'].sum()}, index = range(0,1))
    #else:
        #branded_totals = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Branded)', 'Installs': 0, 'Cost': 0}, index = range(0,1))
        #branded_totals_af = pd.DataFrame({'Date': END_DATE, 'Network': 'ASA ( Branded)', 'Installs': 0, 'Cost': 0}, index = range(0,1))


    upload = custom.copy()
    upload_af = df_af.copy()
    upload_af['ARPU'] = upload_af['Revenue'] / upload_af['Installs']
    upload['Revenue'] = upload_af['ARPU'] * upload['Installs']
    upload['ROAS'] = upload['Revenue'] / upload['Cost']
    #print(upload)
    #sheet_name = 'Daily_overview'
    #drive_g(upload, sheet_name)  
    #rev_af['Country'] = rev_af['Country'].apply(lambda x: 'GB' if x == 'UK' else x)
    rev_date = upload.groupby(['date', 'type', 'Country']).sum().reset_index()
    rev_af = upload_af.groupby(['Date', 'type', 'Country']).sum().reset_index()
    rev_date = pd.merge(rev_date, rev_af[['Date', 'Total Revenue', 'Installs', 'type', 'Country']], how= 'left', left_on= ['date', 'type', 'Country'], right_on=['Date', 'type', 'Country'])
    #rev_date['Revenue'] = rev_date['installs'] * (rev_date['Total Revenue'] / rev_date['Installs'])
    

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
    custom_key['type'] = custom_key['campaignName'].apply(lambda x: 'Branded' if 'BRAND' in str(x) else 'Non-Branded')

    custom_key['avgCPA'] = custom_key['avgCPA'].astype('float')
    custom_key['avgCPT'] = custom_key['avgCPT'].astype('float')
    custom_key['localSpend'] = custom_key['localSpend'].astype('float')

    custom['avgCPA'] = custom['avgCPA'].astype('float')
    custom['avgCPT'] = custom['avgCPT'].astype('float')
    custom['localSpend'] = custom['localSpend'].astype('float')



    fig = make_subplots( rows=1, cols=2, column_widths=[0.65, 0.35], specs=[[{"secondary_y": True}, {}]],
                subplot_titles=("Daily ASA Installs vs. CPI", "Installs by Country" ))


    
    # Add traces
    fig.add_trace(go.Scatter(x=custom.date, y=custom.groupby('date').sum()['localSpend']/custom.groupby('date').sum()['installs'],
                    mode='lines+markers',
                    name='avgCPI', yaxis='y2'), secondary_y=True, row=1, col=1)

    fig.add_trace(go.Bar(x=custom.date, y=custom.groupby('date').sum()['newDownloads'],
                    name='newDownloads', marker_color = 'rgb(158,185,243)'), row=1, col=1)

    fig.add_trace(go.Bar(x=custom.date, y=custom.groupby('date').sum()['redownloads'],
                    name='reDownloads', marker_color = 'rgb(229,196,148)'), row=1, col=1)
    
    fig.add_trace(go.Bar(x=rev.groupby('Country').sum().index, y=rev.groupby('Country').sum()['installs'],
                 marker_color = '#511CFB'), row=1, col=2)
    
    #fig.add_trace(go.Bar(x=rev.groupby('Country').sum().index, y=rev.groupby(['Country', 'type']).sum()['installs'].loc[slice(None), 'Non-Branded'],
                   # name='Non-Branded', marker_color = '#2CA02C'), row=1, col=2)
    
    fig.add_trace(go.Scatter(x=rev.groupby('Country').sum().index, y=rev.groupby('Country').sum()['localSpend'],
                    mode='lines+markers', marker_color = '#EF553B',
                    name='Cost'),row=1, col=2)
    
    
    fig.update_layout(barmode = 'stack', height = 600)


    #revenue
    #STATES USA
    #fig_camp_ = px.bar(rev_date.groupby(['date', 'type', 'Country']).sum().reset_index(), x='date', y='installs', color = 'type',
       #         facet_col='Country', facet_col_wrap=2)
    #fig_camp_.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    #fig_camp_.update_yaxes(matches=None, showticklabels=True, title_text='')
    #fig_camp_.update_xaxes(matches='x')
    #fig_camp_.update_layout(
       # title_text="Daily Installs per Country", height = 550, barmode = 'stack')

    #fig.add_trace(go.Bar(x=custom.groupby('Country').sum().index, y = custom.groupby('Country').sum()["newDownloads"], 
                   # showlegend = False, marker_color = 'rgb(158,185,243)'), row= 1, col = 2)

    #fig.add_trace(go.Bar(x=custom.groupby('Country').sum().index, y = custom.groupby('Country').sum()["redownloads"], 
                   # showlegend = False, marker_color = 'rgb(229,196,148)'), row= 1, col = 2)
            

    

    bar_key = custom_key.groupby(['keyword', 'Country', 'type']).sum()
    bar_key.reset_index(inplace = True)

    fig_key = px.bar(bar_key, x="keyword", y = "installs", color="localSpend", facet_col="type", facet_col_wrap=1, 
           hover_data=["localSpend", "taps", 'Country'], title = 'Keywords performance Branded vs Non-Branded (Stacked = Country)')
    fig_key.update_layout(height = 550, xaxis={'visible': False, 'showticklabels': False})
    
    tab = bar_key.sort_values('installs', ascending = False).head(20)
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Keyword','Installs', 'Country']),
                 cells=dict(values=[tab.keyword.values, tab.installs.values, tab.Country.values]))
                     ])
    
    #fig_key_sub = make_subplots(rows=1, cols=2, specs=[[{"secondary_y": True}, {"secondary_y": True}]],
            #subplot_titles=('Installs KPIs (Competitor)', 'Installs KPIs (Non-competitor)'))
    
    #lista = custom_key.groupby(['keyword', 'Country', 'type']).sum().reset_index()

    #fig_key_sub.add_trace(go.Bar(x=bar_comp[bar_comp['type'] == 'COMPETITOR']["Country"], y = bar_comp[bar_comp['type'] == 'COMPETITOR']["installs"], name = 'installs', marker_color='rgb(55, 83, 109)'), 1,1)
    #fig_key_sub.add_trace(go.Line(x=bar_comp[bar_comp['type'] == 'COMPETITOR']["Country"], y = bar_comp[bar_comp['type'] == 'COMPETITOR']["conversionRate"], name = 'conversionRate', marker_color='rgb(26, 118, 255)'), secondary_y = True, row = 1, col = 1)
    #fig_key_sub.add_trace(go.Bar(x=bar_comp[bar_comp['type'] == 'NON-COMPETITOR']["Country"], y = bar_comp[bar_comp['type'] == 'NON-COMPETITOR']["installs"], name = 'installs', marker_color='rgb(55, 83, 109)', showlegend=False), 1,2)
    #fig_key_sub.add_trace(go.Line(x=bar_comp[bar_comp['type'] == 'NON-COMPETITOR']["Country"], y = bar_comp[bar_comp['type'] == 'NON-COMPETITOR']["conversionRate"], name = 'conversionRate', marker_color='rgb(26, 118, 255)', showlegend=False), secondary_y = True, row = 1, col = 2)
    #fig_key_sub.update_layout(barmode='group', xaxis_tickangle=-45, width=1500, height=620)
    
    
    #rev_country = rev_date.groupby('Country').sum().reset_index()
    #rev_country['ROAS'] = rev_country['Revenue'] / rev_country.localSpend
    #rev_country.sort_values('ROAS', ascending = False, inplace = True)

    #trace = go.Table(header=dict(values=['Country','Revenue', 'ROAS']),
                 #cells=dict(values=[rev_country.Country.values, np.round(rev_country.Revenue.values, 2), np.round(rev_country.ROAS.values, 1)]), domain=dict(x=[0.52, 1],y=[0, 1]))
            
    #trace1 = go.Pie(values=rev_country.localSpend, labels=rev_country.Country, hole=.4, name = 'localSpend', domain=dict(x=[0, 0.23],y=[0, 1]), title_text = 'Cost', textposition='inside', textinfo='label', hoverinfo="label+value")
    #trace2 = go.Pie(values=rev_country.Revenue, labels=rev_country.Country, hole=.4, name = 'Revenue', domain=dict(x=[0.26, 0.49],y=[0, 1]), title_text = 'Revenue', textposition='inside', textinfo='label', hoverinfo="label+value")
    
    
    #fig_dough = go.Figure(data = [trace,trace1, trace2])
    #fig_dough.update_layout(title_text="ASA Breakdown by Country")

    path = 'C:\\Users\\User\\Documents\\Python Scripts'

    with open(join(path,'Asa_Soc.html'), 'w') as f:
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
        #f.write(fig_camp_.to_html(full_html=False, include_plotlyjs='cdn'))
        #f.write(fig_dough.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_key.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(figkey_tab.to_html(full_html=False, include_plotlyjs='cdn'))
        #f.write(fig_key_sub.to_html(full_html=False, include_plotlyjs='cdn'))
        
        
        
        
           


def download_campaigns_report():
    # URL, where we through out request
    url = "https://api.searchads.apple.com/api/v3/reports/campaigns"

    # We call our function, that creates a JSON request for us
    report = create_campaigns_report()

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
    url = "https://api.searchads.apple.com/api/v3/reports/campaigns/{}/keywords".format(campaignId)

    # We call our function, that creates a JSON request for us
    report = create_keywords_report()

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
    main()