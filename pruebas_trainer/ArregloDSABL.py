import pandas as pd
from datasets import Dataset, load_dataset, DatasetDict
from scipy import datasets
import torch

datasetD = Dataset.load_from_disk(r'D:\1 Curso upm\TFG 1\datasets\DS_ABL')

print(datasetD)

ds2 = datasetD

ds2 = ds2.rename_column("tribe", "labels")
ds2 = ds2.map(lambda example: {'labels': 0 if example['labels'] == 3 else example['labels']})

df = pd.DataFrame(ds2)
print(df)


try:
    ds2 = ds2.train_test_split(test_size=0.1)
    size = 0.1 * len(ds2)
    print(size)
    print(ds2)


    ds2.push_to_hub("mrovejaxd/ABLDSArr11_07", private=True)
    ds2.save_to_disk(r'D:\1 Curso upm\TFG 1\datasets\ABLDSArr11_07')
    
    
except Exception as e:
    print("D",e)

