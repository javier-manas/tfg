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


#lista de todos los modelos disponibles
a = "mrovejaxd/goemotions_bertspanish_finetunig_a"
b = "mrovejaxd/goemotions_bertspanish_finetunig_b"
c = "mrovejaxd/goemotions_bertspanish_finetunig_c"
d = "mrovejaxd/goemotions_bertspanish_finetunig_d"
e = "mrovejaxd/goemotions_bertspanish_finetunig_e"
f = "mrovejaxd/goemotions_bertspanish_finetunig_f"
g = "mrovejaxd/goemotions_bertspanish_finetunig_g"
h = "mrovejaxd/goemotions_bertspanish_finetunig_h"

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


ABL_trad_g  = "mrovejaxd/ABL_trad_g"
ABL_trad_i  = "mrovejaxd/ABL_trad_i"
ABL_trad_2a  = "mrovejaxd/ABL_trad_2a"
ABL_trad_2h  = "mrovejaxd/ABL_trad_2h"


FNST_trad_g = "mrovejaxd/FNST_trad_g"
FNST_trad_i = "mrovejaxd/FNST_trad_i"
FNST_trad_2a = "mrovejaxd/FNST_trad_2a"
FNST_trad_2j = "mrovejaxd/FNST_trad_2j"

ruta_aleatorio = r'D:\1 Mierdas\Escritorio\textosaleatorio.txt'
ruta_jonathan = r'D:\1 Mierdas\Escritorio\TextosJonathan.txt'
ruta_Schawrtz = r'D:\1 Mierdas\Escritorio\TextosSchawrtz.txt'
ruta_fnst = r'D:\1 Mierdas\Escritorio\Textosfnst.txt'
ruta_abl = r'D:\1 Mierdas\Escritorio\Textosabl.txt'

acumulado_abl = [0.0,0.0,0.0]
acumulado_fnst = [0.0,0.0,0.0,0.0]
acumulado_Schawrtz = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
acumulado_Jonathan = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

#val_Schawrtz = h
#val_Jonathan = h

lista_frases = ['']
lista_frases1 = ["frase numero uno", "Cuando me siento triste escucho música.", "Todos los sonidos posibles excepto la llave, no puedo ver cómo se perdió en la primera búsqueda. ", "Mierda, supongo que por accidente compré un partido de boxeo de Pay-Per-View.", "el sol es divertido" , "El mismo maldito problema, un poco mejor dominio del idioma inglés.", "la guerra es algo terrible pero inherente al ser humano" , "espero aprobar este examen, mi padre me va a pegar de lo contrario", "quiero terminar mis responsabilidades y tener vacaciones, ojala llegue pronto ese dia"]
lista_frases2 = ["quiero el amor y ayudar", "no me gusta lo que odio y matar", "lloro cuando veo cosas tristes"]
lista_frases3 = ["Hoy es el mejor día de mi vida!", "Ya estoy harto de tus excusas!", "Siento un dolor profundo en el corazón que parece no tener fin."]
lista_frases4 = ["Estoy tan agradecido por tenerte como madre, siempre haré lo que esté en mis manos para cuidarte.", "Cuando me siento triste escucho música.", 'Vamos a darlo todo en este proyecto y asegurarnos de que sea el mejor de la clase', 'Es vital que tomemos medidas hoy para proteger nuestros bosques y océanos, porque nuestro futuro y el de las próximas generaciones depende de ello']
lista_frases5 = ["Viva dios, la patria y el rey", "que pereza hacer la tarea, mejor copio de Roberto", "ayer desarrolle una nueva inteligencia artificial", "El camino del alma es estar en paz consigo misma", "necesitamos reciclar para salvar al planeta"]
lista_frases6 = ["hola"]
lista_frases7 = ["No tengo tiempo para ayudar a otros, estoy demasiado ocupado con mis propios asuntos.", "El placer es la única cosa que vale la pena buscar en esta vida.", "No cuestiono las órdenes de mis superiores, simplemente las ejecuto."]
lista_frases8 = ["Imaginémonos que cada cosa que hacemos tiene eco en los demás. Que somos inspiración y ejemplo. El éxito nunca es individual, es un logro colectivo. Sigamos dándolo todo para superar nuestros límites. ", 'Que usted @Mtelladof salga a defender a Ferreras muestra su complicidad con el periodismo corrupto que, junto a sus cloacas policiales, les hace el trabajo sucio. Lo tienen fácil con un presidente que tiene más miedo a Ferreras que agallas, pero Belarra sí dijo la verdad', '¡Qué admirable es la capacidad humana para perseverar frente a la adversidad y brillar aún en las circunstancias más difíciles!']
lista_frases9 = ['En un mundo lleno de desafíos, creo firmemente en la importancia de la bondad y la empatía. Cada día, trato de hacer un pequeño acto de amabilidad, ya sea ayudando a un vecino con sus compras, ofreciendo una palabra de aliento a un colega o simplemente sonriendo a un extraño en la calle. Estoy convencido de que estas pequeñas acciones, aunque parezcan insignificantes, tienen el poder de transformar nuestro entorno y crear una comunidad más solidaria y comprensiva. Al final del día, es la suma de estas buenas intenciones lo que realmente marca la diferencia en el mundo.']
lista_frases10 = ['Sentado en la oscuridad de su sala de estar, Martín escuchaba atentamente cada ruido exterior, su corazón latiendo con un ritmo ansioso. Había revisado las cerraduras de las puertas y ventanas al menos tres veces, pero aún sentía una inquietud punzante. Las noticias recientes de robos en el vecindario resonaban en su mente, alimentando su preocupación constante. Aunque las luces de seguridad iluminaban el perímetro de su casa, y las cámaras de vigilancia mostraban una calle desierta, no podía deshacerse de la sensación de vulnerabilidad. Cada crujido de la madera, cada susurro del viento, se convertía en una posible amenaza. Martín se levantó para verificar una vez más, su mente atrapada en un ciclo interminable de duda y desasosiego, buscando la certeza de que todo estaba bien pero nunca encontrándola completamente.']
lista_frases11 = ['De pie en la cima de la colina, con el vasto paisaje extendiéndose ante él, Carlos respiraba profundamente, llenando sus pulmones de aire fresco y puro. Sentía el viento acariciando su rostro y el sol calentando su piel, símbolos tangibles de la libertad que tanto apreciaba. Cada día, decidía su propio rumbo sin ataduras ni restricciones, confiando únicamente en su instinto y deseo de explorar. Para él, la libertad era el mayor tesoro, la capacidad de forjar su propio destino sin rendir cuentas a nadie. Las decisiones eran suyas, tanto los aciertos como los errores, y en esa autonomía encontraba un poder indescriptible. Mirando el horizonte, Carlos sentía una gratitud inmensa por la libertad de ser quien era, de vivir sin cadenas, de soñar y perseguir esos sueños sin límites.']
lista_frases12 = ['Desde mi perspectiva, alcanzar el éxito en cualquier campo es aprovechar al máximo cada situación a mi favor. La estrategia consiste en identificar oportunidades lucrativas y actuar con determinación para obtener el máximo beneficio personal. Las relaciones son herramientas para expandir mi red y no dudo en usarlas para asegurar mi progreso. La competencia es un desafío emocionante que disfruto superando con astucia y audacia. En mi camino hacia el éxito, no hay espacio para la duda o la moralidad; cada decisión está guiada por el deseo de acumular riqueza y poder.']
lista_frases13 = ['Desde mi perspectiva, la mente abierta es el camino hacia el descubrimiento constante y el crecimiento personal. Estoy constantemente en busca de conocimiento, explorando nuevas ideas y perspectivas que amplíen mi comprensión del mundo. Creo firmemente en la importancia de la educación continua y en la capacidad de adaptarse a los cambios rápidos y dinámicos que caracterizan nuestro entorno actual. Para mí, ser un "cerebrito" no se trata solo de acumular datos, sino de aplicar el pensamiento crítico y la creatividad para resolver problemas complejos y encontrar soluciones innovadoras. Estoy motivado por el deseo de hacer contribuciones significativas y positivas a la sociedad, utilizando mis habilidades y conocimientos para generar un impacto tangible en mi comunidad y más allá.']
lista_frases14 = ["Después de años de trabajo duro, parece que aún no estoy avanzando en mi carrera. Es desalentador ver cómo otros tienen éxito mientras yo sigo en el mismo lugar.",'After years of hard work, it feels like Im still not making any progress in my career. Its disheartening to see others succeed while Im stuck in the same place.']
lista_frases15 = ["As a priest, I find solace in guiding others through their spiritual journeys. It is a privilege to witness the faith and resilience of my parishioners every day.","Como sacerdote, encuentro consuelo en guiar a otros en sus caminos espirituales. Es un privilegio presenciar la fe y la resiliencia de mis feligreses cada día."]
lista_frases16 = ["As an athlete, I dedicate myself fully to training and improving my skills every day. The discipline and determination required are immense, but the rewards of achieving personal bests make it all worthwhile.","Como deportista, me dedico completamente al entrenamiento y a mejorar mis habilidades todos los días. La disciplina y la determinación requeridas son inmensas, pero las recompensas de alcanzar mis mejores marcas personales hacen que todo valga la pena."]
lista_frases17 = ["I thrive on competition and constantly push myself to be the best in everything I do. Winning is not just a goal but a mindset that drives me to excel in every challenge.","Disfruto de la competencia y siempre me esfuerzo por ser el mejor en todo lo que hago. Ganar no es solo un objetivo, sino una mentalidad que me impulsa a destacarme en cada desafío."]
lista_frases18 = ['Imaginémonos que cada cosa que hacemos tiene eco en los demás. Que somos inspiración y ejemplo. El éxito nunca es individual, es un logro colectivo. Sigamos dándolo todo para superar nuestros límites. Vamos','Los extranjeros son el 13,4% de la población en España y cometen la mitad de los delitos y la mitad de los asesinatos de mujeres. En ciertos delitos el porcentaje extranjero se dispara. Para quienes digan que inmigración y delincuencia nada tienen que ver.','Se terminó Motomami pero mi agradecimiento a Dios, a la vida, a mi familia, mi equipo y a todos los que me apoyáis es de x vida. Motomami ha sido un huracán que ha traído y se ha llevado tantas cosas en mi vida que no sé ni por dónde empezar. Gracias a todxs lxs motomamis del mundo x haberme dado tanto amor durante todo este tiempo.']
lista_frases19 = ["Es curioso que un pueblo que despojó de la mayoría de poderes al monarca ahora le exija que haga aquello que le prohibieron. Incluso algunos sostienen -no sabemos si por ignorancia o por maldad- que el Rey podría haberse negado a firmarla y abdicar"]
lista_frases20 = ['¡Qué increíble es poder presenciar el talento y la dedicación que pones en todo lo que haces! Cada proyecto que emprendes es un testimonio de tu compromiso y pasión. Tu capacidad para superar desafíos y convertir cada obstáculo en una oportunidad es verdaderamente inspiradora. Me siento honrado de ser testigo de tu evolución y de aprender de tu ejemplo.']
lista_frases21 = ["me gusta compartir mis conocimientos y colaborar"]
lista_frases21 = ["Sería espantoso y aterrador que esa masa perturbada, inmoral y execrable que colocó en el poder a gobernantes que redactaron la infame ley de amnistía encima tuviera la capacidad de escoger al jefe de Estado.  Menos señalar a Felipe VI y más a su pueblo."]


#valores modificables ------------------------------------------------------------------------------------------------------------------------------

revision_manual = True
verificacion = False
emociones_en_valores = False

#lista de frases y modelos de revision manual
lista_frases = lista_frases21
listamodelos = [h, FNST_trad_2j, ABL_trad_2h]

emociones = False
valores_eticos_Schawrtz = True
valores_eticos_Jonathan = False
ABL = False
FNST = False

#modelos usados en verificacion y emociones_en_valores 
Schawrtz  = h
Jonathan =  h
abl = ABL_trad_2h
fnst = FNST_trad_2j   
 



#valores modificables +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 


def leerDocumento(ruta):
        
    if os.path.exists(ruta):
       with open(ruta, 'r', encoding='utf-8') as file:
        contenido = file.read()
        # Extraer textos y atributos usando una expresión regular
        documento = re.findall(r'Texto \d+: [“"](.*?)[”"] (\w+)', contenido, re.DOTALL)
        
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
          
    #se lee el documento y se hace pd
    documento = leerDocumento(ruta)
    classifier = pipeline("text-classification",model= modelo, top_k=None)

    if ruta == r'D:\1 Mierdas\Escritorio\TextosSchawrtz.txt':
        etico = 'Schawrtz'
    elif ruta == r'D:\1 Mierdas\Escritorio\TextosJonathan.txt':
        etico = 'Jonathan'
    else: etico = 'nada'
    

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

        acumulado =  [x / len(frases) for x in acumulado]

        acumulado = [(dic[i], valor) for i, valor in enumerate(acumulado)]   

        #scharwtz y jonathan
        if etico == 'Jonathan':              
                Nmedia = [0.0,0.0,0.0,0.0,0.0,0.0]
                media = [valor for emocion, valor in acumulado]
                Nmedia[0] = (media[0] + media[8] + media[5] + media[15] + media[17] + media[18] + media[23] + media[20]) / 8
                Nmedia[1] = (media[3] + media[4] + media[10] + media[6]) / 4
                Nmedia[2] = (media[0] + media[5] + media[15] + media[17] + media[18] + media[21] + media[24] ) / 7
                Nmedia[3] = (media[2] + media[10] + media[11] + media[21] + media[26]) / 5
                Nmedia[4] = (media[17] + media[18] + media[21] + media[23] + media[24]) / 5
                Nmedia[5] = (media[2] + media[8] + media[17] + media[23] + media[20] + media[10] ) / 6
                acumulado = [(dicJonathan[i], Nmedia[i]) for i in range(len(Nmedia))]
                
        if etico == 'Schawrtz':
             
                Nmedia = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
                media = [valor for emocion, valor in acumulado]
                Nmedia[0] = (media[6] + media[7] + media[22]) / 3
                Nmedia[1] = (media[1] + media[13] + media[7] + media[26]) / 4
                Nmedia[2] = (media[2] + media[11]) / 2
                Nmedia[3] = (media[8] + media[1] + media[13]) / 3
                Nmedia[4] = (media[8] + media[2] + media[16] + media[17] + media[21] + media[25] + media[0]) / 7
                Nmedia[5] = (media[14] + media[3] + media[19] + media[23] + media[25]) / 5
                Nmedia[6] = (media[3] + media[4] + media[12] + media[10] + media[24]) / 5
                Nmedia[7] = (media[4] + media[10] + media[9] + media[18] + media[14] + media[21] + media[12]) / 7
                Nmedia[8] = (media[5] + media[15] + media[18] + media[0]) / 4
                Nmedia[9] = (media[0] + media[15] + media[5] + media[20] + media[22]) / 5
                acumulado = [(dicSchwartz[i], Nmedia[i]) for i in range(len(Nmedia))]

        #se enfrenta el acumulado a la clase del texto +1 acierto o +1 fallo a la clase
        clase_identificada = max(acumulado, key=lambda x: x[1])  
        clase_identificada = clase_identificada[0]
        expected_clase = row['atributo']
        if clase_identificada == expected_clase:
            aciertos.append(expected_clase)
                
        else:
            fallos.append(expected_clase)
            if False:
                print(texto)
                print(acumulado)
                print()

    #se suman todos los aciertos y falllos de cada clase y del documento
    clases = set(aciertos) | set(fallos)  
    clases = list(clases)

    resultados=[]

    for clase in clases:
        contar_aciertos = aciertos.count(clase)
        contar_fallos = fallos.count(clase)

        resultados.append({"Clase": clase, "Aciertos": contar_aciertos, "Fallos": contar_fallos})

    total_aciertos = 0
    total_fallos = 0

    for resultado in resultados:
        total_aciertos += resultado["Aciertos"]
        total_fallos += resultado["Fallos"]

        total = resultado["Aciertos"] + resultado["Fallos"]
        porcentaje_acierto_clase = (resultado["Aciertos"] / total * 100) if total > 0 else 0
        resultado["Porcentaje Acierto"] = porcentaje_acierto_clase

    total = total_aciertos + total_fallos
    porcentaje_acierto_global = (total_aciertos / total * 100) if total > 0 else 0
    #se muestran

    print("Resultados por clase:")
    for resultado in resultados:
        print(f"Clase: {resultado['Clase']}, Aciertos: {resultado['Aciertos']}, Fallos: {resultado['Fallos']}, Porcentaje de Acierto: {resultado['Porcentaje Acierto']:.2f}%")

    print(f"\nTotal Aciertos: {total_aciertos}, Total Fallos: {total_fallos}")
    print(f"Porcentaje de Acierto Global: {porcentaje_acierto_global:.2f}%")
    print()
    print('fin del conjunto de textos')
    print()
    print()

def Emociones_en_valores(ruta,modelo):
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




print('inicio\n')
if(revision_manual):
    for modelo in listamodelos:

        classifier = pipeline("text-classification",model= modelo, top_k=None)

        print(modelo)
        print('')

        for i in range(len(lista_frases)):

            frases = re.split(r'[.!?]', lista_frases[i])
            frases = [frase.strip() for frase in frases if frase.strip()]

            acumulado_emociones = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
            acumulado_abl = [0.0,0.0,0.0]
            acumulado_fnst = [0.0,0.0,0.0,0.0]
            acumulado_Schawrtz = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
            acumulado_Jonathan = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]


            
                
            if (modelo.startswith('mrovejaxd/goemotions_bertspanish') and emociones):
                for h in range(len(frases)):
        
                    analizador = classifier(frases[h])

                    analizador_ordenado = sorted(analizador[0], key=lambda x: int(x['label'].split('_')[-1]))

                    salida = [item['score'] for item in analizador_ordenado]
                    
                    acumulado_emociones = [x + y for x, y in zip(acumulado_emociones, salida)]
                acumulado_emociones =  [x / len(frases) for x in acumulado_emociones]
                print("5 emociones mas valoradas" + " : " + str(lista_frases[i]))
                print("")

                indices_maximos = sorted(range(len(acumulado_emociones)), key=lambda i: acumulado_emociones[i], reverse=True)[:5]

                emociones_maximas = [(midic[i], acumulado_emociones[i]) for i in indices_maximos]

                for h, valor in emociones_maximas:
                        print(f'{h}: {valor}')
                print("")


            if (modelo.startswith('mrovejaxd/ABL') and ABL):
                for h in range(len(frases)):

                    analizador = classifier(frases[h])

                    analizador_ordenado = sorted(analizador[0], key=lambda x: int(x['label'].split('_')[-1]))

                    salida = [item['score'] for item in analizador_ordenado]

                    acumulado_abl = [x + y for x, y in zip(acumulado_abl, salida)]

                acumulado_abl =  [x / len(frases) for x in acumulado_abl]
                print("ABL : " + str(lista_frases[i]))
                print("")

                indices_maximos = sorted(range(len(acumulado_abl)), key=lambda i: acumulado_abl[i], reverse=True)[:3]

                abl_maximas = [(dicABL[i], acumulado_abl[i]) for i in indices_maximos]

                for h, valor in abl_maximas:
                        print(f'{h}: {valor}')
                print("")
                
            if (modelo.startswith('mrovejaxd/FNST') and FNST):
                for h in range(len(frases)):

                    analizador = classifier(frases[h])

                    analizador_ordenado = sorted(analizador[0], key=lambda x: int(x['label'].split('_')[-1]))

                    salida = [item['score'] for item in analizador_ordenado]

                    acumulado_fnst = [x + y for x, y in zip(acumulado_fnst, salida)]
                acumulado_fnst =  [x / len(frases) for x in acumulado_fnst]
                print("FNST : " + str(lista_frases[i]))
                print("")

                indices_maximos = sorted(range(len(acumulado_fnst)), key=lambda i: acumulado_fnst[i], reverse=True)[:4]

                fnst_maximas = [(dicFNST[i], acumulado_fnst[i]) for i in indices_maximos]

                for h, valor in fnst_maximas:
                        print(f'{h}: {valor}')
                print("")

            if (modelo.startswith('mrovejaxd/goemotions_bertspanish') and valores_eticos_Schawrtz):
                for h in range(len(frases)):
            
                    analizador = classifier(frases[h])

                    analizador_ordenado = sorted(analizador[0], key=lambda x: int(x['label'].split('_')[-1]))

                    salida = [item['score'] for item in analizador_ordenado]
                    
                    acumulado_Schawrtz = [x + y for x, y in zip(acumulado_Schawrtz, salida)]
                acumulado_Schawrtz =  [x / len(frases) for x in acumulado_Schawrtz]
                print("val_Schawrtz : " + str(lista_frases[i]))
                print("")
                
                Nmedia = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
                media = acumulado_Schawrtz
                Nmedia[0] = (media[6] + media[7] + media[22]) / 3
                Nmedia[1] = (media[1] + media[13] + media[7] + media[26]) / 4
                Nmedia[2] = (media[2] + media[11]) / 2
                Nmedia[3] = (media[8] + media[1] + media[13]) / 3
                Nmedia[4] = (media[8] + media[2] + media[16] + media[17] + media[21] + media[25] + media[0]) / 7
                Nmedia[5] = (media[14] + media[3] + media[19] + media[23] + media[25]) / 5
                Nmedia[6] = (media[3] + media[4] + media[12] + media[10] + media[24]) / 5
                Nmedia[7] = (media[4] + media[10] + media[9] + media[18] + media[14] + media[21] + media[12]) / 7
                Nmedia[8] = (media[5] + media[15] + media[18] + media[0]) / 4
                Nmedia[9] = (media[0] + media[15] + media[5] + media[20] + media[22]) / 5

                
                for h in range(len(Nmedia)):
                        print(f"valor etico: {dicSchwartz[h]}, valor: {Nmedia[h]}")
                print("")
            if (modelo.startswith('mrovejaxd/goemotions_bertspanish') and valores_eticos_Jonathan):
                for h in range(len(frases)):
            
                    analizador = classifier(frases[h])

                    analizador_ordenado = sorted(analizador[0], key=lambda x: int(x['label'].split('_')[-1]))

                    salida = [item['score'] for item in analizador_ordenado]
                    
                    acumulado_Jonathan = [x + y for x, y in zip(acumulado_Jonathan, salida)]
                acumulado_Jonathan =  [x / len(frases) for x in acumulado_Jonathan]
                print("val_Jonathan : " + str(lista_frases[i]))
                print("")

                Nmedia = [0.0,0.0,0.0,0.0,0.0,0.0]
                media = acumulado_Jonathan
                Nmedia[0] = (media[0] + media[8] + media[5] + media[15] + media[17] + media[18] + media[23] + media[20]) / 8
                Nmedia[1] = (media[3] + media[4] + media[10] + media[6]) / 4
                Nmedia[2] = (media[0] + media[5] + media[15] + media[17] + media[18] + media[21] + media[24] ) / 7
                Nmedia[3] = (media[2] + media[10] + media[11] + media[21] + media[26]) / 5
                Nmedia[4] = (media[17] + media[18] + media[21] + media[23] + media[24]) / 5
                Nmedia[5] = (media[2] + media[8] + media[17] + media[23] + media[20] + media[10] ) / 6

                for h in range(len(Nmedia)):
                        print(f"valor etico: {dicJonathan[h]}, valor: {Nmedia[h]}")
                print("")





if (verificacion):
    
    #analizarTextos(ruta_aleatorio,abl)
    analizarTextos(ruta_jonathan,Jonathan)
    analizarTextos(ruta_Schawrtz,Schawrtz)
    #analizarTextos(ruta_abl,abl)
    #analizarTextos(ruta_fnst,fnst)


if (emociones_en_valores):
    Emociones_en_valores(ruta_jonathan,Jonathan)
    Emociones_en_valores(ruta_Schawrtz,Schawrtz)


print('fin\n')
