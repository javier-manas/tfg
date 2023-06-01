from datasets import Dataset
import pandas as pd
from datasets import load_dataset

# Cargar el dataset desde disco
#dataset = Dataset.load_from_disk(r'D:\1 Curso upm\TFG 1\datasets\DSprueba')

dataset = load_dataset("mrovejaxd/ABLDS")

# Obtener una vista previa de los primeros N ejemplos del dataset
df = pd.DataFrame(dataset)
print(df)

