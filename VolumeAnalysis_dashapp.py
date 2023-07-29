import dash
from dash import html, dcc, dash_table
import yfinance as yf
import pandas as pd
from nselib import capital_market



pd.set_option('display.max_rows', None)
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="2y")
    data['3 Day Avg Volume'] = data['Volume'].rolling(window=3).mean().fillna(0).round().astype(int)
    data['Weekly Avg Volume'] = data['Volume'].rolling(window=5).mean().fillna(0).round().astype(int)
    data['Monthly Avg Volume'] = data['Volume'].rolling(window=20).mean().fillna(0).round().astype(int)
    data['Yearly Avg Volume'] = data['Volume'].rolling(window=252).mean().fillna(0).round().astype(int)
    data['Ticker'] = ticker
    data['Change %'] = (data['Close'].pct_change() * 100).fillna(0).round(2)

    data = data.round(2)

    return data[['Ticker', 'Open', 'High', 'Low', 'Close', 'Change %', 'Volume', '3 Day Avg Volume', 'Weekly Avg Volume', 'Monthly Avg Volume', 'Yearly Avg Volume']]

# LIST FOR YF IMPORTS 
stock_tickers = ['ABCAPITAL.NS', 'ABB.NS', 'AARTIIND.NS', 'ASIANPAINT.NS', 'APOLLOTYRE.NS', 'ABFRL.NS', 'AUROPHARMA.NS', 'BANDHANBNK.NS','ABBOTINDIA.NS', 'AXISBANK.NS', 'BATAINDIA.NS', 'BEL.NS', 
               'GODREJCP.NS', 'HINDPETRO.NS', 'ASHOKLEY.NS','ICICIGI.NS', 'ACC.NS', 'ADANIENT.NS', 'ADANIPORTS.NS', 'AUBANK.NS', 'BAJFINANCE.NS', 'BALKRISIND.NS', 'ALKEM.NS', 'AMBUJACEM.NS',
               'APOLLOHOSP.NS', 'BERGEPAINT.NS', 'COFORGE.NS', 'CUMMINSIND.NS', 'IPCALAB.NS', 'BAJAJFINSV.NS', 'BALRAMCHIN.NS', 'BANKBARODA.NS',
               'DIVISLAB.NS', 'BHARATFORG.NS', 'BHARTIARTL.NS','BIOCON.NS', 'BOSCHLTD.NS', 'BPCL.NS', 'DIXON.NS', 'BSOFT.NS', 'EICHERMOT.NS',
               'CANFINHOME.NS', 'CHAMBLFERT.NS', 'CHOLAFIN.NS', 'CIPLA.NS', 'COLPAL.NS', 'CONCOR.NS', 'ATUL.NS', 'COROMANDEL.NS', 'BAJAJ-AUTO.NS',
               'CROMPTON.NS', 'CUB.NS', 'DABUR.NS', 'DALBHARAT.NS', 'GUJGASLTD.NS', 'DEEPAKNTR.NS' , 'DELTACORP.NS', 'DRREDDY.NS', 'ESCORTS.NS', 
               'HCLTECH.NS', 'FEDERALBNK.NS', 'GAIL.NS', 'HDFCLIFE.NS', 'GLENMARK.NS', 'GMRINFRA.NS', 'GNFC.NS', 'GODREJPROP.NS', 'GRANULES.NS',
               'HAL.NS', 'HAVELLS.NS', 'HDFCBANK.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDCOPPER.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 
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


all_stocks_data = pd.DataFrame()
for ticker in stock_tickers:
    stock_data = get_stock_data(ticker)
    all_stocks_data = all_stocks_data._append(stock_data.iloc[-1], ignore_index=True)


def highlight_crossing(s):
    crossing_styles = [''] * len(s)
    if s['Volume'] > s['3 Day Avg Volume']:
        crossing_styles[7] = 'color: green;'
    if s['Volume'] > s['Weekly Avg Volume']:
        crossing_styles[8] = 'color: orange;'
    if s['Volume'] > s['Monthly Avg Volume']:
        crossing_styles[9] = 'color: blue;'
    if s['Volume'] > s['Yearly Avg Volume']:
        crossing_styles[10] = 'color: red;'
    return crossing_styles

highlighted_stocks_data = all_stocks_data.style.apply(highlight_crossing, axis=1)

# LIST FOR NSELIB IMPORTS 
stock_symbols = ['ABCAPITAL', 'ABB', 'AARTIIND', 'ASIANPAINT', 'APOLLOTYRE', 'ABFRL', 'AUROPHARMA', 'BANDHANBNK','ABBOTINDIA', 'AXISBANK', 'BATAINDIA', 'BEL', 
                'GODREJCP', 'HINDPETRO', 'ASHOKLEY','ICICIGI', 'ACC', 'ADANIENT', 'ADANIPORTS', 'AUBANK', 'BAJFINANCE', 'BALKRISIND', 'ALKEM', 'AMBUJACEM',
                'APOLLOHOSP', 'BERGEPAINT', 'COFORGE', 'CUMMINSIND', 'IPCALAB', 'BAJAJFINSV', 'BALRAMCHIN', 'BANKBARODA',
                'DIVISLAB', 'BHARATFORG', 'BHARTIARTL','BIOCON', 'BOSCHLTD', 'BPCL', 'DIXON', 'BSOFT', 'EICHERMOT',
                'CANFINHOME', 'CHAMBLFERT', 'CHOLAFIN', 'CIPLA', 'COLPAL', 'CONCOR', 'ATUL', 'COROMANDEL', 'BAJAJ-AUTO',
                'CROMPTON', 'CUB', 'DABUR', 'DALBHARAT', 'GUJGASLTD', 'DEEPAKNTR' , 'DELTACORP', 'DRREDDY', 'ESCORTS', 
                'HCLTECH', 'FEDERALBNK', 'GAIL', 'HDFCLIFE', 'GLENMARK', 'GMRINFRA', 'GNFC', 'GODREJPROP', 'GRANULES', 'HAL', 'HAVELLS', 'HDFCBANK', 'HEROMOTOCO', 'HINDALCO', 'HINDCOPPER', 'HINDUNILVR', 'ICICIBANK', 
                'ICICIPRULI', 'INDHOTEL', 'INDIACEM', 'INDIGO', 'INDUSINDBK', 'INFY', 'IDFC', 'INTELLECT', 'IOC', 'IRCTC',
                'JKCEMENT', 'JSWSTEEL', 'BRITANNIA', 'JUBLFOOD', 'KOTAKBANK', 'L&TFH', 'IDFCFIRSTB', 'LALPATHLAB', 'LICHSGFIN',
                'LT', 'LTIM', 'LTTS', 'M&M', 'M&MFIN', 'MANAPPURAM', 'MARICO', 'MCDOWELL-N','MCX', 'METROPOLIS', 'MFSL', 
                'MOTHERSON', 'MPHASIS', 'MRF', 'NATIONALUM', 'NAUKRI', 'NAVINFLUOR', 'NESTLEIND', 'MARUTI', 'NMDC', 
                'OBEROIRLTY', 'ONGC', 'PERSISTENT', 'PETRONET', 'PFC', 'PIDILITIND', 'PIIND', 'PNB', 'POLYCAB', 'POWERGRID',
                'PVRINOX', 'RAIN', 'RAMCOCEM', 'RBLBANK', 'RECLTD', 'RELIANCE', 'SBICARD', 'SBIN', 'SHREECEM', 'SRF', 'SUNPHARMA',
                'SUNTV', 'SYNGENE', 'TATACHEM', 'TATACOMM', 'TATACONSUM', 'TATAMOTORS', 'TATAPOWER', 'TATASTEEL', 'TCS', 'TECHM',
                'TRENT', 'UBL', 'ULTRACEMCO', 'UPL', 'VOLTAS', 'WIPRO', 'ZEEL', 'BHEL', 'IBULHSGFIN', 'IEX', 'INDUSTOWER',
                'OFSS', 'SBILIFE', 'EXIDEIND', 'TVSMOTOR', 'COALINDIA', 'DLF', 'GRASIM', 'IGL', 'JINDALSTEL', 'LAURUSLABS',
                'MGL', 'NTPC', 'SAIL', 'SHRIRAMFIN','TITAN','TORNTPHARM', 'INDIAMART', 'CANBK', 'LUPIN', 'PAGEIND',
                'ZYDUSLIFE', 'SIEMENS', 'ITC', 'HDFCAMC', 'VEDL', 'IDEA', 'MUTHOOTFIN', 'PEL']


data_dict = {symbol: capital_market.price_volume_and_deliverable_position_data(symbol=symbol, period='1D') for symbol in stock_symbols}
combined_data = pd.concat([pd.DataFrame(data) for data in data_dict.values()], keys=stock_symbols)


# APP

app = dash.Dash(__name__)
header_style = {
    'backgroundColor': 'lightgrey',  
    'fontWeight': 'bold',           
    'textAlign': 'center',          
    'border': '1px solid white'     
}


app.layout = html.Div([
    html.H1("Screener App"),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Volume BuildUp Data', value='tab-1'),
        dcc.Tab(label='Security Deliverable Data', value='tab-2'),
    ]),
    
    html.Div(id='tab-content')
])


@app.callback(
    dash.dependencies.Output('tab-content', 'children'),
    [dash.dependencies.Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H2("Volume BuildUp Data"),
            dash_table.DataTable(
                id='stock-table',
                columns=[{'name': col, 'id': col} for col in highlighted_stocks_data.columns],
                data=all_stocks_data.to_dict('records'),
                style_cell={
                    'textAlign': 'left',
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
                style_data_conditional=[
                    {
                        'if': {
                            'filter_query': '{Volume} > {3 Day Avg Volume}',
                            'column_id': '3 Day Avg Volume'
                        },
                        'backgroundColor': 'blue',
                        'color': 'white'  
                    },
                    {
                        'if': {
                            'filter_query': '{Volume} > {Weekly Avg Volume}',
                            'column_id': 'Weekly Avg Volume'
                        },
                        'backgroundColor': 'blue',
                        'color': 'white'  
                    },
                    {
                        'if': {
                            'filter_query': '{Volume} > {Monthly Avg Volume}',
                            'column_id': 'Monthly Avg Volume'
                        },
                        'backgroundColor': 'blue',
                        'color': 'white' 
                    },
                    {
                        'if': {
                            'filter_query': '{Volume} > {Yearly Avg Volume}',
                            'column_id': 'Yearly Avg Volume'
                        },
                        'backgroundColor': 'blue',
                        'color': 'white'  
                    },
                ],
                style_header=header_style,  
            )
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H2("Security Deliverable Data"),
            dash_table.DataTable(
                id='table',
                columns=[{'name': col, 'id': col} for col in combined_data.columns],
                data=combined_data.to_dict('records'),
                filter_action='native',  
                sort_action='native',   
                sort_mode='single',      
                style_table={'overflowX': 'auto'},  
                style_header=header_style,  
            )
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
