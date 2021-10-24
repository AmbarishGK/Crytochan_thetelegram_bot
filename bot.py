import re
import telebot
from pycoingecko import CoinGeckoAPI
API_KEY = ""
bot = telebot.TeleBot(API_KEY)
cg = CoinGeckoAPI()
all_coin_list = cg.get_coins_list()
all_symbol_id_hash = {}
all_symbol_list = []
coin_price_hash = {}

for i in all_coin_list:
    all_symbol_list.append(i['symbol'].lower())
    all_symbol_id_hash[i['symbol']] = i['id']


def find_price(message):
    # token_name = ['jandk','augd','BTC','huwa','doge'] 
    # print(token_name)
    token_name = re.sub('\W+',' ', message.text).split()
    token_name = list(map(lambda x: x.lower(), token_name))
    symbols = set(all_symbol_list).intersection(token_name)

    for i in symbols:
        coin_id = all_symbol_id_hash[i]
        coin_price_hash[coin_id] = cg.get_coin_by_id(coin_id)['market_data']['current_price']['inr']
        print(coin_price_hash[coin_id])
        if not coin_price_hash:
            bot.send_message(message.chat.id, "No Data ?!?!")
            return False
        else:
            return True


@bot.message_handler(func=find_price)
def get_price(message):
    for i in coin_price_hash:
        x = str(i + ": " + coin_price_hash[i])
        bot.send_message(message.chat.id, x)

