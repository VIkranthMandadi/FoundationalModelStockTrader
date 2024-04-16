import yfinance as yf
import pandas as pd

def get_sp500_tickers():
    # Download the list of S&P 500 components from Wikipedia
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_df = pd.read_html(url)[0]  # Read the first table from the webpage
    
    # Extract the tickers from the dataframe
    sp500_tickers = sp500_df['Symbol'].tolist()
    
    return sp500_tickers

def fetch_sp500_data(start_date, end_date):
    sp500_tickers = get_sp500_tickers()
    sp500_data = yf.download(sp500_tickers, start=start_date, end=end_date)
    return sp500_data['Adj Close']

def save_to_csv(data, output_file):
    data.to_csv(output_file)

def main():
    # Define the date range for the data
    start_date = '2020-01-01'
    end_date = '2023-12-31'
    
    # Fetch S&P 500 data
    sp500_data = fetch_sp500_data(start_date, end_date)
    
    # Save data to CSV
    output_file = 'sp500_stock_data.csv'
    save_to_csv(sp500_data, output_file)
    
    print(f"S&P 500 stock data saved to {output_file}")

if __name__ == "__main__":
    main()

