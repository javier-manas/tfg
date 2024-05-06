import requests
import json
import praw
import time
import prawcore
import re

#from translate import Translator

#translator = Translator(provider='libre',from_lang='en', to_lang='es')

reddit = praw.Reddit(
    client_id="1N1ZzxSfW7QXsaC9g2iY0w",
    client_secret="OfO9fLXgivt2oPNFIxzGpgZPWakDbg",
    user_agent="Bebeconkeso ",
)

def clean_tweet(text:str) -> str:
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"www.\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)  
    return text

def get_latest_submissions(tribe):
    submissions = set()
    # choose the subreddits you want to retrieve comments from here
    if tribe == 'F':
        tribes = 'Conservative+Traditionalist+Religion'

    if tribe == 'N':
        tribes = 'science+technology+math'

    if tribe == 'S':
        tribes = 'Meditation+yoga+spirituality'

    if tribe == 'T':
        tribes = 'environment+ClimateAction+ZeroWaste'

    if tribe == 'A':
        tribes = 'nextfuckinglevel+sports+GYM'
    
    if tribe == 'B':
        tribes = 'wholesomememes+Art+GetMotivated'
    
    if tribe == 'L':
        tribes = 'CryptoCurrency+MoneyMaking+adultery'



    for submission in reddit.subreddit(tribes).top(time_filter='all', limit=10):
        submissions.add(submission)
    for submission in reddit.subreddit(tribes).hot(limit=10):
        submissions.add(submission)
    return submissions

def  gatherData(tribus):

    submissions = get_latest_submissions(tribus)
    print(len(submissions))

    comments = []
    count = 1


    for submission in submissions:
        #title =  translator.translate(clean_tweet(submission.title))
        title = clean_tweet(submission.title)
        #selftext = translator.translate(clean_tweet(submission.selftext))
        selftext = clean_tweet(submission.selftext)
        #if len(title) > 10:
            #comments.append(title)
        #if len(selftext) > 10:
           # comments.append(selftext)
        submission.comments.replace_more(limit=15)
        for comment in submission.comments.list():

            #body = translator.translate(clean_tweet(comment.body))
            body = clean_tweet(comment.body)
            if len(body) > 10:
                comments.append(body)

            if count % 30000 == 0:
                print("Demasiadas solicitudes. Esperando ...")
                time.sleep(120)

            if count % 1000 == 0:
                print(count)
                print(body)

            count += 1





    print('finished')

    comments_json = json.dumps(comments)

    # saves comments in a json
    ruta = r'D:\2 cosas\1 Curso upm\TFG 1\datasets\DatasetsABLingles\DS_en_' + tribus + '.json'
    jsonFile = open(ruta, "w")
    jsonFile.write(comments_json)
    jsonFile.close()

    time.sleep(240)
    print('continuing')

gatherData('A')
gatherData('B')
gatherData('L')
