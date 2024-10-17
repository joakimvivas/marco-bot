from fastapi import FastAPI
from app.routers import chatbot
from app.models.gpt_model import load_model_and_tokenizer

# Create a FastAPI app instance
app = FastAPI()

# Include the chatbot router to manage the bot's routes
app.include_router(chatbot.router)

# Startup event: Load the model and tokenizer when the app starts
@app.on_event("startup")
async def startup_event():
    try:
        load_model_and_tokenizer()  # Load the fine-tuned model and tokenizer
        print("Model and tokenizer loaded successfully.")  # Log success message
    except Exception as e:
        print(f"Error during startup: {e}")  # Log any error during startup

# Shutdown event: Perform any necessary cleanup when the app is shutting down
@app.on_event("shutdown")
async def shutdown_event():
    try:
        print("Application is shutting down...")  # Log shutdown process
    except Exception as e:
        print(f"Error during shutdown: {e}")  # Log any error during shutdown
