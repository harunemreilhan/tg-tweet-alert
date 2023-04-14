import twint
import json
import asyncio
import nest_asyncio
import time
import requests

tweet_list = []


def load_pandas():
    with open ("pandas.json") as f:
        return json.load(f)
    
def load_config():
    with open ("config.json") as f:
        return json.load(f)


def search_tweets():
    tweets = []
    c = twint.Config()
    c.Search = config["keywords"]
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

async def main():  
    while True: 
        search_tweets()
        i = 0
        while i < len(tweet_list):
            time.sleep(config["time_interval"])
            send_message(config["caption"] + tweet_list[i])
            i += 1
        tweet_list.clear()

def send_message(message):
    response = requests.post(
        url='https://api.telegram.org/bot{0}/{1}'.format(tgbot_token, "sendMessage"),
        data={'chat_id': group_id, 'text': message}
    ).json()


def init():
    global config, tgbot_token, group_id
    config = load_config()
    tgbot_token = config["tgbot_token"]
    group_id = config["group_id"]

if __name__ == "__main__":
    nest_asyncio.apply()
    init()
    loop =  asyncio.get_event_loop()
    loop.run_until_complete(main())