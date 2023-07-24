import yfinance as yf
import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

# Function to fetch stock data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="2y")
    data['3 Day Avg Volume'] = data['Volume'].rolling(window=3).mean().fillna(0).round().astype(int)
    data['Weekly Avg Volume'] = data['Volume'].rolling(window=5).mean().fillna(0).round().astype(int)
    data['Monthly Avg Volume'] = data['Volume'].rolling(window=20).mean().fillna(0).round().astype(int)
    data['Yearly Avg Volume'] = data['Volume'].rolling(window=252).mean().fillna(0).round().astype(int)
    data['Ticker'] = ticker
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

# Calculate the moving averages
all_stocks_data['10-day MA'] = all_stocks_data.groupby('Ticker')['Close'].rolling(window=10).mean().reset_index(0, drop=True).round(2)
all_stocks_data['20-day MA'] = all_stocks_data.groupby('Ticker')['Close'].rolling(window=20).mean().reset_index(0, drop=True).round(2)
all_stocks_data['50-day MA'] = all_stocks_data.groupby('Ticker')['Close'].rolling(window=50).mean().reset_index(0, drop=True).round(2)
all_stocks_data['150-day MA'] = all_stocks_data.groupby('Ticker')['Close'].rolling(window=150).mean().reset_index(0, drop=True).round(2)
all_stocks_data['200-day MA'] = all_stocks_data.groupby('Ticker')['Close'].rolling(window=200).mean().reset_index(0, drop=True).round(2)

# Calculate the distance from each average to the current price as a percentage
all_stocks_data['10-day Distance'] = ((all_stocks_data['Close'] - all_stocks_data['10-day MA']) / all_stocks_data['Close'] * 100).round(2)
all_stocks_data['20-day Distance'] = ((all_stocks_data['Close'] - all_stocks_data['20-day MA']) / all_stocks_data['Close'] * 100).round(2)
all_stocks_data['50-day Distance'] = ((all_stocks_data['Close'] - all_stocks_data['50-day MA']) / all_stocks_data['Close'] * 100).round(2)
all_stocks_data['150-day Distance'] = ((all_stocks_data['Close'] - all_stocks_data['150-day MA']) / all_stocks_data['Close'] * 100).round(2)
all_stocks_data['200-day Distance'] = ((all_stocks_data['Close'] - all_stocks_data['200-day MA']) / all_stocks_data['Close'] * 100).round(2)

# Calculate the total stocks above and below each moving average
above_below_df = pd.DataFrame(index=['Above', 'Below'])
above_below_df['10-day MA'] = [len(all_stocks_data[all_stocks_data['10-day Distance'] < 0]), len(all_stocks_data[all_stocks_data['10-day Distance'] >= 0])]
above_below_df['20-day MA'] = [len(all_stocks_data[all_stocks_data['20-day Distance'] < 0]), len(all_stocks_data[all_stocks_data['20-day Distance'] >= 0])]
above_below_df['50-day MA'] = [len(all_stocks_data[all_stocks_data['50-day Distance'] < 0]), len(all_stocks_data[all_stocks_data['50-day Distance'] >= 0])]
above_below_df['150-day MA'] = [len(all_stocks_data[all_stocks_data['150-day Distance'] < 0]), len(all_stocks_data[all_stocks_data['150-day Distance'] >= 0])]
above_below_df['200-day MA'] = [len(all_stocks_data[all_stocks_data['200-day Distance'] < 0]), len(all_stocks_data[all_stocks_data['200-day Distance'] >= 0])]

# Create Dash application
app = dash.Dash(__name__)
server = app.server

# Layout of the dashboard
app.layout = html.Div(children=[
    html.H1('Moving Average Scanner and Volume Analysis'),
    html.H2('Price Distance From Moving Averages'),
    dash_table.DataTable(
        id='moving-averages-table',
        columns=[{"name": col, "id": col} for col in all_stocks_data.columns],
        data=all_stocks_data.to_dict('records'),
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
