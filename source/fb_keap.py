import requests   
from pandas.io.json import json_normalize 
import pandas as pd  
from os.path import join
import os
import datetime
import numpy as np

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








def main(start, end):

    END_DATE = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")
    #report_id_to_file(START_DATE, END_DATE)

    my_app_id = '819895851973964' #'760820158011849'
    my_app_secret = '776c0a66c7c01d67f17742351ef9b2bf' #'762c8b6bbf2ab8a317f5652d2c2cfc1a'
    my_access_token = "EAALpsOECfUwBAPzqrV1smtCVKRv95WQ8bfhJh22O1bFUL02wxZBKnFyJjqfbNZAUk0Lw41Fq0JZBaqdOLZAM5o1aBHcMGaP1v7KsSS6QGaBPZBd6Tfk1PpwHJs0AECELUSkH9kxQZBR5MJgSE2ChbtcIynVhVxFYo8Qpb85f3huGNMAkpSJW08"

    FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

    sess = AdAccount('act_1163695460802157')  #'act_234375110958056'
    FIELDS = ['buying_type', 'objective']
    campaigns = sess.get_campaigns(fields = FIELDS)
    
    params = {
         'time_range': {'since': END_DATE, 'until': END_DATE},
         'fields': ['campaign_name', 'ad_name', "adset_name",'impressions', 'inline_link_clicks', 'spend', 'purchase_roas', 'actions']
     }

    df = pd.DataFrame(columns = ['campaign_name', 'date_start', 'date_stop', 'impressions', 'inline_link_clicks','spend', 'purchase_roas', 'actions'])
    
    indx = 0
    for campaign in campaigns:
        response = campaign.get_insights(params=params)
        for i in response:
            for col in i:
                df.loc[indx, col] = i[col]
        indx += 1
    df['spend'] = df['spend'].astype('float')
    print(df)

    df['purchase_roas'] = df['purchase_roas'].apply(lambda x: x if x is np.nan else x[0]['value'] )
    
    for i in df.index:
        if type(df.loc[i, 'actions']) != float:
            for j in df.loc[i, 'actions']:
                if j['action_type'] == 'mobile_app_install':
                    df.loc[i, 'actions'] = int(j['value'])
            if type(df.loc[i, 'actions']) != int:
                df.loc[i, 'actions'] = 0

    df['actions'] = df['actions'].astype('float')
    df['CPI'] = df['spend'] / df['actions']
    df['Revenue'] = df['purchase_roas'].astype('float') * df['spend']
    df.fillna('0', inplace = True)
    
    print(df)
    
    df.to_csv('fb_db_keap.csv', header = False, mode = 'a') 

    
    df_cum_total = pd.read_csv('fb_db_keap.csv')
    #df_cum_total = pd.concat([df_cum_total, df], axis = 0)
    idx = [ i for i in df_cum_total.index if 'BLP' not in df_cum_total.loc[i, 'campaign_name']]
    df_cum_total = df_cum_total.loc[idx]
    
    
    df_cum_total['Revenue'] = df_cum_total['Revenue'].astype('float')
    df_cum_total['impressions'] = df_cum_total['impressions'].astype('float')
    df_cum_total['inline_link_clicks'] = df_cum_total['inline_link_clicks'].astype('float')
    df_cum_total['purchase_roas'] = df_cum_total['purchase_roas'].astype('float')
    df_cum_total['avgCPA'] = df_cum_total['spend'].astype('float') / df_cum_total['actions'].astype('float')


    df_daily = df_cum_total.groupby('date_start').sum()
    df_daily['CPI'] = df_daily['spend'] / df_daily['actions']
    anno_df = df_daily[df_daily['spend'] > 0]
    text = np.round(anno_df["spend"].sum()/anno_df['actions'].sum(), 1)
    text_2 = np.round(anno_df['actions'].sum()/len(anno_df), 0)
    #Increasing spend on top <br> countries and keywords <br> with CPI below 1 <br> is recommended.
    #Focusing on reveneu kpis <br> is recommended or <br> retention metrics.
    if text >= 1:
        text = 'Overall CPI <br> is <b> {} </b> above 1.<br>Avg installs per <br> day is <b>{}</b>'.format(text, text_2) 
    else:
        text = 'Overall CPI <br> is <b> {} </b> below 1.<br>Avg installs per <br> day is <b>{}</b>'.format(text, text_2)
    #text = (df_daily["CPI"][-7:].sum() / 7) / (df_daily["CPI"].sum() / len(df_daily)) * 100

    figs_fb = []

    #fig = make_subplots( rows=1, cols=2, column_widths=[0.5, 0.5], specs=[[{'secondary_y':True}, {'secondary_y':True}]],
                    #subplot_titles=("Daily FB Conversions vs. CPI", "Cumulative FB KPIs" ))
   

    # Add traces

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df_daily.index, y=df_daily.CPI, name = 'CPI', marker_color = '#AB63FA'), secondary_y = True)

    fig.add_trace(go.Bar(x=df_daily.index, y=df_daily.actions, name = 'Installs',marker_color = '#00B5F7' ))

    #fig.add_trace(go.Scatter(x=df_daily.index, y=df_daily['spend'].cumsum(),
                   # mode='lines+markers',
                   # name='Cost', marker_color = '#EF553B'), row =1 , col = 2)
    #fig.add_trace(go.Bar(x=df_daily.index, y=df_daily['Revenue'].cumsum(), marker_color = 'rgb(204,204,204)', name = 'Revenue'),  row=1, col=2)

    fig.update_layout(title_text = "Daily Facebook Installs vs. CPI",
        annotations=[
            go.layout.Annotation(
                text=str(text),
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1.1,
                y=0.8,
                bordercolor='black',
                borderwidth=1
            )
        ]
    )
    fig.update_yaxes(title_text="Installs", secondary_y=False)
    fig.update_yaxes(title_text="CPI", secondary_y=True)
    fig.update_xaxes(title_text="Day")
    figs_fb.append(fig)

    camp = df_cum_total.groupby(['date_start', 'campaign_name']).sum().reset_index()

    fig = make_subplots( rows=3, cols=2, column_widths=[0.5, 0.5], row_heights=[0.3, .2, 0.5], specs=[[{ "colspan": 2, "secondary_y": True}, None], [{ "colspan": 2, "secondary_y": True}, None], [ { "colspan": 2, "secondary_y": True}   , None]],
                subplot_titles=("FB KPIs overall", "CPA vs CPT", "FB CPA per campaign" ))

    # Add traces
    
    fig.add_trace(go.Scatter(x=df_daily.index, y=df_daily['spend'],
                    mode='lines+markers',
                    name='Spend', yaxis='y2'), secondary_y=True, row=1, col=1)
    fig.add_trace(go.Scatter(x=df_daily.index, y=df_daily['spend']/df_daily['inline_link_clicks'],
                    mode='lines+markers',
                    name='avgCPT', yaxis='y2'), secondary_y=True, row=2, col=1)
    for i in camp.groupby('campaign_name').sum().reset_index()['campaign_name'].unique():
        fig.add_trace(go.Scatter(x=df_daily.index, y=camp[camp['campaign_name'] == i]['avgCPA'],
                   mode='lines+markers', name=i + ' avgCPI'), row=3, col=1)

    fig.add_trace(go.Scatter(x=df_daily.index, y=df_daily['avgCPA'],
                    mode='lines+markers',
                    name='avgCPI', yaxis='y2', marker_color = 'orange'), secondary_y=True, row=1, col=1)
    fig.add_trace(go.Scatter(x=df_daily.index, y=df_daily['avgCPA'],
                    mode='lines+markers',
                    name='avgCPI',  showlegend = False, marker_color = 'orange'), row=2, col=1)

    fig.add_trace(go.Bar(x=df_daily.index, y = df_daily["impressions"], name='Impressions',
                    marker_color = 'grey'), row= 1, col = 1)

    fig.add_trace(go.Bar(x=df_daily.index, y = df_daily["inline_link_clicks"], name='clicks',
                     marker_color = '#2CA02C'), row= 1, col = 1)

    fig.add_trace(go.Bar(x=df_daily.index, y = df_daily["actions"], name='installs',
                     marker_color = 'brown'), row= 1, col = 1)
    fig.update_layout(barmode = 'stack')

    figs_fb.append(fig)
    
    #start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
    #end_date = datetime.datetime.strptime(end, '%Y-%m-%d')
    #df_cum_total['date_start'] = pd.to_datetime(df_cum_total['date_start'], format = '%Y-%m-%d')
    df_camp =  df_cum_total.copy() #df_cum_total[(df_cum_total['date_start'] >= start_date) & (df_cum_total['date_start'] <= end_date)]
    #df_camp['date_start'] = df_camp['date_start'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df_camp = df_camp.groupby('campaign_name').sum().reset_index()
    df_camp['ROAS'] = df_camp['Revenue'] / df_camp['spend']
    df_camp['CTR'] = df_camp['inline_link_clicks'] / df_camp['impressions']
    df_camp['Conv.Rate'] = df_camp['actions'] / df_camp['inline_link_clicks']
    df_camp.sort_values('Conv.Rate', ascending = False, inplace = True)
    print(df_camp.head())

    trace0 = go.Pie(values=df_camp.impressions, labels=df_camp.campaign_name, hole=.4, name = 'Impressions', domain=dict(x=[0, 0.24],y=[0, 1]), title_text = 'Impressions', textposition='inside', textinfo='percent', hoverinfo="label+value")
    trace1 = go.Pie(values=df_camp.inline_link_clicks, labels=df_camp.campaign_name, hole=.4, name = 'Clicks', domain=dict(x=[0.25, 0.49],y=[0, 1]), title_text = 'Clicks', textposition='inside', textinfo='percent', hoverinfo="label+value")
    trace2 = go.Pie(values=df_camp.actions, labels=df_camp.campaign_name, hole=.4, name = 'Installs', domain=dict(x=[0.50, 0.74],y=[0, 1]), title_text = 'Installs', textposition='inside', textinfo='percent', hoverinfo="label+value")
    trace3 = go.Pie(values=df_camp.spend, labels=df_camp.campaign_name, hole=.4, name = 'Cost', domain=dict(x=[0.75, .99],y=[0, 1]), title_text = 'Cost', textposition='inside', textinfo='percent', hoverinfo="label+value")
    
   
    
    fig_dough = go.Figure(data = [trace0,trace1, trace2,trace3])
    fig_dough.update_layout(title_text="FB Breakdown by Campaign")
    fig_dough.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.96,
        xanchor="right",
        x=1), height = 600)

    figs_fb.append(fig_dough)

    trace = go.Table(header=dict(values=['Campaign','CTR', 'Conv.Rate']),
              cells=dict(values=[df_camp.campaign_name.values, np.round(df_camp.CTR.values, 2), np.round(df_camp['Conv.Rate'].values, 1)]))
    
    fig_tab = go.Figure(data = [trace])
    figs_fb.append(fig_tab)
    

    #performance_df_and = get_geo_by_date_report(app_id, api_token, start_date, END_DATE)

    #android = get_installs_report(app_id, api_token, END_DATE, END_DATE)

    #inapp_android = get_inapp_report(app_id, api_token, END_DATE, END_DATE)


    #android.to_csv('install_android.csv', header = False, mode = 'a')

    #installs_af = pd.read_csv('install_android.csv')
   
    #inapp_android.to_csv('purchases_android.csv', header = False, mode = 'a')

    #purchases_af = pd.read_csv('purchases_android.csv')
   

    #api_token = 'f0cbd5d4-1f74-412e-bead-d6c93dc226fb'

    #app_id = 'id1506654910'

    #performance_df_ios = get_geo_by_date_report(app_id, api_token, start_date, END_DATE)

    #print(performance_df_ios.columns)

    #ios = get_installs_report(app_id, api_token, END_DATE, END_DATE)
    #inapp_ios = get_inapp_report(app_id, api_token, END_DATE, END_DATE)

    #ios.to_csv('installs_ios.csv', header = False, mode = 'a')
    #inapp_ios.to_csv('purchases_ios.csv', header = False, mode = 'a')

    #ios_i = pd.read_csv('installs_ios.csv')
    
    #ios_pur =  pd.read_csv('purchases_ios.csv')
    
    
    #mapping = {'AW':'ABW','AF':'AFG','AO':'AGO','AI':'AIA','AX':'ALA','AL':'ALB','AD':'AND','AE':'ARE','AR':'ARG','AM':'ARM','AS':'ASM','AQ':'ATA','TF':'ATF','AG':'ATG','AU':'AUS','AT':'AUT','AZ':'AZE','BI':'BDI','BE':'BEL','BJ':'BEN','BQ':'BES','BF':'BFA','BD':'BGD','BG':'BGR','BH':'BHR','BS':'BHS','BA':'BIH','BL':'BLM','BY':'BLR','BZ':'BLZ','BM':'BMU','BO':'BOL','BR':'BRA','BB':'BRB','BN':'BRN','BT':'BTN','BV':'BVT','BW':'BWA','CF':'CAF','CA':'CAN','CC':'CCK','CH':'CHE','CL':'CHL','CN':'CHN','CI':'CIV','CM':'CMR','CD':'COD','CG':'COG','CK':'COK','CO':'COL','KM':'COM','CV':'CPV','CR':'CRI','CU':'CUB','CW':'CUW','CX':'CXR','KY':'CYM','CY':'CYP','CZ':'CZE','DE':'DEU','DJ':'DJI','DM':'DMA','DK':'DNK','DO':'DOM','DZ':'DZA','EC':'ECU','EG':'EGY','ER':'ERI','EH':'ESH','ES':'ESP','EE':'EST','ET':'ETH','FI':'FIN','FJ':'FJI','FK':'FLK','FR':'FRA','FO':'FRO','FM':'FSM','GA':'GAB','GB':'GBR','GE':'GEO','GG':'GGY','GH':'GHA','GI':'GIB','GN':'GIN','GP':'GLP','GM':'GMB','GW':'GNB','GQ':'GNQ','GR':'GRC','GD':'GRD','GL':'GRL','GT':'GTM','GF':'GUF','GU':'GUM','GY':'GUY','HK':'HKG','HM':'HMD','HN':'HND','HR':'HRV','HT':'HTI','HU':'HUN','ID':'IDN','IM':'IMN','IN':'IND','IO':'IOT','IE':'IRL','IR':'IRN','IQ':'IRQ','IS':'ISL','IL':'ISR','IT':'ITA','JM':'JAM','JE':'JEY','JO':'JOR','JP':'JPN','KZ':'KAZ','KE':'KEN','KG':'KGZ','KH':'KHM','KI':'KIR','KN':'KNA','KR':'KOR','KW':'KWT','LA':'LAO','LB':'LBN','LR':'LBR','LY':'LBY','LC':'LCA','LI':'LIE','LK':'LKA','LS':'LSO','LT':'LTU','LU':'LUX','LV':'LVA','MO':'MAC','MF':'MAF','MA':'MAR','MC':'MCO','MD':'MDA','MG':'MDG','MV':'MDV','MX':'MEX','MH':'MHL','MK':'MKD','ML':'MLI','MT':'MLT','MM':'MMR','ME':'MNE','MN':'MNG','MP':'MNP','MZ':'MOZ','MR':'MRT','MS':'MSR','MQ':'MTQ','MU':'MUS','MW':'MWI','MY':'MYS','YT':'MYT','NA':'NAM','NC':'NCL','NE':'NER','NF':'NFK','NG':'NGA','NI':'NIC','NU':'NIU','NL':'NLD','NO':'NOR','NP':'NPL','NR':'NRU','NZ':'NZL','OM':'OMN','PK':'PAK','PA':'PAN','PN':'PCN','PE':'PER','PH':'PHL','PW':'PLW','PG':'PNG','PL':'POL','PR':'PRI','KP':'PRK','PT':'PRT','PY':'PRY','PS':'PSE','PF':'PYF','QA':'QAT','RE':'REU','RO':'ROU','RU':'RUS','RW':'RWA','SA':'SAU','SD':'SDN','SN':'SEN','SG':'SGP','GS':'SGS','SH':'SHN','SJ':'SJM','SB':'SLB','SL':'SLE','SV':'SLV','SM':'SMR','SO':'SOM','PM':'SPM','RS':'SRB','SS':'SSD','ST':'STP','SR':'SUR','SK':'SVK','SI':'SVN','SE':'SWE','SZ':'SWZ','SX':'SXM','SC':'SYC','SY':'SYR','TC':'TCA','TD':'TCD','TG':'TGO','TH':'THA','TJ':'TJK','TK':'TKL','TM':'TKM','TL':'TLS','TO':'TON','TT':'TTO','TN':'TUN','TR':'TUR','TV':'TUV','TW':'TWN','TZ':'TZA','UG':'UGA','UA':'UKR','UM':'UMI','UY':'URY','US':'USA','UZ':'UZB','VA':'VAT','VC':'VCT','VE':'VEN','VG':'VGB','VI':'VIR','VN':'VNM','VU':'VUT','WF':'WLF','WS':'WSM','YE':'YEM','ZA':'ZAF','ZM':'ZMB','ZW':'ZWE'}

    #dfs=[installs_af,purchases_af,ios_i,ios_pur]

    #temps = []
    #for frame in dfs:
    #    frame = frame[frame['Media Source'] == "Facebook Ads"]
    #    frame['iso_alpha'] = frame['Country Code'].map(mapping)
    #    frame = frame[frame['iso_alpha'] == 'USA']
    #    frame["Event Time"] = frame["Event Time"].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
    #    frame["Day"] = frame["Event Time"].apply(lambda x: x.strftime(format = "%Y-%m-%d"))
    #    temps.append(frame)
    
    
    #for frame in temps:
    #  print(len(frame))
    #  if len(frame) > 0:
    #    if (frame.equals(temps[0])) or (frame.equals(temps[2])):
    #      frame = frame[['Event Time','Media Source','Channel','Campaign','Adset','Country Code', 'iso_alpha', 'State', 'Device Category', 'Platform']]
    #      frame = frame.rename(columns = {'Event Time':'Installs'})
    #      frame = frame.groupby(['iso_alpha', 'State', 'Platform']).count().reset_index()
    #      frame = frame.groupby(['State', 'Platform']).sum().reset_index()
    #      fig = px.choropleth(frame,locations="State", color = 'Installs', locationmode="USA-states", hover_name="State", color_continuous_scale=px.colors.sequential.Plasma, scope="usa")
    #      fig.update_layout(title_text = 'FB {} Installs by State (From Jan 1st - Until {})'.format(frame['Platform'][0], END_DATE), dragmode=False)
    #      figs_fb.append(fig)
    #    else:
    #      frame = frame[['Event Time','Event Name','Event Value','Event Revenue Preferred','Media Source','Channel','Campaign','Adset','Country Code', 'iso_alpha','State', 'Device Category', 'Platform']]
    #      frame = frame.rename(columns = {'Event Revenue Preferred':'Purchases Revenue'})
    #      frame = frame.groupby(['iso_alpha', 'State', 'Platform']).sum().reset_index()
    #      frame = frame.groupby(['State', 'Platform']).sum().reset_index()
    #      fig = px.choropleth(frame,locations="State", color = 'Purchases Revenue', locationmode="USA-states", hover_name="State", color_continuous_scale=px.colors.sequential.Plasma, scope="usa")
    #      fig.update_layout(title_text = 'FB {} Purchases by State (From Jan 1st - Until {})'.format(frame['Platform'][0], END_DATE), dragmode=False)
    #      figs_fb.append(fig)




    #joined_installs = pd.concat([temps[0], temps[2]], axis = 0)
    ##joined_installs['Day'] = joined_installs["Day"].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
    #START_DATE = datetime.datetime.now() - datetime.timedelta(days = 29)
    #joined_installs = joined_installs[joined_installs['Day'] > START_DATE]
    #joined_installs["Day"] = joined_installs["Day"].apply(lambda x: x.strftime(format = "%Y-%m-%d"))
    #usa_installs = joined_installs.groupby('State').count().reset_index()
    #usa_installs = usa_installs.rename(columns = {'Event Time':'Installs'})
    

    #joined_purchases = pd.concat([temps[1], temps[3]], axis = 0)
    #joined_purchases['Day'] = joined_purchases["Day"].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
    #joined_purchases = joined_purchases[joined_purchases['Day'] > START_DATE]
    #joined_purchases["Day"] = joined_installs["Day"].apply(lambda x: x.strftime(format = "%Y-%m-%d"))
    #usa_purchases = joined_purchases.groupby('State').sum().reset_index()
    #usa_purchases = usa_purchases.rename(columns = {'Event Revenue Preferred':'Purchases Revenue'})

    

    #fig_usa_i = px.choropleth(usa_installs,locations="State", color = 'Installs', hover_name="State", locationmode="USA-states", color_continuous_scale=px.colors.sequential.Plasma, scope="usa")
    #fig_usa_p= px.choropleth(usa_purchases, locations="State", color="Purchases Revenue", hover_name="State", locationmode="USA-states", color_continuous_scale=px.colors.sequential.Plasma, scope="usa")

    
    #fig_usa_i.update_layout(
    #title_text = 'FB Total Installs by State (From Jan 1st - Until {})'.format(END_DATE), dragmode=False)
    #fig_usa_p.update_layout(
    #title_text = 'FB Total Purchases by State (From Jan 1st - Until {})'.format(END_DATE), dragmode=False)
    #figs_fb.append(fig_usa_i)
    #figs_fb.append(fig_usa_p)



    #joined_installs = joined_installs.groupby(["Day", "Channel"]).count().reset_index()
    #joined_installs["Total"] = joined_installs["Event Time"]
    #joined_installs["Event"] = "Installs"

    #joined_purchases = joined_purchases.groupby(["Day", "Channel"]).sum().reset_index()
    #joined_purchases["Total"] = joined_purchases['Event Revenue Preferred']
    #joined_purchases["Event"] = "Purchases"

    #joined_all = pd.concat([joined_installs, joined_purchases], axis = 0)
    #print(joined_all["Day"])
    #print(joined_all["Channel"])
    ###MAIN COUNTRY CHANNEL

    #channel_fig = px.bar(joined_all, x="Day", y="Total", color="Channel", facet_col = "Event")
    #channel_fig.update_layout(title_text = 'FB Channel Performance')
    #channel_fig.update_traces(mode='markers+lines')
    #channel_fig.update_yaxes(title_text= "Revenue", row =1, col =2)
    #channel_fig.update_yaxes(title_text= "Installs", row =1, col =1)
    #figs_fb.append(channel_fig)
    ###COUNTRY PERFORMANCE BY CHANNEL

    #fig_map_rev = px.choropleth(df_fig_af, locations="iso_alpha", color="Total Revenue", hover_name="iso_alpha", color_continuous_scale=px.colors.sequential.Plasma)
    #fig_map_conv.update_layout(
    #title_text="Installs by Geolocation")
    #fig_map_rev.update_layout(
    #title_text="Revenue by Geolocation")
    

    #df_af_ios = get_geo_by_date_report(app_id, api_token, start_date, END_DATE)
    #df_af_ios = df_af_ios[df_af_ios['Media Source (pid)'] == 'Facebook Ads'].reset_index(drop = True)
    #df_ios = df_af_ios[['Date', 'Country', 'Campaign (c)', 'Impressions', 'Clicks', 'Installs', 'Total Revenue', 'Total Cost',
       #                         'ARPU']].reset_index(drop = True)
    #idx = [ i for i in df_ios.index if 'AGN' in df_ios.loc[i, 'Campaign (c)']]
    #df_ios = df_ios.loc[idx, :]
    #print(df_ios)

    #app_id = 'com.ugroupmedia.pnp14'
    #df_af_android = get_geo_by_date_report(app_id, api_token, start_date, END_DATE)
    #df_af_android = df_af_android[df_af_android['Media Source (pid)'] == 'Facebook Ads'].reset_index(drop = True)
    #df_android = df_af_android[['Date', 'Country', 'Campaign (c)', 'Impressions', 'Clicks', 'Installs', 'Total Revenue', 'Total Cost',
     #                           'ARPU']].reset_index(drop = True)
    #idx = [ i for i in df_android.index if 'AGN' in df_android.loc[i, 'Campaign (c)']]
    #df_android = df_android.loc[idx, :]
    #print(df_android)

    #df_country = pd.concat([df_ios, df_android], axis = 0)
    #df_country = df_country.groupby(['Date', 'Country', 'Campaign (c)']).sum().reset_index().sort_values('Date')
    #df_country = df_country[df_country['Total Revenue'] > 0 ].reset_index(drop = True)

    #fig_camp = px.bar(df_country, x='Date', y='Installs', color='Campaign (c)',
     #           facet_col='Country', facet_col_wrap=2)
    #fig_camp.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    ##fig_camp.update_yaxes(matches=None, showticklabels=True, title_text='')
    #fig_camp.update_xaxes(matches=None, showticklabels=True, title_text='')
    #fig_camp.update_layout(
       # title_text="Daily FB Campaigns Installs per Country", height = 950, barmode = 'stack')

    with open('Fb_keap.html', 'w') as file:
        for fig in figs_fb:
            file.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

    

def get_installs_report(app_id, api_token, start_date, end_date):

    
    
    client = AppsFlyer(api_token=api_token, app_id=app_id)
    df = client.installs_report(start_date, end_date, as_df=True)
    
    return df
  
def get_uninstalls_report(app_id, api_token, start_date, end_date):

    
    
    client = AppsFlyer(api_token=api_token, app_id=app_id)
    df = client.uninstall_events_report(start_date, end_date, as_df=True)
    
    return df

def get_inapp_report(app_id, api_token, start_date, end_date):

    

    client = AppsFlyer(api_token=api_token, app_id=app_id)
    df = client.in_app_events_report(start_date, end_date, as_df=True)
    
    return df  
    
def get_geo_by_date_report(app_id, api_token, start_date, end_date):
    
    client = AppsFlyer(api_token=api_token, app_id=app_id)
    df = client.geo_by_date_report(start_date, end_date, as_df=True)
    
    return df

def drive_fb(df, sheet_name):
    spreadsheet_key = '1tsnBq1_ZW4o5MHbte_FuT6NYHbHdwzX4ScxjH9asKU4'
    spread = Spread(spreadsheet_key) 
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

if __name__ == "__main__":
    main('2021-05-10', '2021-06-06')

