from .extraction import extract_name, extract_phone, extract_email, extract_city, extract_career, extract_university, extract_age

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
        # Extract the user name
        extracted_name = extract_name(user_input)
        if extracted_name:
            user_data["nombre"] = extracted_name
            conversation_state["state"] = "awaiting_email"
            print(f"Nombre: {user_data['nombre']}")
            return f"Encantado, {user_data['nombre']}. ¿Cuál es tu correo electrónico?"
        else:
            # If the name could not be extracted, ask the user to repeat it
            return "Lo siento, no pude entender tu nombre. Por favor, ¿podrías decírmelo nuevamente?"

    elif current_state == "awaiting_email":
        extracted_email = extract_email(user_input)
        if extracted_email:
            user_data["email"] = extracted_email
            conversation_state["state"] = "awaiting_phone"
            print(f"Email: {user_data['email']}")
            return f"Gracias. ¿Cuál es tu número de teléfono?"
        else:
            return f"Parece que el correo electrónico no es válido. Por favor, proporciónalo nuevamente."

    elif current_state == "awaiting_phone":
        # Extract phone number
        extracted_phone = extract_phone(user_input)
        if extracted_phone:
            user_data["phone"] = extracted_phone
            conversation_state["state"] = "awaiting_city"
            print(f"Teléfono: {user_data['phone']}")
            return f"Perfecto. ¿En qué ciudad vives actualmente?"
        else:
            return f"El número de teléfono parece inválido. Por favor, proporciónalo nuevamente (9 dígitos)."

    elif current_state == "awaiting_city":
        # Extract the user's city
        extracted_city = extract_city(user_input)
        if extracted_city:
            user_data["city"] = extracted_city
            conversation_state["state"] = "awaiting_career"
            print(f"Ciudad: {user_data['city']}")
            return f"Gracias. ¿Qué carrera universitaria has estudiado?"
        else:
            return f"No pude identificar tu ciudad. Por favor, indícala nuevamente."

    elif current_state == "awaiting_career":
        # Extract the user's race
        extracted_career = extract_career(user_input)
        if extracted_career:
            user_data["career"] = extracted_career
            conversation_state["state"] = "awaiting_university"
            print(f"Carrera: {user_data['career']}")
            return f"Excelente. ¿En qué universidad te graduaste?"
        else:
            return f"No pude entender tu carrera universitaria. Por favor, indícala nuevamente."

    elif current_state == "awaiting_university":
        # Extract user's university
        extracted_university = extract_university(user_input)
        if extracted_university:
            user_data["university"] = extracted_university
            conversation_state["state"] = "awaiting_age"
            print(f"Universidad: {user_data['university']}")
            return f"Genial. Y ahora para finalizar, ¿cuál es tu edad?"
        else:
            return f"No pude identificar tu universidad. Por favor, indícala nuevamente."

    elif current_state == "awaiting_age":
        # Extract user age
        extracted_age = extract_age(user_input)
        if extracted_age:
            user_data["age"] = extracted_age
            conversation_state["state"] = "registration_complete"
            print(f"Edad: {user_data['age']}")
            print("Datos del usuario:")
            print(user_data)
            return f"Perfecto. Tu perfil ha sido creado exitosamente, {user_data['nombre']}. ¡Gracias por registrarte!"
        else:
            return f"No pude entender tu edad. Por favor, indícala en años."

    elif current_state == "registration_complete":
        # Registration completed
        return f"Si necesitas algo más, no dudes en decírmelo."

    else:
        # Unknown or unmanaged status
        return f"Lo siento, no he entendido tu respuesta. Por favor, intenta de nuevo."
