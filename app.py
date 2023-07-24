import dash
from dash import dcc, html
import pandas as pd
import yfinance as yf

# Function to fetch stock data
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

# Define the stock tickers
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
        crossing_styles[7] = 'color: green;'
    if s['Volume'] > s['Weekly Avg Volume']:
        crossing_styles[8] = 'color: orange;'
    if s['Volume'] > s['Monthly Avg Volume']:
        crossing_styles[9] = 'color: blue;'
    if s['Volume'] > s['Yearly Avg Volume']:
        crossing_styles[10] = 'color: red;'
    return crossing_styles

# Apply the highlight function to the DataFrame
highlighted_stocks_data = all_stocks_data.style.apply(highlight_crossing, axis=1)

# Extract data from the Styler object and convert to DataFrame
highlighted_stocks_data_df = highlighted_stocks_data.data

# Create Dash application
app = dash.Dash(__name__)
server = app.server

# Dash layout
app.layout = html.Div([
    html.H1("Stock Data Dashboard"),
    dcc.Graph(
        id='stock-table',
        figure={
            'data': [{
                'type': 'table',
                'header': {
                    'values': highlighted_stocks_data_df.columns,
                    'align': 'center',
                    'fill': {'color': 'grey'},
                    'line': {'color': 'white'}
                },
                'cells': {
                    'values': highlighted_stocks_data_df.values.tolist(),
                    'align': 'center',
                    'fill': {'color': 'white'},
                    'line': {'color': 'white'}
                }
            }],
            'layout': {
                'margin': {'l': 10, 'r': 10, 't': 50, 'b': 50}
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

