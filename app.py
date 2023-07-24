import dash
from dash import html, dcc
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

    return data[['Ticker', 'Open', 'High', 'Low', 'Close', 'Change %', 'Volume', '3 Day Avg Volume', 'Weekly Avg Volume', 'Monthly Avg Volume', 'Yearly Avg Volume']]

# List of stock tickers (Feel free to add more or remove as needed)
stock_tickers = ['ABCAPITAL.NS', 'ABB.NS', 'AARTIIND.NS', 'ASIANPAINT.NS', 'APOLLOTYRE.NS', 'ABFRL.NS', 'AUROPHARMA.NS', 'BANDHANBNK.NS', 'ABBOTINDIA.NS', 'AXISBANK.NS']

# Create an empty DataFrame to store the data for all stocks
all_stocks_data = pd.DataFrame()

# Fetch data for each stock and append it to the DataFrame
for ticker in stock_tickers:
    stock_data = get_stock_data(ticker)
    all_stocks_data = all_stocks_data.append(stock_data.iloc[-1], ignore_index=True)

# Function to highlight crossing volume values in green font
def highlight_crossing(row):
    crossing_styles = [''] * len(row)
    if row['Volume'] > row['3 Day Avg Volume']:
        crossing_styles[6] = 'color: green;'
    if row['Volume'] > row['Weekly Avg Volume']:
        crossing_styles[7] = 'color: green;'
    if row['Volume'] > row['Monthly Avg Volume']:
        crossing_styles[8] = 'color: green;'
    if row['Volume'] > row['Yearly Avg Volume']:
        crossing_styles[9] = 'color: green;'
    return crossing_styles

# Apply the highlight function to the DataFrame
highlighted_stocks_data = all_stocks_data.apply(highlight_crossing, axis=1)

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Stock Data Table"),  # Add the title
    dash_table.DataTable(
        id='stock-table',
        columns=[
            {'name': col, 'id': col}
            if col not in ('Ticker', 'Open', 'High', 'Low', 'Close')
            else {'name': col, 'id': col, 'type': 'numeric', 'format': {'specifier': '.2f'}}
            for col in all_stocks_data.columns
        ],
        data=all_stocks_data.to_dict('records'),
        style_cell={
            'textAlign': 'left',
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_data_conditional=[
            {'if': {'filter_query': '{Volume} > {`3 Day Avg Volume`}'}, 'color': 'green', 'fontWeight': 'bold'},
            {'if': {'filter_query': '{Volume} > {`Weekly Avg Volume`}'}, 'color': 'orange', 'fontWeight': 'bold'},
            {'if': {'filter_query': '{Volume} > {`Monthly Avg Volume`}'}, 'color': 'blue', 'fontWeight': 'bold'},
            {'if': {'filter_query': '{Volume} > {`Yearly Avg Volume`}'}, 'color': 'red', 'fontWeight': 'bold'},
        ],
        style_header={
            'fontWeight': 'bold'
        },
        filter_action='native',  # Enable native filtering
        sort_action='native',    # Enable native sorting
        sort_mode='multi'        # Allow multiple column sorting
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
