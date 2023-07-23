# Import necessary libraries
import yfinance as yf
import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

# Function to get stock data and calculate moving averages
# (Your existing code for these functions)

# List of stock tickers (Feel free to add more or remove as needed)
stock_tickers = ['ABCAPITAL.NS', 'ABB.NS', 'AARTIIND.NS', 'ASIANPAINT.NS', 'APOLLOTYRE.NS', 'ABFRL.NS', 'AUROPHARMA.NS', 'BANDHANBNK.NS', 'ABBOTINDIA.NS', 'AXISBANK.NS']

# Create the Dash application
app = dash.Dash(__name__)
server = app.server

# Create the layout for the different pages using dcc.Tabs
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='moving-averages', children=[
        dcc.Tab(label='Moving Averages', value='moving-averages'),
        dcc.Tab(label='Stock Data', value='stock-data'),
    ]),
    html.Div(id='page-content')
])

# Callback to render the content for the selected tab
@app.callback(Output('page-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    # (Your existing code for rendering content based on selected tab)

if __name__ == '__main__':
    app.run_server(debug=True)

