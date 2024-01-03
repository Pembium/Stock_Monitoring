import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator 
from datetime import date, timedelta, datetime
import json
import numpy as np
from stockBot import Chat_Bot

def process(data, listing, purchase_list):
    today = date.today()
    startDate = today - timedelta(weeks=5*6)
    date_format = '%Y-%m-%d'

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
    plt.close()

    temp_data = sixMonthPrices[::-1]
    start_price = temp_data[0]
    end_price = temp_data[-1]

    percentage_change = ((start_price - end_price)/start_price) * 100


    fifty_day_average = np.average(temp_data[-48:-38])
    one_eighty_day_average = np.average(temp_data[-132:-122])

    if fifty_day_average < one_eighty_day_average and end_price < one_eighty_day_average:
        delta_list = [temp_data[n] - temp_data[n-1] for n in range(1, len(temp_data))]
        
        gain = np.average(list(filter(lambda d: d > 0, delta_list[-14:])))
        loss = -1 * np.average(list(filter(lambda d: d < 0, delta_list[-14:])))
        rs = gain/loss
        rsi = 100 - (100 / (1 + rs))

        message = f'Stock: {listing}, RS: {round(rs, -3)}, RSI: {round(rsi, -3)}'
        cb.sendMSG(message)

        photo = f'stock_plots/6_month_data_{listing}.png'
        
        stock_info = {"Stock": listing, "RS": rs, "RSI": rsi}
        purchase_list.append(stock_info)