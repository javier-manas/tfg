import json
import pandas as pd
from datasets import Dataset, load_dataset, DatasetDict
from scipy import datasets

from datasets import Dataset, concatenate_datasets

# Cargar los dos datasets
dataset1 = DatasetDict.load_from_disk(r'D:\2 cosas\1 Curso upm\TFG 1\datasets\ABLDSArr11_07')

train_datasets = [dataset1['train']]
test_datasets = [dataset1['test']]


print(train_datasets)
print(test_datasets)
df = pd.DataFrame(dataset1['train'])



datasetD = Dataset.load_from_disk(r'D:\2 cosas\1 Curso upm\TFG 1\datasets\DS_ABL')

print(datasetD)
df = pd.DataFrame(datasetD)
print(df)

ruta = r'D:\2 cosas\1 Curso upm\TFG 1\datasets\DatasetsABLingles\DS_en_trad_A.json'
with open(ruta) as json_file:
    data = json.load(json_file)  

print("cucutras")
print(len(data))
