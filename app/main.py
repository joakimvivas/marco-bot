import os  # Import to work with directories and file paths
from transformers import AutoTokenizer, AutoModelForCausalLM  # Import for model and tokenizer
from fastapi import FastAPI
from app.routers import chatbot
from app.models.gpt_model import load_model_and_tokenizer, train_model  # Import functions from your model management
from app.models.gpt_model import MODEL_DIR  # Import the directory where the model is stored

# Create a FastAPI app instance
app = FastAPI()

# Include the chatbot router to manage the bot's routes
app.include_router(chatbot.router)

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
            
            # Add a new padding token if not present
            tokenizer.add_special_tokens({'pad_token': '[PAD]'})
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
