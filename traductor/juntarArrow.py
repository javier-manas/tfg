import pandas as pd
from datasets import Dataset, load_dataset, DatasetDict
from scipy import datasets

from datasets import Dataset, concatenate_datasets

# Cargar los dos datasets
dataset1 = DatasetDict.load_from_disk(r'D:\2 cosas\1 Curso upm\TFG 1\datasets\ABLDSArr11_07')
dataset2 = DatasetDict.load_from_disk(r'D:\2 cosas\1 Curso upm\TFG 1\datasets\ABLDSArr19_06')

# Combinar los conjuntos de entrenamiento y de prueba
train_datasets = [dataset1['train'], dataset2['train']]
test_datasets = [dataset1['test'], dataset2['test']]

combined_train_dataset = concatenate_datasets(train_datasets)


combined_test_dataset = concatenate_datasets(test_datasets)

print(combined_train_dataset)
print(combined_test_dataset)
df = pd.DataFrame(combined_test_dataset)
print(df)