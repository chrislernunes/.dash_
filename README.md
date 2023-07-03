# .dash_

# Price & Volume Screener

The above project is a stock analysis dashboard built using Dash, a Python framework for creating web applications. The purpose of the application is to fetch and display stock data for a list of predefined stock symbols from Yahoo Finance. It provides an interactive dashboard where users can view various stock metrics and signals for each stock.


### The main features of the dashboard include:

- Longshort Screener 

The application fetches data such as the stock's opening price, high price, low price, closing price, change, beta, P/E ratio, 52-week high, 52-week low, volume (daily), and average volume. It also analyzes the stock's price and volume signals to determine if it is near a 52-week high or low and if there is a volume surge.

The stock data is presented in a tabular format using the Dash DataTable component. The table includes columns for each metric, including the price signal and volume signal. The color highlights in the table provide visual cues to quickly identify stocks that are near 52-week highs or lows or experiencing a volume surge.

Users can interact with the application by viewing stock data and analyzing signals for all FNO stock. The application allows for easy identification of stocks that meet criteria based on price and volume signals, which can be useful for analysis and trading decisions.

- Moving Average Screener

Moving Averages Table: This table displays the latest stock data for each symbol, including the open, high, low, close prices, volume, and various moving averages (10-day, 20-day, 50-day, 150-day, and 200-day). The moving averages help identify trends and potential support or resistance levels in the stock prices.

Distance from Moving Averages Table: This table calculates the percentage distance of each stock's closing price from the corresponding moving averages. It provides an indication of whether the stock is trading above or below the moving averages, which can be useful for identifying potential buy or sell signals.

Stocks Above and Below Moving Averages Table: This table summarizes the number of stocks that are currently trading above or below each moving average. It gives an overview of the overall market sentiment and can help identify market trends.
