from .extraction import extract_name, extract_phone, extract_email, extract_city

# Initialize the conversation state and store user data
conversation_state = {
    "state": "awaiting_name",  # Initial state expects user's name
    "user_data": {}  # Dictionary to hold extracted user information
}

# Function to handle the conversation flow based on user input and current state
def handle_conversation(user_input):
    current_state = conversation_state["state"]  # Get the current state of the conversation
    user_data = conversation_state["user_data"]  # Get user data stored during the conversation

    if current_state == "awaiting_name":
        # Try to extract the name from the user input
        extracted_name = extract_name(user_input)
        if extracted_name:
            user_data["name"] = extracted_name
            conversation_state["state"] = "awaiting_email"  # Move to next state (email)
            print(f"Name extracted: {user_data['name']}")  # Log extracted name
            return f"Encantado, {user_data['name']}. ¿Cuál es tu correo electrónico?"  # Bot response in Spanish
        else:
            return "Lo siento, no pude entender tu nombre. ¿Puedes repetirlo?"  # Ask for the name again

    elif current_state == "awaiting_email":
        # Try to extract the email from the user input
        extracted_email = extract_email(user_input)
        if extracted_email:
            user_data["email"] = extracted_email
            conversation_state["state"] = "awaiting_phone"  # Move to next state (phone)
            print(f"Email extracted: {user_data['email']}")  # Log extracted email
            return "Gracias. ¿Cuál es tu número de teléfono?"  # Bot response in Spanish
        else:
            return "El correo electrónico parece inválido. Por favor, indícalo nuevamente."  # Ask for email again

    # Handle additional conversation states similarly...

    return "No he entendido tu mensaje. ¿Puedes intentar nuevamente?"  # Default fallback response in Spanish
