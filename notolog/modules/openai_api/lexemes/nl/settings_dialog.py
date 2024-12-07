# Dutch lexemes settings_dialog.py
lexemes = {
    "tab_openai_api_config": "OpenAI API",

    "module_openai_api_label": "OpenAI API",
    "module_openai_api_url_label": "API URL",
    "module_openai_api_url_input_placeholder_text": "API URL",
    "module_openai_api_url_input_accessible_description":
        "De URL van de OpenAI API is het adres van het API-eindpunt, dat kan variëren afhankelijk van de service en versie.\n"
        "De AI-assistent gebruikt het eindpunt voor gesprekschatfunctionaliteit of tekstaanvullingen.\n"
        "Raadpleeg de officiële documentatie van de OpenAI API voor de actuele URL.",
    "module_openai_api_key_label": "API-sleutel",
    "module_openai_api_key_input_placeholder_text": "API-sleutel",
    "module_openai_api_key_input_accessible_description":
        "De API-sleutel van OpenAI is een geheime token die wordt gebruikt voor het authenticeren\n"
        "van verzoeken aan het API-eindpunt.",
    "module_openai_api_supported_models_label": "Ondersteunde modellen",
    "module_openai_api_model_names_combo_placeholder_text": "Kies een model",
    "module_openai_api_model_names_combo_accessible_description":
        "Selecteer uit ondersteunde modellen voor chatgesprekken.",

    "module_openai_api_base_system_prompt_label": "Systeemprompt",
    "module_openai_api_base_system_prompt_edit_placeholder_text": "Basis systeemprompt die elke aanvraag voorafgaat",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "Een basis systeemprompt die elke aanvraag voorafgaat.\n"
        "Dit is gewoonlijk een eenvoudige tekst met instructies of rolkenmerken.",

    "module_openai_api_base_response_temperature_label": "Temperatuur: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "Past de willekeurigheid van de modelresponsen aan. Hogere waarden produceren meer gevarieerde uitkomsten, "
        "terwijl lagere waarden de reacties voorspelbaarder maken.",

    "module_openai_api_base_response_max_tokens_label": "Maximaal aantal respons tokens",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "Het maximale aantal tokens dat ontvangen kan worden in een respons, zoals woorden en leestekens, "
        "regelt de lengte van de uitvoer.",

    "module_openai_api_config_prompt_history_size_label": "Grootte van de promptgeschiedenis",
    "module_openai_api_config_prompt_history_size_input_accessible_description":
        "Regelt het aantal invoeren in de promptgeschiedenis die het systeem bewaart voor referentie.\n"
        "Een waarde van nul laat een onbeperkt aantal invoeren toe."
}
