import pandas as pd
import torch
from datasets import load_dataset
import logging
import matplotlib.pyplot as plt
from transformers import AdamW, get_linear_schedule_with_warmup
import random
import re
import os

# Configurar el nivel de registro en WARNING o ERROR
logging.basicConfig(level=logging.WARNING)


print(torch.cuda.is_available())
    
print(torch.cuda.device_count())




dataset1 = "mrovejaxd/DS_ABL_trad"
nombrerepo1 = "ABL_trad_2g"
dataset2 = "mrovejaxd/DS_FNST_sinpodemos"
nombrerepo2 = "FNST_trad_2g"


learning_rate = 1e-7
batch_size=16
num_train_epochs=16
weight_decay=0.001
evaluation_strategy="epoch"
push_to_hub=True
max_grad_norm=0.5
save_strategy="no"



def clean_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r'\@w+|\#','', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    return text


ds = load_dataset(dataset1)
print("training")

ds = ds.map(lambda x: {'text': clean_text(x['text'])})


print(f"Tamaño del dataset de entrenamiento: {len(ds['train'])}")
print(f"Tamaño del dataset de prueba: {len(ds['test'])}")


numero_aleatorio = random.randint(0, 99)

small_train_dataset = ds["train"].shuffle(seed=numero_aleatorio)
small_test_dataset = ds["test"].shuffle(seed=numero_aleatorio)


pretrainedmodel = "dccuchile/bert-base-spanish-wwm-cased"

from transformers import AutoTokenizer
print("training")

tokenizer = AutoTokenizer.from_pretrained(pretrainedmodel)
print("training")


def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True)

tokenized_train = small_train_dataset.map(preprocess_function, batched=True)
tokenized_test = small_test_dataset.map(preprocess_function, batched=True)

from transformers import DataCollatorWithPadding
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

from transformers import BertForSequenceClassification
model = BertForSequenceClassification.from_pretrained(pretrainedmodel, num_labels=3)

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

from transformers import TrainingArguments, Trainer
from transformers.optimization import Adafactor, AdafactorSchedule


training_args = TrainingArguments(
    output_dir=nombrerepo1,
    learning_rate=learning_rate,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    num_train_epochs=num_train_epochs,
    weight_decay=weight_decay,
    evaluation_strategy=evaluation_strategy,
    push_to_hub=push_to_hub,
    max_grad_norm=max_grad_norm,
    save_strategy=save_strategy 
)



optimizer = AdamW(model.parameters(), lr=1e-6)
num_training_steps = len(tokenized_train) * training_args.num_train_epochs
lr_scheduler = get_linear_schedule_with_warmup(
    optimizer, num_warmup_steps=0, num_training_steps=num_training_steps
)



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

print("training")
trainer.train()

trainer.evaluate()

if (True):
    trainer.push_to_hub()

#-------------------------------------------------------------------------------


train_logs1 = trainer.state.log_history










ds = load_dataset(dataset2)
print("training")

ds = ds.map(lambda x: {'text': clean_text(x['text'])})


print(f"Tamaño del dataset de entrenamiento: {len(ds['train'])}")
print(f"Tamaño del dataset de prueba: {len(ds['test'])}")


small_train_dataset = ds["train"].shuffle(seed=numero_aleatorio)
small_test_dataset = ds["test"].shuffle(seed=numero_aleatorio)


pretrainedmodel = "dccuchile/bert-base-spanish-wwm-cased"

from transformers import AutoTokenizer
print("training")

tokenizer = AutoTokenizer.from_pretrained(pretrainedmodel)
print("training")


def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True)

tokenized_train = small_train_dataset.map(preprocess_function, batched=True)
tokenized_test = small_test_dataset.map(preprocess_function, batched=True)

from transformers import DataCollatorWithPadding
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# Define DistilBERT as our base model:
from transformers import BertForSequenceClassification
model = BertForSequenceClassification.from_pretrained(pretrainedmodel, num_labels=4)

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


training_args = TrainingArguments(
    output_dir=nombrerepo2,
    learning_rate=learning_rate,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    num_train_epochs=num_train_epochs,
    weight_decay=weight_decay,
    evaluation_strategy=evaluation_strategy,
    push_to_hub=push_to_hub,
    max_grad_norm=max_grad_norm,
    save_strategy=save_strategy 
)

#optimizer = Adafactor(model.parameters(), scale_parameter=True, relative_step=True, warmup_init=True, lr=None)
#lr_scheduler = AdafactorSchedule(optimizer)

optimizer = AdamW(model.parameters(), lr=1e-6)
# Scheduler
num_training_steps = len(tokenized_train) * training_args.num_train_epochs
lr_scheduler = get_linear_schedule_with_warmup(
    optimizer, num_warmup_steps=0, num_training_steps=num_training_steps
)

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

# Compute the evaluation metrics
trainer.evaluate()

if (True):
    # Upload the model to the Hub
    trainer.push_to_hub()
#-------------------------------------------------------------------------------


# Recuperar los registros de entrenamiento
train_logs = trainer.state.log_history

# Extraer las métricas de interés
train_loss = []
train_accuracy = []
train_f1 = []
train_steps_loss = []
train_steps_accuracy = []
train_steps_f1 = []

# Iterar sobre los registros para recolectar métricas disponibles
for step, log in enumerate(train_logs1):
    if "loss" in log:
        train_loss.append(log["loss"])
        train_steps_loss.append(step)
    if "eval_accuracy" in log:
        train_accuracy.append(log["eval_accuracy"])
        train_steps_accuracy.append(step)
    if "eval_f1" in log:
        train_f1.append(log["eval_f1"])
        train_steps_f1.append(step)

# Crear gráficos y mostrarlos como ventanas emergentes
if train_loss:
    plt.figure(figsize=(10, 5))
    plt.plot(train_steps_loss, train_loss, label="Training Loss")
    plt.xlabel("Training Steps")
    plt.ylabel("Loss")
    plt.title("Training Loss Over Steps")
    plt.legend()
    plt.show()

if train_accuracy:
    plt.figure(figsize=(10, 5))
    plt.plot(train_steps_accuracy, train_accuracy, label="Training Accuracy")
    plt.xlabel("Training Steps")
    plt.ylabel("Accuracy")
    plt.title("Training Accuracy Over Steps")
    plt.legend()
    plt.show()

if train_f1:
    plt.figure(figsize=(10, 5))
    plt.plot(train_steps_f1, train_f1, label="Training F1")
    plt.xlabel("Training Steps")
    plt.ylabel("F1 Score")
    plt.title("Training F1 Score Over Steps")
    plt.legend()
    plt.show()


# Extraer las métricas de interés
train_loss = []
train_accuracy = []
train_f1 = []
train_steps_loss = []
train_steps_accuracy = []
train_steps_f1 = []

# Iterar sobre los registros para recolectar métricas disponibles
for step, log in enumerate(train_logs):
    if "loss" in log:
        train_loss.append(log["loss"])
        train_steps_loss.append(step)
    if "eval_accuracy" in log:
        train_accuracy.append(log["eval_accuracy"])
        train_steps_accuracy.append(step)
    if "eval_f1" in log:
        train_f1.append(log["eval_f1"])
        train_steps_f1.append(step)

# Crear gráficos y mostrarlos como ventanas emergentes
if train_loss:
    plt.figure(figsize=(10, 5))
    plt.plot(train_steps_loss, train_loss, label="Training Loss")
    plt.xlabel("Training Steps")
    plt.ylabel("Loss")
    plt.title("Training Loss Over Steps")
    plt.legend()
    plt.show()

if train_accuracy:
    plt.figure(figsize=(10, 5))
    plt.plot(train_steps_accuracy, train_accuracy, label="Training Accuracy")
    plt.xlabel("Training Steps")
    plt.ylabel("Accuracy")
    plt.title("Training Accuracy Over Steps")
    plt.legend()
    plt.show()

if train_f1:
    plt.figure(figsize=(10, 5))
    plt.plot(train_steps_f1, train_f1, label="Training F1")
    plt.xlabel("Training Steps")
    plt.ylabel("F1 Score")
    plt.title("Training F1 Score Over Steps")
    plt.legend()
    plt.show()

