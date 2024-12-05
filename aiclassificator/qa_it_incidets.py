import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, TrainingArguments, Trainer
import ast
import torch

# Load the dataset
dataset_path = 'aiclassificator/qa_incidents_dataset.csv'
data = pd.read_csv(dataset_path)

# Convert the 'answers' from stringified dictionaries to actual dictionaries
data['answers'] = data['answers'].apply(ast.literal_eval)

def preprocess(text):
    text = text.lower().strip()
    return text

for index, row in data.iterrows():
    context = preprocess(row['context'])
    answer = row['answers']
    answer_text = preprocess(answer['text'])
    
    # Find the corrected start position if not -1 or incorrect
    corrected_start = context.find(answer_text)
    if corrected_start != -1:
        data.at[index, 'answers'] = {'text': answer_text, 'answer_start': corrected_start}
    else:
        print(f"Answer not found in context for index {index}: {answer_text}")

# Save the corrected dataset
corrected_dataset_path = 'aiclassificator/corrected_qa_incidents_dataset.csv'
data.to_csv(corrected_dataset_path, index=False)

print(data.head())

# Convert DataFrame to Hugging Face dataset
hf_dataset = Dataset.from_pandas(data)
hf_dataset = hf_dataset.train_test_split(test_size=0.1)

# Tokenization function to prepare data for the model
tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")

def prepare_data(examples):
    tokenized_inputs = tokenizer(
        examples['question'],
        examples['context'],
        truncation="only_second",
        max_length=512,
        padding="max_length",
        return_offsets_mapping=True,
        return_overflowing_tokens=False
    )

    start_positions = []
    end_positions = []

    for i in range(len(examples['answers'])):
        answer = examples['answers'][i]
        start_char = answer['answer_start']
        answer_text = answer['text']
        end_char = start_char + len(answer_text)

        sequence_ids = tokenized_inputs.sequence_ids(i)
        offset_mapping = tokenized_inputs.offset_mapping[i]

        start_position = next(
            (idx for idx, (start, end) in enumerate(offset_mapping)
             if start <= start_char < end and sequence_ids[idx] == 1), 0
        )
        end_position = next(
            (idx for idx, (start, end) in enumerate(offset_mapping)
             if start < end_char <= end and sequence_ids[idx] == 1), 0
        )

        start_positions.append(start_position)
        end_positions.append(end_position)

    tokenized_inputs.update({
        'start_positions': start_positions,
        'end_positions': end_positions
    })

    return tokenized_inputs

# Apply the function to tokenize data
tokenized_data = hf_dataset.map(prepare_data, batched=True)
tokenized_data.set_format(type='torch', columns=['input_ids', 'attention_mask', 'start_positions', 'end_positions'])
model = AutoModelForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=3,              # number of training epochs
    per_device_train_batch_size=12,  # batch size for training
    per_device_eval_batch_size=16,   # batch size for evaluation
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir='./logs',            # directory for storing logs
    logging_steps=10,
    evaluation_strategy="epoch"
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_data["train"],
    eval_dataset=tokenized_data["test"],
    tokenizer=tokenizer
)

# Start training
trainer.train()

# Save the fine-tuned model and tokenizer
model_path = "aiclassificator/model"
tokenizer.save_pretrained(model_path)
model.save_pretrained(model_path)