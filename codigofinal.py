import pandas as pd
from datasets import Dataset
from tweety.bot import Twitter
import re

def clean_tweet(text:str) -> str:
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"www.\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)  
    return text

def gen():
    #usuarios ocultos por bien a su privacidad
    bee = []
    ant = []
    leech = []

    twitter_client = Twitter()
    tribe = 1
    for i in range(len(bee)):
        print(bee[i])
        tweets = twitter_client.get_tweets(bee[i],8)
        for tweet in tweets:
            clean = clean_tweet(tweet.text)
            if len(clean) < 5:
                continue
            id = tweet.id
            yield {"id": id, "text": clean, "tribe": tribe}
    
    tribe = 2
    for i in range(len(ant)):
        tweets = twitter_client.get_tweets(ant[i],8)
        print(ant[i])
        for tweet in tweets:
            clean = clean_tweet(tweet.text)
            if len(clean) < 5:
                continue
            id = tweet.id
            yield {"id": id, "text": clean, "tribe": tribe}

    tribe = 3
    for i in range(len(leech)):
        print(leech[i])
        tweets = twitter_client.get_tweets(leech[i],8)
        for tweet in tweets:
            clean = clean_tweet(tweet.text)
            if len(clean) < 5:
                continue
            id = tweet.id
            yield {"id": id, "text": clean, "tribe": tribe}
         
ds = Dataset.from_generator(gen)

ds.save_to_disk(r'D:\1 Curso upm\TFG 1\datasets\DS_ABL')

df = pd.DataFrame(ds)
print(df)
num_lineas = df.shape[0]
print("num lineas: ", num_lineas)
