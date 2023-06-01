from tweety.bot import Twitter

tweets = Twitter().get_tweets('elonmusk', 2)
for tweet in tweets:
    print(tweet)