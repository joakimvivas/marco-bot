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
            bot_response = f"Encantado, {user_data['nombre']}. ¿Cuál es tu correo electrónico?"
            print(f"Nombre: {user_data['nombre']}")
            return {"bot_response": bot_response}
        else:
            # If the name could not be extracted, ask the user to repeat it
            bot_response = "Lo siento, no pude entender tu nombre. Por favor, ¿podrías decírmelo nuevamente?"
            return {"bot_response": bot_response}

    elif current_state == "awaiting_email":
        extracted_email = extract_email(user_input)
        if extracted_email:
            user_data["email"] = extracted_email
            conversation_state["state"] = "awaiting_phone"
            bot_response = "Gracias. ¿Cuál es tu número de teléfono?"
            print(f"Email: {user_data['email']}")
            return {"bot_response": bot_response}
        else:
            bot_response = "Parece que el correo electrónico no es válido. Por favor, proporciónalo nuevamente."
            return {"bot_response": bot_response}

    elif current_state == "awaiting_phone":
        # Extract phone number
        extracted_phone = extract_phone(user_input)
        if extracted_phone:
            user_data["phone"] = extracted_phone
            conversation_state["state"] = "awaiting_city"
            bot_response = "Perfecto. ¿En qué ciudad vives actualmente?"
            print(f"Teléfono: {user_data['phone']}")
            return {"bot_response": bot_response}
        else:
            bot_response = "El número de teléfono parece inválido. Por favor, proporciónalo nuevamente (9 dígitos)."
            return {"bot_response": bot_response}

    elif current_state == "awaiting_city":
        # Extract the user's city
        extracted_city = extract_city(user_input)
        if extracted_city:
            user_data["city"] = extracted_city
            conversation_state["state"] = "awaiting_career"
            bot_response = "Gracias. ¿Qué carrera universitaria has estudiado?"
            print(f"Ciudad: {user_data['city']}")
            return {"bot_response": bot_response}
        else:
            bot_response = "No pude identificar tu ciudad. Por favor, indícala nuevamente."
            return {"bot_response": bot_response}

    elif current_state == "awaiting_career":
        # Extract the user's race
        extracted_career = extract_career(user_input)
        if extracted_career:
            user_data["career"] = extracted_career
            conversation_state["state"] = "awaiting_university"
            bot_response = "Excelente. ¿En qué universidad te graduaste?"
            print(f"Carrera: {user_data['career']}")
            return {"bot_response": bot_response}
        else:
            bot_response = "No pude entender tu carrera universitaria. Por favor, indícala nuevamente."
            return {"bot_response": bot_response}

    elif current_state == "awaiting_university":
        # Extract user's university
        extracted_university = extract_university(user_input)
        if extracted_university:
            user_data["university"] = extracted_university
            conversation_state["state"] = "awaiting_age"
            bot_response = "Genial. Y ahora para finalizar, ¿cuál es tu edad?"
            print(f"Universidad: {user_data['university']}")
            return {"bot_response": bot_response}
        else:
            bot_response = "No pude identificar tu universidad. Por favor, indícala nuevamente."
            return {"bot_response": bot_response}

    elif current_state == "awaiting_age":
        # Extract user age
        extracted_age = extract_age(user_input)
        if extracted_age:
            user_data["age"] = extracted_age
            conversation_state["state"] = "registration_complete"
            bot_response = (
                f"Perfecto. Tu perfil ha sido creado exitosamente, {user_data['nombre']}. "
                "¡Gracias por registrarte!"
            )
            print(f"Edad: {user_data['age']}")
            print("Datos del usuario:")
            print(user_data)
            return {"bot_response": bot_response}
        else:
            bot_response = "No pude entender tu edad. Por favor, indícala en años."
            return {"bot_response": bot_response}

    elif current_state == "registration_complete":
        # Registration completed
        bot_response = "Si necesitas algo más, no dudes en decírmelo."
        return {"bot_response": bot_response}

    else:
        # Unknown or unmanaged status
        bot_response = "Lo siento, no he entendido tu respuesta. Por favor, intenta de nuevo."
        return {"bot_response": bot_response}
