import yfinance as yf
import pandas as pd

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

# Fetch stock data
stock_symbols = ['ABCAPITAL.NS', 'ABB.NS', 'AARTIIND.NS', 'ASIANPAINT.NS', 'APOLLOTYRE.NS', 'ABFRL.NS', 'AUROPHARMA.NS', 'BANDHANBNK.NS','ABBOTINDIA.NS', 'AXISBANK.NS', 'BATAINDIA.NS', 'BEL.NS']

stock_data_df = pd.DataFrame()

for symbol in stock_symbols:
    stock_data = yf.download(symbol, start='2022-06-01')
    stock_data["Symbol"] = symbol
    stock_data_df = pd.concat([stock_data_df, stock_data], ignore_index=True)

# Calculate the moving averages
stock_data_df['10-day MA'] = stock_data_df.groupby('Symbol')['Close'].rolling(window=10).mean().reset_index(0, drop=True).round(2)
stock_data_df['20-day MA'] = stock_data_df.groupby('Symbol')['Close'].rolling(window=20).mean().reset_index(0, drop=True).round(2)
stock_data_df['50-day MA'] = stock_data_df.groupby('Symbol')['Close'].rolling(window=50).mean().reset_index(0, drop=True).round(2)
stock_data_df['150-day MA'] = stock_data_df.groupby('Symbol')['Close'].rolling(window=150).mean().reset_index(0, drop=True).round(2)
stock_data_df['200-day MA'] = stock_data_df.groupby('Symbol')['Close'].rolling(window=200).mean().reset_index(0, drop=True).round(2)

latest_data = stock_data_df.groupby('Symbol').tail(1).round(2)
moving_avg_df = latest_data[['Symbol', 'Open', 'High', 'Low', 'Close', '10-day MA', '20-day MA', '50-day MA', '150-day MA', '200-day MA']]

# Calculate the distance from each average to the current price as a percentage
moving_avg_df['10-day Distance'] = ((moving_avg_df['Close'] - moving_avg_df['10-day MA']) / moving_avg_df['Close'] * 100).round(2)
moving_avg_df['20-day Distance'] = ((moving_avg_df['Close'] - moving_avg_df['20-day MA']) / moving_avg_df['Close'] * 100).round(2)
moving_avg_df['50-day Distance'] = ((moving_avg_df['Close'] - moving_avg_df['50-day MA']) / moving_avg_df['Close'] * 100).round(2)
moving_avg_df['150-day Distance'] = ((moving_avg_df['Close'] - moving_avg_df['150-day MA']) / moving_avg_df['Close'] * 100).round(2)
moving_avg_df['200-day Distance'] = ((moving_avg_df['Close'] - moving_avg_df['200-day MA']) / moving_avg_df['Close'] * 100).round(2)

above_below_df = pd.DataFrame(index=['Above', 'Below'])

# Calculate the total stocks above and below each moving average
above_below_df['10-day MA'] = [len(moving_avg_df[moving_avg_df['10-day Distance'] < 0]), len(moving_avg_df[moving_avg_df['10-day Distance'] >= 0])]
above_below_df['20-day MA'] = [len(moving_avg_df[moving_avg_df['20-day Distance'] < 0]), len(moving_avg_df[moving_avg_df['20-day Distance'] >= 0])]
above_below_df['50-day MA'] = [len(moving_avg_df[moving_avg_df['50-day Distance'] < 0]), len(moving_avg_df[moving_avg_df['50-day Distance'] >= 0])]
above_below_df['150-day MA'] = [len(moving_avg_df[moving_avg_df['150-day Distance'] < 0]), len(moving_avg_df[moving_avg_df['150-day Distance'] >= 0])]
above_below_df['200-day MA'] = [len(moving_avg_df[moving_avg_df['200-day Distance'] < 0]), len(moving_avg_df[moving_avg_df['200-day Distance'] >= 0])]

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
    html.H1('Stock Dashboard', style={'textAlign': 'center'}),
    
    # Moving Average Table
    html.H2('Price Distance From Moving Averages', style={'textAlign': 'center'}),
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
            {
                'if': {
                    'column_id': '10-day Distance',
                    'filter_query': '{10-day Distance} >= 0'
                },
                'backgroundColor': 'green',
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
                    'column_id': '20-day Distance',
                    'filter_query': '{20-day Distance} >= 0'
                },
                'backgroundColor': 'green',
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
                    'column_id': '50-day Distance',
                    'filter_query': '{50-day Distance} >= 0'
                },
                'backgroundColor': 'green',
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
                    'column_id': '150-day Distance',
                    'filter_query': '{150-day Distance} >= 0'
                },
                'backgroundColor': 'green',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': '200-day Distance',
                    'filter_query': '{200-day Distance} < 0'
                },
                'backgroundColor': 'red',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': '200-day Distance',
                    'filter_query': '{200-day Distance} >= 0'
                },
                'backgroundColor': 'green',
                'color': 'white',
            }
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

    # Stocks Above and Below Moving Averages Table
    html.H2('Stocks Above and Below Moving Averages', style={'textAlign': 'center'}),
    dash_table.DataTable(
        id='above-below-table',
        columns=[{"name": col, "id": col} for col in above_below_df.columns],
        data=above_below_df.to_dict('records'),
        style_cell={'textAlign': 'center'},
    ),
    
    # Stock Ticker Dropdown and Data Table
    html.H2('Select a Stock Ticker', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='stock-ticker-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in stock_tickers],
        value=stock_tickers[0]
    ),
    html.H2('Stock Data', style={'textAlign': 'center'}),
    dash_table.DataTable(
        id='stock-data-table',
        columns=[{"name": col, "id": col} for col in all_stocks_data.columns],
        data=all_stocks_data.to_dict('records'),
        style_cell={'textAlign': 'center'},
        style_data_conditional=[
            {
                'if': {'column_id': 'Change %', 'filter_query': '{Change %} > 0'},
                'backgroundColor': 'green',
                'color': 'white',
            },
            {
                'if': {'column_id': 'Change %', 'filter_query': '{Change %} < 0'},
                'backgroundColor': 'red',
                'color': 'white',
            }
        ],
        sort_action='native',
        sort_mode='single',
        sort_by=[{'column_id': 'Ticker', 'direction': 'asc'}],
        sort_as_null=True,
    ),
])

@app.callback(
    Output('stock-data-table', 'data'),
    Input('stock-ticker-dropdown', 'value')
)
def update_stock_data(selected_ticker):
    updated_data = get_stock_data(selected_ticker)
    return updated_data.to_dict('records')

server = app.server

# Replace the app object with the server object
application = server

if __name__ == '__main__':
    application.run(debug=True)
