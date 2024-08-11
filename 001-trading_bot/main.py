import time
from polygon import RESTClient
import config

# Initialize the Polygon client
client = RESTClient(config.API_KEY)

def fetch_options_data(symbol):
    max_requests_per_minute = 5
    interval = 60 / max_requests_per_minute  # Interval in seconds between requests
    retries = 3
    delay = 1  # Start with 1 second delay

    request_count = 0
    start_time = time.time()
    
    while retries > 0:
        try:
            # Check if the time interval has passed
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time < interval * request_count:
                time.sleep(interval * request_count - elapsed_time)  # Sleep until next allowed request time
            
            response = client.list_options_contracts()  # Adjust method as needed

            if response and 'results' in response:
                for option in response['results']:
                    if option['symbol'] == symbol:
                        volume = option['volume']
                        
                        if volume > 500:
                            message = (f"اسم السهم: {option['symbol']}\n"
                                       f"تاريخ انتهاء العقد: {option['expiration_date']}\n"
                                       f"الاسترايك: {option['strike_price']}\n"
                                       f"نوع الصفقة: {option['type']}\n"
                                       f"سعر الصفقة: {option['price']}\n"
                                       f"حجم الصفقة: {option['volume']}\n\n"
                                       f"سعر ASK: {option['ask']}\n"
                                       f"سعر BID: {option['bid']}\n\n"
                                       f"حجم التداول: {option['total_volume']}\n"
                                       f"عدد صفقات اليوم: {option['trades_today']}\n"
                                       f"سعر الافتتاح: {option['opening_price']}\n"
                                       f"أعلى سعر: {option['highest_price']}\n"
                                       f"أدنى سعر: {option['lowest_price']}\n"
                                       f"سعر الإغلاق: {option['closing_price']}\n"
                                    )
                            print(message)
                break  # Exit loop on success
            
            else:
                print("No options data found or incorrect response structure.")
                break  # Exit loop if no data or wrong structure

            request_count += 1
        
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
            retries -= 1

    if retries == 0:
        print("Failed to fetch data after multiple retries.")

# Example usage
symbol = 'AAPL'
fetch_options_data(symbol)
