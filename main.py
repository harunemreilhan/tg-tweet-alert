import twint
import json
import requests
import telebot

BOT_TOKEN = "5874063359:AAGTAAxCAqOfUmgDsNWYNRaybjhtq9HH_h0"
bot = telebot.TeleBot(BOT_TOKEN)
tgbot_token = BOT_TOKEN

@bot.message_handler(commands=['start'])
def start(message):
    sent = bot.send_message(message.chat.id, 'Let\'s Start')
    main_keywords(message) 

@bot.message_handler(commands=['addkeywords'])
def main_keywords(message):
    sent = bot.send_message(message.chat.id, 'Please input your keywords like this type: \n keyword1 OR keyword2 OR KEYWORD OR Keyword4')
    bot.register_next_step_handler(sent, addkeywords)


def addkeywords(message):
    global keywords, group_id
    keywords = f"{message.text}"
    bot.send_message(message.chat.id, "Thanks")
    group_id = int(f"{message.chat.id}")
    start()


def start():
    tweet_list = []


    def load_pandas():
        with open ("pandas.json") as f:
            return json.load(f)

    def search_tweets():
        tweets = []
        c = twint.Config()
        c.Search = keywords
        c.Store_object = True
        c.Limit = 100
        c.Pandas = True
        c.Store_object_tweets_list = tweets
        print("------------------------------------------------------")
        twint.run.Search(c)
        Tweets_df = twint.storage.panda.Tweets_df.drop_duplicates("id")
        Tweets_df.to_json("pandas.json")
        if len(tweets) > 0:
            was_send()
        else:    
            while len(tweets) == 0:
                search_tweets()
        print("------------------------------------------------------")



    sent_list = []

    def load_links():
        with open("sent.txt") as sent:
            for links in sent:
                links = links.strip()
                sent_list.append(links)

    def was_send():
        load_links()
        write_file = open("sent.txt" , "a")
        get_links = load_pandas()
        try:
            links = get_links["link"]
            for i in links:
                i = str(i)
                if links[i] not in sent_list:
                    tweet_list.append(links[i])
                    write_file.write(links[i] + "\n")
                else:
                    continue
                i = int(i)
                i += 1
        except KeyError:
            search_tweets()

    def main():  
        while True: 
            search_tweets()
            i = 0
            while i < len(tweet_list):
                send_message("New Tweet!" + tweet_list[i])
                i += 1
            tweet_list.clear()

    def send_message(message):
        response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(tgbot_token, "sendMessage"),
            data={'chat_id': group_id, 'text': message}
        ).json()


    if __name__ == "__main__":
        main()


bot.polling()
