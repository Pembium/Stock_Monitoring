import requests
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator 
from datetime import date, timedelta, datetime
import json
from stockBot import Chat_Bot
from stock_processing import process
import sys

def url_request(STOCK_LISTING, API_KEY):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK_LISTING}&outputsize=full&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()
    return data

def read_json(JSON):
    f = open(JSON)
    file = json.load(f)
    f.close
    return file

if __name__ == "__main__":
    config = read_json("config.json")
    API_KEY = config["API_KEY"]
    USER_ID = config["USER_ID"]
    TOKEN = config["TOKEN"]
    
    cb = Chat_Bot(USER_ID, TOKEN)

    listings = list(read_json("listings.json").values())

    today = date.today()

    init_message = f'Generating recommended stock options for {today}'
    cb.sendMSG(init_message)

    #flag for if there is any useful data gained
    MSGFlag = False

    for listing in listings:
        data = url_request(listing, API_KEY)
        if 'Information' in data:
            print("Run out of API calls - Do we need to reduce the amount of calls made?")
            cb.sendMSG("Run out of API calls - Do we need to reduce the amount of calls made?")
            sys.exit(0)
        #Save file 
        with open(f'/Stock_monitoring/{listing}.json', 'w') as fp:
            json.dump(data, fp)

        process(data, listing)
    
    if not MSGFlag:
        cb.sendMSG("No stocks worth purchasing")

