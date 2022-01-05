from googleads import adwords, oauth2
from appsflyer import AppsFlyer
import pandas as pd
import io
from datetime import datetime, timedelta
import numpy as np


import locale
import sys
import _locale

from gspread_pandas import Spread, Client

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

    start_date_ = '2020-12-01'
    end_date_ = (datetime.now() - timedelta(days= 1))

    refresh_token = '1//05p3VlB4YhmS0CgYIARAAGAUSNwF-L9IrpzuJI77loPPwqj_ocPytox6LsrTfc1lK16ea8qrE4LJaZxQIK4wyoNn-B57m_2DAk4c'
    client_id = '422898392645-kq6mc00a3h0c857qdp8jsre7pi9gjntv.apps.googleusercontent.com'
    client_secret = 'AH28CNr8Lnuuhw-irN6smI_O'
    developer_token = 'PJY5mhXidEqXfbuCZES9PQ'
    client_customer_id = '5419218164'
    


    df = get_campaign_performance_report(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date_, end_date_)

    print(df.columns)

    #Pick uac campaigns
    #index_uac = [i for i in df.index if 'NB' not in df.loc[i,'Campaign'] and 'BRANDED' not in df.loc[i,'Campaign'] and 'UAC' in df.loc[i,'Campaign'] and df.loc[i, 'Campaign serving status'] == 'eligible']
    #uac_campaigns = df.iloc[index_uac,:]

    #index_uac = [i for i in df_19.index if 'NB' not in df_19.loc[i,'Campaign'] and 'BRANDED' not in df_19.loc[i,'Campaign'] and 'UAC' in df_19.loc[i,'Campaign'] ]
    #uac_campaigns_19 = df_19.iloc[index_uac,:]
    
    #Pick nb campaigns
    #index_nb = [i for i in df.index if 'BRANDED' not in df.loc[i,'Campaign'] and 'UAC' not in df.loc[i,'Campaign'] and 'S - NB' in df.loc[i,'Campaign'] and df.loc[i, 'Campaign serving status'] == 'eligible' ]
    #nb_campaigns = df.iloc[index_nb,:]

    #index_nb = [i for i in df_19.index if 'BRANDED' not in df_19.loc[i,'Campaign'] and 'UAC' not in df_19.loc[i,'Campaign'] and 'S - NB' in df_19.loc[i,'Campaign'] ]
    #nb_campaigns_19 = df_19.iloc[index_nb,:]

    #Pick branded campaigns
    #index_b = [i for i in df.index if 'UAC' not in df.loc[i,'Campaign'] and 'NB' not in df.loc[i,'Campaign'] and 'BRANDED' in df.loc[i,'Campaign'] and df.loc[i, 'Campaign serving status'] == 'eligible' ]
    #b_campaigns = df.iloc[index_b,:]

    ##index_b = [i for i in df_19.index if 'UAC' not in df_19.loc[i,'Campaign'] and 'NB' not in df_19.loc[i,'Campaign'] and 'BRANDED' in df_19.loc[i,'Campaign'] ]
    #b_campaigns_19 = df_19.iloc[index_b,:]


    #uac_campaigns['type'] = 'UAC'
    #nb_campaigns['type'] = 'Non-Branded'
    #b_campaigns['type'] = 'Branded'

    #uac_campaigns_19['type'] = 'UAC'
    #nb_campaigns_19['type'] = 'Non-Branded'
    #b_campaigns_19['type'] = 'Branded'

    #unified = pd.concat([uac_campaigns, nb_campaigns, b_campaigns], axis = 0)
    #temp = unified.copy()
    

    ### Filtering by end_date
    #uac_campaigns_day = uac_campaigns[uac_campaigns['Day'] == end_date_.strftime('%Y-%m-%d')]

    #nb_campaigns_day = nb_campaigns[nb_campaigns['Day'] == end_date_.strftime('%Y-%m-%d')]

    #b_campaigns_day = b_campaigns[b_campaigns['Day'] == end_date_.strftime('%Y-%m-%d')]      

    ## Budget sheet (just end date totals)
    #if len(uac_campaigns_day.columns) > 0:
      #  uac_totals = pd.DataFrame({'Date': end_date_.strftime('%Y-%m-%d'), 'Network': 'Google UAC', 'Installs': uac_campaigns_day['Conversions'].sum() , 'Cost': uac_campaigns_day['Cost'].sum(), 'Revenue' : uac_campaigns_day['Total conv. value'].sum()}, index = range(0,1))
    #else:
      #  uac_totals = pd.DataFrame({'Date': end_date_.strftime('%Y-%m-%d'), 'Network': 'Google UAC', 'Installs': 0, 'Cost': 0, 'Revenue': 0}, index = range(0,1))
    #if len(nb_campaigns_day.columns) > 0:
      #  nb_totals = pd.DataFrame({'Date': end_date_.strftime('%Y-%m-%d'), 'Network': 'Google Search (Non-Branded)', 'Installs': nb_campaigns_day['Conversions'].sum() , 'Cost': nb_campaigns_day['Cost'].sum(), 'Revenue' : nb_campaigns_day['Total conv. value'].sum()}, index = range(0,1))
    #else:
      #  nb_totals = pd.DataFrame({'Date': end_date_.strftime('%Y-%m-%d'), 'Network': 'Google Search (Non-Branded)', 'Installs': 0, 'Cost': 0, 'Revenue': 0}, index = range(0,1))
    #if len(b_campaigns_day.columns) > 0:
      #  branded_totals = pd.DataFrame({'Date': end_date_.strftime('%Y-%m-%d'), 'Network': 'Google Search (Branded)', 'Installs': b_campaigns_day['Conversions'].sum() , 'Cost': b_campaigns_day['Cost'].sum(), 'Revenue' : b_campaigns_day['Total conv. value'].sum()}, index = range(0,1))
    #else:
      #  branded_totals = pd.DataFrame({'Date': end_date_.strftime('%Y-%m-%d'), 'Network': 'Google Search (Branded)', 'Installs': 0, 'Cost': 0, 'Revenue': 0}, index = range(0,1))

    

    #upload = pd.concat([uac_totals,branded_totals, nb_totals], axis =0)
    df['Cost'] = df['Cost'] / 1000000
    df['ROAS'] = df['Total conv. value'] / df['Cost']

    ###FOR COUNTRIES APPS
       #df_geo = get_geo_performance(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date_, end_date_)
       #df_geo = df_geo[df_geo['Campaign state'] == 'enabled']
       #locations = list(df_geo[df_geo['Location'] != ' --']['Location'].unique())
       #print(locations)

       #loc_details = get_location(client_id, client_secret, refresh_token, developer_token, client_customer_id, locations)
       #print(loc_details)
       #dict_loc = {}

       #for location in loc_details:
           #dict_loc[str(location['location']['id'])] = location['location']['locationName']

       #df_geo['Cost'] = df_geo['Cost'] / 1000000
       #df_geo['locationName'] = df_geo['Location'].apply(lambda x: dict_loc[str(x)] if str(x) != ' --' else 'Other' )
       #df_geo['locationName'] = df_geo['locationName'].fillna('Other')

    mapping = {'AW':'ABW','AF':'AFG','AO':'AGO','AI':'AIA','AX':'ALA','AL':'ALB','AD':'AND','AE':'ARE','AR':'ARG','AM':'ARM','AS':'ASM','AQ':'ATA','TF':'ATF','AG':'ATG','AU':'AUS','AT':'AUT','AZ':'AZE','BI':'BDI','BE':'BEL','BJ':'BEN','BQ':'BES','BF':'BFA','BD':'BGD','BG':'BGR','BH':'BHR','BS':'BHS','BA':'BIH','BL':'BLM','BY':'BLR','BZ':'BLZ','BM':'BMU','BO':'BOL','BR':'BRA','BB':'BRB','BN':'BRN','BT':'BTN','BV':'BVT','BW':'BWA','CF':'CAF','CA':'CAN','CC':'CCK','CH':'CHE','CL':'CHL','CN':'CHN','CI':'CIV','CM':'CMR','CD':'COD','CG':'COG','CK':'COK','CO':'COL','KM':'COM','CV':'CPV','CR':'CRI','CU':'CUB','CW':'CUW','CX':'CXR','KY':'CYM','CY':'CYP','CZ':'CZE','DE':'DEU','DJ':'DJI','DM':'DMA','DK':'DNK','DO':'DOM','DZ':'DZA','EC':'ECU','EG':'EGY','ER':'ERI','EH':'ESH','ES':'ESP','EE':'EST','ET':'ETH','FI':'FIN','FJ':'FJI','FK':'FLK','FR':'FRA','FO':'FRO','FM':'FSM','GA':'GAB','GB':'GBR','GE':'GEO','GG':'GGY','GH':'GHA','GI':'GIB','GN':'GIN','GP':'GLP','GM':'GMB','GW':'GNB','GQ':'GNQ','GR':'GRC','GD':'GRD','GL':'GRL','GT':'GTM','GF':'GUF','GU':'GUM','GY':'GUY','HK':'HKG','HM':'HMD','HN':'HND','HR':'HRV','HT':'HTI','HU':'HUN','ID':'IDN','IM':'IMN','IN':'IND','IO':'IOT','IE':'IRL','IR':'IRN','IQ':'IRQ','IS':'ISL','IL':'ISR','IT':'ITA','JM':'JAM','JE':'JEY','JO':'JOR','JP':'JPN','KZ':'KAZ','KE':'KEN','KG':'KGZ','KH':'KHM','KI':'KIR','KN':'KNA','KR':'KOR','KW':'KWT','LA':'LAO','LB':'LBN','LR':'LBR','LY':'LBY','LC':'LCA','LI':'LIE','LK':'LKA','LS':'LSO','LT':'LTU','LU':'LUX','LV':'LVA','MO':'MAC','MF':'MAF','MA':'MAR','MC':'MCO','MD':'MDA','MG':'MDG','MV':'MDV','MX':'MEX','MH':'MHL','MK':'MKD','ML':'MLI','MT':'MLT','MM':'MMR','ME':'MNE','MN':'MNG','MP':'MNP','MZ':'MOZ','MR':'MRT','MS':'MSR','MQ':'MTQ','MU':'MUS','MW':'MWI','MY':'MYS','YT':'MYT','NA':'NAM','NC':'NCL','NE':'NER','NF':'NFK','NG':'NGA','NI':'NIC','NU':'NIU','NL':'NLD','NO':'NOR','NP':'NPL','NR':'NRU','NZ':'NZL','OM':'OMN','PK':'PAK','PA':'PAN','PN':'PCN','PE':'PER','PH':'PHL','PW':'PLW','PG':'PNG','PL':'POL','PR':'PRI','KP':'PRK','PT':'PRT','PY':'PRY','PS':'PSE','PF':'PYF','QA':'QAT','RE':'REU','RO':'ROU','RU':'RUS','RW':'RWA','SA':'SAU','SD':'SDN','SN':'SEN','SG':'SGP','GS':'SGS','SH':'SHN','SJ':'SJM','SB':'SLB','SL':'SLE','SV':'SLV','SM':'SMR','SO':'SOM','PM':'SPM','RS':'SRB','SS':'SSD','ST':'STP','SR':'SUR','SK':'SVK','SI':'SVN','SE':'SWE','SZ':'SWZ','SX':'SXM','SC':'SYC','SY':'SYR','TC':'TCA','TD':'TCD','TG':'TGO','TH':'THA','TJ':'TJK','TK':'TKL','TM':'TKM','TL':'TLS','TO':'TON','TT':'TTO','TN':'TUN','TR':'TUR','TV':'TUV','TW':'TWN','TZ':'TZA','UG':'UGA','UA':'UKR','UM':'UMI','UY':'URY','US':'USA','UZ':'UZB','VA':'VAT','VC':'VCT','VE':'VEN','VG':'VGB','VI':'VIR','VN':'VNM','VU':'VUT','WF':'WLF','WS':'WSM','YE':'YEM','ZA':'ZAF','ZM':'ZMB','ZW':'ZWE'}
    
        #lista = list(df_af.Country.unique())
        #print(lista)
        #lista.pop(137)
        #index = [i for i in df_af.index if df_af.loc[i, 'Country'] in lista]
        #df_af = df_af.loc[index]
        #df_af['Country'] = df_af.Country.apply(lambda x: np.where(x == 'UK', 'GB', x))
        #df_geo['iso_alpha'] = df_geo.locationName.map(mapping) 
        #df_fig_geo = df_geo.groupby('iso_alpha').sum().reset_index()

        #fig_map_conv = px.choropleth(df_fig_geo, locations="iso_alpha", color="Conversions", hover_name="iso_alpha", color_continuous_scale=px.colors.sequential.Plasma)
        #fig_map_rev = px.choropleth(df_fig_geo, locations="iso_alpha", color="Total conv. value", hover_name="iso_alpha", color_continuous_scale=px.colors.sequential.Plasma)
        #fig_map_conv.update_layout(
        #title_text="Installs by Geolocation")
        #fig_map_rev.update_layout(
        #title_text="Revenue by Geolocation")

    #unified_19 = pd.concat([uac_campaigns_19, nb_campaigns_19, b_campaigns_19], axis = 0)    

    
    
    figs_adwords = []

    uac_plot = df.groupby('Day').sum().reset_index().sort_values('Day', ascending = True)
    uac_plot['avgCPC'] = uac_plot['Cost'] / uac_plot['Conversions']
    uac_plot['TTR'] = uac_plot['Clicks'] / uac_plot['Impressions']
    uac_plot['convRate'] = uac_plot['Conversions'] / uac_plot['Clicks']
    uac_plot['ROAS'] = uac_plot['Total conv. value'] / uac_plot['Cost']
    print(uac_plot)

     
    #df_geo['ROAS'] = df_geo['Total conv. value'].astype('float') / df_geo['Cost'].astype('float')
    #df_geo['ARPU'] = df_geo['Total conv. value'].astype('float') / df_geo['Conversions'].astype('float')
    


    
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


    #geo_camp_uni = pd.concat([df_geo_camp_uac, df_geo_camp_nb, df_geo_camp_b], axis = 0)
    #geo_camp_uni_19 = pd.concat([df_geo_camp_uac_19, df_geo_camp_nb_19, df_geo_camp_b_19], axis = 0)

    #print(geo_camp_uni['locationName'].unique())
    #dic_country = {'AU' :'Australia', 'CA': 'Canada', 'UK': 'United Kingdom', 'IT': 'Italy', 'FR': 'France', 'US': 'United States',
    #                'AR': 'Argentina', 'MX': 'Mexico', 'BE':'Belgium', 'ES':'Spain', 'ZA':'South Africa', 'NZ': 'New Zealand', 'CH':'Switzerland', 'IE':'Ireland'}
    #df_level['Country'] = df_level['Country'].map(dic_country)
    #df_subs = df_level.groupby(['Date','type', 'Country']).sum().reset_index()

    #print(df_geo)
    #print(df_geo.columns)
    #geo_report = df_geo.groupby(['Day','locationName']).sum().reset_index().sort_values('Day', ascending = True)
    
    #geo_report19 = geo_camp_uni_19.groupby(['Day','type', 'locationName']).sum().reset_index()
    
    #geo_report = pd.merge(geo_report, df_subs, how = 'left', left_on= ['Day', 'type', 'locationName'], right_on= ['Date', 'type', 'Country'])
    #geo_report['Total conv. value'] = geo_report['Total conv. value'].astype('float') + geo_report['af_subscribe (Sales in CAD)'].astype('float')

    #geo_camp_total = pd.concat([geo_report, geo_report19], axis = 0)
    #geo_camp_total['Year'] = geo_camp_total['Day'].apply(lambda x: str(x)[:4])
    #geo_camp_total['Day'] = pd.to_datetime(geo_camp_total['Day'], format='%Y-%m-%d')

   
    #geo_camp_fig = geo_report.copy()


    #geo_report = geo_report[geo_report['locationName'] != 'Other']
    #geo_camp_total = geo_camp_total.groupby(['Day', 'locationName','type', 'Year']).sum().reset_index().sort_values('Day', ascending = True)
    #geo_camp_total['Day'] = geo_camp_total['Day'].apply(lambda x: x.strftime('%b-%d'))
    #print(geo_report)
    

    
    fig = make_subplots( rows=1, cols=2, column_widths=[0.5, 0.5], specs=[[{'secondary_y':True}, {'secondary_y':True}]],
                    subplot_titles=("Daily Adwords Conversions vs. CPC", "Daily Adwords Revenue KPIs" ))

    # Add traces

    fig.add_trace(go.Scatter(x=uac_plot.Day, y=uac_plot['Cost'],
                    mode='lines+markers',
                    name='Cost', marker_color = '#109618'), row =1 , col = 2)
    fig.add_trace(go.Scatter(x=uac_plot.Day, y=uac_plot.avgCPC, name = 'CPC', marker_color = '#EF553B'), secondary_y = True, row=1, col=1)
    fig.add_trace(go.Scatter(x=uac_plot.Day, y=uac_plot['ROAS'],
                   mode='lines+markers',
                    name='Daily ROAS', marker_color = '#511CFB'), secondary_y = True, row =1 , col = 2)

    fig.add_trace(go.Bar(x=uac_plot.Day, y=uac_plot['Conversions'],
                    name='Conversions', marker_color = 'rgb(204,204,204)'), row=1, col=1)
    

    
    #fig.add_trace(go.Bar(x=uac_plot.Day, y=uac_plot.groupby(['Day','type']).sum()['Total conv. value'].loc[slice(None), 'UAC'], marker_color = 'rgb(204,204,204)', name = 'UAC-Rev', showlegend = False),  row=1, col=2)
    #fig.add_trace(go.Bar(x=plot_rev.groupby('Day').sum().index, y=plot_rev.groupby(['Day','type']).sum()['Total conv. value'].loc[slice(None), 'Non-Branded'], marker_color = '#FF6692', name = 'Non-Branded-Rev', showlegend = False),  row=1, col=2)
    #fig.add_trace(go.Bar(x=plot_rev.groupby('Day').sum().index, y=plot_rev.groupby(['Day','type']).sum()['Total conv. value'].loc[slice(None), 'Branded'], marker_color = '#AB63FA', name = 'Branded-Rev', showlegend = False),  row=1, col=2)
    
    fig.add_trace(go.Bar(x=uac_plot.Day, y=uac_plot['Total conv. value'],
                    name='Revenue', marker_color = '#FEAF16'), row =1 , col = 2)
    
    fig.update_layout(barmode = 'stack', height = 600)
    fig.update_yaxes(title_text="Conversions", secondary_y=False, row = 1, col =1)
    fig.update_yaxes(title_text="CPC", secondary_y=True, row = 1, col =1)
    fig.update_yaxes(title_text="Revenue/Cost", secondary_y=False, row = 1, col =2)
    fig.update_yaxes(title_text="ROAS", secondary_y=True, row = 1, col =2)
    figs_adwords.append(fig)

    #DO STATES WITH AF DATA
    #fig_camp_ = px.scatter(geo_report, x='Day', y='Conversions',
    #           facet_col='locationName', facet_col_wrap=2).update_traces(mode='lines+markers')
    #fig_camp_.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    #fig_camp_.update_yaxes(matches=None, showticklabels=True, title_text='')
    #fig_camp_.update_xaxes(matches='x')
    #fig_camp_.update_layout(
        #title_text="Daily Conversions per Country", height = 950)

    day = 14
    budgets = pd.DataFrame()
    while day >= 0:
        end_date_ = (datetime.now() - timedelta(days= day))
        df_b = get_budget_report(client_id, client_secret, refresh_token, developer_token, client_customer_id, end_date_, end_date_)
        df_b['Day'] = (datetime.now() - timedelta(days= day)).strftime('%b-%d')
        budgets = pd.concat([budgets, df_b], axis = 0)
        day -= 1
    print(budgets)
    budgets['Cost'] = budgets['Cost'].astype('float') /1000000
    budgets['Budget'] = budgets['Budget'].astype('float') /1000000
    budgets = budgets[(budgets['Budget state'] == 'Enabled') & (budgets['Cost'] > 0 )] 

    budgets = budgets.groupby(['Day', 'Budget Name']).sum().reset_index()
    budgets['ROAS'] = budgets['Total conv. value'] / budgets['Cost']
    print(budgets)

    day = 14
    def fbudgets(days, df):
        values = pd.DataFrame()
        totals = pd.DataFrame()
        while days >=0 :
            #print(days)
            temp = (df[df['Day'] == (datetime.now() - timedelta(days= 14 - days)).strftime('%b-%d')]['Cost'].values / df[df['Day'] == (datetime.now() - timedelta(days= 14 - days)).strftime('%b-%d')]['Budget']) * 100
            df_1 = pd.DataFrame(pd.concat([temp,df[df['Day'] == (datetime.now() - timedelta(days= 14 - days)).strftime('%b-%d')]['Budget Name'], df[df['Day'] == (datetime.now() - timedelta(days= 14 - days)).strftime('%b-%d')]['ROAS']], axis = 1))
            df_2 = pd.DataFrame(pd.concat([df[df['Day'] == (datetime.now() - timedelta(days= 14 - days)).strftime('%b-%d')]['Budget'], df[df['Day'] == (datetime.now() - timedelta(days= 14 - days)).strftime('%b-%d')]['Budget Name']], axis = 1))
            if days == 14:
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
    bvalues.columns = ['Budget', 'Name', 'ROAS', 'Budget_yes','ROAS_yes', 'Budget_2', 'ROAS_2','Budget_3', 'ROAS_3', 'Budget_4', 'ROAS_4', 'Budget_5', 'ROAS_5', 'Budget_6', 'ROAS_6','Budget_7', 'ROAS_7',
                           'Budget_8', 'ROAS_8', 'Budget_9', 'ROAS_9', 'Budget_10', 'ROAS_10', 'Budget_11','ROAS_11','Budget_12', 'ROAS_12','Budget_13', 'ROAS_13','Budget_14','ROAS_14']
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
        

    favg(bvalues, 0, 17, 'Average_current')
    favg(bvalues, 17, 31, 'Average_past')
    favg(btotals, 0, 8, 'Average_current_T')
    favg(btotals, 8, 16, 'Average_past_T')



    #colors = n_colors('rgb(102, 166, 30)', 'rgb(230, 245, 201)', 9, colortype='rgb')
    bvalues = pd.merge(bvalues, btotals, how = 'left', on = 'Name')
    bvalues.sort_values('Budget', inplace = True, ascending = False)


    tab = go.Figure()
    tab.add_trace(go.Table(header=dict(values=['Budget Name','Today (%)', 'Total B.', 'ROAS','Yestr (%)', 'Total B.', 'ROAS','2 Days Ago (%)', 'Total B.','ROAS',  'Avg week (%)', 'Total_B_Avg']),
                 cells=dict(values=[bvalues['Name'].values, np.round(bvalues['Budget'],1),  np.round(bvalues['Budget_T'], 1) , np.round(bvalues['ROAS'],1), np.round(bvalues['Budget_yes'], 1) , np.round(bvalues['Budget_yes_T'], 1), np.round(bvalues['ROAS_yes'],1), np.round(bvalues['Budget_2'], 1) , np.round(bvalues['Budget_2_T'], 1), np.round(bvalues['ROAS_2'],1), np.round(bvalues['Average_current'],1), np.round(bvalues['Average_current_T'], 1) ],
                  fill=dict(color=['rgb(245, 245, 245)',#unique color for the first column
                                            ['rgba(166, 216, 84, 0.8)' if val >= 1 else 'rgba(251, 180, 174, 0.8)' for val in np.round(bvalues['ROAS'],1)] ]))))
    tab.update_layout(title_text = "Budget Stats Current Week (Green Rows above 1 Today's ROAS)" , height = 250)

    figs_adwords.append(tab)

    end_d = "2021-01-27"
    installs_af = pd.read_csv('~/Downloads/cc_run/install_android.csv')
    purchases_af = pd.read_csv('~/Downloads/cc_run/purchases_android.csv')
    ios_i = pd.read_csv('~/Downloads/cc_run/installs_ios.csv')
    ios_pur =  pd.read_csv('~/Downloads/cc_run/purchases_ios.csv')
    
    dfs=[installs_af,purchases_af,ios_i,ios_pur]
    temps = []
    for frame in dfs:
        frame = frame[frame['Media Source'] == "googleadwords_int"]
        frame['iso_alpha'] = frame['Country Code'].map(mapping)
        frame = frame[frame['iso_alpha'] == 'USA']
        frame["Event Time"] = frame["Event Time"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
        frame["Day"] = frame["Event Time"].apply(lambda x: x.strftime(format = "%Y-%m-%d"))
        temps.append(frame)
    
    
    for frame in temps:
      print(len(frame))
      if len(frame) > 0:
        if (frame.equals(temps[0])) or (frame.equals(temps[2])):
          frame = frame[['Event Time','Media Source','Channel','Campaign','Adset','Country Code', 'iso_alpha', 'State', 'Device Category', 'Platform']]
          frame = frame.rename(columns = {'Event Time':'Installs'})
          frame = frame.groupby(['iso_alpha', 'State', 'Platform']).count().reset_index()
          frame = frame.groupby(['State', 'Platform']).sum().reset_index()
          fig = px.choropleth(frame,locations="State", color = 'Installs', locationmode="USA-states", hover_name="State", color_continuous_scale=px.colors.sequential.Plasma, scope="usa")
          fig.update_layout(title_text = '{} Adwords Installs by State (From Jan 1st to {})'.format(frame['Platform'][0], end_d), dragmode=False)
          figs_adwords.append(fig)
        else:
          frame = frame[['Event Time','Event Name','Event Value','Event Revenue Preferred','Media Source','Channel','Campaign','Adset','Country Code', 'iso_alpha','State', 'Device Category', 'Platform']]
          frame = frame.rename(columns = {'Event Revenue Preferred':'Purchases'})
          frame = frame.groupby(['iso_alpha', 'State', 'Platform']).sum().reset_index()
          frame = frame.groupby(['State', 'Platform']).sum().reset_index()
          fig = px.choropleth(frame,locations="State", color = 'Purchases', locationmode="USA-states", hover_name="State", color_continuous_scale=px.colors.sequential.Plasma, scope="usa")
          fig.update_layout(title_text = '{} Adwords Purchases by State (From Jan 1st to {})'.format(frame['Platform'][0], end_d), dragmode=False)
          figs_adwords.append(fig)


    joined_installs = pd.concat([temps[0], temps[2]], axis = 0)
    usa_installs = joined_installs.groupby('State').count().reset_index()
    usa_installs = usa_installs.rename(columns = {'Event Time':'Installs'})
    

    joined_purchases = pd.concat([temps[1], temps[3]], axis = 0)
    usa_purchases = joined_purchases.groupby('State').sum().reset_index()
    usa_purchases = usa_purchases.rename(columns = {'Event Revenue Preferred':'Purchases'})

    fig_usa_i = px.choropleth(usa_installs,locations="State", color = 'Installs', hover_name="State", locationmode="USA-states", color_continuous_scale=px.colors.sequential.Plasma, scope="usa")
    fig_usa_p= px.choropleth(usa_purchases, locations="State", color="Purchases", hover_name="State", locationmode="USA-states", color_continuous_scale=px.colors.sequential.Plasma, scope="usa")

    
    fig_usa_i.update_layout(
    title_text = 'Adwords Total Installs by State (From Jan 1st to {})'.format(end_d), dragmode=False)
    fig_usa_p.update_layout(
    title_text = 'Adwords Total Purchases by State (From Jan 1st to {})'.format(end_d), dragmode=False)
    figs_adwords.append(fig_usa_i)
    figs_adwords.append(fig_usa_p)

    joined_installs = joined_installs.groupby(["Day", "Channel"]).count().reset_index()
    joined_installs["Total"] = joined_installs["Event Time"]
    joined_installs["Event"] = "Installs"

    joined_purchases = joined_purchases.groupby(["Day", "Channel"]).sum().reset_index()
    joined_purchases["Total"] = joined_purchases['Event Revenue Preferred']
    joined_purchases["Event"] = "Purchases"

    joined_all = pd.concat([joined_installs, joined_purchases], axis = 0)
    print(joined_all["Day"])
    print(joined_all["Channel"])
    ###MAIN COUNTRY CHANNEL

    channel_fig = px.line(joined_all, x="Day", y="Total", color="Channel", facet_col = "Event")
    channel_fig.update_layout(title_text = 'Adwords Channel Performance')
    channel_fig.update_traces(mode='markers+lines')
    channel_fig.update_yaxes(title_text= "Revenue", row =1, col =1)
    channel_fig.update_yaxes(title_text= "Revenue", row =1, col =2)
    channel_fig.update_yaxes(title_text= "Installs", row =1, col =1)
    figs_adwords.append(channel_fig)
    ###COUNTRY PERFORMANCE BY CHANNEL

    #tab_past = go.Figure()
    #tab_past.add_trace(go.Table(header=dict(values=['Budget Name', 'Day 14 (%)', 'Total','ROAS', 'Day 13 (%)', 'Total','ROAS', 'Day 12 (%)', 'Total', 'ROAS', 'Day 11 (%)', 'Total', 'ROAS', 'Day 10 (%)', 'Total', 'ROAS', 'Day 9 (%)', 'Total','ROAS', 'Day 8 (%)', 'Total','ROAS', 'Avg week (%)', 'Total_Avg']),
        #         cells=dict(values=[bvalues['Name'].values, np.round(bvalues['Budget_14'],1),  np.round(bvalues['Budget_14_T'], 1) , np.round(bvalues['ROAS_14'], 1), np.round(bvalues['Budget_13'], 1) , np.round(bvalues['Budget_13_T'], 1) , np.round(bvalues['ROAS_13'], 1), np.round(bvalues['Budget_12'], 1), np.round(bvalues['Budget_12_T'], 1), np.round(bvalues['ROAS_12'], 1), np.round(bvalues['Budget_11'], 1) , np.round(bvalues['Budget_11_T'], 1), np.round(bvalues['ROAS_11'], 1), np.round(bvalues['Budget_10'], 1) , np.round(bvalues['Budget_10_T'], 1), np.round(bvalues['ROAS_10'], 1), np.round(bvalues['Budget_9'], 1) , np.round(bvalues['Budget_9_T'], 1), np.round(bvalues['ROAS_9'], 1), np.round(bvalues['Budget_8'], 1) , np.round(bvalues['Budget_8_T'], 1), np.round(bvalues['ROAS_8'], 1), np.round(bvalues['Average_past'],1), np.round(bvalues['Average_past_T'], 1) ])))
    #tab_past.update_layout(title_text = 'Budget Stats Last Week')

    return figs_adwords

def get_geo_performance(client_id, client_secret, refresh_token, developer_token, client_customer_id, start_date, end_date):

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
    SELECT Id, Date, CampaignName, CampaignStatus, Conversions, Impressions, Clicks, ConversionValue, Cost
    FROM CAMPAIGN_LOCATION_TARGET_REPORT
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

def drive_g(df, sheet_name):
    spreadsheet_key = '1tsnBq1_ZW4o5MHbte_FuT6NYHbHdwzX4ScxjH9asKU4'
    spread = Spread(spreadsheet_key) 
    cell = spread.get_sheet_dims(sheet_name)
    startc = 'A' + str(cell[0] + 1)
    spread.df_to_sheet(df, index=False, sheet=sheet_name, start=startc, headers = False)

def get_installs_report(app_id, api_token, start_date, end_date):

    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    client = AppsFlyer(api_token=api_token, app_id=app_id)
    df = client.installs_report(start_date, end_date, as_df=True)
    
    return df
  
def get_uninstalls_report(app_id, api_token, start_date, end_date):

    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    client = AppsFlyer(api_token=api_token, app_id=app_id)
    df = client.uninstall_events_report(start_date, end_date, as_df=True)
    
    return df

def get_inapp_report(app_id, api_token, start_date, end_date):

    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    client = AppsFlyer(api_token=api_token, app_id=app_id)
    df = client.in_app_events_report(start_date, end_date, as_df=True)
    
    return df

def get_location(client_id, client_secret, refresh_token, developer_token, client_customer_id, locations):
  # Initialize appropriate service.
    oauth2_client = oauth2.GoogleRefreshTokenClient(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token
    )

    # Define output as a string buffer

    # Initialize appropriate service.
    client = adwords.AdWordsClient(developer_token, oauth2_client)

    location_criterion_service = client.GetService(
      'LocationCriterionService', version='v201809')

  # Create the selector.
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

  # Make the get request.
    location_criteria = location_criterion_service.get(selector)
    return location_criteria

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

    

if __name__ == "__main__":
    main()
