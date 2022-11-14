import telebot
import time
import requests

def get_currency_data():
    platforms = ["binance", "coinbase-exchange"]

    url = "https://api.coinmarketcap.com/data-api/v3/exchange/market-pairs/latest?slug="
    param = "&category=spot&start="
    num = "&limit=500"
    data1 = requests.get(url=url+platforms[0]+param+"1"+num).json()
    data2 = requests.get(url=url+platforms[1]+param+"1"+num).json()

    prices1 = []
    symbols1 = set()
    prices2 = []
    symbols2 = set()

    for coin in data1['data']['marketPairs']:
        symbols1.add(coin['quoteSymbol'])
        coin_data = {"quoteSymbol": coin['quoteSymbol'] ,
                     "marketid": coin['marketId'],
                     "marketUrl": coin['marketUrl'],
                     "currency": coin['baseCurrencyName'],
                     "price": coin['price']}
        prices1.append(coin_data)

    for coin in data2['data']['marketPairs']:
        symbols2.add(coin['quoteSymbol'])
        coin_data = {"quoteSymbol": coin['quoteSymbol'] ,
                     "marketid": coin['marketId'],
                     "marketUrl": coin['marketUrl'],
                     "currency": coin['baseCurrencyName'],
                     "price": coin['price']}
        prices2.append(coin_data)

    symbols1 = list(symbols1)
    symbols2 = list(symbols2)

    res1 = {}
    res2 = {}

    for symbol in symbols1:
        to_classify = []
        for price in prices1:
            if symbol == price['quoteSymbol']:
                to_classify.append(price)
        res1[symbol] = to_classify

    for symbol in symbols2:
        to_classify = []
        for price in prices2:
            if symbol == price['quoteSymbol']:
                to_classify.append(price)
        res2[symbol] = to_classify

    return res1,res2

bot = telebot.TeleBot('5746629756:AAF6uBBEu3EtTIXI6Yq0ZHTD_DAgOYDrSRk')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'check_response':
        bot.send_message(message.from_user.id, "Working")
    elif message:
        while True:
            res1, res2 = get_currency_data()
            for key in list(res1.keys()):
                for coin_data1 in res1[key]:
                    try:
                        for coin_data2 in res2[key]:
                            if (coin_data1['currency'] == coin_data2['currency'] and coin_data1['price'] > 1.1 * coin_data2['price']) \
                                    or (coin_data1['currency'] == coin_data2['currency'] and coin_data2['price'] > 1.1 * coin_data1['price']):
                                symbol1 = "quoteSymbol: " + coin_data1['quoteSymbol']
                                symbol2 = "quoteSymbol: " + coin_data2['quoteSymbol']
                                currency1 = "Currency: " + coin_data1['currency']
                                currency2 = "Currency: " + coin_data2['currency']
                                price1 = "Price: " + str(coin_data1['price'])
                                price2 = "Price: " + str(coin_data2['price'])
                                url1 = "Url: " + coin_data1['marketUrl']
                                url2 = "Url: " + coin_data2['marketUrl']
                                bot.send_message(message.from_user.id, symbol1 + "\n" + currency1 + "\n" + price1 + "\n" + url1)
                                bot.send_message(message.from_user.id, symbol2 + "\n" + currency2 + "\n" + price2 + "\n" + url2)
                    except:
                        pass
            time.sleep(60)



bot.polling(none_stop=True, interval=0)
