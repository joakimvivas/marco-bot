from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.services.conversation import handle_conversation

# Initialize the API router
router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Pydantic model to validate incoming messages
class Message(BaseModel):
    user_message: str  # The message sent by the user

# Endpoint to serve the main HTML page
@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint to handle user messages and return bot responses
@router.post("/send-message/")
async def send_message(message: Message):
    user_message = message.user_message.strip()  # Clean up the user's message
    bot_response = handle_conversation(user_message)  # Get bot's response based on conversation state
    return {"bot_response": bot_response}

# Endpoint to start the conversation and reset the state
@router.get("/start-conversation/")
async def start_conversation():
    global conversation_state
    # Reset conversation state and user data
    conversation_state = {
        "state": "awaiting_name",  # Reset state to expect user's name
        "user_data": {}  # Clear stored user data
    }
    return {
        "bot_responses": [
            "Hola, soy Marco y te ayudaré a registrar tu perfil.",
            "Primero, ¿cómo te llamas?"
        ]
    }
