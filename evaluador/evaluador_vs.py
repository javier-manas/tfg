import re
import numpy as np
from transformers import pipeline

a = "mrovejaxd/goemotions_bertspanish_finetunig_a"
b = "mrovejaxd/goemotions_bertspanish_finetunig_b"
c = "mrovejaxd/goemotions_bertspanish_finetunig_c"
d = "mrovejaxd/goemotions_bertspanish_finetunig_d"
e = "mrovejaxd/goemotions_bertspanish_finetunig_e"
A = "mrovejaxd/goemotions_bertmultilingual"
B = "mrovejaxd/goemotions_distilbertbase"
C = "mrovejaxd/goemotions_bertspannish"
D = "j-hartmann/emotion-english-distilroberta-base"
E = "joeddav/distilbert-base-uncased-go-emotions-student"
f = "mrovejaxd/goemotions_bertspanish_finetunig_f"

aclassifier = pipeline("text-classification",model= a, return_all_scores=True)

bclassifier = pipeline("text-classification", model= b, return_all_scores=True)

cclassifier = pipeline("text-classification", model= c, return_all_scores=True)

dclassifier = pipeline("text-classification", model= d, return_all_scores=True)

eclassifier = pipeline("text-classification", model= e, return_all_scores=True)

Aclassifier = pipeline("text-classification", model= A, return_all_scores=True)

Bclassifier = pipeline("text-classification", model= B, return_all_scores=True)

Cclassifier = pipeline("text-classification", model= C, return_all_scores=True)

Dclassifier = pipeline("text-classification", model= D, return_all_scores=True)

Eclassifier = pipeline("text-classification", model= E, return_all_scores=True)

fclassifier = pipeline("text-classification", model= f, return_all_scores=True)


#c y d sacan valores demasiado altos y por la cara, A y B parece que son solo ingles, D y E no los uso por razones similares 

#inicializar las variables comunes como lista frases y las variables total y media de roberta

lista_frases1 = ["frase numero uno", "Cuando me siento triste escucho música.", "Todos los sonidos posibles excepto la llave, no puedo ver cómo se perdió en la primera búsqueda. ", "Mierda, supongo que por accidente compré un partido de boxeo de Pay-Per-View.", "el sol es divertido" , "El mismo maldito problema, un poco mejor dominio del idioma inglés.", "la guerra es algo terrible pero inherente al ser humano" , "espero aprobar este examen, mi padre me va a pegar de lo contrario", "quiero terminar mis responsabilidades y tener vacaciones, ojala llegue pronto ese dia"]
lista_frases2 = ["quiero el amor y ayudar", "no me gusta lo que odio y matar", "lloro cuando veo cosas tristes"]
lista_frases3 = ["Hoy es el mejor día de mi vida! Todo está saliendo como siempre soñé", "Ya estoy harto de tus excusas! No puedo creer tu falta de responsabilidad", "Siento un dolor profundo en el corazón que parece no tener fin. Extraño mucho a esa persona"]

listamodelos = [a, b, c, d, f]

midic={0: 'admiration', 1: 'amusement', 2: 'anger', 3: 'annoyance', 4: 'approval', 5: 'caring', 6: 'confusion', 7: 'curiosity', 8: 'desire', 9: 'disappointment', 10: 'disapproval', 11: 'disgust', 12: 'embarrassment', 13: 'excitement', 14: 'fear', 15: 'gratitude', 16: 'grief', 17: 'joy', 18: 'love', 19: 'nervousness', 20: 'optimism', 21: 'pride', 22: 'realization', 23: 'relief', 24: 'remorse', 25: 'sadness', 26: 'surprise', 27: 'neutral'}

dicetico={0: 'Anger', 1: 'Disgust', 2: 'Fear', 3: 'Joy', 4: 'Sadness', 5: 'Surprise', 6: 'Neutral'}

dicSchwartz={0: 'selfDirection', 1: 'stimulation', 2: 'power', 3: 'hedonism', 4: 'achievement', 5: 'security', 6: 'conformity', 7: 'tradition', 8: 'benevolence', 9: 'universalism'}

dicJonathan={0: 'care', 1: 'fairness', 2: 'loyalty', 3: 'authority', 4: 'sanctity'}

#codigo para obtener los resultados 

resumentribus = []
lista_frases = lista_frases3

for modelo in listamodelos:

    total= [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    media= [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    classifier = pipeline("text-classification",model= modelo, return_all_scores=True)
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
        
        
        
        #calcular media
        mediavalores = np.mean(nuevalista)

#reajustamiento para que la media sea x --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
       
    #ya no es necesario el reajustamiento
    
        if 1 == 2:
            listaaux= []
            factor = mediavalores/1
            #otro factor 0.0357 1
            for i in nuevalista:
                aux = i / factor
                listaaux.append(aux)
            salida = listaaux
            
            for i in range(len(lista_aux)):
                total[i] = total[i] - nuevalista[i]
                total[i] = total[i] + salida[i]
            
        else: salida = nuevalista
        
#reajustamiento para que la media sea x ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        #Recorrer la lista y modificar los valores mayores a 1.1
        salida = [0.0001 if elemento > 1.1 else elemento for elemento in salida]

        #imprimir la media de los valores de la frase
        nuevamediavalores = np.mean(salida)
        print("media: " + str(nuevamediavalores))
        print("")
      
      
        # Obtener los 5 valores más altos y sus índices 
        top5 = sorted([(i, valor) for i, valor in enumerate(salida) if valor <= 1.1], key=lambda x: x[1], reverse=True)[:5]

        for indice, valor in top5:
            print(f"emocion: {midic[indice]}, valor: {valor}")
        print("")
        
                       
#emocionnes simplificadas por frase--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
        if 1 == 2:
            #emocionnes simplificadas por frase
            Nmedia = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
            media = salida
            Nmedia[0] = (media[2] + media[3] + media[10]) / 3
            Nmedia[1] = (media[11]) / 1
            Nmedia[2] = (media[19] + media[14]) / 2
            Nmedia[3] = (media[18] + media[1] + media[4] + media[13] + media[15] + media[18] + media[20] + media[23] + media[21] + media[0] + media[8] + media[5]) / 12
            Nmedia[4] = (media[25] + media[9] + media[12] + media[24] + media[16]) / 5
            Nmedia[5] = (media[26] + media[22] + media[6] + media[7]) / 4
            Nmedia[6] = (media[27]) / 1

            print("emocionnes simplificadas: ")
            print("")
            for i in range(len(Nmedia)):
                    print(f"emocion: {dicetico[i]}, valor: {Nmedia[i]}")
            print("")
        
#emocionnes simplificadas por frase++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++     

#valores eticos sicologos por frase--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        if 1 == 1:
            #Sociologist Schwartz
            Nmedia = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
            media = salida
            Nmedia[0] = (media[6] + media[7] + media[22]) / 3
            Nmedia[1] = (media[1] + media[13] + media[7] + media[26]) / 4
            Nmedia[2] = (media[2] + media[11]) / 2
            Nmedia[3] = (media[8] + media[1] + media[13]) / 3
            Nmedia[4] = (media[9] + media[8] + media[2] + media[16] + media[17] + media[21] + media[25] + media[0]) / 8
            Nmedia[5] = (media[14] + media[3] + media[19] + media[23]) / 4
            Nmedia[6] = (media[3] + media[4] + media[12] + media[10] + media[24]) / 5
            Nmedia[7] = (media[4] + media[10] + media[9] + media[18] + media[14] + media[21] + media[12]) / 7
            Nmedia[8] = (media[5] + media[15] + media[18] + media[0]) / 4
            Nmedia[9] = (media[0] + media[15] + media[5] + media[20] + media[22]) / 5

            print("valores eticos pertenecientes al Sociologist Schwartz")
            print("")
            for i in range(len(Nmedia)):
                    print(f"valor etico: {dicSchwartz[i]}, valor: {Nmedia[i]}")
            print("")

            #psychologist Jonathan
            Nmedia = [0.0,0.0,0.0,0.0,0.0]
            media = salida
            Nmedia[0] = (media[0] + media[8] + media[5] + media[15] + media[17] + media[18] + media[23] + media[20]) / 8
            Nmedia[1] = (media[2] + media[3] + media[4] + media[10] + media[6]) / 5
            Nmedia[2] = (media[0] + media[5] + media[15] + media[17] + media[18] + media[21] + media[24] ) / 7
            Nmedia[3] = (media[2] + media[10] + media[11] + media[21] + media[26]) / 5
            Nmedia[4] = (media[15] + media[17] + media[18] + media[21] + media[23] + media[24]) / 6


            print("valores eticos pertenecientes al psychologist Jonathan")
            print("")
            for i in range(len(Nmedia)):
                    print(f"valor etico: {dicJonathan[i]}, valor: {Nmedia[i]}")
            print("")
#valores eticos sicologos por frase++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#ant bee leech por frase--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        if 1 == 2:
            #% de hormiga abeja o leech por frase
            Nmedia = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
            media = salida
            Nmedia[0] = (media[2] + media[3]) / 2
            Nmedia[1] = (media[3] + media[11] + media[12] + media[20]) / 4
            Nmedia[2] = (media[6] + media[9] + media[14] + media[19]) / 4
            Nmedia[3] = (media[1] + media[4] + media[5] + media[13] + media[17] + media[19] + media[21] + media[22]) / 8
            Nmedia[4] = (media[4] + media[10] + media[15] + media[26]) / 4
            Nmedia[5] = (media[9] + media[10] + media[12] + media[16] + media[23] + media[24]) / 6
            Nmedia[6] = (media[0] + media[5] + media[7] + media[8] + media[13] + media[18] + media[25]) / 7

            ant = 0.0
            bee = 0.0
            leech = 0.0

            ant = ant + abs(0.15 - Nmedia[0])
            bee = bee + abs(0.22 - Nmedia[0])
            leech = leech + abs(0.3 - Nmedia[0])

            ant = ant + abs(0.45 - Nmedia[1])
            bee = bee + abs(0.57 - Nmedia[1])
            leech = leech + abs(0.61 - Nmedia[1])

            ant = ant + abs(0.16 - Nmedia[2])
            bee = bee + abs(0.12 - Nmedia[2])
            leech = leech + abs(0.21 - Nmedia[2])

            ant = ant + abs(0.51 - Nmedia[3])
            bee = bee + abs(0.47 - Nmedia[3])
            leech = leech + abs(0.33 - Nmedia[3])

            ant = ant + abs(0.23 - Nmedia[4])
            bee = bee + abs(0.18 - Nmedia[4])
            leech = leech + abs(0.45 - Nmedia[4])

            ant = ant + abs(0.14 - Nmedia[5])
            bee = bee + abs(0.08 - Nmedia[5])
            leech = leech + abs(0.11 - Nmedia[5])

            ant = ant + abs(0.63 - Nmedia[6])
            bee = bee + abs(0.73 - Nmedia[6])
            leech = leech + abs(0.51 - Nmedia[6])


            # print("")
            #print("la diferencia de la muestra analizada respecto a la esperada. El resultado ideal seria 0")
            #print("ant: " + str(ant))
            #print("bee: " + str(bee))
            #print("leech: " + str(leech))
            #print("")

            menor = min(ant, bee, leech)
            ant = (ant - menor)/3
            bee = (bee - menor)/3
            leech = (leech - menor)/3

            Pant = 0.33 - ant + bee + leech
            Pbee = 0.33 - bee + ant + leech
            Pleech = 0.33 - leech + bee + ant

            aux = (Pant + Pbee + Pleech) - 1
            aux = aux/3

            Pant = Pant - aux
            Pbee = Pbee - aux
            Pleech = Pleech - aux

            BIant = int(Pant * 100)
            BIbee = int(Pbee * 100)
            BIleech = int(Pleech * 100)


            print("Segun esta frase: " + str(BIant) + "% ant, " + str(BIbee) + "% bee y " + str(BIleech) + "% leech.")
            print("")
            
#ant bee leech por frase++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        print("------------------------------------------------------------------------------------------------------------")

#final
    print("") 
    print("**************************************************************************************************************************************")
    print("") 
    print("**************************************************************************************************************************************")
    print("") 
    print("**************************************************************************************************************************************")
    print("") 

#compendio final de la media de todas las frases--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if 1 == 2:
        # salida con la media de todos los valores
        print()
        for o in range(len(lista_aux)):
          media[o] = total[o] / len(lista_frases)

        print("")
        print("media de valores totales:")
        print("")

        for indice, valor in enumerate(media):
            print(f"emocion: {midic[indice]}, valor: {valor}")

        print("")
        mediatotal = np.mean(media)
        print("media total: " + str(mediatotal))
        print("")

        #Media Sociologist Schwartz
        Nmedia = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        media = salida
        Nmedia[0] = (media[2] + media[8]) / 2
        Nmedia[1] = (media[8] + media[9]) / 2
        Nmedia[2] = (media[1] + media[8] + media[15] + media[17] + media[20] + media[21]) / 6
        Nmedia[3] = (media[1] + media[7] + media[13] + media[17] + media[18]) / 5
        Nmedia[4] = (media[6] + media[7] + media[20]) / 3
        Nmedia[5] = (media[5] + media[15] + media[18] + media[20]) / 4
        Nmedia[6] = (media[4] + media[5] + media[15]) / 3
        Nmedia[7] = (media[0] + media[3] + media[5] + media[9] + media[10] + media[12] + media[18]) / 7
        Nmedia[8] = (media[12] + media[15] + media[27]) / 3
        Nmedia[9] = (media[2] + media[14]) / 2

        print("Todas las frases: valores eticos pertenecientes al Sociologist Schwartz")
        print("")
        for i in range(len(Nmedia)):
            print(f"valor etico: {dicSchwartz[i]}, valor: {Nmedia[i]}")
        print("")

        #Media psychologist Jonathan
        Nmedia = [0.0,0.0,0.0,0.0,0.0]
        media = salida
        Nmedia[0] = (media[4] + media[3] + media[5] + media[18]) / 4
        Nmedia[1] = (media[2] + media[15] + media[16] + media[22] + media[24] + media[27]) / 6
        Nmedia[2] = (media[2] + media[4] + media[21] ) / 3
        Nmedia[3] = (media[0] + media[4] + media[14] ) / 3
        Nmedia[4] = (media[3] + media[9] + media[10] + media[11] ) / 4


        print("Todas las frases: valores eticos pertenecientes al psychologist Jonathan")
        print("")
        for i in range(len(Nmedia)):
            print(f"valor etico: {dicJonathan[i]}, valor: {Nmedia[i]}")
        print("")
        #media de los valores eticos de todas las frases
        Nmedia = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]

        Nmedia[0] = (media[2] + media[3]) / 2
        Nmedia[1] = (media[3] + media[11] + media[12] + media[20]) / 4
        Nmedia[2] = (media[6] + media[9] + media[14] + media[19]) / 4
        Nmedia[3] = (media[1] + media[4] + media[5] + media[13] + media[17] + media[19] + media[21] + media[22]) / 8
        Nmedia[4] = (media[4] + media[10] + media[15] + media[26]) / 4
        Nmedia[5] = (media[9] + media[10] + media[12] + media[16] + media[23] + media[24]) / 6
        Nmedia[6] = (media[0] + media[5] + media[7] + media[8] + media[13] + media[18] + media[25]) / 7

        print("")
        print("Todas las frases: valores eticos pertenecientes al articulo de Peter")
        print("")

        for i in range(len(Nmedia)):
                print(f"valor etico: {dicetico[i]}, valor: {Nmedia[i]}")
        print("")

        #codigo para obtener ant, bee y leech del total de las frases

        ant = 0.0
        bee = 0.0
        leech = 0.0

        ant = ant + abs(0.15 - Nmedia[0])
        bee = bee + abs(0.22 - Nmedia[0])
        leech = leech + abs(0.3 - Nmedia[0])

        ant = ant + abs(0.45 - Nmedia[1])
        bee = bee + abs(0.57 - Nmedia[1])
        leech = leech + abs(0.61 - Nmedia[1])

        ant = ant + abs(0.16 - Nmedia[2])
        bee = bee + abs(0.12 - Nmedia[2])
        leech = leech + abs(0.21 - Nmedia[2])

        ant = ant + abs(0.51 - Nmedia[3])
        bee = bee + abs(0.47 - Nmedia[3])
        leech = leech + abs(0.33 - Nmedia[3])

        ant = ant + abs(0.23 - Nmedia[4])
        bee = bee + abs(0.18 - Nmedia[4])
        leech = leech + abs(0.45 - Nmedia[4])

        ant = ant + abs(0.14 - Nmedia[5])
        bee = bee + abs(0.08 - Nmedia[5])
        leech = leech + abs(0.11 - Nmedia[5])

        ant = ant + abs(0.63 - Nmedia[6])
        bee = bee + abs(0.73 - Nmedia[6])
        leech = leech + abs(0.51 - Nmedia[6])


       # print()
        #print("la diferencia de la muestra analizada respecto a la esperada. El resultado ideal seria 0")
        #print("ant: " + str(ant))
        #print("bee: " + str(bee))
        #print("leech: " + str(leech))

        print()

        menor = min(ant, bee, leech)
        ant = (ant - menor)/3
        bee = (bee - menor)/3
        leech = (leech - menor)/3

        Pant = 0.33 - ant + bee + leech
        Pbee = 0.33 - bee + ant + leech
        Pleech = 0.33 - leech + bee + ant

        aux = (Pant + Pbee + Pleech) - 1
        aux = aux/3

        Pant = Pant - aux
        Pbee = Pbee - aux
        Pleech = Pleech - aux

        BIant = int(Pant * 100)
        BIbee = int(Pbee * 100)
        BIleech = int(Pleech * 100)

        resumentribus.append(BIant)
        resumentribus.append(BIbee)
        resumentribus.append(BIleech)

        print()

        print("**********************************************************************************")
        print("Segun las frases analizadas, el usuario es " + str(BIant) + "% ant, " + str(BIbee) + "% bee y " + str(BIleech) + "% leech.")
        print("**********************************************************************************")

        print()
    
#compendio final de la media de todas las frases ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++