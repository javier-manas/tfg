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
        tribes = 'esHistoria+vzlalibre+DerechoGenial'
    
    if tribe == 'N':
        tribes = 'LGBTes+ciencia+Tecnologia'
    
    if tribe == 'S':
        tribes = 'filosofia_en_espanol+Espiritualidad+laexperienciahumana'
    
    if tribe == 'T':
        tribes = 'podemos+Veganismo+CurioseandoElMundo'



    for submission in reddit.subreddit(tribes).top(time_filter='all'):
        submissions.add(submission)
    for submission in reddit.subreddit(tribes).hot(limit=500):
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
        if len(title) > 5:
            comments.append(title)
        if len(selftext) > 5:
            comments.append(selftext)
        submission.comments.replace_more(limit=15)
        for comment in submission.comments.list():
            
            #body = translator.translate(clean_tweet(comment.body))
            body = clean_tweet(comment.body)
            if len(body) > 5:
                comments.append(body)

            if count % 15000 == 0:
                print("Demasiadas solicitudes. Esperando ...")
                time.sleep(120)

            if count % 1000 == 0:
                print(count)
                print(body)
            
            count += 1
            
        



    print('finished')

    comments_json = json.dumps(comments)
    
    # saves comments in a json
    ruta = r'D:\1 Curso upm\TFG 1\datasets\DS_' + tribus + '.json'
    jsonFile = open(ruta, "w")
    jsonFile.write(comments_json)
    jsonFile.close()

    time.sleep(240)
    print('continuing')

#gatherData('F')
#gatherData('N')
gatherData('S')
gatherData('T')










