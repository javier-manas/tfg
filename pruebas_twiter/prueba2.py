#python web

import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import re
import spacy
nlp = spacy.load('en_core_web_lg')
from twitterscraper import query_tweets
from twitterscraper.query import query_tweets_from_user
import datetime as dt

begin_date = dt.date(2020,7,1)
end_date = dt.date(2020,7,13)

limit = 100
lang = 'english'

user = 'realDonaldTrump'
tweets = query_tweets_from_user(user)
df = pd.DataFrame(t.__dicvt__ for t in tweets)

df =df.loc[df['screen_name'] == user]

df =df['text']

df