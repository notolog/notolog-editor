# German lexemes settings_dialog.py
lexemes = {
    "tab_openai_api_config": "OpenAI API",

    "module_openai_api_label": "OpenAI API",
    "module_openai_api_url_label": "API-URL",
    "module_openai_api_url_input_placeholder_text": "API-URL",
    "module_openai_api_url_input_accessible_description":
        "Die URL der OpenAI-API ist die Adresse des API-Endpunkts, die je nach Dienst und Version variieren kann.\n"
        "Der KI-Assistent verwendet diejenige für die Funktionalität von Chatgesprächen oder Textvervollständigungen.\n"
        "Bitte konsultieren Sie die offizielle Dokumentation der OpenAI-API, um die aktuelle URL zu erhalten.",
    "module_openai_api_key_label": "API-Schlüssel",
    "module_openai_api_key_input_placeholder_text": "API-Schlüssel",
    "module_openai_api_key_input_accessible_description":
        "Der OpenAI-API-Schlüssel ist ein geheimer Token, der zur Authentifizierung\n"
        "von Anfragen an den API-Endpunkt verwendet wird.",
    "module_openai_api_supported_models_label": "Unterstützte Modelle",
    "module_openai_api_model_names_combo_placeholder_text": "Modell wählen",
    "module_openai_api_model_names_combo_accessible_description":
        "Wählen Sie aus unterstützten Modellen für Chat-Gespräche aus.",

    "module_openai_api_base_system_prompt_label": "Systemprompt",
    "module_openai_api_base_system_prompt_edit_placeholder_text": "Basis-Systemprompt, der jeder Anfrage vorausgeht",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "Ein Basis-Systemprompt, der jeder Anfrage vorausgeht.\n"
        "In der Regel handelt es sich um einfachen Text mit Anweisungen oder Rollenmerkmalen.",

    "module_openai_api_base_response_temperature_label": "Temperatur: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "Passt die Zufälligkeit der Modellantworten an. Höhere Werte produzieren vielfältigere Ausgaben, "
        "während niedrigere Werte die Antworten vorhersehbarer machen.",

    "module_openai_api_base_response_max_tokens_label": "Maximale Antwort-Token",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "Maximale Anzahl von Token, die in einer Antwort empfangen werden, wie Wörter und Zeichensetzung, "
        "steuert die Länge der Ausgabe.",

    "module_openai_api_config_prompt_history_size_label": "Größe der Prompt-Historie",
    "module_openai_api_config_prompt_history_size_input_accessible_description":
        "Steuert die Anzahl der Einträge in der Prompt-Historie, die das System zur Referenz behält.\n"
        "Ein Wert von null ermöglicht unbegrenzte Einträge."
}
