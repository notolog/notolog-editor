# Italian lexemes settings_dialog.py
lexemes = {
    "tab_openai_api_config": "API di OpenAI",

    "module_openai_api_label": "API di OpenAI",
    "module_openai_api_url_label": "URL API",
    "module_openai_api_url_input_placeholder_text": "URL API",
    "module_openai_api_url_input_accessible_description":
        "L'URL dell'API di OpenAI è l'indirizzo dell'endpoint dell'API, che può variare a seconda del servizio\n"
        "e della versione. L'Assistente AI utilizza quello dedicato alla funzionalità di chat conversazionale o\n"
        "al completamento del testo. Consultare la documentazione ufficiale dell'API di OpenAI per ottenere l'URL attuale.",
    "module_openai_api_key_label": "Chiave API",
    "module_openai_api_key_input_placeholder_text": "Chiave API",
    "module_openai_api_key_input_accessible_description":
        "La chiave API di OpenAI è un token segreto utilizzato per autenticare le richieste all'endpoint dell'API.",
    "module_openai_api_supported_models_label": "Modelli supportati",
    "module_openai_api_model_names_combo_placeholder_text": "Scegli un modello",
    "module_openai_api_model_names_combo_accessible_description":
        "Seleziona tra i modelli supportati per le conversazioni in chat.",

    "module_openai_api_base_system_prompt_label": "Prompt di sistema",
    "module_openai_api_base_system_prompt_edit_placeholder_text": "Prompt di sistema base che precede ogni richiesta",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "Un prompt di sistema base che precede ogni richiesta.\n"
        "Di solito è un testo semplice con istruzioni o caratteristiche del ruolo.",

    "module_openai_api_base_response_temperature_label": "Temperatura: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "Regola la casualità delle risposte del modello. Valori più alti producono risultati più vari, "
        "mentre valori più bassi rendono le risposte più prevedibili.",

    "module_openai_api_base_response_max_tokens_label": "Massimo numero di token per risposta",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "Il numero massimo di token da ricevere in risposta, come parole e punteggiatura, "
        "controllando la lunghezza dell'output.",

    "module_openai_api_config_prompt_history_size_label": "Dimensione della cronologia dei prompt",
    "module_openai_api_config_prompt_history_size_input_accessible_description":
        "Controlla il numero di voci nella cronologia dei prompt che il sistema mantiene per riferimento.\n"
        "Un valore zero permette voci illimitate."
}
