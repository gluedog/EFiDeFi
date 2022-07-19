# Telegram Price Bot for EOS Tokens
# By Gluedog

import http.client
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

import random
import urllib.request, json
from urllib.request import Request, urlopen  # Python 3


def hello(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="hello")

def start_callback(update, context): # Test function
  user_says = " ".join(context.args)
  update.message.reply_text("You said: " + user_says + " Beans")

def getDefi(update, context):
    defi_coinlist = ['YFC', 'CHEX', 'BOX', 'DFS', 'DAD', 'DAPP', 'EOS', 'ZEOS', 'VIG', 'DMD', 'DEX', 'DOP', 'HUB', 'PIZZA', 'XSOV', 'BOID',]

    eosprice_dict  = {'CHEX':0,'BOX':0, 'DFS':0, 'DAD':0, 'DAPP':0, 'EOS':0, 'ZEOS':0, 'VIG':0, 'DMD':0, 'DEX':0, 'DOP':0, 'HUB':0, 'PIZZA':0, 'XSOV':0, 'BOID': 0,}
    usdtprice_dict = {'CHEX':0,'BOX':0, 'DFS':0, 'DAD':0, 'DAPP':0, 'EOS':0, 'ZEOS':0, 'VIG':0, 'DMD':0, 'DEX':0, 'DOP':0, 'HUB':0, 'PIZZA':0, 'XSOV':0, 'BOID': 0,}
    change24hr_dict = {'CHEX':0,'BOX':0, 'DFS':0, 'DAD':0, 'DAPP':0, 'EOS':0, 'ZEOS':0, 'VIG':0, 'DMD':0, 'DEX':0, 'DOP':0, 'HUB':0, 'PIZZA':0, 'XSOV':0, 'BOID': 0,}

    # Get the json dictionary from the bloks API
    req = Request("http://www.api.bloks.io/tokens")
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3')
    url = urlopen(req)

    data = json.loads(url.read().decode())
    print("We got the data in getDefi().")

    marketcaps = []
    skip = False # Simple workaround to not display the old EFi V1 coins.

    for coin in defi_coinlist:
    # Let's get the eos price and usdt price and 24 hour change.
    # Then we can sort the change24hr_dict dictionary from highest to lowest and we just print it in that order.
        for token in data:
            if token['account'].upper() == "DOLPHINTOKEN" or token['account'].upper() == "EOSDMDTOKENS" or token['account'].upper() == "EOSHUBTOKENS":
                skip = True; print("skip",skip)
            else:
                skip = False; print("skip",skip)

            if token['symbol'].upper() == "EOS":
                eos_marketcap = token['price']['marketcap_usd']
            if (token['symbol'].upper() == coin) and skip != True:
                eosprice_dict[coin] = token['price']['quotes']['EOS']
                usdtprice_dict[coin] = token['price']['quotes']['USDT']
                change24hr_dict[coin] = token['price']['change_24hr']
                marketcaps.append(token['price']['marketcap_usd'])
                break

    print(eosprice_dict)
    print(usdtprice_dict)
    print(change24hr_dict)
    print('Printing Sorted Dictionary')
    reverse_ordered_dict = dict(sorted(change24hr_dict.items(), key=lambda item: item[1]))
    correct_ordered_values_list = (list(reversed(sorted(reverse_ordered_dict.values()))))

    # Just did a hack here where I loaded the dictionary with all the USD prices, and then sorted them according to those values, then printing them out.

    ordered_symbols = []


    for value in correct_ordered_values_list:
        ordered_symbols.append((list(change24hr_dict.keys())[list(change24hr_dict.values()).index(value)]))

    # Giving a plus sign to the positive numbers in the 24hr % changed dict:

    for key in change24hr_dict:
        if float(change24hr_dict[key]) > 0:
            change24hr_dict[key] = "+"+str(round(float(change24hr_dict[key]),2))
        else:
            change24hr_dict[key] = str(round(float(change24hr_dict[key]),2))

    return_value = ""

    #print("Printing Marketcaps")
    #print(marketcaps)

    #print("Eos Marketcap",eos_marketcap)

    total_marketcap = 0
    for value in marketcaps:
        total_marketcap += value

    total_marketcap -= eos_marketcap

    #print("Total Marketcap",total_marketcap)

    for key in ordered_symbols:
        print(key+(key+(" "*(5-len(key)))+" | "+str(round(float(eosprice_dict[key]),4))+(" "*(8-len(str(round(float(eosprice_dict[key]),4)))))+\
        "EOS | "+str(change24hr_dict[key])+"%"+"\n"))

        return_value += key+(" "*(5-len(key)))+" | "+str(round(float(eosprice_dict[key]),4))+(" "*(8-len(str(round(float(eosprice_dict[key]),4)))))+\
        "EOS | "+str(change24hr_dict[key])+"%"+"\n"
    return_value += "\nTotal Marketcap: "+str("${:,.0f}".format(float(total_marketcap)))

        # Need to add a line with the Total_marketcap here

    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="`"+return_value+"`", parse_mode=telegram.ParseMode.MARKDOWN)


def getPrice(update, context): # We need some user agents for the Bloks API.
    req = Request("http://www.api.bloks.io/tokens")
    user_agent1 = "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0"
    user_agent0 = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"
    req.add_header('User-Agent', user_agent1)
    url = urlopen(req)

    data = json.loads(url.read().decode())

    requested_symbol = " ".join(context.args)
    print("We got the data in getPrice(). Info requested on "+requested_symbol.upper())

    price = "None"
    priceusd = "None"
    change24hr = "None"
    skip = False

    for token in data:
        if token['account'].upper() == "DOLPHINTOKEN" or token['account'].upper() == "EOSDMDTOKENS" or token['account'].upper() == "EOSHUBTOKENS":
            skip = True; print("skip",skip) # Skip the old versions of the token with the same ticker symbols
        else:
            skip = False; print("skip",skip)

        if (token['symbol'] == requested_symbol.upper()) and skip != True:
            try:
                price = token['price']['quotes']['EOS']
                priceusd = token['price']['quotes']['USDT']
                change24hr_tmp0 = token['price']['change_24hr']
                change24hr_tmp1 = str(round(float(change24hr_tmp0),2))
                if change24hr_tmp1.startswith("-"):
                    change24hr = change24hr_tmp1
                    up_or_down = "🔻"
                else:
                    change24hr = "+"+change24hr_tmp1
                    up_or_down = "✅"

                vol_24hr = token['price']['volume_usd_24h']
                marketcap = token['price']['marketcap_usd']
                rank = token['rank']
                circulating = token['supply']['circulating']

                print(price)
                break
            except Exception:
                price = 'No such token detected.'
                print(price)

    try:
        priceinfo = "*"+requested_symbol.upper()+" price*:\n"+ str(round(float(priceusd),6))+" USD "+"("+change24hr+"% "+up_or_down+")"+"\n"+\
               str(round(float(price),6))+" EOS\n\n"

        volumeinfo = "*"+requested_symbol.upper()+" 24hr Volume*:\n"+"{:,.0f}".format(float(vol_24hr))+" USD"

        if len(str(rank)) > 0:
            marketcapinfo = "\n\nEOSIO Rank "+str(rank)+" | ${:,.0f}".format(float(marketcap))+ " Marketcap | {:,.0f}".format(float(circulating))+ " "+requested_symbol.upper()+" circulating"
        else:
            marketcapinfo = "\n\n${:,.0f}".format(float(marketcap))+ " Marketcap | {:,.0f}".format(float(circulating))+ " "+requested_symbol.upper()+" circulating"
    except Exception as e:
        print(e)
        response = "The EFi V2 Bot is under maintenance. Visit https://eosv2.finance to learn more about the project."

    chat_id = update.effective_chat.id
    try:
        context.bot.send_message(chat_id=chat_id, text=priceinfo+volumeinfo+marketcapinfo, parse_mode=telegram.ParseMode.MARKDOWN)
    except Exception as e:
        print(e)
        context.bot.send_message(chat_id=chat_id, text="This Token is not supported", parse_mode=telegram.ParseMode.MARKDOWN)


def chonge_handler(update, context):
    chonge_replies = ["Shut Up, Chonge!", "LOL Chonge, you're never right...", "Chonge, you want to fight me?", "What did you say about my Momma, Chonge?",\
                      "Chonge, if you keep talking I'm going to have to send wilma out to get you!", "Chonge, I'm smarter than you are.", "Ok bro, whatever",\
                      "LMAO Chonge just talks crap all day", "Even wilma is smarter than Chonge", "Dude, Chonge, stop talking to me....", "I think Chonge has a crush on me"]

    horselorde_replies = ["Shut Up, Horselorde!", "LOL Horselorde, you're such a pleb...", "Horselorde, you want to fight me?", "What did you say about my Momma, Horselorde?",\
                      "Horselorde, if you keep talking I'm going to have to send wilma out to get you!", "Horselorde, I'm smarter than you are.", "Ok bro, whatever",\
                      "LMAO Horselorde just talks crap all day", "Even wilma is smarter than Horselorde", "Dude, Horselorde, stop talking to me...."]

    # Update this so it has a list of messages it will send to people.
    print(update.message.from_user.username,"has sent a message")
    # Tells chonge to shut up, once every 5 or so messages.
    rand = random.randint(1,10)
    if rand < 2 and update.message.from_user.username == "chonge":
        print("Telling Chonge to shut up!")
        chat_id = update.effective_chat.id
        chongetext = random.choice(chonge_replies)
        context.bot.send_message(chat_id=chat_id, text=chongetext, parse_mode=telegram.ParseMode.MARKDOWN)

    if rand < 2 and update.message.from_user.username == "Horselorde":
        print("Telling Horselorde to shut up!")
        chat_id = update.effective_chat.id
        horselordetext = random.choice(horselorde_replies)
        context.bot.send_message(chat_id=chat_id, text=horselordetext, parse_mode=telegram.ParseMode.MARKDOWN)


def main():

    telegram_bot_token = "XXXXXX" # Your telegram Bot token goes here

    updater = Updater(token=telegram_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("hello", hello))
    dispatcher.add_handler(CommandHandler("p", getPrice))
    dispatcher.add_handler(CommandHandler("defi", getDefi))
    dispatcher.add_handler(CommandHandler("start", start_callback))
    #dispatcher.add_handler(MessageHandler(Filters.text, chonge_handler))
    updater.start_polling()


if __name__ == '__main__':
    main()
