from nselib import capital_market
import dash
from dash import dcc, html, dash_table

import pandas as pd

# Assuming you have a list of stock symbols
stock_symbols = ['SBIN', 'ACC', 'INFY', 'TCS']

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

# Define the layout of the app
app.layout = html.Div([
    html.H1("Stock Data Dashboard"),
    dash_table.DataTable(
        id='table',
        columns=common_headers,
        data=combined_data.to_dict('records'),
        filter_action='native',  # Enable native filter behavior
        style_table={'overflowX': 'auto'},  # Enable horizontal scrollbar for the table
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
