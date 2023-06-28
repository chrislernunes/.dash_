# Moving Average Screener

import yfinance as yf
import pandas as pd

import dash
from dash import dcc, html, dash_table

from dash.dependencies import Input, Output

# Fetch stock data
stock_symbols = ['ABCAPITAL.NS', 'ABB.NS', 'AARTIIND.NS', 'ASIANPAINT.NS', 'APOLLOTYRE.NS', 'ABFRL.NS', 'AUROPHARMA.NS', 'BANDHANBNK.NS','ABBOTINDIA.NS', 'AXISBANK.NS', 'BATAINDIA.NS', 'BEL.NS', 
               'GODREJCP.NS', 'HINDPETRO.NS', 'ASHOKLEY.NS','ICICIGI.NS', 'ACC.NS', 'ADANIENT.NS', 'ADANIPORTS.NS', 'AUBANK.NS', 'BAJFINANCE.NS', 'BALKRISIND.NS', 'ALKEM.NS', 'AMBUJACEM.NS',
               'APOLLOHOSP.NS', 'BERGEPAINT.NS', 'COFORGE.NS', 'CUMMINSIND.NS', 'IPCALAB.NS', 'BAJAJFINSV.NS', 'BALRAMCHIN.NS', 'BANKBARODA.NS',
               'DIVISLAB.NS', 'BHARATFORG.NS', 'BHARTIARTL.NS','BIOCON.NS', 'BOSCHLTD.NS', 'BPCL.NS', 'DIXON.NS', 'BSOFT.NS', 'EICHERMOT.NS',
               'CANFINHOME.NS', 'CHAMBLFERT.NS', 'CHOLAFIN.NS', 'CIPLA.NS', 'COLPAL.NS', 'CONCOR.NS', 'ATUL.NS', 'COROMANDEL.NS', 'BAJAJ-AUTO.NS',
               'CROMPTON.NS', 'CUB.NS', 'DABUR.NS', 'DALBHARAT.NS', 'GUJGASLTD.NS', 'DEEPAKNTR.NS' , 'DELTACORP.NS', 'DRREDDY.NS', 'ESCORTS.NS', 
               'HCLTECH.NS', 'FEDERALBNK.NS', 'GAIL.NS', 'HDFCLIFE.NS', 'GLENMARK.NS', 'GMRINFRA.NS', 'GNFC.NS', 'GODREJPROP.NS', 'GRANULES.NS',
               'HAL.NS', 'HAVELLS.NS', 'HDFC.NS', 'HDFCBANK.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDCOPPER.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 
               'ICICIPRULI.NS', 'INDHOTEL.NS', 'INDIACEM.NS', 'INDIGO.NS', 'INDUSINDBK.NS', 'INFY.NS', 'IDFC.NS', 'INTELLECT.NS', 'IOC.NS', 'IRCTC.NS',
               'JKCEMENT.NS', 'JSWSTEEL.NS', 'BRITANNIA.NS', 'JUBLFOOD.NS', 'KOTAKBANK.NS', 'L&TFH.NS', 'IDFCFIRSTB.NS', 'LALPATHLAB.NS', 'LICHSGFIN.NS',
               'LT.NS', 'LTIM.NS', 'LTTS.NS', 'M&M.NS', 'M&MFIN.NS', 'MANAPPURAM.NS', 'MARICO.NS', 'MCDOWELL-N.NS','MCX.NS', 'METROPOLIS.NS', 'MFSL.NS', 
               'MOTHERSON.NS', 'MPHASIS.NS', 'MRF.NS', 'NATIONALUM.NS', 'NAUKRI.NS', 'NAVINFLUOR.NS', 'NESTLEIND.NS', 'MARUTI.NS', 'NMDC.NS', 
               'OBEROIRLTY.NS', 'ONGC.NS', 'PERSISTENT.NS', 'PETRONET.NS', 'PFC.NS', 'PIDILITIND.NS', 'PIIND.NS', 'PNB.NS', 'POLYCAB.NS', 'POWERGRID.NS',
               'PVRINOX.NS', 'RAIN.NS', 'RAMCOCEM.NS', 'RBLBANK.NS', 'RECLTD.NS', 'RELIANCE.NS', 'SBICARD.NS', 'SBIN.NS', 'SHREECEM.NS', 'SRF.NS', 'SUNPHARMA.NS',
               'SUNTV.NS', 'SYNGENE.NS', 'TATACHEM.NS', 'TATACOMM.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS',
               'TRENT.NS', 'UBL.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'VOLTAS.NS', 'WIPRO.NS', 'ZEEL.NS', 'BHEL.NS', 'IBULHSGFIN.NS', 'IEX.NS', 'INDUSTOWER.NS',
               'OFSS.NS', 'SBILIFE.NS', 'EXIDEIND.NS', 'TVSMOTOR.NS', 'COALINDIA.NS', 'DLF.NS', 'GRASIM.NS', 'IGL.NS', 'JINDALSTEL.NS', 'LAURUSLABS.NS',
               'MGL.NS', 'NTPC.NS', 'SAIL.NS', 'SHRIRAMFIN.NS','TITAN.NS','TORNTPHARM.NS', 'INDIAMART.NS', 'CANBK.NS', 'LUPIN.NS', 'PAGEIND.NS',
               'ZYDUSLIFE.NS', 'SIEMENS.NS', 'ITC.NS', 'HDFCAMC.NS', 'VEDL.NS', 'IDEA.NS', 'MUTHOOTFIN.NS', 'PEL.NS'] 


stock_data_df = pd.DataFrame()

# Create Dash application
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.H1('Moving Average Scanner'),
    html.H2('Price Distance From Moving Averages'),
    dash_table.DataTable(
        id='moving-averages-table',
        columns=[
            {"name": col, "id": col, "type": "numeric", "format": Format(precision=2, scheme=Scheme.fixed)}
            if col.endswith("Distance")
            else {"name": col, "id": col}
            for col in moving_avg_df.columns
        ],
        data=moving_avg_df.to_dict('records'),
        style_cell={'textAlign': 'center'},
        style_data_conditional=[
            {
                'if': {
                    'column_id': '10-day Distance',
                    'filter_query': '{10-day Distance} < 0'
                },
                'backgroundColor': 'red',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': '20-day Distance',
                    'filter_query': '{20-day Distance} < 0'
                },
                'backgroundColor': 'red',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': '50-day Distance',
                    'filter_query': '{50-day Distance} < 0'
                },
                'backgroundColor': 'red',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': '150-day Distance',
                    'filter_query': '{150-day Distance} < 0'
                },
                'backgroundColor': 'red',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': '200-day Distance',
                    'filter_query': '{200-day Distance} < 0'
                },
                'backgroundColor': 'red',
                'color': 'white',
            }
        ]
    ),
    html.H2('Stocks Above and Below Moving Averages'),
    dash_table.DataTable(
        id='above-below-table',
        columns=[
            {"name": col, "id": col, "type": "numeric", "format": Format(precision=2, scheme=Scheme.fixed)}
            if col.endswith("MA")
            else {"name": col, "id": col}
            for col in above_below_df.columns
        ],
        data=above_below_df.to_dict('records'),
        style_cell={'textAlign': 'center'},
    ),
])
