# arbitrage_bot

It is arbitrage bot written in python, it parses data from coinbase exchange and binance and compare them, When one of them is greater for more than 10 percent it sennds to user notification


How to use
# build an image
docker build -t arbitrage_bot .
# running an image
docker run -p 100:100 -d arbitrage_bot
