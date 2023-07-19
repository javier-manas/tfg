import requests
import json
import praw
import time
import prawcore
import re
from datasets import Dataset
import pandas as pd

tribus = ['F', 'N', 'S', 'T']


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
        ruta = r'D:\1 Curso upm\TFG 1\datasets\DS_' + tribe + '.json'
        with open(ruta) as json_file:
            data = json.load(json_file)

        
        frases = extract_sentences(data)

        frases = remove_duplicates(frases)

        for frase in frases:
            if tribe == 'F':
                yield {"text": frase, "labels": 0}
            
            if tribe == 'N':
                yield {"text": frase, "labels": 1}
            
            if tribe == 'S':
                yield {"text": frase, "labels": 2}
            
            if tribe == 'T':
                yield {"text": frase, "labels": 3}


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


    ds2.push_to_hub("mrovejaxd/DS_FNST", private=True)
    ds2.save_to_disk(r'D:\1 Curso upm\TFG 1\datasets\DS_FNST')
    
    
except Exception as e:
    print("D",e)





