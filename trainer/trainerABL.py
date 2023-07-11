import pandas as pd
import torch
from datasets import load_dataset
import logging

# Configurar el nivel de registro en WARNING o ERROR
logging.basicConfig(level=logging.WARNING)


if not (torch.cuda.is_available()):
    print("no")
    
print(torch.cuda.device_count())


# Load data
from datasets import load_dataset
ds = load_dataset("mrovejaxd/ABLDSArr11_07")
print("training")

# Create a smaller training dataset for faster training times
small_train_dataset = ds["train"].shuffle(seed=42).select([i for i in list(range(12000))])
small_test_dataset = ds["test"].shuffle(seed=42).select([i for i in list(range(1200))])
print(small_train_dataset[0])
print(small_test_dataset[0])

pretrainedmodel = "dccuchile/bert-base-spanish-wwm-cased"

# Set DistilBERT tokenizer
from transformers import AutoTokenizer
print("training")

tokenizer = AutoTokenizer.from_pretrained(pretrainedmodel)
print("training")


# Prepare the text inputs for the model
def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True)

tokenized_train = small_train_dataset.map(preprocess_function, batched=True)
tokenized_test = small_test_dataset.map(preprocess_function, batched=True)

# Use data_collector to convert our samples to PyTorch tensors and concatenate them with the correct amount of padding
from transformers import DataCollatorWithPadding
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# Define DistilBERT as our base model:
from transformers import BertForSequenceClassification
model = BertForSequenceClassification.from_pretrained(pretrainedmodel, num_labels=3)

# Define the evaluation metrics 
import numpy as np
from datasets import load_metric
from sklearn.metrics import f1_score

def compute_metrics(eval_pred):
    load_accuracy = load_metric("accuracy")
    load_f1 = load_metric("f1")

    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    accuracy = load_accuracy.compute(predictions=predictions, references=labels)["accuracy"]
    f1 = load_f1.compute(predictions=predictions, references=labels, average='macro')["f1"]
    
    return {"accuracy": accuracy, "f1": f1}

# Define a new Trainer with all the objects we constructed so far
from transformers import TrainingArguments, Trainer
from transformers.optimization import Adafactor, AdafactorSchedule

repo_name = "ABL_d"

training_args = TrainingArguments(
    output_dir=repo_name,
    learning_rate=1e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=1,
    weight_decay=0.001,
    save_strategy="epoch", 
    push_to_hub=True,
)

optimizer = Adafactor(model.parameters(), scale_parameter=True, relative_step=True, warmup_init=True, lr=None)

lr_scheduler = AdafactorSchedule(optimizer)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_test,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    optimizers=(optimizer, lr_scheduler)
)

# Train the model
print("training")
trainer.train()

# Upload the model to the Hub
trainer.push_to_hub()

# Compute the evaluation metrics
trainer.evaluate()

