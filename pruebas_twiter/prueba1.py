#scrape twiter

import pandas as pd
from tqdm.notebook import tqdm
import snscrape.modules.twitter as snstw

scraper = snstw.TwitterSearchScraper("#python")

tweets = []
for i, tweet in enumerate(scraper.get_items()):
    
    data = [
        tweet.date,
        tweet.id, 
        tweet.content, 
        tweet.user.username
    ]
    tweets.append(data)
    if i > 50:
        break

tweet_df = pd.DataFrame(tweets, columns=['date','id','content','username'])

#deprecated