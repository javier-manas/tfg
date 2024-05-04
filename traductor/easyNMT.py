from easynmt import EasyNMT
import requests
import json
import praw
import time
import prawcore
import re
from datasets import Dataset
import pandas as pd


model = EasyNMT('opus-mt')
tribus = ['F','N','S','T']


def inicio(data):
    cont = 0
    dataset = []
    while (len(data)> 50): 
        aux, resto = trad(data)
        dataset.append(aux)
        data = resto
        cont = cont +1
        if (cont%10==0):
            print (cont)

    return dataset

def trad(data):
    try:
        aux = data[:50]
        resto = data[50:]
        aux = model.translate(aux, target_lang='es')

        return aux, resto
       
    except Exception:
        aux = []
        resto = data[50:]
        print('-')
        return aux, resto
        
        

for tribe in tribus:
    ruta = r'D:\2 cosas\1 Curso upm\TFG 1\datasets\DatasetsFNSTingles\DS_en_' + tribe + '.json'
    with open(ruta) as json_file:
        data = json.load(json_file)
        
        dataset = inicio(data)
       
        comments_json = json.dumps(dataset)

        # saves comments in a json
        ruta = r'D:\2 cosas\1 Curso upm\TFG 1\datasets\DatasetsFNSTingles\DS_en_trad_auto_'+ tribe +'.json'
        jsonFile = open(ruta, "w")
        jsonFile.write(comments_json)
        jsonFile.close()
        print('termine '+ tribe)
    
print('termine terminado')

        




