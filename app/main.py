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

# Startup event: Load the model and tokenizer when the app starts
@app.on_event("startup")
async def startup_event():
    global model, tokenizer
    try:
        # Check if the directory contains files (i.e., the model exists)
        if not os.listdir(MODEL_DIR):
            print("Model directory is empty. Downloading and initializing resources...")

            # Load the tokenizer and model from Hugging Face
            tokenizer = AutoTokenizer.from_pretrained("gpt2")
            model = AutoModelForCausalLM.from_pretrained("gpt2")

            # Ensure that the tokenizer and model are loaded correctly
            if tokenizer is None or model is None:
                raise ValueError("Failed to load model or tokenizer from Hugging Face")

            # Ensure that special tokens are added
            special_tokens_dict = {}
            if tokenizer.pad_token is None or tokenizer.pad_token_id is None:
                special_tokens_dict['pad_token'] = '[PAD]'
            if tokenizer.eos_token is None or tokenizer.eos_token_id is None:
                special_tokens_dict['eos_token'] = '<|endoftext|>'
            
            if special_tokens_dict:
                tokenizer.add_special_tokens(special_tokens_dict)
                model.resize_token_embeddings(len(tokenizer))  # Resize model embeddings to account for new tokens

            # Ensure that eos_token_id and pad_token_id are set
            if tokenizer.eos_token_id is None:
                tokenizer.eos_token = '<|endoftext|>'
                tokenizer.eos_token_id = tokenizer.convert_tokens_to_ids(tokenizer.eos_token)
            if tokenizer.pad_token_id is None:
                tokenizer.pad_token_id = tokenizer.convert_tokens_to_ids(tokenizer.pad_token)

            print(f"eos_token: {tokenizer.eos_token}, eos_token_id: {tokenizer.eos_token_id}")
            print(f"pad_token: {tokenizer.pad_token}, pad_token_id: {tokenizer.pad_token_id}")

            # Save the tokenizer and model after adding special tokens
            tokenizer.save_pretrained(MODEL_DIR)
            model.save_pretrained(MODEL_DIR)

            # Train the model
            train_model()  # Ensure that the model is trained using the provided data
            print("Model and tokenizer initialized and trained.")
        
        else:
            print(f"Loading model and tokenizer from {MODEL_DIR}.")
            load_model_and_tokenizer()  # Load the existing fine-tuned model and tokenizer
            print("Model and tokenizer loaded successfully.")
    
    except Exception as e:
        print(f"Error during startup: {e}")

# Shutdown event: Perform any necessary cleanup when the app is shutting down
@app.on_event("shutdown")
async def shutdown_event():
    try:
        print("Application is shutting down...")
    except Exception as e:
        print(f"Error during shutdown: {e}")
