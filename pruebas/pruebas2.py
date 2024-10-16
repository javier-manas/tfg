import re
import numpy as np
from transformers import pipeline
import json
import pandas as pd
import os

from collections import Counter


midic={0: 'admiration', 1: 'amusement', 2: 'anger', 3: 'annoyance', 4: 'approval', 5: 'caring', 6: 'confusion', 7: 'curiosity', 8: 'desire', 9: 'disappointment', 10: 'disapproval', 11: 'disgust', 12: 'embarrassment', 13: 'excitement', 14: 'fear', 15: 'gratitude', 16: 'grief', 17: 'joy', 18: 'love', 19: 'nervousness', 20: 'optimism', 21: 'pride', 22: 'realization', 23: 'relief', 24: 'remorse', 25: 'sadness', 26: 'surprise', 27: 'neutral'}

dicetico={0: 'Anger', 1: 'Disgust', 2: 'Fear', 3: 'Joy', 4: 'Sadness', 5: 'Surprise', 6: 'Neutral'}

dicSchwartz={0: 'selfDirection', 1: 'stimulation', 2: 'power', 3: 'hedonism', 4: 'achievement', 5: 'security', 6: 'conformity', 7: 'tradition', 8: 'benevolence', 9: 'universalism'}

dicJonathan={0: 'care', 1: 'fairness', 2: 'loyalty', 3: 'authority', 4: 'sanctity',5: 'liberty'}

dicTribes={0: 'spiritualists', 1: 'nerds', 2: 'fatherlanders', 3: 'treehuggers'}

dicABL={0: 'leech', 1: 'bee', 2: 'ant'}

dicFNST={0: 'fatherlander', 1: 'nerd', 2: 'spiritualist', 3: 'treehugger'}


def leerDocumento(ruta):
        
    if os.path.exists(ruta):
       with open(ruta, 'r', encoding='utf-8') as file:
        contenido = file.read()
        # Extraer textos y atributos usando una expresión regular
        documento = re.findall(r'Texto \d+:\s*[“"](.*?)[”"]\s*(\w+)', contenido, re.DOTALL)
        
        # Separar textos y atributos
        textos = [texto for texto, atributo in documento]
        atributos = [atributo for texto, atributo in documento]

        # Crear el DataFrame
        df = pd.DataFrame({"texto": textos, "atributo": atributos})
        return df

    else:
        print("El archivo no existe en la ruta especificada.")
        return


def analizarTextos(ruta,modelo):
    cont  = 0   
    #se lee el documento y se hace pd
    documento = leerDocumento(ruta)
    classifier = pipeline("text-classification",model= modelo, top_k=None)

    if ruta == r'D:\1 Mierdas\Escritorio\TextosSchawrtz.txt':
        etico = 'Schawrtz'
    elif ruta == r'D:\1 Mierdas\Escritorio\TextosJonathan.txt':
        etico = 'Jonathan'
    else: etico = 'nada'
    
    acumuladototal = acumulado_Jonathan
    aciertos = []
    fallos = []

    #for
    for index, row in documento.iterrows():
        #se coge el primer texto
        texto = row['texto']
                
    #se separan las frases del texto y se reinician los acumulados y diccionarios
        frases = re.split(r'[.!?]', texto)
        frases = [frase.strip() for frase in frases if frase.strip()]

        if modelo == abl:
            acumulado = acumulado_abl
        elif modelo == fnst:
            acumulado = acumulado_fnst
        else:
            acumulado = acumulado_Jonathan


        if modelo == abl:
            dic = dicABL
        elif modelo == fnst:
            dic = dicFNST
        else:
            dic = midic

        #se evalua cada frase y se añade al acumulado
        for i in range(len(frases)):
            
            

            analizador = classifier(frases[i])

            analizador_ordenado = sorted(analizador[0], key=lambda x: int(x['label'].split('_')[-1]))

            salida = [item['score'] for item in analizador_ordenado]

            acumulado = [x + y for x, y in zip(acumulado, salida)]

            acumuladototal = [x + y for x, y in zip(acumulado, salida)]

        acumulado =  [x / len(frases) for x in acumulado]

        acumulado = [(dic[i], valor) for i, valor in enumerate(acumulado)]   

        
        
        cont = cont +1

        if (cont == 40) and True:
            cont= 0
            print(acumuladototal)
            print()
            acumuladototal = acumulado_Jonathan
        
 




    
acumulado_abl = [0.0,0.0,0.0]
acumulado_fnst = [0.0,0.0,0.0,0.0]
acumulado_Schawrtz = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
acumulado_Jonathan = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

Schawrtz  = 'mrovejaxd/goemotions_bertspanish_finetunig_h'
Jonathan =  'mrovejaxd/goemotions_bertspanish_finetunig_h'
abl = 'mrovejaxd/ABL_trad_2h'
fnst = 'mrovejaxd/FNST_trad_2j'    
    

# se piden estos para correr la funcion documento, modelo
ruta_prueba = r'D:\1 Mierdas\Escritorio\textosprueba.txt'
ruta_jonathan = r'D:\1 Mierdas\Escritorio\TextosJonathan.txt'
ruta_Schawrtz = r'D:\1 Mierdas\Escritorio\TextosSchawrtz.txt'
ruta_fnst = r'D:\1 Mierdas\Escritorio\Textosfnst.txt'
ruta_abl = r'D:\1 Mierdas\Escritorio\Textosabl.txt'


ruta_jonathan = ruta_prueba
#analizarTextos(ruta_prueba,Jonathan)
#analizarTextos(ruta_jonathan,Jonathan)
#analizarTextos(ruta_Schawrtz,Schawrtz)
#analizarTextos(ruta_abl,abl)
#analizarTextos(ruta_fnst,fnst)



print('fin\n')


