from datasets import Dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

file_path = "aiclassificator/enhanced_incident_dataset.csv"

import pandas as pd
data = pd.read_csv(file_path)
custom_dataset = Dataset.from_pandas(data)

custom_dataset = custom_dataset.train_test_split(test_size=0.2)
train_dataset = custom_dataset["train"]
test_dataset = custom_dataset["test"]

model_name = "allenai/unifiedqa-t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def preprocess_custom_data(dataset):
    inputs = []
    targets = []

    for example in dataset:
        question = example["question"]
        context = example["context"]
        answer = example["answer"]

        # Estructura de los modelos T5 
        input_text = f"question: {question} context: {context}"
        inputs.append(input_text)
        targets.append(answer)

    return inputs, targets

train_inputs, train_targets = preprocess_custom_data(train_dataset)
test_inputs, test_targets = preprocess_custom_data(test_dataset)

# Tokenizer
def tokenize_data(inputs, targets, tokenizer, max_length=512):
    tokenized_inputs = tokenizer(inputs, padding="max_length", truncation=True, max_length=max_length, return_tensors="pt")
    tokenized_targets = tokenizer(targets, padding="max_length", truncation=True, max_length=max_length, return_tensors="pt")

    labels = tokenized_targets.input_ids
    labels[labels == tokenizer.pad_token_id] = -100

    return tokenized_inputs, labels

tokenized_train_inputs, tokenized_train_labels = tokenize_data(train_inputs, train_targets, tokenizer)
tokenized_test_inputs, tokenized_test_labels = tokenize_data(test_inputs, test_targets, tokenizer)

from torch.utils.data import DataLoader, Dataset
from transformers import AdamW

class IncidentDataset(Dataset):
    def __init__(self, inputs, labels):
        self.inputs = inputs
        self.labels = labels

    def __len__(self):
        return len(self.inputs["input_ids"])

    def __getitem__(self, idx):
        return {key: val[idx] for key, val in self.inputs.items()}, self.labels[idx]

train_dataset = IncidentDataset(tokenized_train_inputs, tokenized_train_labels)

# Batch_size alto para intentar estabilizar gradientes
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)

# Optimizer
# AdamW balancea eficiencia y regularización, buena opcion para modelos preentrenados
optimizer = AdamW(model.parameters(), lr=5e-5)

# Dispositivo para usar tarjeta de video
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.train()

# Epochs -> valor intermedio
for epoch in range(20):
    for batch in train_loader:
        inputs = {key: val.to(device) for key, val in batch[0].items()}
        labels = batch[1].to(device)

        outputs = model(**inputs, labels=labels)
        loss = outputs.loss

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    print(f"Epoch {epoch + 1}, Loss: {loss.item()}")

output_dir = "aiclassificator/trained_unifiedqa_model"

model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)

print(f"Modelo y tokenizer guardados en {output_dir}")
