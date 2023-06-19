# Log in to your Hugging Face account 
# Get your API token here https://huggingface.co/settings/token

# Activate GPU for faster training by clicking on 'Runtime' > 'Change runtime type' and then selecting GPU as the Hardware accelerator
# Then check if GPU is available
import pandas as pd
import torch
from datasets import load_dataset

if (torch.cuda.is_available()):
    print("si")

# Load data

dataset = load_dataset("mrovejaxd/ABLDS")
print(dataset)
df = pd.DataFrame(dataset)
print(df)

dataset = load_dataset("mrm8488/go_emotions-es-mt")
print(dataset)
df = pd.DataFrame(dataset)
print(df)