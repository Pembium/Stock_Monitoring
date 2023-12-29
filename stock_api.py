import requests
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator 
from datetime import date, timedelta, datetime
import json
import numpy as np
from stockBot import Chat_Bot
import sys

def url_request(STOCK_LISTING):
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

    startDate = today - timedelta(weeks=4.5*6)
    date_format = '%Y-%m-%d'

    #flag for if there is any useful data gained
    MSGFlag = False

    for listing in listings:
        data = url_request(listing)
        if 'Information' in data:
            print("Run out of API calls - Do we need to reduce the amount of calls made?")
            cb.sendMSG("Run out of API calls - Do we need to reduce the amount of calls made?")
            sys.exit(0)

        data['Time Series (Daily)'] = {datetime.strptime(x, date_format).date():y for x,y in data['Time Series (Daily)'].items()}
        shareTimeStamps = list(data['Time Series (Daily)'].keys())

        sharePrices = [float(data['Time Series (Daily)'][t]['4. close']) for t in shareTimeStamps]

        sixMonthDates = list(filter(lambda n: n > startDate, shareTimeStamps))
        sixMonthPrices = sharePrices[len(sixMonthDates) - 1::-1][::-1]

        plt.figure(figsize=(15, 6))
        plt.ylabel(f'Price (USD)')
        plt.title(f'Stock: {listing}')
        plt.plot(sixMonthDates, sixMonthPrices)

        #decimate x axis for the plot
        ax = plt.gca()
        n = len(sixMonthDates) // 5
        ax.xaxis.set_major_locator(MultipleLocator(n))
        plt.savefig(f'stock_plots/6_month_data_{listing}.png')

        temp_data = sixMonthPrices[::-1]
        start_price = temp_data[0]
        end_price = temp_data[-1]

        percentage_change = ((start_price - end_price)/start_price) * 100


        fifty_day_average = np.average(temp_data[-55:-45])
        one_eighty_day_average = np.average(temp_data[-185:-175])

        if fifty_day_average < one_eighty_day_average and end_price < one_eighty_day_average:
            delta_list = [temp_data[n] - temp_data[n-1] for n in range(1, len(temp_data))]
            
            gain = np.average(list(filter(lambda d: d > 0, delta_list[-14:])))
            loss = -1 * np.average(list(filter(lambda d: d < 0, delta_list[-14:])))
            rs = gain/loss
            rsi = 100 - (100 / (1 + rs))

            message = f'Stock: {listing}, RS: {round(rs, -3)}, RSI: {round(rsi, -3)}'
            cb.sendMSG(message)

            photo = f'stock_plots/6_month_data_{listing}.png'
            cb.sendPhoto(photo)

            MSGFlag = True
    
    if not MSGFlag:
        cb.sendMSG("No stocks worth purchasing")

