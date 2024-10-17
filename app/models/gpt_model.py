import os
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
import torch
import json

# Path to store the fine-tuned GPT-2 model
MODEL_DIR = "app/models/gpt2_finetuned"

# Create the model directory if it doesn't exist
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# Global variables for the model and tokenizer
model = None
tokenizer = None

# Function to load the model and tokenizer
def load_model_and_tokenizer():
    global model, tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)  # Load the tokenizer from saved model
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR)  # Load the model from saved model

    # Add padding token if not present
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        model.resize_token_embeddings(len(tokenizer))  # Resize model to account for added tokens
    tokenizer.pad_token = '[PAD]'  # Set padding token

# Function to train the model using custom data
def train_model():
    global model, tokenizer

    # Load training data from a JSON file
    with open('app/data-training.json', 'r', encoding='utf-8') as file:
        training_data = json.load(file)

    inputs = []  # List to hold tokenized inputs

    # Loop through each entry in the training data
    for entry in training_data:
        input_text = entry['input']
        response_text = entry['response']

        # Combine input and response with the EOS token
        combined_text = input_text + tokenizer.eos_token + response_text + tokenizer.eos_token

        # Tokenize the combined text
        encoded_dict = tokenizer(
            combined_text,
            truncation=True,  # Truncate to max length
            padding='max_length',  # Pad to max length
            max_length=512,  # Maximum length for the input
            return_tensors='pt'  # Return PyTorch tensors
        )

        input_ids = encoded_dict['input_ids'].squeeze()  # Input IDs for the model
        attention_mask = encoded_dict['attention_mask'].squeeze()  # Attention mask for the model

        # Create labels by masking the input portion
        labels = input_ids.clone()

        # Tokenize input to get its length in tokens
        user_input_ids = tokenizer(
            input_text + tokenizer.eos_token,
            truncation=True,
            max_length=512,
            add_special_tokens=False,
            return_tensors='pt'
        )['input_ids'].squeeze()

        user_input_len = user_input_ids.size(0)  # Get the length of the input tokens

        # Mask the input tokens in the labels
        labels[:user_input_len] = -100  # Mask input tokens to ignore during loss calculation

        # Append tokenized input and labels to the list
        inputs.append({
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': labels
        })

    # Create a custom dataset class
    class CustomDataset(torch.utils.data.Dataset):
        def __init__(self, inputs):
            self.inputs = inputs

        # Return input at a specific index
        def __getitem__(self, idx):
            return self.inputs[idx]

        # Return the total number of inputs
        def __len__(self):
            return len(self.inputs)

    # Create dataset from inputs
    dataset = CustomDataset(inputs)

    # Define training arguments
    training_args = TrainingArguments(
        output_dir=MODEL_DIR,  # Directory to save the model
        per_device_train_batch_size=2,  # Batch size per device
        num_train_epochs=5,  # Number of epochs to train
        logging_dir='./logs',  # Directory for logging
        logging_steps=1,  # Log loss after every step
        save_total_limit=2,  # Keep only the last 2 saved models
        save_steps=500  # Save the model every 500 steps
    )

    # Create a Trainer to handle training
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,  # The dataset for training
    )

    # Start the training process
    trainer.train()

    # Save the trained model and tokenizer
    model.save_pretrained(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)
