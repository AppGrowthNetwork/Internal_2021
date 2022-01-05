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
from datetime import datetime, time, timedelta
import numpy as np


access_token = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwia2lkIjpudWxsfQ..NI45XLvGW2ZuX_Ni.yS5NlKEqJodxb3IalLNBAKp0DA1-ce4gIz7bjN8lJru8IoFgHdOMBPqGvsONhdL9XLyjds3yZ3tQng0-fEctqvCBdU24LoKitVoddvCNGDUkGmngjY-I6iExux0k8xAeLG8Xun18X1xe-lcxsO82A-gu-9c16DFSiCWgBvrFQ8JAaKGhCIT6eA5c16FLym9Ik0_heqneovZPiYgYBETmjq5B3ilSHquwV_L9Jl4O6HUwX5NiL9_OJsTc3U31fYMZeO0uZ4I1yWCtDu3jM7NDUyo.YiZphIzdwqk-Hp2mKJwopA"

ORG_ID = "396670" # Your ORG_ID, you can find in Apple Search ads, cabinet in the top right menu

START_DATE = "2021-09-02"
END_DATE = (datetime.now() - timedelta(days = 1)).strftime("%Y-%m-%d")

path = 'C:\\Users\\User\\Downloads\\Santa_Admin_ASA_Cert\\'
ORG_ID = "396670" # Your ORG_ID, you can find in Apple Search ads, cabinet in the top right menu
APPLE_CERT = (join(path, 'AGN1.pem'), join(path, 'AGN1.key'))


## table of total installs.

def main():

    app_id = "id902026228"
    api_token = "6ebbb043-2c07-4972-8678-9687ae87ee9a"

    start_DATE_ = '2021-09-10'
    end_DATE_ = (datetime.now() - timedelta(days= 1)).strftime("%Y-%m-%d")

    df_af_asa = get_geo_by_date_report(app_id, api_token, start_DATE_, end_DATE_)
    #df_af_asa = df_af_asa[df_af_asa['Media Source (pid)'] == 'googleadwords_int']
    #print(df_af_asa['Campaign (c)'].unique())

    api_id = "com.ugroupmedia.pnp14"
    
    df_af_and = get_geo_by_date_report(api_id, api_token, start_DATE_, end_DATE_)

    df_af = pd.concat([df_af_asa, df_af_and], axis = 0)

    #df_af_and = df_af_and[df_af_and['Media Source (pid)'] == 'googleadwords_int']

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

    custom_date = custom.groupby(['date', 'campaignName']).sum().reset_index()
    custom_date['Revenue'] = 0

    start_date_ = '2021-09-10'
    end_date_ = (datetime.now() - timedelta(days= 1))

    #start_date = '2019-10-16'
    #end_date = (datetime.now() - timedelta(days= 367))

    client_id = '422898392645-kq6mc00a3h0c857qdp8jsre7pi9gjntv.apps.googleusercontent.com'
    client_secret = 'AH28CNr8Lnuuhw-irN6smI_O'
    refresh_token = '1//05LY8e-9GfD1lCgYIARAAGAUSNwF-L9IrMOJp5otbd6lxLQCfUeDCBQ6CYyGUSsy2O4hmD0iyHrkx4r-kF_9g2Xe9zv75p2uZGxw'
    developer_token = 'PJY5mhXidEqXfbuCZES9PQ'
    client_customer_id = '3096033436'

    #api_id = "com.ugroupmedia.pnp14"
    #api_token = "94c1018e-ab1a-4eb2-95b4-b46dc0c5de89"

    ##GOOGLE

    df = get_campaign_performance_report(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date_, end_date_)
    #df_19 = get_campaign_performance_report(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date, end_date)
    
    idx = [i for i in df.index if '2021' in df.loc[i, 'Campaign']]
    df = df.loc[idx, :].reset_index()
    #Pick uac campaigns
    index_uac = [i for i in df.index if 'NB' not in df.loc[i,'Campaign'] and 'BRANDED' not in df.loc[i,'Campaign'] and 'UAC' in df.loc[i,'Campaign']]
    uac_campaigns = df.iloc[index_uac,:]
    
    #Pick nb campaigns
    index_nb = [i for i in df.index if 'BRANDED' not in df.loc[i,'Campaign'] and 'UAC' not in df.loc[i,'Campaign'] and 'S - NB' in df.loc[i,'Campaign']]
    nb_campaigns = df.iloc[index_nb,:]

    #Pick branded campaigns
    index_b = [i for i in df.index if 'UAC' not in df.loc[i,'Campaign'] and 'NB' not in df.loc[i,'Campaign'] and 'BRANDED' in df.loc[i,'Campaign']  ]
    b_campaigns = df.iloc[index_b,:]

    uac_campaigns['type'] = 'UAC'
    nb_campaigns['type'] = 'Non-Branded'
    b_campaigns['type'] = 'Branded'


    unified = pd.concat([uac_campaigns, nb_campaigns, b_campaigns], axis = 0)
    g = unified.copy()

    g['Cost'] = g['Cost'] / 1000000

    g = g.groupby(['Day', 'Campaign']).sum().reset_index()

    ###FACEBOOK

    def type_df(df, type, notype):
            indx = [i for i in df.index if type in df.loc[i, 'campaign_name'] and notype not in df.loc[i, 'campaign_name']]
            new_df = df.loc[indx, :]
            return new_df

    path = 'C:\\Users\\User\\Documents\\Python Scripts'
    df_fb = pd.read_csv(join(path,'fb_santa21.csv'))
    aud_df = type_df(df_fb, 'AUD', 'ACQ')        
    aud_df['type'] = 'audience'

    acq_df = type_df(df_fb, 'ACQ', 'AUD')
    acq_df['type'] = 'acquisition'

    df_fb = pd.concat([aud_df, acq_df], axis = 0)
    df_fb = df_fb.groupby(['date_start', 'campaign_name']).sum().reset_index()
    print(df_fb)

    cols = ['Day', 'Campaign', 'Cost', 'Revenue', 'Conversions']
    g = g[['Day', 'Campaign','Cost','Total conv. value', 'Conversions']]
    g.columns = cols
    custom_date = custom_date[['date', 'campaignName', 'localSpend', 'Revenue', 'installs']]
    custom_date.columns = cols
    df_fb = df_fb[['date_start', 'campaign_name', 'spend', 'Revenue', 'actions']]
    df_fb.columns = cols

    custom_date['Source'] = 'Apple Search Ads'
    g['Source'] = 'googleadwords_int'
    df_fb['Source'] = 'Facebook Ads'

    uni = pd.concat([g, custom_date, df_fb], axis = 0)
    uni = uni.fillna(0)
    print(uni.head())
    print(uni.tail())

    

    uni['Day'] = pd.to_datetime(uni['Day'], format = '%Y-%m-%d')
    
    df_af['Date'] = pd.to_datetime(df_af['Date'], format = '%Y-%m-%d')

    totals_ = pd.merge(uni, df_af.groupby(['Date', 'Campaign (c)', 'Media Source (pid)']).sum().reset_index(), how = 'left', left_on = ['Day', 'Campaign', 'Source'], right_on = ['Date', 'Campaign (c)', 'Media Source (pid)'])
    idx = [i for i in totals_.index if 'Test' not in totals_.loc[i, 'Campaign']]
    totals_ = totals_.loc[idx, :]
    totals = totals_.groupby(['Day', 'Source']).sum().reset_index()
    new = [totals.loc[i, 'Cost'] if totals.loc[i,'Source'] == 'Facebook Ads' else totals.loc[i, 'Total Cost'] for i in totals.index]
    totals['Total Cost'] = new
    totals.sort_values('Day', inplace = True)
    start = '2021-10-09'
    totals = totals[totals['Day'] >= datetime.strptime(start, "%Y-%m-%d")]
    totals_grouped = totals.groupby('Day').sum().reset_index()
    totals['Day'] = totals['Day'].apply(lambda x: x.strftime('%Y-%m-%d'))
    totals_grouped['Day'] = totals_grouped['Day'].apply(lambda x: x.strftime('%Y-%m-%d'))
    

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

    
    figs_pnp = []

    fig = make_subplots( rows=1, cols=2, column_widths=[0.5, 0.5], specs=[[{"secondary_y": True}, {"secondary_y": True}]],
                subplot_titles=("Daily PNP Installs vs. Daily CPI", "Daily Revenue KPIs PNP" ))

    # Add traces
    fig.add_trace(go.Scatter(x=totals_grouped['Day'], y=totals_grouped['Total Cost'],
                    mode='lines+markers',
                    name='Cost', marker_color='rgba(228,26,28, .9)'), secondary_y=False, row = 1, col = 2)
    fig.add_trace(go.Scatter(x=totals_grouped['Day'], y=totals_grouped['af_purchase (Sales in CAD)'] / totals_grouped['Total Cost'] ,
                    mode='lines+markers',
                    name='ROAS', marker_color='#3366CC', yaxis='y2'),secondary_y=True, row = 1, col = 2)
    fig.add_trace(go.Scatter(x=totals_grouped['Day'], y=totals_grouped['af_purchase (Sales in CAD)'] / totals_grouped['Installs'],
                    mode='lines+markers',
                    name='ARPU', marker_color='#AB63FA', yaxis='y2'),secondary_y=True, row = 1, col = 2)
    
    fig.add_trace(go.Bar(x=totals[totals['Source'] == 'googleadwords_int']['Day'], y= totals[totals['Source'] == 'googleadwords_int']['Installs'],
                    name='Adwords', marker_color = 'rgb(204,204,204)'), row=1, col=1)
    fig.add_trace(go.Bar(x=totals[totals['Source'] == 'Apple Search Ads']['Day'], y=totals[totals['Source'] == 'Apple Search Ads']['Installs'],
                    name='ASA', marker_color = 'rgba(255,127,0, 1)'), row=1, col=1)
    fig.add_trace(go.Bar(x=totals[totals['Source'] == 'Facebook Ads']['Day'], y=totals[totals['Source'] == 'Facebook Ads']['Installs'],
                    name='Facebook', marker_color = 'rgba(0,134,149, 1)'), row=1, col=1)
    #fig.add_trace(go.Scatter(x=totals_grouped['Day'], y=totals_grouped['af_purchase (Sales in CAD)'],
    #                mode='lines+markers',
    #                name='Revenue', marker_color = 'LightSkyBlue'), secondary_y=False, row = 1, col = 2) 
    #fig.add_trace(go.Scatter(x=totals_grouped['Day'], y=totals_grouped['Installs'],
    #                mode='lines+markers',
    #                name='Installs', marker_color='#00CC96'), secondary_y=False, row=1, col=1)
    fig.add_trace(go.Scatter(x=totals_grouped['Day'], y=totals_grouped['Total Cost'] / totals_grouped['Installs'],
                    mode='lines+markers',
                    name='avgCPI', marker_color='rgba(242,183,1, 1)'), secondary_y=True, row=1, col=1) 
    fig.add_trace(go.Bar(x=totals[totals['Source'] == 'googleadwords_int']['Day'], y=totals[totals['Source'] == 'googleadwords_int']['af_purchase (Sales in CAD)'],
                    name='Adwords', marker_color = 'rgb(204,204,204)', showlegend = False), row = 1, col = 2)
    fig.add_trace(go.Bar(x=totals[totals['Source'] == 'Apple Search Ads']['Day'], y=totals[totals['Source'] == 'Apple Search Ads']['af_purchase (Sales in CAD)'],
                    name='ASA', marker_color = 'rgba(255,127,0, 1)', showlegend = False), row = 1, col = 2)
    fig.add_trace(go.Bar(x=totals[totals['Source'] == 'Facebook Ads']['Day'], y=totals[totals['Source'] == 'Facebook Ads']['af_purchase (Sales in CAD)'],
                    name='Facebook', marker_color = 'rgba(0,134,149, 1)', showlegend = False), row = 1, col = 2)
      
    fig.update_layout(barmode = 'stack')

    figs_pnp.append(fig)


    fig_dough = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]],
            subplot_titles=['Installs', 'Spend', 'Revenue'])
            
    fig_dough.add_trace(go.Pie(values=totals.Installs, labels=totals.Source, hole=.4, name = 'Installs'),1, 1)
    fig_dough.add_trace(go.Pie(values=totals['Total Cost'], labels=totals.Source,hole=.4, name = 'Cost'),1, 2)
    fig_dough.add_trace(go.Pie(values=totals['af_purchase (Sales in CAD)'], labels=totals.Source, hole=.4, name = 'Revenue'),1, 3)
    fig_dough.update_traces(hoverinfo="label+percent+name+value")

    fig_dough.update_layout(
         title={ 'text': "Aggregated KPI's by Source", 'y':1, 'x':0.5, 'xanchor': 'center','yanchor': 'top'})

    figs_pnp.append(fig_dough)

    dic_country = {"AF":"AFGHANISTAN","AX":"ÅLAND ISLANDS","AL":"ALBANIA","DZ":"ALGERIA","AS":"AMERICAN SAMOA","AD":"ANDORRA","AO":"ANGOLA","AI":"ANGUILLA","AQ":"ANTARCTICA","AG":"ANTIGUA AND BARBUDA","AR":"ARGENTINA","AM":"ARMENIA","AW":"ARUBA","AU":"AUSTRALIA","AT":"AUSTRIA","AZ":"AZERBAIJAN","BS":"BAHAMAS","BH":"BAHRAIN","BD":"BANGLADESH","BB":"BARBADOS","BY":"BELARUS","BE":"BELGIUM","BZ":"BELIZE","BJ":"BENIN","BM":"BERMUDA","BT":"BHUTAN","BO":"BOLIVIA, PLURINATIONAL STATE OF","BQ":"BONAIRE, SINT EUSTATIUS AND SABA","BA":"BOSNIA AND HERZEGOVINA","BW":"BOTSWANA","BV":"BOUVET ISLAND","BR":"BRAZIL","IO":"BRITISH INDIAN OCEAN TERRITORY","BN":"BRUNEI DARUSSALAM","BG":"BULGARIA","BF":"BURKINA FASO","BI":"BURUNDI","KH":"CAMBODIA","CM":"CAMEROON","CA":"CANADA","CV":"CAPE VERDE","KY":"CAYMAN ISLANDS","CF":"CENTRAL AFRICAN REPUBLIC","TD":"CHAD","CL":"CHILE","CN":"CHINA","CX":"CHRISTMAS ISLAND","CC":"COCOS (KEELING) ISLANDS","CO":"COLOMBIA","KM":"COMOROS","CG":"CONGO","CD":"CONGO, THE DEMOCRATIC REPUBLIC OF THE","CK":"COOK ISLANDS","CR":"COSTA RICA","CI":"CÔTE D'IVOIRE","HR":"CROATIA","CU":"CUBA","CW":"CURAÇAO","CY":"CYPRUS","CZ":"CZECH REPUBLIC","DK":"DENMARK","DJ":"DJIBOUTI","DM":"DOMINICA","DO":"DOMINICAN REPUBLIC","EC":"ECUADOR","EG":"EGYPT","SV":"EL SALVADOR","GQ":"EQUATORIAL GUINEA","ER":"ERITREA","EE":"ESTONIA","ET":"ETHIOPIA","FK":"FALKLAND ISLANDS (MALVINAS)","FO":"FAROE ISLANDS","FJ":"FIJI","FI":"FINLAND","FR":"FRANCE","GF":"FRENCH GUIANA","PF":"FRENCH POLYNESIA","TF":"FRENCH SOUTHERN TERRITORIES","GA":"GABON","GM":"GAMBIA","GE":"GEORGIA","DE":"GERMANY","GH":"GHANA","GI":"GIBRALTAR","GR":"GREECE","GL":"GREENLAND","GD":"GRENADA","GP":"GUADELOUPE","GU":"GUAM","GT":"GUATEMALA","GG":"GUERNSEY","GN":"GUINEA","GW":"GUINEA-BISSAU","GY":"GUYANA","HT":"HAITI","HM":"HEARD ISLAND AND MCDONALD ISLANDS","VA":"HOLY SEE (VATICAN CITY STATE)","HN":"HONDURAS","HK":"HONG KONG","HU":"HUNGARY","IS":"ICELAND","IN":"INDIA","ID":"INDONESIA","IR":"IRAN, ISLAMIC REPUBLIC OF","IQ":"IRAQ","IE":"IRELAND","IM":"ISLE OF MAN","IL":"ISRAEL","IT":"ITALY","JM":"JAMAICA","JP":"JAPAN","JE":"JERSEY","JO":"JORDAN","KZ":"KAZAKHSTAN","KE":"KENYA","KI":"KIRIBATI","KP":"KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF","KR":"KOREA, REPUBLIC OF","KW":"KUWAIT","KG":"KYRGYZSTAN","LA":"LAO PEOPLE'S DEMOCRATIC REPUBLIC","LV":"LATVIA","LB":"LEBANON","LS":"LESOTHO","LR":"LIBERIA","LY":"LIBYA","LI":"LIECHTENSTEIN","LT":"LITHUANIA","LU":"LUXEMBOURG","MO":"MACAO","MK":"MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF","MG":"MADAGASCAR","MW":"MALAWI","MY":"MALAYSIA","MV":"MALDIVES","ML":"MALI","MT":"MALTA","MH":"MARSHALL ISLANDS","MQ":"MARTINIQUE","MR":"MAURITANIA","MU":"MAURITIUS","YT":"MAYOTTE","MX":"MEXICO","FM":"MICRONESIA, FEDERATED STATES OF","MD":"MOLDOVA, REPUBLIC OF","MC":"MONACO","MN":"MONGOLIA","ME":"MONTENEGRO","MS":"MONTSERRAT","MA":"MOROCCO","MZ":"MOZAMBIQUE","MM":"MYANMAR","NA":"NAMIBIA","NR":"NAURU","NP":"NEPAL","NL":"NETHERLANDS","NC":"NEW CALEDONIA","NZ":"NEW ZEALAND","NI":"NICARAGUA","NE":"NIGER","NG":"NIGERIA","NU":"NIUE","NF":"NORFOLK ISLAND","MP":"NORTHERN MARIANA ISLANDS","NO":"NORWAY","OM":"OMAN","PK":"PAKISTAN","PW":"PALAU","PS":"PALESTINE, STATE OF","PA":"PANAMA","PG":"PAPUA NEW GUINEA","PY":"PARAGUAY","PE":"PERU","PH":"PHILIPPINES","PN":"PITCAIRN","PL":"POLAND","PT":"PORTUGAL","PR":"PUERTO RICO","QA":"QATAR","RE":"RÉUNION","RO":"ROMANIA","RU":"RUSSIAN FEDERATION","RW":"RWANDA","BL":"SAINT BARTHÉLEMY","SH":"SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA","KN":"SAINT KITTS AND NEVIS","LC":"SAINT LUCIA","MF":"SAINT MARTIN (FRENCH PART)","PM":"SAINT PIERRE AND MIQUELON","VC":"SAINT VINCENT AND THE GRENADINES","WS":"SAMOA","SM":"SAN MARINO","ST":"SAO TOME AND PRINCIPE","SA":"SAUDI ARABIA","SN":"SENEGAL","RS":"SERBIA","SC":"SEYCHELLES","SL":"SIERRA LEONE","SG":"SINGAPORE","SX":"SINT MAARTEN (DUTCH PART)","SK":"SLOVAKIA","SI":"SLOVENIA","SB":"SOLOMON ISLANDS","SO":"SOMALIA","ZA":"SOUTH AFRICA","GS":"SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS","SS":"SOUTH SUDAN","ES":"SPAIN","LK":"SRI LANKA","SD":"SUDAN","SR":"SURINAME","SJ":"SVALBARD AND JAN MAYEN","SZ":"SWAZILAND","SE":"SWEDEN","CH":"SWITZERLAND","SY":"SYRIAN ARAB REPUBLIC","TW":"TAIWAN, PROVINCE OF CHINA","TJ":"TAJIKISTAN","TZ":"TANZANIA, UNITED REPUBLIC OF","TH":"THAILAND","TL":"TIMOR-LESTE","TG":"TOGO","TK":"TOKELAU","TO":"TONGA","TT":"TRINIDAD AND TOBAGO","TN":"TUNISIA","TR":"TURKEY","TM":"TURKMENISTAN","TC":"TURKS AND CAICOS ISLANDS","TV":"TUVALU","UG":"UGANDA","UA":"UKRAINE","AE":"UNITED ARAB EMIRATES","GB":"UNITED KINGDOM","UK":"UNITED KINGDOM","US":"UNITED STATES","USA":"UNITED STATES","UM":"UNITED STATES MINOR OUTLYING ISLANDS","UY":"URUGUAY","UZ":"UZBEKISTAN","VU":"VANUATU","VE":"VENEZUELA, BOLIVARIAN REPUBLIC OF","VN":"VIET NAM","VG":"VIRGIN ISLANDS, BRITISH","VI":"VIRGIN ISLANDS, U.S.","WF":"WALLIS AND FUTUNA","EH":"WESTERN SAHARA","YE":"YEMEN","ZM":"ZAMBIA","ZW":"ZIMBABWE"}

    def capi(x):
        word = ''
        words = x.split(' ')
        for i in words:
            char = i.capitalize() + ' '
            word = word + char
        return word[:-1]

    
    def nation(df, source, campaign):
        idx_fb = [i for i in df.index if df.loc[i,source] == 'Facebook Ads']
        idx_asa = [i for i in df.index if df.loc[i,source] == 'Apple Search Ads']
        idx_g = [i for i in df.index if df.loc[i,source] == 'googleadwords_int']
        df.loc[idx_fb, 'Country'] = df.loc[idx_fb, campaign].apply(lambda x: x.split('_')[-2] if len(x.split('_')) > 1 else 'USA')
        df.loc[idx_fb, 'Country'] = df.loc[idx_fb, 'Country'].apply(lambda x: capi(dic_country[x]) if x in dic_country.keys() else x)
        df.loc[idx_g,'Country'] = df.loc[idx_g,campaign].apply(lambda x: x.split('_')[-1])
        df.loc[idx_g,'Country'] = df.loc[idx_g,'Country'].apply(lambda x: capi(dic_country[x]) if x in dic_country.keys() else x)
        df.loc[idx_asa,'Country'] = df.loc[idx_asa,campaign].apply(lambda x: x.split('-')[0].replace(' ', ''))
        df.loc[idx_asa,'Country'] = df.loc[idx_asa,'Country'].apply(lambda x: capi(dic_country[x]) if x in dic_country.keys() else x)

    def lan(df, source, campaign):
        idx_fb = [i for i in df.index if df.loc[i,source] == 'Facebook Ads']
        idx_asa = [i for i in df.index if df.loc[i,source] == 'Apple Search Ads']
        idx_g = [i for i in df.index if df.loc[i,source] == 'googleadwords_int']
        df.loc[idx_fb, 'Lan'] = df.loc[idx_fb, campaign].apply(lambda x: x.split('_')[-4] if len(x.split('_')) > 1 else 'EN')
        df.loc[idx_asa, 'Lan'] = df.loc[idx_asa, campaign].apply(lambda x: x.split('-')[1].replace(' ', ''))
        df.loc[idx_g,'Lan'] = df.loc[idx_g,campaign].apply(lambda x: x.split('_')[-2])
    

    skan = pd.read_csv('C:\\Users\\User\\Documents\\Python Scripts\\pnp\\data_skan.csv')
    raw = pd.read_csv('C:\\Users\\User\\Documents\\Python Scripts\\pnp\\data_raw.csv')
       
    totals_['Day'] = totals_['Day'].apply(lambda x: x.strftime('%Y-%m-%d'))
    tab = pd.merge(totals_.groupby(['Day', 'Campaign', 'Source']).sum().reset_index(), skan.groupby(['date', 'ad_network_campaign_name', 'media_source']).count().reset_index(), how = 'left', left_on =['Day', 'Campaign', 'Source'], right_on = ['date', 'ad_network_campaign_name', 'media_source'] )
    tab = tab.rename(columns = {'install_type': 'installs'})
    if 'skad_revenue' not in tab.columns:
        tab['skad_revenue'] = 0
    tab = tab.groupby(['Day','Campaign', 'Source']).sum().reset_index()

    tab['Day'] = tab['Day'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    tab['Day'] = tab['Day'].apply(lambda x: x.date())
    tab['ROAS'] = (tab['af_purchase (Sales in CAD)'] + tab['skad_revenue']) / tab['Total Cost']

    raw['af_purchase'] = raw['event_name'].apply(lambda x: 1 if x == 'af_purchase' else 0)
    #raw['country_name'] = raw['country_code'].map(dic_country) 
    #raw['country_name'] = raw['country_name'].apply(lambda x: capi(x))
    raw['date'] = raw['event_time_selected_timezone'].apply(lambda x: datetime.strptime(x.split('.')[0], '%Y-%m-%d %H:%M:%S'))
    raw['date'] = raw['date'].apply(lambda x: x.date())
    raw_tab = raw.groupby(['date', 'campaign', 'media_source']).sum().reset_index()
    tab_tab = pd.merge(tab, raw_tab, how = 'left', left_on = ['Day','Campaign', 'Source'], right_on= ['date', 'campaign', 'media_source'])
    tab_tab = tab_tab.groupby(['Day', 'Campaign', 'Source']).sum().reset_index()
    tab_tab['Country'] = 0 
    tab_tab['Lan'] = 0
    nation(tab_tab, 'Source', 'Campaign')
    print(tab_tab['Country'])
    lan(tab_tab, 'Source', 'Campaign')
    print(tab_tab['Lan'])

    #tab_tab['Day'] = tab_tab['Day'].apply(lambda x: x.strftime('%Y-%m-%d'))

    tab_tab['Day'] = tab_tab['Day'].apply(lambda x: datetime.combine(x, time(0, 0)))
    idx = [i for i in tab_tab.index if 'Test' not in tab_tab.loc[i, 'Campaign']]
    tab_tab = tab_tab.loc[idx, :]
    tab_tab_7 = tab_tab[tab_tab['Day'] >= datetime.now() - timedelta(days = 7)]

    tab_1 = tab_tab.groupby(['Campaign']).sum().reset_index()
    tab_1['CPA(login)'] = tab_1['Total Cost'] / (tab_1['Installs'] + tab_1['installs'])
    tab_1['CPA(buyer)'] = tab_1['Total Cost'] / (tab_1['af_purchase'])
    tab_1['ROAS'] = tab_1['af_purchase (Sales in CAD)'] / tab_1['Total Cost']
    tab_1.sort_values('ROAS', ascending = False, inplace = True)
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Campaign', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_1['Campaign'].values, tab_1['Installs'].values + tab_1['installs'].values, np.round(tab_1['Total Cost'].values / (tab_1['Installs'].values + tab_1['installs'].values), 2), np.round(tab_1['af_purchase (Sales in CAD)'].values, 2) , np.round(tab_1['CPA(login)'].values, 2) , np.round(tab_1['CPA(buyer)'].values,2), np.round(tab_1['ROAS'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Campaign Table Breakdown From {} to {}".format(start_date_, end_date_.strftime('%Y-%m-%d')))

    figs_pnp.append(figkey_tab)

    tab_1_7 = tab_tab_7.groupby(['Campaign']).sum().reset_index()
    tab_1_7['CPA(login)'] = tab_1_7['Total Cost'] / (tab_1_7['Installs'] + tab_1_7['installs'])
    tab_1_7['CPA(buyer)'] = tab_1_7['Total Cost'] / (tab_1_7['af_purchase'])
    tab_1_7['ROAS'] = tab_1_7['af_purchase (Sales in CAD)'] / tab_1_7['Total Cost']
    tab_1_7.sort_values('ROAS', ascending = False, inplace = True)
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Campaign', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_1_7['Campaign'].values, tab_1_7['Installs'].values + tab_1_7['installs'].values, np.round(tab_1_7['Total Cost'].values / (tab_1_7['Installs'].values + tab_1_7['installs'].values), 2), np.round(tab_1_7['af_purchase (Sales in CAD)'].values, 2) , np.round(tab_1_7['CPA(login)'].values, 2) , np.round(tab_1_7['CPA(buyer)'].values,2), np.round(tab_1_7['ROAS'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Campaign Table Breakdown Last 7 days")

    figs_pnp.append(figkey_tab)

    
    tab_2 = tab_tab.groupby('Country').sum().reset_index()
    tab_2['CPA(login)'] = tab_2['Total Cost'] / (tab_2['Installs'] + tab_2['installs'])
    tab_2['CPA(buyer)'] = tab_2['Total Cost'] / (tab_2['af_purchase'])
    tab_2['ROAS'] = tab_2['af_purchase (Sales in CAD)'] / tab_2['Total Cost']
    tab_2.sort_values('ROAS', ascending = False, inplace = True)
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Country', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_2['Country'].values, tab_2['Installs'].values + tab_2['installs'].values, np.round(tab_2['Total Cost'].values / (tab_2['Installs'].values + tab_2['installs'].values), 2), np.round(tab_2['af_purchase (Sales in CAD)'].values, 2) , np.round(tab_2['CPA(login)'].values, 2) , np.round(tab_2['CPA(buyer)'].values,2), np.round(tab_2['ROAS'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Country Table Breakdown From {} to {}".format(start_date_, end_date_.strftime('%Y-%m-%d')))

    figs_pnp.append(figkey_tab)

    tab_2_7 = tab_tab_7.groupby('Country').sum().reset_index()
    tab_2_7['CPA(login)'] = tab_2_7['Total Cost'] / (tab_2_7['Installs'] + tab_2_7['installs'])
    tab_2_7['CPA(buyer)'] = tab_2_7['Total Cost'] / (tab_2_7['af_purchase'])
    tab_2_7['ROAS'] = tab_2_7['af_purchase (Sales in CAD)'] / tab_2_7['Total Cost']
    tab_2_7.sort_values('ROAS', ascending = False, inplace = True)
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Country', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_2_7['Country'].values, tab_2_7['Installs'].values + tab_2_7['installs'].values, np.round(tab_2_7['Total Cost'].values / (tab_2_7['Installs'].values + tab_2_7['installs'].values), 2), np.round(tab_2_7['af_purchase (Sales in CAD)'].values, 2) , np.round(tab_2_7['CPA(login)'].values, 2) , np.round(tab_2_7['CPA(buyer)'].values,2), np.round(tab_2_7['ROAS'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Country Table Breakdown Last 7 days")

    figs_pnp.append(figkey_tab)

    tab_3 = tab_tab.groupby('Lan').sum().reset_index()
    tab_3['CPA(login)'] = tab_3['Total Cost'] / (tab_3['Installs'] + tab_3['installs'])
    tab_3['CPA(buyer)'] = tab_3['Total Cost'] / (tab_3['af_purchase'])
    tab_3['ROAS'] = tab_3['af_purchase (Sales in CAD)'] / tab_3['Total Cost']
    tab_3.sort_values('ROAS', ascending = False, inplace = True)
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Language', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_3['Lan'].values, tab_3['Installs'].values + tab_3['installs'].values, np.round(tab_3['Total Cost'].values / (tab_3['Installs'].values + tab_3['installs'].values), 2), np.round(tab_3['af_purchase (Sales in CAD)'].values, 2) , np.round(tab_3['CPA(login)'].values, 2) , np.round(tab_3['CPA(buyer)'].values,2), np.round(tab_3['ROAS'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Language Table Breakdown From {} to {}".format(start_date_, end_date_.strftime('%Y-%m-%d')))

    figs_pnp.append(figkey_tab)

    tab_3_7 = tab_tab_7.groupby('Lan').sum().reset_index()
    tab_3_7['CPA(login)'] = tab_3_7['Total Cost'] / (tab_3_7['Installs'] + tab_3_7['installs'])
    tab_3_7['CPA(buyer)'] = tab_3_7['Total Cost'] / (tab_3_7['af_purchase'])
    tab_3_7['ROAS'] = tab_3_7['af_purchase (Sales in CAD)'] / tab_3_7['Total Cost']
    tab_3_7.sort_values('ROAS', ascending = False, inplace = True)
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Language', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_3_7['Lan'].values, tab_3_7['Installs'].values + tab_3_7['installs'].values, np.round(tab_3_7['Total Cost'].values / (tab_3_7['Installs'].values + tab_3_7['installs'].values), 2), np.round(tab_3_7['af_purchase (Sales in CAD)'].values, 2) , np.round(tab_3_7['CPA(login)'].values, 2) , np.round(tab_3_7['CPA(buyer)'].values,2), np.round(tab_3_7['ROAS'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Language Table Breakdown Last 7 days")

    figs_pnp.append(figkey_tab)

    '''

    #uni = uni[['Day', 'Revenue', 'Total_Cost', 'Total_Installs', 'Total_Impressions', 'Total_Taps', 'TTR', 'convRate', 'ARPU', 'ROAS', 'avgCPI']]

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

    #fig = make_subplots( rows=1, cols=1, specs=[[{"secondary_y": True}]]) #, {"secondary_y": True}, column_widths=[1], subplot_titles=() "Total Daily Keap Installs vs. Daily CPI", "Cumulative KPIs Keap", 


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

    '''
    with open('Aggregated_PNP.html', 'w') as f:
        for fig in figs_pnp:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    

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