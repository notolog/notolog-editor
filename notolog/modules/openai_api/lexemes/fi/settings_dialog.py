# Finnish lexemes settings_dialog.py
lexemes = {
    "tab_openai_api_config": "OpenAI API",

    "module_openai_api_label": "OpenAI API",
    "module_openai_api_url_label": "API:n URL",
    "module_openai_api_url_input_placeholder_text": "API:n URL",
    "module_openai_api_url_input_accessible_description":
        "OpenAI API:n URL on API-päätepisteen osoite, joka voi vaihdella palvelun ja version mukaan.\n"
        "AI-assistentti käyttää sitä keskusteluchatin tai tekstintäydennysten toimintoihin.\n"
        "Katso ajantasainen URL OpenAI API:n virallisesta dokumentaatiosta.",
    "module_openai_api_key_label": "API-avain",
    "module_openai_api_key_input_placeholder_text": "API-avain",
    "module_openai_api_key_input_accessible_description":
        "OpenAI API-avain on salainen tunniste, jota käytetään pyyntöjen todentamiseen API-päätepisteessä.",
    "module_openai_api_supported_models_label": "Tuettu mallit",
    "module_openai_api_model_names_combo_placeholder_text": "Valitse malli",
    "module_openai_api_model_names_combo_accessible_description":
        "Valitse tuetuista malleista chat-keskusteluihin.",

    "module_openai_api_base_system_prompt_label": "Järjestelmäkehotus",
    "module_openai_api_base_system_prompt_edit_placeholder_text":
        "Perusjärjestelmäkehotus, joka edeltää jokaista pyyntöä",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "Perusjärjestelmäkehotus, joka edeltää jokaista pyyntöä.\n"
        "Yleensä yksinkertainen teksti, jossa on ohjeita tai roolin ominaisuuksia.",

    "module_openai_api_base_response_temperature_label": "Lämpötila: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "Säätää mallin vastausten satunnaisuutta. Korkeammat arvot tuottavat monimuotoisempia tuloksia, "
        "kun taas matalammat arvot tekevät vastauksista ennustettavampia.",

    "module_openai_api_base_response_max_tokens_label": "Vastauksen maksimitokenit",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "Määrittää vastauksessa vastaanotettavien tokenien enimmäismäärän, kuten sanat ja välimerkit, "
        "halliten tulosteen pituutta.",

    "module_openai_api_config_prompt_history_size_label": "Kehotushistorian koko",
    "module_openai_api_config_prompt_history_size_input_accessible_description":
        "Hallitsee järjestelmän säilyttämien kehotushistorian merkintöjen määrää.\n"
        "Nolla-arvo sallii rajattomat merkinnät."
}
