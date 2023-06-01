from tweety.bot import Twitter
import re
from typing import List
import pandas as pd
from tweety.types import Tweet



def clean_tweet(text:str) -> str:
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"www.\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)  
    return text

def create_dataframe_from_tweets(tweets: List[Tweet]) -> pd.DataFrame:
    pd.set_option('display.max_rows', None)
    rows = []
    for tweet in tweets:
        tribe = 1
        clean_text = clean_tweet(tweet.text)
        if len(clean_text) < 2:
            continue
        rows.append(
            {
                "id": tweet.id,
                "text": clean_text,
                "tribe": tribe,
                
            }
        )

        df = pd.DataFrame(
        rows, columns=["id", "text", "tribe"]
    )
    df.set_index("id", inplace=True)
    if df.empty:
        return df
    
    num_lineas = df.shape[0]
    print("num lineas: ", num_lineas)
    return df.sort_values(by="id", ascending=False)

#usuarios ocultos por bien a su privacidad
bee = ["Isasaweis","OLGATANON1313","AlejandroSanz","pacoleonbarrios","albertochicote","rosalia","enriqueolvera","DaniboubeTV","karguinano","SamySpain","VEGAOFICIAL","carlo_cocina","MuseoEscultura","UNIoficial","ingenieriared","ManzaneraAutor","CompositorHabla","LaCocinadMasito","JBarroso_Autor","GabiMartinArte","CarlosUrrozARTE","escrituraI","Arte_Master","A_tejer","CaroDuarteArte","En_Amor_ArtE","janogarcia_","perezreverte","one_arquitecto","arquitectozarat","ArquitectoAB","jmaarquitecto","PipeelArquitect","juanmoyaromero","arquitecto","veryescribir","tejerconlucila","AlbertLory1","matiasrcisneros","cocinadelpirata","gustamonton","IndiRP1","CdeCiencia","QuantumFracture","doctorfision","JaSantaolalla","jaimealtozano","lahiperactina","pedropabloisla","isabelaguilera"]
ant = []
leech = []


twitter_client = Twitter()




#tweets = twitter_client.get_tweets("elonmusk", 1)

lista=[]
tribe = bee
for i in range(len(tribe)):
    id = tribe[i]
    print(id)
    tweets = twitter_client.get_tweets(tribe[i])
    lista.append(tweets)
    print(lista[i])

lista=[]
tribe = ant
for i in range(len(tribe)):
    id = tribe[i]
    print(id)
    tweets = twitter_client.get_tweets(tribe[i])
    lista.append(tweets)
    print(lista[i])

lista=[]
tribe = leech
for i in range(len(tribe)):
    id = tribe[i]
    print(id)
    tweets = twitter_client.get_tweets(tribe[i])
    lista.append(tweets)
    print(lista[i])



