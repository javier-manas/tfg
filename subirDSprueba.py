from datasets import Dataset
import pandas as pd


# Cargar el dataset desde disco
dataset = Dataset.load_from_disk(r'D:\1 Curso upm\TFG 1\datasets\DS_ABL')

# dataset = dataset.map(...)  # do all your processing here
dataset.push_to_hub("mrovejaxd/ABLDS", private=True)