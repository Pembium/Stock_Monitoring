# Stock Monitoring

## Description:
* This script uses alpha vantage API to retireve data on 25 US stocks. 
* This data is then processed looking for recent dips in stock which may be under valued at the moment. 
* The results are then sent a telegram bot.

## Utilisation
* To use this script, the config file must be populated with the appropriate keys, tokens and user IDS. Relevent links to sources/tutorials:
  - API_KEY: https://www.alphavantage.co/support/#api-key
  - USER_ID: https://www.alphr.com/telegram-find-user-id/
  - Token: https://core.telegram.org/bots
    - This requires setting up a bot. Please refer to the above link for how to do this
* Running stock_api.py as main pings the alhpa vantage API and sends the results to a personal telegram bot
* Running stockBot.py as main sends test messages to a personal telegram bot
* Personally I run it via a cron job once per day due to the limit in API pings (25 as of writing this)
