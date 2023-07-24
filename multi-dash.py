import yfinance as yf
import pandas as pd

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

# Set the option to display all rows
pd.set_option('display.max_rows', None)

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="2y")
    data['3 Day Avg Volume'] = data['Volume'].rolling(window=3).mean().fillna(0).round().astype(int)
    data['Weekly Avg Volume'] = data['Volume'].rolling(window=5).mean().fillna(0).round().astype(int)
    data['Monthly Avg Volume'] = data['Volume'].rolling(window=20).mean().fillna(0).round().astype(int)
    data['Yearly Avg Volume'] = data['Volume'].rolling(window=252).mean().fillna(0).round().astype(int)
    data['Ticker'] = ticker

    # Calculate the change percentage and add it as a new column, rounded to 2 decimal points
    data['Change %'] = (data['Close'].pct_change() * 100).fillna(0).round(2)

    return data[['Ticker', 'Open', 'High', 'Low', 'Close', 'Change %', 'Volume', '3 Day Avg Volume', 'Weekly Avg Volume', 'Monthly Avg Volume', 'Yearly Avg Volume']]

# List of stock tickers (Feel free to add more or remove as needed)
stock_tickers = ['ABCAPITAL.NS', 'ABB.NS', 'AARTIIND.NS', 'ASIANPAINT.NS', 'APOLLOTYRE.NS', 'ABFRL.NS', 'AUROPHARMA.NS', 'BANDHANBNK.NS', 'ABBOTINDIA.NS', 'AXISBANK.NS']

# Create an empty DataFrame to store the data for all stocks
all_stocks_data = pd.DataFrame()

# Fetch data for each stock and append it to the DataFrame
for ticker in stock_tickers:
    stock_data = get_stock_data(ticker)
    all_stocks_data = all_stocks_data.append(stock_data.iloc[-1])

# Reset the index of the DataFrame
all_stocks_data.reset_index(inplace=True, drop=True)

# Function to highlight crossing volume values in green font
def highlight_crossing(s):
    crossing_styles = [''] * len(s)
    if s['Volume'] > s['3 Day Avg Volume']:
        crossing_styles[6] = 'color: green;'
    if s['Volume'] > s['Weekly Avg Volume']:
        crossing_styles[7] = 'color: orange;'
    if s['Volume'] > s['Monthly Avg Volume']:
        crossing_styles[8] = 'color: blue;'
    if s['Volume'] > s['Yearly Avg Volume']:
        crossing_styles[9] = 'color: red;'
    return crossing_styles

# Apply the highlight function to the DataFrame
highlighted_stocks_data = all_stocks_data.style.apply(highlight_crossing, axis=1)

# Create Dash application
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.H1('Stock Dashboard'),
    
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
                'backgroundColor': 'red',
                'color': 'white',
            },
            # ... repeat the styling for other columns as needed
        ],
        sort_action='native',
        sort_mode='single',
        sort_by=[
            {
                'column_id': '10-day Distance',
                'direction': 'asc',
            }
        ],
        sort_as_null=True,
    ),

    html.H2('Stocks Above and Below Moving Averages'),
    dash_table.DataTable(
        id='above-below-table',
        columns=[{"name": col, "id": col} for col in above_below_df.columns],
        data=above_below_df.to_dict('records'),
        style_cell={'textAlign': 'center'},
    ),
    
    html.H2('Stock Data'),
    dash_table.DataTable(
        id='stock-data-table',
        columns=[{"name": col, "id": col} for col in highlighted_stocks_data.columns],
        data=highlighted_stocks_data.to_dict('records'),
        style_cell={'textAlign': 'center'},
        style_data_conditional=highlighted_stocks_data.data,
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
