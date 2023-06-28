# Moving Average Screener
# Created by Chrisler Nunes
# 28th June 20023

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





for symbol in stock_symbols:
    stock_data = yf.download(symbol, start='2021-01-01', end='2023-06-26')
    stock_data["Symbol"] = symbol
    stock_data_df = pd.concat([stock_data_df, stock_data], ignore_index=True)

# Calculate the moving averages
stock_data_df['10-day MA'] = stock_data_df.groupby('Symbol')['Close'].rolling(window=10).mean().reset_index(0, drop=True).round(2)
stock_data_df['20-day MA'] = stock_data_df.groupby('Symbol')['Close'].rolling(window=20).mean().reset_index(0, drop=True).round(2)
stock_data_df['50-day MA'] = stock_data_df.groupby('Symbol')['Close'].rolling(window=50).mean().reset_index(0, drop=True).round(2)
stock_data_df['150-day MA'] = stock_data_df.groupby('Symbol')['Close'].rolling(window=150).mean().reset_index(0, drop=True).round(2)
stock_data_df['200-day MA'] = stock_data_df.groupby('Symbol')['Close'].rolling(window=200).mean().reset_index(0, drop=True).round(2)

latest_data = stock_data_df.groupby('Symbol').tail(1).round(2)
moving_avg_df = latest_data[['Symbol', 'Open', 'High', 'Low', 'Close', 'Volume', '10-day MA', '20-day MA', '50-day MA', '150-day MA', '200-day MA']]

# Calculate the distance from each average to the current price as a percentage
moving_avg_df['10-day Distance'] = ((moving_avg_df['Close'] - moving_avg_df['10-day MA']) / moving_avg_df['Close'] * 100).round(2)
moving_avg_df['20-day Distance'] = ((moving_avg_df['Close'] - moving_avg_df['20-day MA']) / moving_avg_df['Close'] * 100).round(2)
moving_avg_df['50-day Distance'] = ((moving_avg_df['Close'] - moving_avg_df['50-day MA']) / moving_avg_df['Close'] * 100).round(2)
moving_avg_df['150-day Distance'] = ((moving_avg_df['Close'] - moving_avg_df['150-day MA']) / moving_avg_df['Close'] * 100).round(2)
moving_avg_df['200-day Distance'] = ((moving_avg_df['Close'] - moving_avg_df['200-day MA']) / moving_avg_df['Close'] * 100).round(2)

above_below_df = pd.DataFrame(index=['Above', 'Below'])

# Calculate the total stocks above and below each moving average
above_below_df['10-day MA'] = [len(moving_avg_df[moving_avg_df['10-day Distance'] < 0]), len(moving_avg_df[moving_avg_df['10-day Distance'] > 0])]
above_below_df['20-day MA'] = [len(moving_avg_df[moving_avg_df['20-day Distance'] < 0]), len(moving_avg_df[moving_avg_df['20-day Distance'] > 0])]
above_below_df['50-day MA'] = [len(moving_avg_df[moving_avg_df['50-day Distance'] < 0]), len(moving_avg_df[moving_avg_df['50-day Distance'] > 0])]
above_below_df['150-day MA'] = [len(moving_avg_df[moving_avg_df['150-day Distance'] < 0]), len(moving_avg_df[moving_avg_df['150-day Distance'] > 0])]
above_below_df['200-day MA'] = [len(moving_avg_df[moving_avg_df['200-day Distance'] < 0]), len(moving_avg_df[moving_avg_df['200-day Distance'] > 0])]

# Create Dash application
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.H1('Moving Average Scanner'),
    html.H2('Price Distance From Moving Averages'),
    dash_table.DataTable(
        id='moving-averages-table',
        columns=[{"name": col, "id": col} for col in moving_avg_df.columns],
        data=moving_avg_df.to_dict('records'),
        style_cell={'textAlign': 'center'},
        style_data_conditional=[
            {
                'if': {
                    'column_id': '10-day Distance',
                    'filter_query': '{10-day Distance} < 0'
                },
                'backgroundColor': 'green',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': '20-day Distance',
                    'filter_query': '{20-day Distance} < 0'
                },
                'backgroundColor': 'green',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': '50-day Distance',
                    'filter_query': '{50-day Distance} < 0'
                },
                'backgroundColor': 'green',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': '150-day Distance',
                    'filter_query': '{150-day Distance} < 0'
                },
                'backgroundColor': 'green',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': '200-day Distance',
                    'filter_query': '{200-day Distance} < 0'
                },
                'backgroundColor': 'green',
                'color': 'white',
            }
        ]
    ),
    html.H2('Stocks Above and Below Moving Averages'),
    dash_table.DataTable(
        id='above-below-table',
        columns=[{"name": col, "id": col} for col in above_below_df.columns],
        data=above_below_df.to_dict('records'),
        style_cell={'textAlign': 'center'},
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
