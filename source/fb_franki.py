import pandas as pd  
from os.path import join
from gspread_pandas import Spread
import datetime
import numpy as np
import time

from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adsinsights import AdsInsights
from facebookads.api import FacebookAdsApi

from appsflyer import AppsFlyer

from plotly.offline import plot
import plotly.express as px
from plotly.graph_objs import *
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from google.oauth2.service_account import Credentials
import time

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'C:\\Python39\\Lib\\site-packages\\gspread_pandas\\google_secret.json',
    scopes=scopes
)





def main():

    
    #report_id_to_file(START_DATE, END_DATE)
    my_app_id = '477643753180434'
    my_app_secret = '58dde228e99be54cbbb7c8976fcf1e67'
    my_access_token = "EAAGyaho8zRIBANou0asxEbzeF9gKIXx2uOTaHQqtgYFUwVRqBsNPz02Wj5IGu4DgmIrbSKVZCeXhHd3JO7BqjRfDhQi7mvbCSfQyBCAsRvpj0WLHiRCjJNBXRo84dZBBIkW1HzMEHeb0QKHhzDsACTZA8OB7Tsl1KUGgZBRwJdcdwHBIB12RjijZA8eEQKFVMQtM4ophRswZDZD"
    
    
    
    FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)



    sess = AdAccount('act_159810069529751')
    START_DATE = '2021-09-09'
    END_DATE = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")
    FIELDS = ['buying_type', 'objective']

    app_id = "id902026228"
    api_token = "6ebbb043-2c07-4972-8678-9687ae87ee9a"

    df_af_ios = get_geo_by_date_report(app_id, api_token, START_DATE, END_DATE)
    df_af_ios = df_af_ios[df_af_ios['Media Source (pid)'] == 'Facebook Ads'].reset_index(drop = True)
    df_ios = df_af_ios[['Date', 'Country', 'Campaign (c)', 'Impressions', 'Clicks', 'Installs', 'af_purchase (Sales in CAD)', 'Total Revenue', 'Total Cost']].reset_index(drop = True)
    #idx = [ i for i in df_ios.index if 'AGN' in df_ios.loc[i, 'Campaign (c)']]
    #df_ios = df_ios.loc[idx, :]

    app_id = 'com.ugroupmedia.pnp14'
    df_af_android = get_geo_by_date_report(app_id, api_token, START_DATE, END_DATE)
    df_af_android = df_af_android[df_af_android['Media Source (pid)'] == 'Facebook Ads'].reset_index(drop = True)
    df_android = df_af_android[['Date', 'Country', 'Campaign (c)', 'Impressions', 'Clicks', 'Installs', 'af_purchase (Sales in CAD)', 'Total Revenue', 'Total Cost']].reset_index(drop = True)
    #idx = [ i for i in df_android.index if 'AGN' in df_android.loc[i, 'Campaign (c)']]
    #df_android = df_android.loc[idx, :]

    df_af = pd.concat([df_ios, df_android], axis = 0)
    df_af.reset_index(inplace = True)
    
    for day in range(6):
        END_DATE = (datetime.datetime.now() - datetime.timedelta(days = 6 - day)).strftime("%Y-%m-%d")
        print(END_DATE)
        campaigns = sess.get_campaigns(fields = FIELDS)
    
        params = {
            'time_range': {'since': END_DATE, 'until': END_DATE},
            #'action_breakdowns' : ['action_device','action_type'],
            #'summary' : ['campaign_name','spend','actions'],
            #'summary_action_breakdowns' :['action_device', 'action_type'],
            'fields': ['campaign_name','impressions', 'inline_link_clicks', 'spend', 'purchase_roas', 'actions']
            #'fields': ['campaign_name','spend', 'action_values']
        }

        df = pd.DataFrame(columns = ['campaign_name', 'date_start', 'date_stop', 'impressions', 'inline_link_clicks','spend', 'purchase_roas', 'actions'])
        #df = pd.DataFrame(columns = ['campaign_name','date_start', 'date_stop', 'spend', 'action_values'])
    
        indx = 0
        for campaign in campaigns:
            response = campaign.get_insights(params=params)
            for i in response:
                for col in i:
                    df.loc[indx, col] = i[col]
            indx += 1
        df['spend'] = df['spend'].astype('float')
        #print(df.columns)
        #print(df['action_values'])
    
        #idx = [i for i in df.index if 'RMK' in df.loc[i, 'campaign_name']]
        #acq = df.loc[idx, :].reset_index(drop = True)
        idx = [i for i in df.index if 'RMK' in df.loc[i, 'campaign_name']]
        idx = ~df.index.isin(idx)
        acq = df.iloc[idx,:].reset_index(drop = True)
    
        #print(acq.campaign_name.unique())
        df['purchase_roas'] = acq['purchase_roas'].apply(lambda x: x if x is np.nan else float(x[0]['value']) )
    
        #print(acq['actions'])
        idx = df['actions'].notna()
        acq = df.loc[idx,: ]
        for i in acq.index:
            action = 0
            for j in acq.loc[i, 'actions']:
                #print(j['action_type'])
                #if j['action_type'] == 'onsite_conversion.purchase':
                    #action += int(j['value'])
                #if j['action_type'] == 'offsite_conversion.fb_pixel_purchase':
                    #action += int(j['value'])
                #if j['action_type'] == 'onsite_web_purchase':
                    #action += int(j['value'])
                #if j['action_type'] == 'onsite_web_app_purchase':
                    #action += int(j['value'])
                if j['action_type'] == 'mobile_app_install':
                    action += int(j['value'])
            if type(action) != int:
                acq.loc[i, 'actions'] = 0
            else:
                acq.loc[i, 'actions'] = action
    
        #print(len(acq))
        #print(acq.actions.sum())
        #android = []
        #iOS = []
        #website = []
        #for i in range(len(acq)):
            #summa_website = 0
            #summa_ios = 0
            #summa_android = 0
            #print(acq.loc[i, 'action_values'])
            #for j in acq.loc[i, 'action_values']:
                #if j['action_type'] == 'omni_purchase':
                    #if 'desktop' in j['action_device']: 
                        #summa_website += float(j['value'])
                    #if ('iphone' in j['action_device']) or ('ipad' in j['action_device']):
                        #summa_ios += float(j['value'])
                    #if 'android_smartphone' in j['action_device'] or ('android_tablet' in j['action_device']):
                        #summa_android += float(j['value'])
            #if summa_website > 0:
                #website.append(summa_website)
            #else:
                #website.append(int(0))
            #if summa_android > 0:
                #android.append(summa_android)
            #else:
                #android.append(int(0))
            #if summa_ios > 0:
                #iOS.append(summa_ios)
            #else:
                #iOS.append(int(0))
    
        #acq['website'] = website
        #acq['android'] = android
        #acq['iOS'] = iOS

        #print(acq['website'].sum())
        #print(acq['android'].sum())
        #print(acq['iOS'].sum())
        #print(acq['spend'].sum())
                    
        acq['actions'] = acq['actions'].astype('float')
        acq['CPI'] = acq['spend'] / acq['actions']
        acq['impressions'] = acq['impressions'].astype('float')
        acq['inline_link_clicks'] = acq['inline_link_clicks'].astype('float')
        if len(acq['purchase_roas'].values) > 0:
            if type(acq['purchase_roas'].values[0]) != float:
                acq['Revenue'] = float(0)
            else:
                acq['Revenue'] = acq['purchase_roas'].astype('float') * acq['spend']
        else:
            acq['Revenue'] = float(0)
        acq.fillna('0', inplace = True)
        print(acq)

        acq['inline_link_clicks'] = acq['inline_link_clicks'].astype('float')
        acq['CPI'] = acq['CPI'].astype('float')
        grouped = acq.groupby(['date_start', 'campaign_name']).sum().reset_index()
        print(grouped.columns)
        for i in df_af[df_af['Date'] == END_DATE]['Campaign (c)'].unique():
            if i not in grouped[grouped['date_start'] == END_DATE]['campaign_name'].unique():
                grouped = pd.concat([grouped, pd.DataFrame([[END_DATE, i, 0,0,0,0,0,0]], columns = grouped.columns, index = range(0,1))], axis = 0, ignore_index=True)
                #grouped = grouped.append({'date_start': END_DATE, 'campaign_name': i}, ignore_index=True)
        plot_rev = pd.merge(grouped,df_af[df_af['Date'] == END_DATE].groupby(['Date', 'Campaign (c)']).sum().reset_index(), how = 'left', left_on =['date_start', 'campaign_name'], right_on = ['Date', 'Campaign (c)'])
        #plot_save = plot_rev.groupby(['date_start', 'campaign_name']).sum().reset_index()
        print(plot_rev.columns)
        #print(plot_save)
        #print('ok')

        skan = pd.read_csv('C:\\Users\\User\\Documents\\Python Scripts\\pnp\\data_skan.csv')
        skan = skan[skan['media_source'] == 'Facebook Ads']
        print(skan.tail())
        for i in skan[skan['date'] == END_DATE]['ad_network_campaign_name'].unique():
            if i not in plot_rev[plot_rev['date_start'] == END_DATE]['campaign_name'].unique():
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

        plot_rev['type'] = 'facebook'
        indx = [i for i in plot_rev.index if 'AUD' in plot_rev.loc[i, 'campaign_name'] and 'ACQ' not in plot_rev.loc[i, 'campaign_name']]
        aud_df = plot_rev.loc[indx, :]
        aud_df['type'] = 'audience'

        indx = [i for i in plot_rev.index if 'ACQ' in plot_rev.loc[i, 'campaign_name'] and 'AUD' not in plot_rev.loc[i, 'campaign_name']]
        acq_df = plot_rev.loc[indx,:]
        acq_df['type'] = 'acquisition'
    
        
        fb_aud = pd.DataFrame({'Date': END_DATE, 'Network': 'Facebook (audience)', 'Installs': aud_df['actions'].astype('float').sum() , 'Installs AF': aud_df['Installs'].astype('float').sum(), 'Installs skan': aud_df['installs'].astype('float').sum(), 'Cost': aud_df['spend'].astype('float').sum(), 'Cost AF': aud_df['Total Cost'].astype('float').sum(), 'Revenue Skan': aud_df['skad_revenue'].astype('float').sum(), 'Revenue': aud_df['Revenue'].astype('float').sum(), 'Revenue AF': aud_df['af_purchase (Sales in CAD)'].astype('float').sum()}, index = range(0,1))
        fb_acq = pd.DataFrame({'Date': END_DATE, 'Network': 'Facebook (Acquisition)', 'Installs': acq_df['actions'].astype('float').sum() , 'Installs AF': acq_df['Installs'].astype('float').sum(), 'Installs skan': acq_df['installs'].astype('float').sum(), 'Cost': acq_df['spend'].astype('float').sum(), 'Cost AF': acq_df['Total Cost'].astype('float').sum(), 'Revenue Skan': acq_df['skad_revenue'].astype('float').sum(), 'Revenue': acq_df['Revenue'].astype('float').sum(), 'Revenue AF': acq_df['af_purchase (Sales in CAD)'].astype('float').sum()}, index = range(0,1))
        fb_totals = pd.concat([fb_aud, fb_acq], axis = 0)
        fb_totals['ROAS'] = fb_totals['Revenue AF'] / fb_totals['Cost']
    

        sheet_name = 'Daily_overview_2021'
        drive_fb(fb_totals, sheet_name, credentials)

        plot_rev = plot_rev[plot_rev['type'] != 'facebook']
        cols = ['date_start','campaign_name','impressions','inline_link_clicks','spend','actions','CPI','Revenue','Impressions','Clicks','Installs','af_purchase (Sales in CAD)','Total Revenue','Total Cost','installs','skad_revenue']
        db_fb = plot_rev[cols]
        print(db_fb)
        path = 'C:\\Users\\User\\Documents\\Python Scripts'
        df_cum_total = pd.read_csv(join(path,'fb_santa21.csv'))
        df_cum_total = df_cum_total[cols]
        #df_cum_total['date_start'] = pd.to_datetime(df_cum_total['date_start'], format = '%Y-%m-%d')
        print(db_fb.iloc[:, 1:].values)
        if len(db_fb) > 0:
            if db_fb['date_start'].values[0] in df_cum_total['date_start'].unique():
                df_cum_total = df_cum_total[df_cum_total['date_start'] != db_fb['date_start'].values[0]]
            df_cum_total = pd.concat([df_cum_total, db_fb], axis = 0)
            df_cum_total.to_csv(join(path,'fb_santa21.csv'), index = False) #, mode = 'a', header = False
        
    
    path = 'C:\\Users\\User\\Documents\\Python Scripts'
    df_cum_total = pd.read_csv(join(path,'fb_santa21.csv'))
    df_cum_20 = pd.read_csv(join(path,'fb_santa_a.csv'))

    #
    STARTS = (datetime.datetime.now() - datetime.timedelta(days = 34))
    ENDS = (datetime.datetime.now() - datetime.timedelta(days = 1))
    ENDS_20 = (datetime.datetime.now() - datetime.timedelta(days = 326))

    print(STARTS, ENDS)
    df_cum_total['af_purchase (Sales in CAD)'] = df_cum_total['af_purchase (Sales in CAD)'].astype('float')
    df_cum_20['Revenue'] = df_cum_20['Revenue'].astype('float')

    df_cum_total['date_start'] = pd.to_datetime(df_cum_total['date_start'], format= '%Y-%m-%d')
    df_cum_20['date_start'] = pd.to_datetime(df_cum_20['date_start'], format= '%Y-%m-%d')

    df_cum_total = df_cum_total[(df_cum_total['date_start'] >= STARTS) & (df_cum_total['date_start'] <= ENDS)]
    df_cum_20 = df_cum_20[(df_cum_20['date_start'] <= ENDS_20)]

    df_cum_total['date_start'] = df_cum_total['date_start'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df_cum_20['date_start'] = df_cum_20['date_start'].apply(lambda x: x.strftime('%Y-%m-%d'))

    df_daily = df_cum_total.groupby('date_start').sum()
    df_daily['Revenue'] = df_daily['af_purchase (Sales in CAD)'] + df_daily['skad_revenue']
    df_daily['CPI'] = df_daily['spend'] / (df_daily['Installs'] + df_daily['installs'])
    df_daily['ARPU'] = df_daily['Revenue'] / (df_daily['Installs'] + df_daily['installs'])

    fb_figs = []
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

    df_camp = df_cum_total.groupby('campaign_name').sum().reset_index()
    df_camp['Revenue'] = df_camp['af_purchase (Sales in CAD)'] + df_camp['skad_revenue']
    df_camp['ROAS'] = df_camp['Revenue'] / df_camp['spend']
    df_camp = df_camp[df_camp['Revenue'] > 0].reset_index(drop = True)
    df_camp.sort_values('ROAS', ascending = False, inplace = True)

    trace = go.Table(header=dict(values=['Campaign','Revenue', 'ROAS']),
                cells=dict(values=[df_camp.campaign_name.values, np.round(df_camp.Revenue.values, 2), np.round(df_camp.ROAS.values, 1)]), domain=dict(x=[0.52, 1],y=[0, 1]))
            
    trace1 = go.Pie(values=df_camp.spend, labels=df_camp.campaign_name, hole=.4, name = 'Cost', domain=dict(x=[0, 0.23],y=[0, 1]), title_text = 'Cost', textposition='inside', textinfo='percent', hoverinfo="label+value")
    trace2 = go.Pie(values=df_camp.Revenue, labels=df_camp.campaign_name, hole=.4, name = 'Revenue', domain=dict(x=[0.26, 0.49],y=[0, 1]), title_text = 'Revenue', textposition='inside', textinfo='percent', hoverinfo="label+value")
    
    
    fig_dough = go.Figure(data = [trace,trace1, trace2])
    fig_dough.update_layout(title_text="FB Breakdown by Campaign")

    fb_figs.append(fig_dough)

    END_DATE = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")

    app_id = "id902026228"
    api_token = "6ebbb043-2c07-4972-8678-9687ae87ee9a"

    
    #df_af = pd.merge(df_af, skan, how = 'left', left_on = ['Date', 'Campaign (c)'], right_on = ['date', 'campaign'])
    corte = df_af.groupby('Country').sum().reset_index()

    corte.sort_values('af_purchase (Sales in CAD)', ascending = False, inplace = True)
    corte = corte.head(15)
    parces = corte.Country.unique()
    idx = [ i for i in df_af.index if df_af.loc[i, 'Country'] in parces]
    df_country = df_af.loc[idx, :]
    df_country = df_country.groupby(['Date', 'Country', 'Campaign (c)']).sum().reset_index().sort_values('Date')
    df_country = df_country[df_country['af_purchase (Sales in CAD)'] > 0 ].reset_index(drop = True)

    ##ADD 2020 values

    fig_camp = px.bar(df_country, x='Date', y='af_purchase (Sales in CAD)', color='Campaign (c)',
               facet_col='Country', facet_col_wrap=2)
    fig_camp.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig_camp.update_yaxes(matches=None, showticklabels=True, title_text='')
    fig_camp.update_xaxes(matches=None, showticklabels=True, title_text='')
    fig_camp.update_layout(
        title_text="Daily FB Campaigns Revenue per Country", height = 750, barmode = 'stack')

    fb_figs.append(fig_camp)

    skan = pd.read_csv('C:\\Users\\User\\Documents\\Python Scripts\\pnp\\data_skan.csv')
    skan = skan[skan['media_source'] == 'Facebook Ads']

    geo_report_tab = pd.merge(df_cum_total, df_af.groupby(['Date', 'Campaign (c)']).sum().reset_index(), how = 'left', left_on= ['date_start', 'campaign_name'], right_on= ['Date', 'Campaign (c)'])
    geo_report_tab = geo_report_tab.groupby(['date_start', 'campaign_name']).sum().reset_index()
    ##MISSING SKAD REVENUE
    geo_report_tab = pd.merge(geo_report_tab, skan.groupby(['date', 'ad_network_campaign_name']).count().reset_index(), how = 'left', left_on =['date_start', 'campaign_name'], right_on = ['date', 'ad_network_campaign_name'] )
    #geo_report_tab = geo_report_tab.rename(columns = {'install_type': 'installs'})
    if 'skad_revenue' not in geo_report_tab.columns:
        geo_report_tab['skad_revenue'] = 0
    geo_report_tab = geo_report_tab.groupby(['date_start','campaign_name']).sum().reset_index()

    geo_report_tab['date_start'] = geo_report_tab['date_start'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    geo_report_tab['date_start'] = geo_report_tab['date_start'].apply(lambda x: x.date())
    geo_report_tab['ROAS'] = geo_report_tab['af_purchase (Sales in CAD)_x'] / geo_report_tab['spend']

    raw = pd.read_csv('C:\\Users\\User\\Documents\\Python Scripts\\pnp\\data_raw.csv')
    raw = raw[raw['media_source'] == 'Facebook Ads']
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
    raw['date'] = raw['event_time_selected_timezone'].apply(lambda x: datetime.datetime.strptime(x.split('.')[0], '%Y-%m-%d %H:%M:%S'))
    raw['date'] = raw['date'].apply(lambda x: x.date())
    raw_tab = raw.groupby(['date', 'campaign']).sum().reset_index()
    tab_tab = pd.merge(geo_report_tab, raw_tab, how = 'left', left_on = ['date_start','campaign_name'], right_on= ['date', 'campaign'])
    tab_1 = tab_tab.groupby(['campaign']).sum().reset_index()
    tab_1['CPA(login)'] = tab_1['spend'] / (tab_1['Installs_x'] + tab_1['installs'])
    tab_1['CPA(buyer)'] = tab_1['spend'] / (tab_1['af_purchase'])
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Campaign', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_1['campaign'].values, tab_1['Installs_x'].values + tab_1['installs'].values, np.round(tab_1['spend'].values / (tab_1['Installs_x'].values + tab_1['installs'].values), 2), np.round(tab_1['af_purchase (Sales in CAD)_x'].values, 2) , np.round(tab_1['CPA(login)'].values, 2) , np.round(tab_1['CPA(buyer)'].values,2), np.round(tab_1['af_purchase (Sales in CAD)_x'].values / tab_1['spend'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Campaign Table Breakdown From {} to {}".format(START_DATE, END_DATE))

    fb_figs.append(figkey_tab)

    tab_tab['date_start'] = tab_tab['date_start'].apply(lambda x: datetime.datetime.combine(x, datetime.time(0, 0)))
    tab_tab_7 = tab_tab[tab_tab['date_start'] >= datetime.datetime.now() - datetime.timedelta(days = 7)]
    tab_1_7 = tab_tab_7.groupby(['campaign']).sum().reset_index()
    tab_1_7['CPA(login)'] = tab_1_7['spend'] / (tab_1_7['Installs_x'] + tab_1_7['installs'])
    tab_1_7['CPA(buyer)'] = tab_1_7['spend'] / (tab_1_7['af_purchase'])
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Campaign', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_1_7['campaign'].values, tab_1_7['Installs_x'].values + tab_1_7['installs'].values, np.round(tab_1_7['spend'].values / (tab_1_7['Installs_x'].values + tab_1_7['installs'].values), 2), np.round(tab_1_7['af_purchase (Sales in CAD)_x'].values, 2) , np.round(tab_1_7['CPA(login)'].values, 2) , np.round(tab_1_7['CPA(buyer)'].values,2), np.round(tab_1_7['af_purchase (Sales in CAD)_x'].values / tab_1_7['spend'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Campaign Table Breakdown Last 7 days")

    fb_figs.append(figkey_tab)


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

    tab_1_7['Language'] = tab_1_7['campaign'].apply(lambda x: x.split('_')[-4] if len(x.split('_')) > 1 else 'EN')
    tab_3_7 = tab_1_7.groupby('Language').sum().reset_index()
    tab_3_7['CPA(login)'] = tab_3_7['spend'] / (tab_3_7['Installs_x'] + tab_3_7['installs'])
    tab_3_7['CPA(buyer)'] = tab_3_7['spend'] / (tab_3_7['af_purchase'])
    figkey_tab = go.Figure(data=[go.Table(header=dict(values=['Language', 'Installs', 'CPI $', 'Revenue $', 'CPA $ (login)', 'CPA $ (buyer)', 'ROAS $']),
                 cells=dict(values=[tab_3_7['Language'].values, tab_3_7['Installs_x'].values + tab_3_7['installs'].values, np.round(tab_3_7['spend'].values / (tab_3_7['Installs_x'].values + tab_3_7['installs'].values), 2), np.round(tab_3_7['af_purchase (Sales in CAD)_x'].values, 2) , np.round(tab_3_7['CPA(login)'].values, 2) , np.round(tab_3_7['CPA(buyer)'].values,2), np.round(tab_3_7['af_purchase (Sales in CAD)_x'].values / tab_3_7['spend'].values, 2)]))
                     ])
    figkey_tab.update_layout(height = 400, title_text="Language Table Breakdown Last 7 days")

    fb_figs.append(figkey_tab)

    
    with open(join(path,'Fb_Prev.html'), 'w') as f:
        for fig in fb_figs:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    


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

if __name__ == "__main__":
    main()

