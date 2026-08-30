# Finnish lexemes settings_dialog.py
lexemes = {
    # Asetusten dialogi
    "window_title": "Asetukset",

    "button_close": "Sulje",

    "tab_general": "Yleiset",
    "tab_workspace": "Työtila",
    "tab_ai_config": "Tekoälyn asetukset",

    "general_app_config_label": "Sovelluksen asetukset",
    "general_app_language_label": "Kieli",
    "general_app_language_combo_placeholder_text": "Valitse kieli",
    "general_app_language_combo_accessible_description": "Sovelluksen käyttöliittymän kieli",
    "general_app_theme_label": "Teema",
    "general_app_theme_combo_placeholder_text": "Valitse teema",
    "general_app_theme_combo_accessible_description": "Sovelluksen käyttöliittymän teema",
    "general_app_default_path_label": "Oletuskansio muistiinpanoille",
    "general_app_default_path_input_accessible_description": "Määritä oletuskansio, johon muistiinpanot tallennetaan",
    "general_app_default_path_input_placeholder_text": "Valitse tai anna kansion polku",
    "general_app_elements_visibility_label": "Hallitse elementtien näkyvyyttä",
    "general_app_main_menu_label": "Päävalikko",
    "general_app_main_menu_checkbox": "Näytä päävalikko",
    "general_app_main_menu_checkbox_accessible_description": "Näytä sovelluksen päävalikkopudotusvalikko",
    "general_app_font_size_label": "Fonttikoko: {size}pt",
    "general_app_font_size_slider_accessible_description": "Säädä sovelluksen yleistä fonttikokoa",

    "general_file_deletion_label": "Tiedostojen poistaminen",
    "general_reversible_file_deletion_checkbox": "Poista tiedostot palautettavasti",
    "general_reversible_file_deletion_checkbox_accessible_description":
        "Siirrä poistetut tiedostot Notologin roskakoriin lisäämällä .del-tunniste",

    "workspace_bottom_bar_show_global_cursor_position_checkbox": "Näytä globaali kursorin sijainti",
    "workspace_bottom_bar_show_global_cursor_position_checkbox_accessible_description":
        "Näytä globaali kursorin sijainti tilarivillä",
    "workspace_bottom_bar_show_navigation_arrows_checkbox": "Näytä navigointinuolet",
    "workspace_bottom_bar_show_navigation_arrows_checkbox_accessible_description": "Näytä navigointinuolet tilapalkissa",

    "workspace_editor_mode_label": "Muokkaustila",
    "workspace_editor_mode_show_line_numbers_checkbox": "Näytä rivinumerot",
    "workspace_editor_mode_show_line_numbers_checkbox_accessible_description": "Näytä rivinumerot editorissa",

    "workspace_view_mode_label": "Katselutila",
    "workspace_view_mode_process_emojis_checkbox": "Muunna tekstiemojit graafisiksi",
    "workspace_view_mode_process_emojis_checkbox_accessible_description": "Muunna tekstiemojit graafisiksi esityksiksi",
    "workspace_view_mode_highlight_todos_checkbox": "Korosta TODOt",
    "workspace_view_mode_highlight_todos_checkbox_accessible_description": "Korosta TODO-tägit tekstissä",
    "workspace_view_mode_open_link_confirmation_checkbox": "Vaatii vahvistuksen linkkien avaamiseen",
    "workspace_view_mode_open_link_confirmation_checkbox_accessible_description":
        "Pyydä vahvistus ennen linkkien avaamista",
    "workspace_view_mode_save_resources_checkbox": "Tallenna ulkoiset kuvat automaattisesti levylle",
    "workspace_view_mode_save_resources_checkbox_accessible_description":
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
    "workspace_bottom_bar_label": "Alapalkki",
    "workspace_bottom_bar_show_system_load_graphs_checkbox": "Näytä suorittimen ja muistin kaaviot",
    "workspace_bottom_bar_show_system_load_graphs_checkbox_accessible_description":
        "Näytä suorittimen ja muistin käyttökaaviot sekä erotin alapalkissa",
    "workspace_bottom_bar_system_load_interval_ms_label": "Kaavioiden päivitysväli",
    "workspace_bottom_bar_system_load_interval_ms_accessible_description":
        "Määritä suorittimen ja muistin käytön lukuväli millisekunteina",
}
