# Create by Chrisler Nunes

# Date 28th June 2023



import dash
from dash import dcc, html, dash_table

import pandas as pd
import yfinance as yf

# Define the list of stock symbols
symbol_sgx = ['ABCAPITAL.NS', 'ABB.NS', 'AARTIIND.NS', 'ASIANPAINT.NS', 'APOLLOTYRE.NS', 'ABFRL.NS', 'AUROPHARMA.NS', 'BANDHANBNK.NS','ABBOTINDIA.NS', 'AXISBANK.NS', 'BATAINDIA.NS', 'BEL.NS', 
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

# Initialize an empty DataFrame
df = pd.DataFrame()


# Fetch data for each stock symbol
for stock in symbol_sgx:
    ticker = yf.Ticker(stock)
    info = ticker.info
    beta = info.get('beta')
    marketcap = info.get('marketCap')
    pe_ratio = info.get('trailingPE')
    high_52week = info.get('fiftyTwoWeekHigh')
    low_52week = info.get('fiftyTwoWeekLow')
    price = ticker.history(period='1d')['Close'][-1]
    open_price = ticker.history(period='1d')['Open'][-1]
    high_price = ticker.history(period='1d')['High'][-1]
    low_price = ticker.history(period='1d')['Low'][-1]
    change = round(ticker.history(period='1d')['Close'][-1] - ticker.history(period='1d')['Open'][-1], 2)

    # Determine if price is near 52-week high or low
    price_signal = ''
    if price >= high_52week * 0.95 and price <= high_52week * 1.05:
        price_signal = 'Near 52-Week High'
        high_52week = f'***{high_52week:.2f}***'
    elif price >= low_52week * 0.95 and price <= low_52week * 1.05:
        price_signal = 'Near 52-Week Low'
        low_52week = f'***{low_52week:.2f}***'

    # Retrieve historical volume data for the last 3 days, 10 days, and 3 months
    history_daily = ticker.history(period='1d')

    volume_daily = history_daily['Volume'][-1]
    average_volume = info.get('averageVolume')

    # Create a signal where 3-day volume exceeds 1-day volume
    volume_signal = 'No Signal'
    if volume_daily > average_volume:
        volume_signal = 'Volume Surge'

    df_temp = pd.DataFrame({'Stock': stock, 'Open': round(open_price, 2), 'High': round(high_price, 2), 'Low': round(low_price, 2), 'Close': round(price, 2), 'Change': change, 'Beta': [beta], 'Marketcap': [marketcap],
                            'P/E Ratio': [pe_ratio],
                            '52 Week High': [high_52week],
                            '52 Week Low': [low_52week],
                            'Volume (Daily)': [volume_daily],
                            'Average Volume': [average_volume],
                            'Price Signal': [price_signal],
                            'Volume Signal': [volume_signal]})
    df = pd.concat([df, df_temp], ignore_index=True)

# Create a Dash app
app = dash.Dash(__name__)
server = app.server

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1('Long_Short_ Screener'),
    dash_table.DataTable(
        id='stock-table',
        data=df.to_dict('records'),
        columns=[
            {'name': 'Stock', 'id': 'Stock'},
            {'name': 'Open', 'id': 'Open'},
            {'name': 'High', 'id': 'High'},
            {'name': 'Low', 'id': 'Low'},
            {'name': 'Close', 'id': 'Close'},
            {'name': 'Change', 'id': 'Change'},
            {'name': 'Beta', 'id': 'Beta'},
            {'name': 'Marketcap', 'id': 'Marketcap'},
            {'name': 'P/E Ratio', 'id': 'P/E Ratio'},
            {'name': '52 Week High', 'id': '52 Week High'},
            {'name': '52 Week Low', 'id': '52 Week Low'},
            {'name': 'Volume (Daily)', 'id': 'Volume (Daily)'},
            {'name': 'Average Volume', 'id': 'Average Volume'},
            {'name': 'Price Signal', 'id': 'Price Signal'},
            {'name': 'Volume Signal', 'id': 'Volume Signal'}
        ],
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{Price Signal} contains "Near"'
                },
                'backgroundColor': 'yellow',
                'color': 'black',
            },
            {
                'if': {
                    'filter_query': '{Volume Signal} contains "Volume Surge"'
                },
                'backgroundColor': 'green',
                'color': 'white',
            }
        ],
        style_table={'height': '800px', 'overflowY': 'scroll'}
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
