# Finnish lexemes settings_dialog.py
lexemes = {
    # Asetusten dialogi
    "window_title": "Asetukset",

    "button_close": "Sulje",

    "tab_general": "Yleiset",
    "tab_editor_config": "Editori",
    "tab_viewer_config": "Katselin",
    "tab_ai_config": "Tekoälyn asetukset",

    "general_app_config_label": "Sovelluksen asetukset",
    "general_app_language_label": "Kieli",
    "general_app_language_combo_placeholder_text": "Valitse kieli",
    "general_app_language_combo_accessible_description": "Sovelluksen käyttöliittymän kieli",
    "general_app_theme_label": "Teema",
    "general_app_theme_combo_placeholder_text": "Valitse teema",
    "general_app_theme_combo_accessible_description": "Sovelluksen käyttöliittymän teema",
    "general_app_main_menu_label": "Päävalikko",
    "general_app_main_menu_checkbox": "Näytä päävalikko",
    "general_app_main_menu_checkbox_accessible_description": "Näytä sovelluksen päävalikkopudotusvalikko",
    "general_app_font_size_label": "Fonttikoko: {size}pt",
    "general_app_font_size_slider_accessible_description": "Säädä sovelluksen yleistä fonttikokoa",

    "general_statusbar_label": "Tilarivi",
    "general_statusbar_show_global_cursor_position_checkbox": "Näytä globaali kursorin sijainti",
    "general_statusbar_show_global_cursor_position_checkbox_accessible_description":
        "Näytä globaali kursorin sijainti tilarivillä",

    "editor_config_label": "Editorin konfigurointi",
    "editor_config_show_line_numbers_checkbox": "Näytä rivinumerot",
    "editor_config_show_line_numbers_checkbox_accessible_description": "Näytä rivinumerot editorissa",

    "viewer_config_label": "Katselimen konfigurointi",
    "viewer_config_process_emojis_checkbox": "Muunna tekstiemojit graafisiksi",
    "viewer_config_process_emojis_checkbox_accessible_description": "Muunna tekstiemojit graafisiksi esityksiksi",
    "viewer_config_highlight_todos_checkbox": "Korosta TODOt",
    "viewer_config_highlight_todos_checkbox_accessible_description": "Korosta TODO-tägit tekstissä",
    "viewer_config_open_link_confirmation_checkbox": "Vaatii vahvistuksen linkkien avaamiseen",
    "viewer_config_open_link_confirmation_checkbox_accessible_description":
        "Pyydä vahvistus ennen linkkien avaamista",
    "viewer_config_save_resources_checkbox": "Tallenna ulkoiset kuvat automaattisesti levylle",
    "viewer_config_save_resources_checkbox_accessible_description":
        "Tallenna automaattisesti ulkoisten kuvien kopiot levylle offline-käyttöä varten.",

    "ai_config_openai_api_label": "OpenAI API",
    "ai_config_openai_api_url_input_placeholder_text": "API URL",
    "ai_config_openai_api_url_input_accessible_description": "OpenAI API:n URL",
    "ai_config_openai_api_key_input_placeholder_text": "API-avain",
    "ai_config_openai_api_key_input_accessible_description": "OpenAI API:n avain",
    "ai_config_openai_api_supported_models_label": "Tuetut mallit",
    "ai_config_ai_model_names_combo_placeholder_text": "Valitse malli",
    "ai_config_ai_model_names_combo_accessible_description": "Valittavissa olevat tuetut mallit",

    "ai_config_base_label": "Perusparametrit",
    "ai_config_base_system_prompt_label": "Järjestelmäkehoite",
    "ai_config_base_system_prompt_edit_placeholder_text": "Perusjärjestelmäkehoite, joka edeltää jokaista pyyntöä",
    "ai_config_base_system_prompt_edit_accessible_description":
        "Perusjärjestelmäkehoite, joka edeltää jokaista pyyntöä. Tämä on pelkkää tekstiä.",
    "ai_config_base_response_max_tokens_label": "Vastauksen enimmäismäärä tokeneita",
    "ai_config_base_response_max_tokens_input_accessible_description": "Vastauksessa saatavien tokenien enimmäismäärä",
}
