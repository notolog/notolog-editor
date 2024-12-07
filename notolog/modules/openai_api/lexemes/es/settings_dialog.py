# Spanish lexemes settings_dialog.py
lexemes = {
    "tab_openai_api_config": "API de OpenAI",

    "module_openai_api_label": "API de OpenAI",
    "module_openai_api_url_label": "URL de la API",
    "module_openai_api_url_input_placeholder_text": "URL de la API",
    "module_openai_api_url_input_accessible_description":
        "La URL de la API de OpenAI es la dirección del punto de conexión de la API, que puede variar según el servicio\n"
        "y la versión. El Asistente de IA utiliza la correspondiente para la funcionalidad de chat conversacional\n"
        "o completaciones de texto. Consulte la documentación oficial de la API de OpenAI para obtener la URL actual.",
    "module_openai_api_key_label": "Clave API",
    "module_openai_api_key_input_placeholder_text": "Clave API",
    "module_openai_api_key_input_accessible_description":
        "La clave API de OpenAI es un token secreto que se utiliza para autenticar solicitudes\n"
        "al punto de conexión de la API.",
    "module_openai_api_supported_models_label": "Modelos compatibles",
    "module_openai_api_model_names_combo_placeholder_text": "Elegir un modelo",
    "module_openai_api_model_names_combo_accessible_description":
        "Seleccione de los modelos compatibles para conversaciones de chat.",

    "module_openai_api_base_system_prompt_label": "Prompt del sistema",
    "module_openai_api_base_system_prompt_edit_placeholder_text": "Prompt del sistema base que precede a cada solicitud",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "Un prompt del sistema base que precede a cada solicitud.\n"
        "Por lo general, es texto plano con instrucciones o características de rol.",

    "module_openai_api_base_response_temperature_label": "Temperatura: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "Ajusta la aleatoriedad de las respuestas del modelo. Valores más altos producen salidas más variadas, "
        "mientras que valores más bajos hacen que las respuestas sean más predecibles.",

    "module_openai_api_base_response_max_tokens_label": "Máximos tokens de respuesta",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "Número máximo de tokens que se recibirán en una respuesta, como palabras y puntuación, "
        "controlando la longitud de la salida.",

    "module_openai_api_config_prompt_history_size_label": "Tamaño del historial de prompts",
    "module_openai_api_config_prompt_history_size_input_accessible_description":
        "Controla el número de entradas en el historial de prompts que el sistema retiene para referencia.\n"
        "Un valor cero permite entradas ilimitadas."
}
