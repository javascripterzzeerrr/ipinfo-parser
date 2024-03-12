from dotenv import load_dotenv
import os
import ipinfo
import time

# Load environment variables from the .env file
load_dotenv()

# Access environment variables
api_key = os.getenv("API_KEY")
print(api_key)

handler = ipinfo.getHandler(api_key)

with open('torbulkexitlist') as f:
    for ip_addr in f:
        print("For ip_addr => ", ip_addr)
        details = handler.getDetails(ip_addr)
        print(details.city)
        time.sleep(10)

    # >> > import ipinfo
    # >> > access_token = '123456789abc'
    # >> > handler = ipinfo.getHandler(access_token)
    # >> > ip_address = '216.239.36.21'
    # >> > details = handler.getDetails(ip_address)
    # >> > details.city
    # 'Mountain View'
    # >> > details.loc
    # '37.3861,-122.0840'
