import pandas as pd
from datasets import Dataset, concatenate_datasets
from tweety.bot import Twitter
import re


def clean_tweet(text:str) -> str:
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"www.\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)  
    return text

def gen1():
    prueba = ["elonmusk"]
    prueba2 = ["Canelo"]
    twitter_client = Twitter()
    tribe = 1
    for i in range(len(prueba)):
        tweets = twitter_client.get_tweets(prueba[i],2)
        for tweet in tweets:
            clean = clean_tweet(tweet.text)
            if len(clean) < 5:
                continue
            id = tweet.id
            yield {"id": id, "text": clean, "tribe": tribe}
    
    tribe = 2
    for i in range(len(prueba2)):
        tweets = twitter_client.get_tweets(prueba2[i],2)
        for tweet in tweets:
            clean = clean_tweet(tweet.text)
            if len(clean) < 5:
                continue
            id = tweet.id
            yield {"id": id, "text": clean, "tribe": tribe}
         
ds1 = Dataset.from_generator(gen1)
pd.set_option('display.max_rows', None)
df = pd.DataFrame(ds1)
print(df)