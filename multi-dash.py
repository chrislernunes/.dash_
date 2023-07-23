# Import necessary libraries
import yfinance as yf
import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

# Function to get stock data and calculate moving averages
def get_stock_data(ticker):
    # Your existing code for calculating moving averages here...
    pass

# Function to highlight crossing volume values in green font
def highlight_crossing(s):
    # Your existing code for highlighting crossing volume values here...
    pass

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
    if tab == 'moving-averages':
        # Your existing code for moving averages table here...
        pass
    elif tab == 'stock-data':
        # Create an empty DataFrame to store the data for all stocks
        all_stocks_data = pd.DataFrame()

        # Fetch data for each stock and append it to the DataFrame
        for ticker in stock_tickers:
            stock_data = get_stock_data(ticker)
            all_stocks_data = all_stocks_data.append(stock_data.iloc[-1])

        # Reset the index of the DataFrame
        all_stocks_data.reset_index(inplace=True, drop=True)

        # Apply the highlight function to the DataFrame
        highlighted_stocks_data = all_stocks_data.style.apply(highlight_crossing, axis=1)

        # Display the table with highlighted crossing volume values
        return html.Div([
            html.H1('Stock Data'),
            dash_table.DataTable(
                id='stock-data-table',
                columns=[{"name": col, "id": col} for col in all_stocks_data.columns],
                data=all_stocks_data.to_dict('records'),
                style_cell={'textAlign': 'center'},
                style_data_conditional=[
                    # Apply any additional conditional styles as needed...
                ],
            ),
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
