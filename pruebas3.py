import json
import itertools

tribus = ['F', 'N', 'S', 'T']

#dice cuantas tuplas tiene cada lista y cuantas tuplas una vez arreglada la lista
for tribu in tribus:


    
    ruta = r'D:\2 cosas\1 Curso upm\TFG 1\datasets\DatasetsFNSTingles\DS_en_trad_auto_' + tribu + ' .json'
    with open(ruta) as json_file:
        data = json.load(json_file)    

    print(tribu)
    print(len(data))

    A = data
    data = list(itertools.chain(*A))

    print(len(data))
    print('')

#arregla las listas para que no sean  listas de tuplas de frases sino listas de frases
for tribu in tribus:


    
    ruta = r'D:\2 cosas\1 Curso upm\TFG 1\datasets\DatasetsFNSTingles\DS_en_trad_auto_' + tribu + ' .json'
    with open(ruta) as json_file:
        data = json.load(json_file)    
    
    A = data
    data = list(itertools.chain(*A))

    comments_json = json.dumps(data)
    ruta = r'D:\2 cosas\1 Curso upm\TFG 1\datasets\DatasetsFNSTingles\DS_en_trad_auto_'+ tribu +'.json'
    jsonFile = open(ruta, "w")
    jsonFile.write(comments_json)
    jsonFile.close()
    print('termine '+ tribu)
    


