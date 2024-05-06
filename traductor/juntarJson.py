import json
from unidecode import unidecode
import re
import itertools

tribus = ['A', 'B', 'L']

def guardar (data, tribu):
    comments_json = json.dumps(data)
    ruta = r'D:\2 cosas\1 Curso upm\TFG 1\datasets\DatasetsFNSTingles\DS_FNST_trad_mix'+ tribu +'.json'
    jsonFile = open(ruta, "w")
    jsonFile.write(comments_json)
    jsonFile.close()
    
#arregla las listas para que no sean  listas de tuplas de frases sino listas de frases y junta dos datasets en uno
for tribu in tribus:

    ruta = r'D:\2 cosas\1 Curso upm\TFG 1\datasets\DatasetsABLingles\DS_en_' + tribu + '.json'
    with open(ruta) as json_file:
        data = json.load(json_file)  

    print(tribu)
    print(len(data))

    ruta = r'D:\2 cosas\1 Curso upm\TFG 1\datasets\FNSTjson\DS_' + tribu + '.json'
    with open(ruta) as json_file:
        data2 = json.load(json_file) 

    data.extend(data2)

    print(len(data))
    print('')
    
    respuesta = input("¿Desea guardar los datos para la tribu {}? (S/N): ".format(tribu))

    # Verificar la respuesta del usuario
    if respuesta.upper() == 'S':
        guardar(data, tribu)
        print(respuesta)
    else:print('dijo no')
