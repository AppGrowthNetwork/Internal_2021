import requests
import json
import pandas as pd

from plotly.subplots import make_subplots
import plotly.graph_objects as go


advertiser_id = 6850879149737771013
START_DATE = "2021-11-15"
END_DATE = "2021-12-13"
url = "https://business-api.tiktok.com/open_api/v1.2/reports/integrated/get/?advertiser_id={}&report_type=BASIC&dimensions=[\"stat_time_day\",\"campaign_id\"]&data_level=AUCTION_CAMPAIGN&start_date={}&end_date={}&metrics=[\"campaign_name\",\"spend\",\"cost_per_conversion\",\"impressions\",\"cpc\",\"cpm\",\"ctr\",\"real_time_app_install\"]&order_field=real_time_app_install&page_size=1000".format(advertiser_id, START_DATE, END_DATE)

r = requests.get(url, headers={"Access-Token":"c29d32b795fa21f4b5d07cae8b3626531e5d9750"})
text = json.loads(r.text)
data = text.get('data', None).get("list", None)

df = pd.DataFrame()
for i in data:
    row = pd.DataFrame([i.get('metrics', None)])
    row['day'] = i.get('dimensions', None).get('stat_time_day', None).split(" ")[0]
    df = pd.concat([df, row])

cols = ["spend","cost_per_conversion","impressions","cpc","cpm","ctr","real_time_app_install"]
for i in cols:
    df[i] = df[i].astype('float')
custom = df.groupby(['day', 'campaign_name']).sum().reset_index()
custom['day'] = pd.to_datetime(custom['day'], format = "%Y-%m-%d")
figs_tiktok = []

fig = make_subplots( rows=3, cols=2, column_widths=[0.5, 0.5], row_heights=[0.3, .2, 0.5], specs=[[{ "colspan": 2, "secondary_y": True}, None], [{ "colspan": 2, "secondary_y": True}, None], [ { "colspan": 2, "secondary_y": True}   , None]],
                subplot_titles=("TikTok's KPIs overall", "CPI vs CTR", "TikTok CPC per campaign" ))

# Add traces
    
fig.add_trace(go.Scatter(x=custom.day, y=custom.groupby('day').sum()['spend'],
                    mode='lines+markers',
                    name='Spend', yaxis='y2'), secondary_y=True, row=1, col=1)
fig.add_trace(go.Scatter(x=custom.day, y=custom.groupby('day').sum()['ctr'],
                    mode='lines+markers',
                    name='CTR', yaxis='y2'), secondary_y=True, row=2, col=1)
for i in custom.groupby('campaign_name').sum().reset_index()['campaign_name'].unique():
    fig.add_trace(go.Scatter(x=custom.day, y=custom[custom['campaign_name'] == i]['cpc'],
                   mode='lines+markers', name=i), row=3, col=1)

fig.add_trace(go.Scatter(x=custom.day, y=custom.groupby('day').sum()['spend']/custom.groupby('day').sum()['real_time_app_install'],
                    mode='lines+markers',
                    name='CPI',  showlegend = False, marker_color = 'orange'), row=2, col=1)

fig.add_trace(go.Bar(x=custom.groupby('day').sum().index, y = custom.groupby('day').sum()["impressions"], name='Impressions',
                    marker_color = 'grey'), row= 1, col = 1)

fig.add_trace(go.Bar(x=custom.groupby('day').sum().index, y = custom.groupby('day').sum()["cpc"] * custom.groupby('day').sum()["spend"], name='taps',
                     marker_color = '#2CA02C'), row= 1, col = 1)

fig.add_trace(go.Bar(x=custom.groupby('day').sum().index, y = custom.groupby('day').sum()["real_time_app_install"], name='installs',
                     marker_color = 'brown'), row= 1, col = 1)

fig.update_layout(barmode = 'stack')

figs_tiktok.append(fig)

with open('dash_tiktok_daily_franki.html', 'w') as f:
        for fig in figs_tiktok:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

##COUNTRY REPORT CALL
##https://business-api.tiktok.com/open_api/v1.2/reports/integrated/get/?advertiser_id=6850879149737771013&report_type=AUDIENCE&dimensions=["stat_time_day","campaign_id", "country_code"]&data_level=AUCTION_CAMPAIGN&start_date=2021-11-10&end_date=2021-11-17&metrics=["campaign_name","spend","cost_per_conversion","impressions","cpc","cpm","ctr"]&order_field=impressions&page_size=1000

##DOCUMENTATION
##https://ads.tiktok.com/marketing_api/docs?id=1701890949889025
