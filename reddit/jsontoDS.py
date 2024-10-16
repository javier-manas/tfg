import requests
import json
import praw
import time
import prawcore
import re
from datasets import Dataset
import pandas as pd

tribus = ['F','N','S','T']
cont=50000

def extract_sentences(data):
    sentences = []
    for text in data:
        # Divide el texto en frases utilizando comas y puntos como separadores
        text_sentences = re.split('[,.]', text)
        # Elimina los espacios en blanco al inicio y final de cada frase
        text_sentences = [sentence.strip() for sentence in text_sentences]
        # Agrega cada frase a la lista de frases
        sentences.extend(text_sentences)
    return sentences

def remove_duplicates(lst):
    return list(set(lst))

def gen():
    for tribe in tribus:
        ruta = r'D:\2 cosas\1 Curso upm\TFG 1\datasets\DatasetsFNSTingles\DS_FNST_trad_mix' + tribe + '.json'
        with open(ruta) as json_file:
            data = json.load(json_file)
        global cont
        print(tribe)
        frases = extract_sentences(data)

        frases = remove_duplicates(frases)

        for frase in frases:
            cont = cont +1
            if tribe == 'F':
                yield {"text": frase, "labels": 0}
            
            if tribe == 'N':
                yield {"text": frase, "labels": 1}
            
            if tribe == 'S':
                yield {"text": frase, "labels": 2}
            
            if tribe == 'T':
                yield {"text": frase, "labels": 3}

            if tribe == 'A':
                yield {"id": str(cont),"text": frase, "labels": 2}
            
            if tribe == 'B':
                yield {"id": str(cont),"text": frase, "labels": 1}
            
            if tribe == 'L':
                yield {"id": str(cont),"text": frase, "labels": 0}

ds = Dataset.from_generator(gen)

df = pd.DataFrame(ds)
print(df)
num_lineas = df.shape[0]
print("num lineas: ", num_lineas)

ds2 = ds

try:
    ds2 = ds2.train_test_split(test_size=0.1)
    size = 0.1 * len(ds2)
    print(size)
    print(ds2)


    ds2.push_to_hub("mrovejaxd/DS_FNST_sinpodemos", private=True)
    ds2.save_to_disk(r'D:\2 cosas\1 Curso upm\TFG 1\datasets\DS_FNST_sinpodemos')
    
    
except Exception as e:
    print("D","s")