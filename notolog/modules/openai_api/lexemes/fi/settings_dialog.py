# Finnish lexemes settings_dialog.py
lexemes = {
    # Settings dialog
    "tab_openai_api_config": "OpenAI API",

    "module_openai_api_label": "OpenAI API",
    "module_openai_api_url_input_placeholder_text": "API URL",
    "module_openai_api_url_input_accessible_description": "OpenAI API:n URL",
    "module_openai_api_key_input_placeholder_text": "API-avain",
    "module_openai_api_key_input_accessible_description": "OpenAI API:n avain",
    "module_openai_api_supported_models_label": "Tuetut mallit",
    "module_openai_api_model_names_combo_placeholder_text": "Valitse malli",
    "module_openai_api_model_names_combo_accessible_description": "Valittavissa olevat tuetut mallit",

    "module_openai_api_base_system_prompt_label": "Järjestelmäkehoite",
    "module_openai_api_base_system_prompt_edit_placeholder_text": "Perusjärjestelmäkehoite, joka edeltää jokaista pyyntöä",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "Perusjärjestelmäkehoite, joka edeltää jokaista pyyntöä. Tämä on pelkkää tekstiä.",

    "module_openai_api_base_response_temperature_label": "Lämpötila: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "Säätää mallin tuloksen satunnaisuutta. Korkeammat arvot lisäävät luovuutta; "
        "matalammat arvot lisäävät determinismiä.",

    "module_openai_api_base_response_max_tokens_label": "Maksimivastausmerkkien määrä",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "Vastauksessa vastaanotettavien merkkien enimmäismäärä, kuten sanat ja välimerkit, "
        "hallitsee tulosteen pituutta.",
}
