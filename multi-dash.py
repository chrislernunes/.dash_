import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import yfinance as yf

# Initialize Dash app
app = dash.Dash(__name__)

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

# Dash layout
app.layout = html.Div([
    html.H1("Stock Data Dashboard"),
    dcc.Graph(
        id='stock-table',
        figure={
            'data': [{
                'type': 'table',
                'header': {
                    'values': highlighted_stocks_data.columns,
                    'align': 'center',
                    'fill': {'color': 'grey'},
                    'line': {'color': 'white'}
                },
                'cells': {
                    'values': highlighted_stocks_data.values.tolist(),
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
