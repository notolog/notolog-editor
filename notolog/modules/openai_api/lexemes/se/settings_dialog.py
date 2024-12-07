# Swedish lexemes settings_dialog.py
lexemes = {
    "tab_openai_api_config": "OpenAI API",

    "module_openai_api_label": "OpenAI API",
    "module_openai_api_url_label": "API-URL",
    "module_openai_api_url_input_placeholder_text": "API-URL",
    "module_openai_api_url_input_accessible_description":
        "URL:en för OpenAI API är adressen till API-slutpunkten, som kan variera beroende på tjänst och version.\n"
        "AI-assistenten använder den för funktioner som konversationschatt eller textkompletteringar.\n"
        "Se den officiella dokumentationen för OpenAI API för att få den aktuella URL:en.",
    "module_openai_api_key_label": "API-nyckel",
    "module_openai_api_key_input_placeholder_text": "API-nyckel",
    "module_openai_api_key_input_accessible_description":
        "OpenAI API-nyckeln är en hemlig token som används för att autentisera begäranden till API-slutpunkten.",
    "module_openai_api_supported_models_label": "Stödda modeller",
    "module_openai_api_model_names_combo_placeholder_text": "Välj en modell",
    "module_openai_api_model_names_combo_accessible_description":
        "Välj från stödda modeller för chattkonversationer.",

    "module_openai_api_base_system_prompt_label": "Systemprompt",
    "module_openai_api_base_system_prompt_edit_placeholder_text": "Bas systemprompt som föregår varje förfrågan",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "En bas systemprompt som föregår varje förfrågan.\n"
        "Vanligtvis enkel text med instruktioner eller rollkarakteristika.",

    "module_openai_api_base_response_temperature_label": "Temperatur: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "Justerar slumpmässigheten i modellens svar. Högre värden ger mer varierade utdata, "
        "medan lägre värden gör svaren mer förutsägbara.",

    "module_openai_api_base_response_max_tokens_label": "Maximalt antal respons-token",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "Maximalt antal token som tas emot i ett svar, såsom ord och skiljetecken, "
        "styr längden på utdatan.",

    "module_openai_api_config_prompt_history_size_label": "Storlek på prompt-historik",
    "module_openai_api_config_prompt_history_size_input_accessible_description":
        "Kontrollerar antalet poster i prompt-historiken som systemet behåller för referens.\n"
        "Ett värde på noll tillåter obegränsade poster."
}
