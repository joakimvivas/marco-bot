from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.services.conversation import handle_conversation  # Mantenemos la importación de handle_conversation

# Initialize the API router
router = APIRouter()  # Asegúrate de que el router esté definido aquí
templates = Jinja2Templates(directory="templates")

# Define a Pydantic model for the message
class Message(BaseModel):
    user_message: str  # The message sent by the user

# Endpoint to serve the main HTML page
@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint to handle user messages and return bot responses
@router.post("/send-message/")
async def send_message(message: Message):
    user_message = message.user_message.strip()
    bot_response = handle_conversation(user_message)  # Make sure this does not cause circular dependency
    return {"bot_response": bot_response}

# Endpoint to start the conversation and reset the state
@router.get("/start-conversation/")
async def start_conversation():
    global conversation_state
    conversation_state = {
        "state": "awaiting_name",
        "user_data": {}
    }
    return {
        "bot_responses": [
            "Hola, soy Marco y te ayudaré a registrar tu perfil.",
            "Primero, ¿cómo te llamas?"
        ]
    }
