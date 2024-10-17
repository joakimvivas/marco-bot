import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from fastapi import FastAPI
from app.routers import chatbot
from app.models.gpt_model import load_model_and_tokenizer, train_model
from app.models.gpt_model import MODEL_DIR

# Create a FastAPI app instance
app = FastAPI()

# Include the chatbot router to manage the bot's routes
app.include_router(chatbot.router)

# Initialize global variables for model and tokenizer
model = None
tokenizer = None

# Function to ensure all special tokens are added
def ensure_special_tokens(tokenizer):
    special_tokens_dict = {}
    if tokenizer.pad_token is None:
        special_tokens_dict['pad_token'] = '[PAD]'  # Add pad token if not present
    if tokenizer.eos_token is None:
        special_tokens_dict['eos_token'] = '<|endoftext|>'  # Add eos token if not present

    if special_tokens_dict:
        tokenizer.add_special_tokens(special_tokens_dict)
        print(f"Added special tokens: {special_tokens_dict}")  # Log the added tokens

# Startup event: Load the model and tokenizer when the app starts
@app.on_event("startup")
async def startup_event():
    global model, tokenizer
    try:
        # Check if the directory contains files (i.e., the model exists)
        if not os.listdir(MODEL_DIR):
            # If the directory is empty, download the pre-trained model from Hugging Face
            print("Model directory is empty. Downloading and initializing resources...")
            tokenizer = AutoTokenizer.from_pretrained("gpt2")
            
            # Ensure that special tokens (eos_token, pad_token) are present in the tokenizer
            ensure_special_tokens(tokenizer)
            
            model = AutoModelForCausalLM.from_pretrained("gpt2")
            
            # Resize the model's embeddings to accommodate the new tokens
            model.resize_token_embeddings(len(tokenizer))
            
            # Train the model (or perform any required fine-tuning)
            train_model()
            print("Model and tokenizer initialized and trained.")
        
        else:
            # If the model directory is not empty, load the model and tokenizer from the directory
            print(f"Loading model and tokenizer from {MODEL_DIR}.")
            load_model_and_tokenizer()  # Load the existing fine-tuned model and tokenizer
            print("Model and tokenizer loaded successfully.")
    
    except Exception as e:
        # Log any error that occurs during startup
        print(f"Error during startup: {e}")

# Shutdown event: Perform any necessary cleanup when the app is shutting down
@app.on_event("shutdown")
async def shutdown_event():
    try:
        print("Application is shutting down...")  # Log shutdown process
    except Exception as e:
        print(f"Error during shutdown: {e}")  # Log any error during shutdown
