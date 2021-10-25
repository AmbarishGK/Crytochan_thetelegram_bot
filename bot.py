import re
import locale
import telebot
from pycoingecko import CoinGeckoAPI
locale.setlocale(locale.LC_MONETARY, 'en_IN')
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
    token_name = re.sub('\W+',' ', message.text).split()
    token_name = list(map(lambda x: x.lower(), token_name))
    symbols = set(all_symbol_list).intersection(token_name)

    for i in symbols:
        coin_id = all_symbol_id_hash[i]
        coin_price_hash[coin_id] = locale.currency(cg.get_coin_by_id(coin_id)['market_data']['current_price']['inr'], grouping=True)
    return True


@bot.message_handler(func=find_price)
def get_price(message):
    if coin_price_hash:
        for i in coin_price_hash.copy():
            x = str(i) + ": " + str(coin_price_hash[i])
            coin_price_hash.pop(i)
            bot.send_message(message.chat.id, x)
    else:
        bot.send_message(message.chat.id, "Doesn't exist")


bot.polling()