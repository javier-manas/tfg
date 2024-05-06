import pandas as pd
from datasets import Dataset, load_dataset, DatasetDict
from scipy import datasets

from datasets import Dataset, concatenate_datasets

# Cargar los dos datasets
dataset1 = DatasetDict.load_from_disk(r'D:\2 cosas\1 Curso upm\TFG 1\datasets\ABLDSArr11_07')
dataset2 = DatasetDict.load_from_disk(r'D:\2 cosas\1 Curso upm\TFG 1\datasets\DS_ABL_trad')

# Combinar los conjuntos de entrenamiento y de prueba
ds = concatenate_datasets([dataset1['train'], dataset1['test'], dataset2['train'], dataset2['test']])

df = pd.DataFrame(ds)
print(df)
num_lineas = df.shape[0]
print("num lineas: ", num_lineas)


ds = ds.train_test_split(test_size=0.1)

ds.push_to_hub("mrovejaxd/DS_ABL_trad", private=True)
ds.save_to_disk(r'D:\2 cosas\1 Curso upm\TFG 1\datasets\DS_ABL_trad_final')


size = 0.1 * len(ds)
print(size)
print(ds)