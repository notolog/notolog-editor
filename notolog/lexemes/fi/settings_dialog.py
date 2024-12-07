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

    "ai_config_inference_module_label": "Päätöksentekomoduuli",
    "ai_config_inference_module_names_combo_label": "Aktiivinen päätöksentekomoduuli",
    "ai_config_inference_module_names_combo_placeholder_text": "Valitse moduuli",
    "ai_config_inference_module_names_combo_accessible_description":
        "Valitse käytettävissä olevista tekoälyn päättelymoduuleista, jotka toimivat AI-assistentin kanssa.\n"
        "Vaihtoehtoihin kuuluvat paikalliset suuret kieli mallit (LLM) reaaliaikaisella käsittelyllä,\n"
        "tai API-pohjaiset toiminnot.",

    "ai_config_base_label": "Perusparametrit",
    "ai_config_multi_turn_dialogue_checkbox": "Monivaiheinen vuoropuhelu keskustelumuistilla",
    "ai_config_multi_turn_dialogue_checkbox_accessible_description":
        "Ota käyttöön monivaiheinen vuoropuhelu, joka säilyttää edellisen viestin keskustelumuistissa.\n"
        "Kun se on pois päältä, vain uusi viesti ja järjestelmäkehote vaikuttavat vastaukseen.",
    "ai_config_convert_to_md_checkbox": "Muunna tulos Markdown-muotoon",
    "ai_config_convert_to_md_checkbox_accessible_description":
        "Muunna tulosviesti Markdown-muotoon.",
}
