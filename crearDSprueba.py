
import pandas as pd
from datasets import Dataset, concatenate_datasets


def gen1():
    cont = 0
    text = "a"
    while(cont < 10):
        yield {"pokemon": cont, "type": text}
        cont = cont + 1
        text = text + str(cont)


def gen2():
    cont = 0
    text = "b"
    while(cont < 10):
        yield {"pokemon": cont, "type": text}
        cont = cont + 1
        text = text + str(cont)

def gen3():
    cont = 0
    text = "c"
    while(cont < 10):
        yield {"pokemon": cont, "type": text}
        cont = cont + 1
        text = text + str(cont)
    
ds1 = Dataset.from_generator(gen1)
ds2 = Dataset.from_generator(gen2)
ds3 = Dataset.from_generator(gen3)
ds = concatenate_datasets([ds1, ds2, ds3])
df = pd.DataFrame(ds)
print(df)
#ds.save_to_disk(r'D:\1 Curso upm\TFG 1\datasets\DSprueba')