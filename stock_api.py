import pandas as pd
import datetime
from pandas_datareader import data as pdr
import boto3
from io import StringIO  # Use StringIO for text (CSV) data

# Assuming yfinance and pandas_datareader are already set up as shown previously

def upload_to_s3(df, bucket_name, path):
    """
    Uploads a DataFrame to S3 in CSV format, replacing the file if it exists.
    """
    # Create a string buffer for the dataframe in CSV format
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    csv_buffer.seek(0)
    
    # Initialize S3 client
    s3_client = boto3.client('s3')
    
    # Upload the DataFrame as CSV
    s3_client.put_object(Bucket=bucket_name, Key=path, Body=csv_buffer.getvalue(), ContentType='text/csv')

def get_stock_data(ticker, duration):
    end_date = datetime.datetime.now()
    if duration == '1 week':
        start_date = end_date - datetime.timedelta(weeks=1)
    elif duration == '1 month':
        start_date = end_date - datetime.timedelta(days=30)
    elif duration == '6 months':
        start_date = end_date - datetime.timedelta(days=30*6)
    elif duration == '1 year':
        start_date = end_date - datetime.timedelta(days=365)
    else:
        return None

    try:
        import yfinance as yf
        yf.pdr_override()
        
        stock_data = pdr.get_data_yahoo(ticker, start=start_date, end=end_date)

        # Define S3 path, ensuring the extension is .csv
        s3_path = "RAW_DATA/" + f"{ticker}_{duration}/{ticker}_data.csv"
        
        # Upload the DataFrame to S3 in CSV format
        upload_to_s3(stock_data, "yfinstockdata", s3_path)

        return stock_data.tail().to_json()  # Keeping the return type consistent with previous example
    except Exception as e:
        print(f"Error fetching or uploading stock data: {e}")
        return None
