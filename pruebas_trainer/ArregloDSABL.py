import pandas as pd
from datasets import Dataset, load_dataset, DatasetDict
from scipy import datasets
import torch

datasetD = Dataset.load_from_disk(r'D:\1 Curso upm\TFG 1\datasets\DS_ABL')

df2 = pd.DataFrame(datasetD)

print(datasetD)
print(df2)

ds2 = datasetD

try:
    ds2 = ds2.train_test_split(test_size=0.1)
    size = 0.1 * len(ds2)
    print(size)
    print(ds2)
    ds2.push_to_hub("mrovejaxd/ABLDSArr19_06", private=True)
    ds2.save_to_disk(r'D:\1 Curso upm\TFG 1\datasets\ABLDSArr19_06')
    
    
except Exception as e:
    print("D",e)

