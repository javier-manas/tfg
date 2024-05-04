import re
import numpy as np
from transformers import pipeline

#lista de todos los modelos disponibles
a = "mrovejaxd/goemotions_bertspanish_finetunig_a"
b = "mrovejaxd/goemotions_bertspanish_finetunig_b"
c = "mrovejaxd/goemotions_bertspanish_finetunig_c"
d = "mrovejaxd/goemotions_bertspanish_finetunig_d"
e = "mrovejaxd/goemotions_bertspanish_finetunig_e"
f = "mrovejaxd/goemotions_bertspanish_finetunig_f"
A = "mrovejaxd/goemotions_bertmultilingual"
B = "mrovejaxd/goemotions_distilbertbase"
C = "mrovejaxd/goemotions_bertspannish"
D = "j-hartmann/emotion-english-distilroberta-base"
E = "joeddav/distilbert-base-uncased-go-emotions-student"

ABL_a = "mrovejaxd/ABL_a"
ABL_b = "mrovejaxd/ABL_b"
ABL_c = "mrovejaxd/ABL_c"
ABL_d = "mrovejaxd/ABL_d"

FNST_a = "mrovejaxd/FNST_a"
FNST_b = "mrovejaxd/FNST_b"


#inicializar las variables comunes como lista frases y las variables total y media de roberta

lista_frases1 = ["frase numero uno", "Cuando me siento triste escucho música.", "Todos los sonidos posibles excepto la llave, no puedo ver cómo se perdió en la primera búsqueda. ", "Mierda, supongo que por accidente compré un partido de boxeo de Pay-Per-View.", "el sol es divertido" , "El mismo maldito problema, un poco mejor dominio del idioma inglés.", "la guerra es algo terrible pero inherente al ser humano" , "espero aprobar este examen, mi padre me va a pegar de lo contrario", "quiero terminar mis responsabilidades y tener vacaciones, ojala llegue pronto ese dia"]
lista_frases2 = ["quiero el amor y ayudar", "no me gusta lo que odio y matar", "lloro cuando veo cosas tristes"]
lista_frases3 = ["Hoy es el mejor día de mi vida!", "Ya estoy harto de tus excusas!", "Siento un dolor profundo en el corazón que parece no tener fin."]
lista_frases4 = ["Cuando me siento triste escucho música."]
lista_frases5 = ["Viva dios la patria y el rey", "ayer desarrolle una nueva inteligencia artificial", "El camino del alma es estar en paz consigo misma", "necesitamos reciclar para salvar al planeta"]


midic={0: 'admiration', 1: 'amusement', 2: 'anger', 3: 'annoyance', 4: 'approval', 5: 'caring', 6: 'confusion', 7: 'curiosity', 8: 'desire', 9: 'disappointment', 10: 'disapproval', 11: 'disgust', 12: 'embarrassment', 13: 'excitement', 14: 'fear', 15: 'gratitude', 16: 'grief', 17: 'joy', 18: 'love', 19: 'nervousness', 20: 'optimism', 21: 'pride', 22: 'realization', 23: 'relief', 24: 'remorse', 25: 'sadness', 26: 'surprise', 27: 'neutral'}

dicetico={0: 'Anger', 1: 'Disgust', 2: 'Fear', 3: 'Joy', 4: 'Sadness', 5: 'Surprise', 6: 'Neutral'}

dicSchwartz={0: 'selfDirection', 1: 'stimulation', 2: 'power', 3: 'hedonism', 4: 'achievement', 5: 'security', 6: 'conformity', 7: 'tradition', 8: 'benevolence', 9: 'universalism'}

dicJonathan={0: 'care', 1: 'fairness', 2: 'loyalty', 3: 'authority', 4: 'sanctity'}

dicTribes={0: 'spiritualists', 1: 'nerds', 2: 'fatherlanders', 3: 'treehuggers'}

dicABL={0: 'leech', 1: 'bee', 2: 'ant'}

dicFNST={0: 'fatherlander', 1: 'nerd', 2: 'spiritualist', 3: 'treehugger'}

#codigo para obtener los resultados 

#valores modificables ---------
lista_frases = lista_frases4
ABL = [ABL_a, ABL_b, ABL_c, ABL_d]
FNST = [FNST_a, FNST_b]
listamodelos = [a, b, c, d, e, f]
listamodelos = [a]
#valores modificables ++++++++++ 

#salidas modificables ---------
reajustamiento = False
emocionessimplificadas = False
valoreseticosporfrase = False
ABLporfrase = False
FNSTporfrase = True
valoreseticostodoeltexto = False
ABLtodoeltexto = False
#salidas modificables ++++++++++ 

ABLcompendio = []

for modelo in listamodelos:

    total= [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    media= [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    classifier = pipeline("text-classification",model= modelo, top_k=None)
    print("modelo: " + str(modelo))
    
    for i in range(len(lista_frases)):
        analizador = classifier(lista_frases[i])

        cadena = str(analizador[0])

        lista_aux = cadena.split('{')

        lista_aux.pop(0)

        nuevalista= []

        for e in range(len(lista_aux)):
            dato = lista_aux[e]
            score = dato.split(':')
            elemento = score[2]
            numero = re.sub(r'[^\d.]+', '', elemento)
            num_float = float(numero)
            nuevalista.append(num_float)
            total[e] = total[e] + num_float

        print("")

        # imprimir la frase
        print("frase num " + str(i) + " : " + str(lista_frases[i]))
        print("")
        
        index = i
        
        #calcular media
        mediavalores = np.mean(nuevalista)

