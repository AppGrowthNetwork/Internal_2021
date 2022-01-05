import requests   
from pandas.io.json import json_normalize 
import pandas as pd  
from os.path import join
import os
from appsflyer import AppsFlyer

from plotly.offline import plot
import plotly.express as px
from plotly.graph_objs import *
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots


from googleads import adwords, oauth2
import io
from datetime import datetime, timedelta
import numpy as np

import locale
import sys
import _locale

access_token = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwia2lkIjpudWxsfQ..mJftZSX3b7czdpzZ.alzUOEivVQkJUhuLQO4J6vIadUTZ9R8PGBblb7erDgwcL7ZTeXMAtf0b6q1nBMrqh8J-JCoFg0i3LAokCeAGqrhxRlxJ6p64QdzPq61Xl_DI9wFynSJcr_k85dCelZsDRvEk70CVKo7DPqdo1n4-cs82N5zkJsYYeNNtpSisoj-m4HoRbFyEglVRBy4w6IKMUOz9L4afPAGxKZPPOE-cYb28ITK7YlqDvjGQOCzxitCVy9mG5WWyP2MEXVS1r0ArEIK_G3Tb_EThOL6L9XSgqLk.c7IJOpflBuWjO_AFxcHeqA"

ORG_ID = "1723370" # Your ORG_ID, you can find in Apple Search ads, cabinet in the top right menu

START_DATE = "2021-09-20"
END_DATE = (datetime.now() - timedelta(days = 1)).strftime("%Y-%m-%d")


## table of total installs.

def main():

    app_id = "id902026228"
    api_token = "94c1018e-ab1a-4eb2-95b4-b46dc0c5de89"

    #df_af_asa = get_geo_by_date_report(app_id, api_token, START_DATE, END_DATE)
    #print(df_af.sort_values('af_purchase (Sales in CAD)', ascending = False))
    #df_af_asa.to_csv('AF_santa_rev.csv')
    #print(df_af.columns)
    #print(df_af_asa['Media Source (pid)'].unique())
    #df_af_asa = df_af_asa[df_af_asa['Media Source (pid)'] == 'Apple Search Ads'].reset_index(drop = True)
    #print(df_af)
    
    # We call our main delivery-boy function to do all the work
    df = download_campaigns_report(START_DATE, END_DATE)
    #df_19 = download_campaigns_report(START_DATE_, END_DATE_)

    # We rename some columns names to make them more beautiful
    new_columns = {x: x.replace("metadata.","") for x in df.columns}
    df = df.rename(columns=new_columns)
    #df_19 = df_19.rename(columns= new_columns)

    # We fill empty rows with zeros
    df = df.fillna(0)
    #df_19 = df_19.fillna(0)

    #if len(df.columns) == 0:
        #df = pd.DataFrame(columns = columns_, index = range(0,1))
        #df.iloc[0] = [0] * 18

    custom = pd.DataFrame()
    for i in range(0,len(df)):
        temp = pd.DataFrame()
        for j in range(0,len(df['granularity'][i])):
            data = df['granularity'][i][j]
            data['campaignId'] = df.loc[i,'campaignId']
            data['campaignName'] = df.loc[i,'campaignName']
            data['Country'] = df.loc[i,'countryOrRegion' ]
            if 'avgCPA' in df['granularity'][i][j].keys():
                data['avgCPA'] = float(df['granularity'][i][j]['avgCPA']['amount'])
                data['avgCPT'] = float(df['granularity'][i][j]['avgCPT']['amount'])
                data['localSpend'] = df['granularity'][i][j]['localSpend']['amount']
            concat = pd.DataFrame(data, index = range(0,1))
            temp= pd.concat([temp, concat], axis = 0)
        custom = pd.concat([custom, temp], axis = 0)
    custom.reset_index(drop = True, inplace= True)
    custom = custom.fillna(0)
    custom['localSpend'] = custom['localSpend'].astype('float')

    #print(custom.columns)
    #print(custom['campaignName'].unique())

    custom_date = custom.groupby(['date']).sum().reset_index()
    #df_af_asa_con = df_af_asa.groupby(['Date']).sum().reset_index()
    #df_af_con = df_af_asa_con[['Date','Installs','Total Revenue']]
    #df_af_asa = df_af_asa.groupby(['Date', 'Country']).sum().reset_index()

    ###REV CONCAT WITH AF
    #revenue = pd.concat([custom_date, df_af_con], axis =1)
    revenue = custom_date.copy()
    #revenue['ARPU'] = revenue['Total Revenue'] / revenue['Installs']
    #revenue['Rev'] = revenue['ARPU'] * revenue['installs']

    #print(revenue)
    #print(revenue.columns)

    start_date_ = '2021-07-01'
    end_date_ = (datetime.now() - timedelta(days= 1))

    #start_date = '2019-10-16'
    #end_date = (datetime.now() - timedelta(days= 367))

    client_id = '422898392645-kq6mc00a3h0c857qdp8jsre7pi9gjntv.apps.googleusercontent.com'
    client_secret = 'AH28CNr8Lnuuhw-irN6smI_O'
    refresh_token = '1//05DNqq3W92nMPCgYIARAAGAUSNwF-L9IrWwdXzq6DkXHrDAaTPecYmgHBLcF6vjLaLMv2K3woigZW5b-Zug1LlAxmptmw9YCXl_Y'
    developer_token = 'PJY5mhXidEqXfbuCZES9PQ'
    client_customer_id = '681-586-9193'

    #api_id = "com.ugroupmedia.pnp14"
    #api_token = "94c1018e-ab1a-4eb2-95b4-b46dc0c5de89"


    df = get_campaign_performance_report(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date_, end_date_)
    #df_19 = get_campaign_performance_report(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date, end_date)
    
    end_date_ = end_date_.strftime('%Y-%m-%d')

    #df_af_g = get_geo_by_date_report(api_id, api_token, start_date_, end_date_)

    
    #Pick uac campaigns
    index_unified = [i for i in df.index if df.loc[i, 'Campaign serving status'] == 'eligible']
    g = df.iloc[index_unified,:]

    #index_uac = [i for i in df_19.index if 'NB' not in df_19.loc[i,'Campaign'] and 'BRANDED' not in df_19.loc[i,'Campaign'] and '2020' in df_19.loc[i,'Campaign'] and df_19.loc[i, 'Campaign serving status'] == 'eligible']
    #g_19 = df_19

    g['Cost'] = g['Cost'] / 1000000

    g = g.groupby('Day').sum().reset_index()
    #print(g)
    #df_af_g = get_geo_by_date_report(api_id, api_token, start_date_, end_date_)
    #df_af_g = df_af_g[df_af_g['Media Source (pid)'] == 'googleadwords_int']
    
    #print(df_af_g.columns)
    #df_date = df_af_g.groupby(['Date']).sum().reset_index()
    #df_level = df_date[['Date','af_subscribe (Sales in CAD)']]

    #g = pd.merge(g, df_level, how = 'left', left_on = 'Day', right_on = 'Date')
    #g['Day'] = pd.to_datetime(g['Day'], format ='%Y-%m-%d')
    #for i in range(len(g)):
        #if (g.loc[i,'Day'] < pd.to_datetime('2020-11-30', format='%Y-%m-%d')) | (g.loc[i,'Day'] > pd.to_datetime('2020-12-02', format='%Y-%m-%d')):  
            #g.loc[i,'Total conv. value'] = g.loc[i,'Total conv. value'] + g.loc[i,'af_subscribe (Sales in CAD)']
    #g['Day'] = g['Day'].apply(lambda x: x.strftime('%Y-%m-%d'))

    #mapping = {'AW':'ABW','AF':'AFG','AO':'AGO','AI':'AIA','AX':'ALA','AL':'ALB','AD':'AND','AE':'ARE','AR':'ARG','AM':'ARM','AS':'ASM','AQ':'ATA','TF':'ATF','AG':'ATG','AU':'AUS','AT':'AUT','AZ':'AZE','BI':'BDI','BE':'BEL','BJ':'BEN','BQ':'BES','BF':'BFA','BD':'BGD','BG':'BGR','BH':'BHR','BS':'BHS','BA':'BIH','BL':'BLM','BY':'BLR','BZ':'BLZ','BM':'BMU','BO':'BOL','BR':'BRA','BB':'BRB','BN':'BRN','BT':'BTN','BV':'BVT','BW':'BWA','CF':'CAF','CA':'CAN','CC':'CCK','CH':'CHE','CL':'CHL','CN':'CHN','CI':'CIV','CM':'CMR','CD':'COD','CG':'COG','CK':'COK','CO':'COL','KM':'COM','CV':'CPV','CR':'CRI','CU':'CUB','CW':'CUW','CX':'CXR','KY':'CYM','CY':'CYP','CZ':'CZE','DE':'DEU','DJ':'DJI','DM':'DMA','DK':'DNK','DO':'DOM','DZ':'DZA','EC':'ECU','EG':'EGY','ER':'ERI','EH':'ESH','ES':'ESP','EE':'EST','ET':'ETH','FI':'FIN','FJ':'FJI','FK':'FLK','FR':'FRA','FO':'FRO','FM':'FSM','GA':'GAB','GB':'GBR','GE':'GEO','GG':'GGY','GH':'GHA','GI':'GIB','GN':'GIN','GP':'GLP','GM':'GMB','GW':'GNB','GQ':'GNQ','GR':'GRC','GD':'GRD','GL':'GRL','GT':'GTM','GF':'GUF','GU':'GUM','GY':'GUY','HK':'HKG','HM':'HMD','HN':'HND','HR':'HRV','HT':'HTI','HU':'HUN','ID':'IDN','IM':'IMN','IN':'IND','IO':'IOT','IE':'IRL','IR':'IRN','IQ':'IRQ','IS':'ISL','IL':'ISR','IT':'ITA','JM':'JAM','JE':'JEY','JO':'JOR','JP':'JPN','KZ':'KAZ','KE':'KEN','KG':'KGZ','KH':'KHM','KI':'KIR','KN':'KNA','KR':'KOR','KW':'KWT','LA':'LAO','LB':'LBN','LR':'LBR','LY':'LBY','LC':'LCA','LI':'LIE','LK':'LKA','LS':'LSO','LT':'LTU','LU':'LUX','LV':'LVA','MO':'MAC','MF':'MAF','MA':'MAR','MC':'MCO','MD':'MDA','MG':'MDG','MV':'MDV','MX':'MEX','MH':'MHL','MK':'MKD','ML':'MLI','MT':'MLT','MM':'MMR','ME':'MNE','MN':'MNG','MP':'MNP','MZ':'MOZ','MR':'MRT','MS':'MSR','MQ':'MTQ','MU':'MUS','MW':'MWI','MY':'MYS','YT':'MYT','NA':'NAM','NC':'NCL','NE':'NER','NF':'NFK','NG':'NGA','NI':'NIC','NU':'NIU','NL':'NLD','NO':'NOR','NP':'NPL','NR':'NRU','NZ':'NZL','OM':'OMN','PK':'PAK','PA':'PAN','PN':'PCN','PE':'PER','PH':'PHL','PW':'PLW','PG':'PNG','PL':'POL','PR':'PRI','KP':'PRK','PT':'PRT','PY':'PRY','PS':'PSE','PF':'PYF','QA':'QAT','RE':'REU','RO':'ROU','RU':'RUS','RW':'RWA','SA':'SAU','SD':'SDN','SN':'SEN','SG':'SGP','GS':'SGS','SH':'SHN','SJ':'SJM','SB':'SLB','SL':'SLE','SV':'SLV','SM':'SMR','SO':'SOM','PM':'SPM','RS':'SRB','SS':'SSD','ST':'STP','SR':'SUR','SK':'SVK','SI':'SVN','SE':'SWE','SZ':'SWZ','SX':'SXM','SC':'SYC','SY':'SYR','TC':'TCA','TD':'TCD','TG':'TGO','TH':'THA','TJ':'TJK','TK':'TKL','TM':'TKM','TL':'TLS','TO':'TON','TT':'TTO','TN':'TUN','TR':'TUR','TV':'TUV','TW':'TWN','TZ':'TZA','UG':'UGA','UA':'UKR','UM':'UMI','UY':'URY','US':'USA','UZ':'UZB','VA':'VAT','VC':'VCT','VE':'VEN','VG':'VGB','VI':'VIR','VN':'VNM','VU':'VUT','WF':'WLF','WS':'WSM','YE':'YEM','ZA':'ZAF','ZM':'ZMB','ZW':'ZWE'}

    #lista = list(df_af_g.Country.unique())
    #print(lista)
    #lista.pop(137)
    #index = [i for i in df_af_g.index if df_af_g.loc[i, 'Country'] in lista]
    #index_asa = [i for i in df_af_asa.index if df_af_asa.loc[i, 'Country'] in lista]
    #df_af_g = df_af_g.loc[index]
    #df_af_asa = df_af_asa.loc[index_asa]
    #df_af_g['Country'] = df_af_g.Country.apply(lambda x: np.where(x == 'UK', 'GB', x))
    #df_af_g['iso_alpha'] = df_af_g.Country.map(mapping) 
    #df_fig_af_1 = df_af_g.groupby('iso_alpha').sum().reset_index()
    #df_af_asa['Country'] = df_af_asa.Country.apply(lambda x: np.where(x == 'UK', 'GB', x))
    #df_af_asa['iso_alpha'] = df_af_asa.Country.map(mapping) 
    #df_fig_af_2 = df_af_asa.groupby('iso_alpha').sum().reset_index()

    #df_fig_af = pd.concat([df_fig_af_1, df_fig_af_2], axis = 0)
    #df_fig_af = df_fig_af.groupby('iso_alpha').sum().reset_index()

    ### YOU DON'T NEED FB YET
    path = 'C:\\Users\\User\\Documents\\Python Scripts'
    df_fb = pd.read_csv(join(path,'fb_db_keap.csv'))
    df_fb['impr'] = df_fb['impressions']
    df_fb.drop(['Unnamed: 0','impressions', 'CPI'], axis = 1, inplace = True)
    #print(df_fb)
    df_fb = df_fb.groupby('date_start').sum().reset_index()
    print(df_fb)

    #print(g.info)
    #print(revenue.info)
    uni = pd.merge(g , revenue, left_on = 'Day', right_on = 'date', how = 'left')
    uni = uni.fillna(0)
    uni = pd.merge(uni, df_fb, left_on = 'Day', right_on = 'date_start', how = 'left')
    #print(uni.head(10))
    #print(uni.columns)

    #Deleted FB columns from operations
    uni['Revenue'] = uni['Total conv. value'] + uni['Revenue']
    uni['Total_Cost'] = uni['localSpend'] + uni['Cost'] + uni['spend']
    uni['Total_Installs'] = uni['Conversions'] + uni['installs'] + uni['actions']
    uni['Total_Impressions'] = uni['impressions'] + uni['Impressions'] + uni['impr']
    uni['Total_Taps'] = uni['Clicks'] + uni['taps'] + uni['inline_link_clicks']
    uni['TTR'] = uni['Total_Taps'] / uni['Total_Impressions']
    uni['convRate'] = uni['Total_Installs'] / uni['Total_Taps']
    uni['ARPU'] = uni['Revenue'] / uni['Total_Installs']
    uni['ROAS'] = uni['Revenue'] / uni['Total_Cost']
    uni['avgCPI'] = uni['Total_Cost'] / uni['Total_Installs']
    
    revenue['Source'] = 'ASA'
    g['Source'] = 'Adwords'
    df_fb['Source'] = 'Facebook'

    total_asa = pd.DataFrame(data = revenue, columns = ['date','impressions', 'taps','installs','localSpend', 'Rev','Source'], index = revenue.index)
    total_g = pd.DataFrame(data = g, columns = ['Day','Impressions','Clicks','Conversions', 'Cost', 'Total conv. value', 'Source'] , index = g.index )
    total_fb = pd.DataFrame(data = df_fb, columns = ['date_start','impr','inline_link_clicks','actions', 'spend', 'Revenue','Source'] , index = df_fb.index )
    cols = ['Day','Impressions', 'Taps', 'Installs', 'Cost', 'Revenue', 'Source']
    total_asa.columns = cols 
    total_g.columns = cols
    total_fb.columns = cols
    
    #concat with fb
    totals = pd.concat([total_asa, total_g, total_fb], axis =0)
    print(totals)
    totals.reset_index(drop = True, inplace = True)
    totals['Day'] = pd.to_datetime(totals['Day'], format = '%Y-%m-%d')
    print(totals)

    fig_3 = make_subplots( rows=1, cols=3, column_widths=[0.32, 0.32, 0.32], specs=[[{'secondary_y':True}, {'secondary_y':True}, {'secondary_y':True}]],
                    subplot_titles=("Daily Adwords Conversions vs. CPI", "Daily Facebook Conversions vs CPI", "Daily ASA Conversions vs CPI" ))

    # Add traces
    fig_3.add_trace(go.Scatter(x=totals[totals['Source'] == 'Adwords'].Day, y=totals[totals['Source'] == 'Adwords']['Cost']  / totals[totals['Source'] == 'Adwords']['Installs'] ,
                    mode='lines+markers',
                    name='CPI', marker_color = '#EF553B'), secondary_y = True, row =1 , col = 1)
    fig_3.add_trace(go.Scatter(x=totals[totals['Source'] == 'Adwords'].Day, y=totals[totals['Source'] == 'Adwords']['Installs'] ,
                    mode='lines+markers',
                    name='Installs', marker_color = 'cyan'), row =1 , col = 1)
    fig_3.add_trace(go.Scatter(x=totals[totals['Source'] == 'Facebook'].Day, y=totals[totals['Source'] == 'Facebook']['Cost']  / totals[totals['Source'] == 'Facebook']['Installs'] ,
                    mode='lines+markers',
                    name='CPI', marker_color = '#EF553B', showlegend = False), secondary_y = True, row =1 , col = 2)
    fig_3.add_trace(go.Scatter(x=totals[totals['Source'] == 'Facebook'].Day, y=totals[totals['Source'] == 'Facebook']['Installs'] ,
                    mode='lines+markers',
                    name='Installs', marker_color = 'cyan', showlegend = False), row =1 , col = 2)
    fig_3.add_trace(go.Scatter(x=totals[totals['Source'] == 'ASA'].Day, y=totals[totals['Source'] == 'ASA']['Cost']  / totals[totals['Source'] == 'ASA']['Installs'] ,
                    mode='lines+markers',
                    name='CPI', marker_color = '#EF553B', showlegend = False), secondary_y = True, row =1 , col = 3)
    fig_3.add_trace(go.Scatter(x=totals[totals['Source'] == 'ASA'].Day, y=totals[totals['Source'] == 'ASA']['Installs'] ,
                    mode='lines+markers',
                    name='Installs', marker_color = 'cyan', showlegend = False), row =1 , col = 3)

    fig_3.update_layout( height = 600, title_text = 'CPIs across three media sources')
            

    uni = uni[['Day', 'Revenue', 'Total_Cost', 'Total_Installs', 'Total_Impressions', 'Total_Taps', 'TTR', 'convRate', 'ARPU', 'ROAS', 'avgCPI']]

    #uni19 = pd.merge(g_19.groupby('Day').sum().reset_index(), custom_date_19, left_on = 'Day', right_on = 'date', how = 'left')

    #uni19 = uni19.fillna(0)

    #uni19['Total_Cost'] = uni19['localSpend'] + uni19['Cost']
    ##uni19['Total_Installs'] = uni19['Conversions'] + uni19['installs']
    #uni19['Total_Impressions'] = uni19['impressions'] + uni19['Impressions']
    #uni19['Total_Taps'] = uni19['Clicks'] + uni19['taps']
    #uni19['TTR'] = uni19['Total_Taps'] / uni19['Total_Impressions']
    #uni19['convRate'] = uni19['Total_Installs'] / uni19['Total_Taps']
    #uni19['avgCPI'] = uni19['Total_Cost'] / uni19['Total_Installs']

    #uni19 = uni19[['Day', 'Total_Cost', 'Total_Installs', 'Total_Impressions', 'Total_Taps', 'TTR', 'convRate', 'avgCPI']]

    #uni19['Day'] = uni19['Day'].apply(lambda x: x.replace('2019-10', "Oct"))
    #uni19['Day'] = uni19['Day'].apply(lambda x: x.replace('2019-11', "Nov"))
    

    #uni20 = uni.copy()
    #uni20['Day'] = uni20['Day'].apply(lambda x: x.replace('2020-10', "Oct"))
    #uni20['Day'] = uni20['Day'].apply(lambda x: x.replace('2020-11', "Nov"))
    

    #fig_map_conv = px.choropleth(df_fig_af, locations="iso_alpha", color="Installs", hover_name="iso_alpha", color_continuous_scale=px.colors.sequential.Plasma)
    #fig_map_rev = px.choropleth(df_fig_af, locations="iso_alpha", color="Total Revenue", hover_name="iso_alpha", color_continuous_scale=px.colors.sequential.Plasma)
    #fig_map_conv.update_layout(
    #title_text="Installs by Geolocation")
    #fig_map_rev.update_layout(
    #title_text="Revenue by Geolocation")

    totals_grouped = totals.groupby('Day').sum().reset_index()
    totals_grouped.sort_values('Day', ascending = True, inplace = True)
    totals_grouped['Day'] = totals_grouped['Day'].apply(lambda x: x.strftime('%b-%d'))
    #print(totals_grouped)

    totals.sort_values('Day', ascending = True, inplace = True)
    totals.reset_index(drop = True, inplace = True)
    totals['Day'] = totals['Day'].apply(lambda x: x.strftime('%b-%d'))
    totals['Day'] = pd.to_datetime(totals['Day'], format = '%b-%d')
    #print(totals)
    totals = totals.groupby(['Day','Source']).sum().reset_index()
    totals['Day'] = totals['Day'].apply(lambda x: x.strftime('%b-%d'))
    print(totals)

    fig = make_subplots( rows=1, cols=1, specs=[[{"secondary_y": True}]]) #, {"secondary_y": True}, column_widths=[1], subplot_titles=() "Total Daily Keap Installs vs. Daily CPI", "Cumulative KPIs Keap", 


    # Add traces
    #fig.add_trace(go.Scatter(x=totals_grouped['Day'], y=totals_grouped['Cost'].cumsum(),
    #                mode='lines+markers',
    #                name='Cost', marker_color='rgba(228,26,28, .9)'), secondary_y=False, row = 1, col = 2)
    #fig.add_trace(go.Scatter(x=totals_grouped['Day'], y=totals_grouped['Revenue'].cumsum() / totals_grouped['Cost'].cumsum() ,
    #                mode='lines+markers',
    #                name='ROAS', marker_color='#3366CC', yaxis='y2'),secondary_y=True, row = 1, col = 2)
    #fig.add_trace(go.Scatter(x=totals_grouped['Day'], y=totals_grouped['Revenue'].cumsum() / totals_grouped['Installs'].cumsum() ,
    #                mode='lines+markers',
    #                name='ARPU', marker_color='#AB63FA', yaxis='y2'),secondary_y=True, row = 1, col = 2)
    
    

    
    fig.add_trace(go.Bar(x=totals[totals['Source'] == 'Adwords']['Day'], y= totals[totals['Source'] == 'Adwords']['Installs'],
                    name='Adwords', marker_color = 'rgb(204,204,204)'), row=1, col=1)
    fig.add_trace(go.Bar(x=totals[totals['Source'] == 'ASA']['Day'], y=totals[totals['Source'] == 'ASA']['Installs'],
                    name='ASA', marker_color = 'rgba(255,127,0, 1)'), row=1, col=1)
    fig.add_trace(go.Bar(x=totals[totals['Source'] == 'Facebook']['Day'], y=totals[totals['Source'] == 'Facebook']['Installs'],
                    name='Facebook', marker_color = 'rgba(0,134,149, 1)'), row=1, col=1)
    #fig.add_trace(go.Scatter(x=totals_grouped['Day'], y=totals_grouped['Revenue'].cumsum(),
    #                mode='lines+markers',
    #                name='Revenue', marker_color = 'LightSkyBlue'), secondary_y=False, row = 1, col = 2) 
    fig.add_trace(go.Scatter(x=totals_grouped['Day'], y=totals_grouped['Installs'],
                    mode='lines+markers',
                    name='Installs', marker_color='#00CC96'), secondary_y=False, row=1, col=1)
    fig.add_trace(go.Scatter(x=totals_grouped['Day'], y=totals_grouped['Cost'] / totals_grouped['Installs'],
                    mode='lines+markers',
                    name='avgCPI', marker_color='rgba(242,183,1, 1)'), secondary_y=True, row=1, col=1) 
    #fig.add_trace(go.Bar(x=totals[totals['Source'] == 'Adwords']['Day'], y=totals[totals['Source'] == 'Adwords']['Revenue'].cumsum(),
    #                name='Adwords', marker_color = 'rgb(204,204,204)', showlegend = False), row = 1, col = 2)
    #fig.add_trace(go.Bar(x=totals[totals['Source'] == 'ASA']['Day'], y=totals[totals['Source'] == 'ASA']['Revenue'].cumsum(),
    #                name='ASA', marker_color = 'rgba(255,127,0, 1)', showlegend = False), row = 1, col = 2)
    #fig.add_trace(go.Bar(x=totals[totals['Source'] == 'Facebook']['Day'], y=totals[totals['Source'] == 'Facebook']['Revenue'].cumsum(),
    #                name='Facebook', marker_color = 'rgba(0,134,149, 1)', showlegend = False), row = 1, col = 2)
      
    
    
    
  
    fig.update_layout(barmode = 'stack', title_text = "Total Daily Keap Installs vs. Daily CPI")


    fig_dough = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]],
            subplot_titles=['Installs', 'Spend', 'Revenue'])
            
    fig_dough.add_trace(go.Pie(values=totals.Installs, labels=totals.Source, hole=.4, name = 'Installs'),1, 1)
    fig_dough.add_trace(go.Pie(values=totals.Cost, labels=totals.Source,hole=.4, name = 'Cost'),1, 2)
    fig_dough.add_trace(go.Pie(values=totals.Revenue, labels=totals.Source, hole=.4, name = 'Revenue'),1, 3)
    fig_dough.update_traces(hoverinfo="label+percent+name+value")

    fig_dough.update_layout(
         title={ 'text': "Aggregated KPI's by Source", 'y':1, 'x':0.5, 'xanchor': 'center','yanchor': 'top'})


    #fig19 = make_subplots( rows=2, cols=2, column_widths=[0.5, 0.5], row_heights=[0.4, 0.6], specs=[[{"secondary_y": True}, {"secondary_y": True}],[ { "colspan": 2, "secondary_y": True}   , None]],
     #               subplot_titles=("Total Impressions 2020 vs. 2019", "Total Installs 2020 vs. 2019", "Conversion Rate 2020 vs. 2019" ))


    #uni20['Day'] = pd.to_datetime(uni20['Day'], format='%b-%d')
    #uni20 = uni20.groupby(['Day']).sum().reset_index().sort_values('Day', ascending = True)
    #uni20['Day'] = uni20['Day'].apply(lambda x: x.strftime('%b-%d'))

    #uni19['Day'] = pd.to_datetime(uni19['Day'], format='%b-%d')
    #uni19 = uni19.groupby(['Day']).sum().reset_index().sort_values('Day', ascending = True)
    #uni19['Day'] = uni19['Day'].apply(lambda x: x.strftime('%b-%d'))

    # Add traces
    #fig19.add_trace(go.Scatter(x=uni20.Day, y=uni20.Total_Impressions,
     #               mode='lines',
      #              name='Impressions'), row=1, col=1)
    #fig19.add_trace(go.Scatter(x=uni20.Day, y=uni20.Total_Installs,
     #               mode='lines',
      #              name='Installs', marker_color='rgba(242,183,1, 1)' ), row=1, col=2)

    #fig19.add_trace(go.Scatter(x=uni19.Day, y=uni19.Total_Installs,
     #               mode='lines',
      #              name='Installs-19', yaxis='y2'), row=1, col=2)

    #fig19.add_trace(go.Scatter(x=uni19.Day, y=uni19.Total_Impressions,
       #             mode='lines',
       #             name='Impressions-19', yaxis='y2'), row=1, col=1)

    #fig19.add_trace(go.Scatter(x=uni20.Day, y=uni20.convRate,
     #               mode='lines',
     #               name='convRate'), row= 2, col = 1)

    #fig19.add_trace(go.Scatter(x=uni19.Day, y=uni19.convRate,
       #             mode='lines',
       #             name='convRate-19', yaxis='y2'), row= 2, col = 1)
    
    #fig_tab = go.Figure(data=[go.Table(header=dict(values=['Day','convRate20', 'convRate19']),
       #          cells=dict(values=[uni20.Day.values, np.round(uni.convRate.values, 2), np.round(uni19.convRate.values,2)]))
       #              ])

    with open('Aggregated_Keap.html', 'w') as f:
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
        #f.write(fig_rev.to_html(full_html=False, include_plotlyjs='cdn'))
        #f.write(fig_cum.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_dough.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_3.to_html(full_html=False, include_plotlyjs='cdn'))
        #f.write(fig_map_rev.to_html(full_html=False, include_plotlyjs='cdn'))
        #f.write(fig19.to_html(full_html=False, include_plotlyjs='cdn'))
        #f.write(fig_tab.to_html(full_html=False, include_plotlyjs='cdn'))
    

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
    SELECT CampaignName, Date, ServingStatus, Clicks, Impressions, Cost, Conversions, ConversionValue
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
        
        
           


def download_campaigns_report(start_date, end_date):
    # URL, where we through out request
    url = "https://api.searchads.apple.com/api/v4/reports/campaigns"
    #"https://api.searchads.apple.com/api/v4/campaigns" -H "Authorization: Bearer {access_token}" \
    # We call our function, that creates a JSON request for us
    report = create_campaigns_report(start_date, end_date)

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
