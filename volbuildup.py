import dash
from dash import html, dash_table
import yfinance as yf
import pandas as pd




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

    # Round all numbers to 2 decimals
    data = data.round(2)

    return data[['Ticker', 'Open', 'High', 'Low', 'Close', 'Change %', 'Volume', '3 Day Avg Volume', 'Weekly Avg Volume', 'Monthly Avg Volume', 'Yearly Avg Volume']]

# List of stock tickers (Feel free to add more or remove as needed)
stock_tickers = ['ABCAPITAL.NS', 'ABB.NS', 'AARTIIND.NS', 'ASIANPAINT.NS', 'APOLLOTYRE.NS', 'ABFRL.NS', 'AUROPHARMA.NS', 'BANDHANBNK.NS', 'ABBOTINDIA.NS', 'AXISBANK.NS']

# Create an empty DataFrame to store the data for all stocks
all_stocks_data = pd.DataFrame()

# Fetch data for each stock and append it to the DataFrame
for ticker in stock_tickers:
    stock_data = get_stock_data(ticker)
    all_stocks_data = all_stocks_data._append(stock_data.iloc[-1], ignore_index=True)

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

# Create a Dash app
app = dash.Dash(__name__)
server = app.server

# Define the layout of the app
app.layout = html.Div([
    html.H1("Volume Buildup Screener"),  # Add the title
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
                'color': 'green'
            },
            {
                'if': {
                    'filter_query': '{Volume} > {Weekly Avg Volume}',
                    'column_id': 'Weekly Avg Volume'
                },
                'color': 'orange'
            },
            {
                'if': {
                    'filter_query': '{Volume} > {Monthly Avg Volume}',
                    'column_id': 'Monthly Avg Volume'
                },
                'color': 'blue'
            },
            {
                'if': {
                    'filter_query': '{Volume} > {Yearly Avg Volume}',
                    'column_id': 'Yearly Avg Volume'
                },
                'color': 'red'
            },
        ],
        style_header={
            'fontWeight': 'bold'
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

