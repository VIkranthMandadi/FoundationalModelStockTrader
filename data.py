import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_sp500_tickers(num_stocks):
    # Download the list of S&P 500 components from Wikipedia
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_df = pd.read_html(url)[0]  # Read the first table from the webpage
    
    # Extract the tickers from the dataframe (select first 'num_stocks' tickers)
    sp500_tickers = sp500_df['Symbol'].tolist()[:num_stocks]
    
    return sp500_tickers

def fetch_stock_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)
    return data['Adj Close']

def reshape_stock_data(stock_data):
    # Reshape the dataframe to have Date, Ticker, and Adj Close as columns
    reshaped_data = stock_data.stack().reset_index()
    reshaped_data.columns = ['Date', 'Ticker', 'Adj Close']
    
    # Sort the reshaped data by Ticker
    reshaped_data_sorted = reshaped_data.sort_values(by='Ticker')
    reshaped_data_sorted = reshaped_data.sort_values(by='Date')
    
    return reshaped_data_sorted

def save_to_csv(data, output_file):
    data.to_csv(output_file, index=False)

def main():
    # Specify the number of stocks to fetch (first 3 stocks)
    num_stocks = 3
    
    # Get the tickers of the first 'num_stocks' stocks from S&P 500
    sp500_tickers = get_sp500_tickers(num_stocks)
    
    # Define the date range (five days ago to yesterday)
    end_date = datetime.now() - timedelta(days=1)  # Yesterday's date
    start_date = end_date - timedelta(days=10)       # Five days ago
    
    # Convert date objects to string format
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    # Fetch stock data for the selected tickers and date range
    stock_data = fetch_stock_data(sp500_tickers, start_date_str, end_date_str)
    
    # Reshape and sort the fetched stock data into desired format (Date, Ticker, Adj Close)
    reshaped_data = reshape_stock_data(stock_data)
    
    # Save reshaped and sorted data to CSV
    output_file = 'sp500_first_3_stocks_last_5_days_sorted.csv'
    save_to_csv(reshaped_data, output_file)
    
    print(f"Stock data for the first {num_stocks} S&P 500 stocks for the last 5 days (sorted by Ticker) saved to {output_file}")

if __name__ == "__main__":
    main()
