from nselib import capital_market
import dash
from dash import dcc, html, dash_table

import pandas as pd

# Assuming you have a list of stock symbols
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

# Create the Dash app

app = dash.Dash(__name__)
server = app.server

# Function to fetch data for each symbol
def fetch_data(symbol):
    return capital_market.price_volume_and_deliverable_position_data(symbol=symbol, period='1D')

# Fetch data for each symbol and store it in a dictionary
data_dict = {symbol: fetch_data(symbol) for symbol in stock_symbols}

# Convert the data to pandas DataFrames and concatenate them
combined_data = pd.concat([pd.DataFrame(data) for data in data_dict.values()], keys=stock_symbols)

# Create a common header for the combined table
common_headers = [{'name': col, 'id': col} for col in combined_data.columns]

# Define header styles
header_style = {
    'backgroundColor': 'orange',  # Change the background color of the headers
    'fontWeight': 'bold',           # Make the headers bold
    'textAlign': 'center',          # Center-align the text in the headers
    'border': '1px solid white'     # Add a white border around the headers
}

# Define the layout of the app
app.layout = html.Div([
    html.H1("Security Deliverable Data"),
    dash_table.DataTable(
        id='table',
        columns=common_headers,
        data=combined_data.to_dict('records'),
        filter_action='native',  # Enable native filter behavior
        style_table={'overflowX': 'auto'},  # Enable horizontal scrollbar for the table
        style_header=header_style,  # Apply the header style
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
